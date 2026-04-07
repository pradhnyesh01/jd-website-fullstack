import json
import logging
import re
from datetime import datetime
from typing import Optional

import httpx
from bs4 import BeautifulSoup

from database import tender_exists, save_tender

logger = logging.getLogger(__name__)

# JD Enterprises business domain keywords
KEYWORDS = [
    "sound system",
    "public address",
    "pa system",
    "audio system",
    "cctv",
    "surveillance camera",
    "security camera",
    "video conferencing",
    "av system",
    "led display",
    "video wall",
    "projection system",
    "stage lighting",
    "lan networking",
    "structured cabling",
]

GEM_PAGE_URL   = "https://bidplus.gem.gov.in/all-bids"
GEM_DATA_URL   = "https://bidplus.gem.gov.in/all-bids-data"
GEM_BID_URL    = "https://bidplus.gem.gov.in/bidding/bid-details/{bid_id}"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-IN,en;q=0.9",
}


def _get_session(client: httpx.Client) -> Optional[str]:
    """
    Load the GEM bids page to acquire session cookies and extract the CSRF token.
    Returns the CSRF token string, or None on failure.
    """
    try:
        resp = client.get(GEM_PAGE_URL, timeout=20)
        resp.raise_for_status()
        match = re.search(r"csrf_bd_gem_nk[',\"][\s:,]+['\"]([a-f0-9]+)['\"]", resp.text)
        if not match:
            match = re.search(r"csrf_bd_gem_nk.*?([a-f0-9]{32})", resp.text)
        if match:
            return match.group(1)
        logger.warning("CSRF token not found in GEM page — page structure may have changed")
    except Exception as e:
        logger.error(f"Failed to load GEM page for session: {e}")
    return None


def _search_keyword(client: httpx.Client, csrf: str, keyword: str) -> list[dict]:
    """
    POST to GEM's internal API for a single keyword search.
    Returns a list of bid dicts.
    """
    results = []
    try:
        postdata = {
            "page": 1,
            "param": {
                "searchBid": keyword,
                "searchType": "fullText",
            },
            "filter": {
                "bidStatusType": "ongoing_bids",
                "byType": "all",
                "highBidValue": "",
                "byEndDate": {"from": "", "to": ""},
            },
        }

        resp = client.post(
            GEM_DATA_URL,
            data={
                "payload": json.dumps(postdata),
                "csrf_bd_gem_nk": csrf,
            },
            headers={**HEADERS, "X-Requested-With": "XMLHttpRequest",
                     "Referer": GEM_PAGE_URL,
                     "Content-Type": "application/x-www-form-urlencoded"},
            timeout=20,
        )
        resp.raise_for_status()

        data = resp.json()
        docs = data.get("response", {}).get("response", {}).get("docs", [])

        for doc in docs:
            bid_id    = str(doc.get("b_id", [""])[0]) if doc.get("b_id") else ""
            bid_number = doc.get("b_bid_number", [""])[0] if doc.get("b_bid_number") else ""
            category  = doc.get("b_category_name", [""])[0] if doc.get("b_category_name") else ""
            ministry  = doc.get("ba_official_details_minName", [""])[0] if doc.get("ba_official_details_minName") else ""
            dept      = doc.get("ba_official_details_deptName", [""])[0] if doc.get("ba_official_details_deptName") else ""
            deadline  = doc.get("final_end_date_sort", [""])[0][:10] if doc.get("final_end_date_sort") else ""
            detail_url = GEM_BID_URL.format(bid_id=bid_id) if bid_id else ""

            if bid_number:
                results.append({
                    "tender_id": bid_number,
                    "title": category,
                    "department": f"{ministry} — {dept}".strip(" —"),
                    "value": "",
                    "deadline": deadline,
                    "url": detail_url,
                    "keyword": keyword,
                })

    except httpx.TimeoutException:
        logger.warning(f"Timeout searching GEM for keyword: {keyword}")
    except Exception as e:
        logger.warning(f"Failed to search GEM for '{keyword}': {e}")

    return results


def debug_scan() -> dict:
    """
    Runs a single keyword test and returns raw details for debugging.
    Use GET /tenders/debug to call this.
    """
    result = {"csrf_found": False, "csrf_token": None, "api_status": None,
              "docs_returned": 0, "sample": None, "error": None}
    try:
        with httpx.Client(headers=HEADERS, follow_redirects=True) as client:
            # Step 1: get session + CSRF
            resp = client.get(GEM_PAGE_URL, timeout=20)
            result["page_status"] = resp.status_code
            result["page_snippet"] = resp.text[:600]   # always capture for diagnosis
            match = re.search(r"csrf_bd_gem_nk[',\"][\s:,]+['\"]([a-f0-9]+)['\"]", resp.text)
            if not match:
                match = re.search(r"csrf_bd_gem_nk.*?([a-f0-9]{32})", resp.text)
            if match:
                csrf = match.group(1)
                result["csrf_found"] = True
                result["csrf_token"] = csrf[:8] + "..."  # partial for security

                # Step 2: try one keyword
                postdata = {
                    "page": 1,
                    "param": {"searchBid": "cctv", "searchType": "fullText"},
                    "filter": {"bidStatusType": "ongoing_bids", "byType": "all",
                               "highBidValue": "", "byEndDate": {"from": "", "to": ""}},
                }
                api_resp = client.post(
                    GEM_DATA_URL,
                    data={"payload": json.dumps(postdata), "csrf_bd_gem_nk": csrf},
                    headers={**HEADERS, "X-Requested-With": "XMLHttpRequest",
                             "Referer": GEM_PAGE_URL,
                             "Content-Type": "application/x-www-form-urlencoded"},
                    timeout=20,
                )
                result["api_status"] = api_resp.status_code
                result["api_raw_snippet"] = api_resp.text[:300]
                try:
                    data = api_resp.json()
                    docs = data.get("response", {}).get("response", {}).get("docs", [])
                    result["docs_returned"] = len(docs)
                    if docs:
                        result["sample"] = {
                            "bid_number": docs[0].get("b_bid_number"),
                            "category": docs[0].get("b_category_name"),
                            "dept": docs[0].get("ba_official_details_deptName"),
                        }
                except Exception as e:
                    result["parse_error"] = str(e)
            else:
                result["error"] = "CSRF token not found in page"
                result["page_snippet"] = resp.text[:500]
    except Exception as e:
        result["error"] = str(e)
    return result


def run_scan() -> dict:
    """
    Search GEM (gem.gov.in) for each domain keyword, deduplicate,
    and save new bids to the database.
    Isolated — failures do not affect the chatbot.
    """
    new_count = 0
    errors = []

    try:
        with httpx.Client(headers=HEADERS, follow_redirects=True) as client:
            csrf = _get_session(client)
            if not csrf:
                return {
                    "new_tenders_found": 0,
                    "keywords_scanned": 0,
                    "error": "Could not obtain CSRF token from GEM portal",
                    "scanned_at": datetime.utcnow().isoformat(),
                }

            for keyword in KEYWORDS:
                try:
                    bids = _search_keyword(client, csrf, keyword)
                    for bid in bids:
                        if not tender_exists(bid["tender_id"]):
                            save_tender(
                                tender_id=bid["tender_id"],
                                title=bid["title"],
                                department=bid["department"],
                                value=bid["value"],
                                deadline=bid["deadline"],
                                url=bid["url"],
                                keyword=bid["keyword"],
                            )
                            new_count += 1
                except Exception as e:
                    errors.append(f"{keyword}: {str(e)}")
                    logger.warning(f"Error processing keyword '{keyword}': {e}")

    except Exception as e:
        logger.error(f"Tender scan failed: {e}")
        return {
            "new_tenders_found": 0,
            "keywords_scanned": 0,
            "error": str(e),
            "scanned_at": datetime.utcnow().isoformat(),
        }

    result = {
        "new_tenders_found": new_count,
        "keywords_scanned": len(KEYWORDS),
        "scanned_at": datetime.utcnow().isoformat(),
    }
    if errors:
        result["partial_errors"] = errors

    return result
