import logging
from datetime import datetime

import httpx
from bs4 import BeautifulSoup

from database import tender_exists, save_tender

logger = logging.getLogger(__name__)

# JD Enterprises business domain keywords — used for client-side filtering
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

# Latest Active Tenders listing — no CAPTCHA required for browsing
BASE_URL = "https://etenders.gov.in/eprocure/app"
LATEST_TENDERS_URL = f"{BASE_URL}?page=FrontEndLatestActiveTenders&service=page"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-IN,en;q=0.9",
}


def _matches_keyword(title: str) -> str | None:
    """Return the first matching keyword if title matches any, else None."""
    title_lower = title.lower()
    for keyword in KEYWORDS:
        if keyword in title_lower:
            return keyword
    return None


def _fetch_tenders_page(client: httpx.Client, page_url: str) -> list[dict]:
    """Fetch a single listing page and return all parsed tender rows."""
    results = []
    try:
        response = client.get(page_url, timeout=20)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # etenders.gov.in uses class="list_table" for tender listings
        table = soup.find("table", {"class": "list_table"})
        if not table:
            logger.warning("No list_table found on page — site structure may have changed")
            return results

        rows = table.find_all("tr")
        for row in rows:
            # Skip header and footer rows
            if row.get("class") and any(
                c in row.get("class", []) for c in ["list_header", "list_footer"]
            ):
                continue

            cols = row.find_all("td")
            if len(cols) < 4:
                continue

            # Column layout: S.No | AOC Date | e-Published Date | Title & Ref No | Organisation | AOC
            title_cell = cols[3] if len(cols) > 3 else cols[-1]
            title_text = title_cell.get_text(separator=" ", strip=True)

            # Extract tender ID from the title cell (Ref.No.)
            tender_id = ""
            anchor = title_cell.find("a")
            if anchor:
                href = anchor.get("href", "")
                detail_url = href if href.startswith("http") else f"{BASE_URL}{href}"
                # Use the link's text or href fragment as tender ID
                tender_id = href.split("tenderId=")[-1].split("&")[0] if "tenderId=" in href else href.split("/")[-1]
            else:
                detail_url = ""

            # Fall back to title as tender ID if nothing else available
            if not tender_id:
                tender_id = title_text[:80]

            organisation = cols[4].get_text(strip=True) if len(cols) > 4 else ""
            deadline = cols[1].get_text(strip=True) if len(cols) > 1 else ""

            results.append({
                "tender_id": tender_id,
                "title": title_text,
                "department": organisation,
                "value": "",          # not shown on listing page
                "deadline": deadline,
                "url": detail_url,
            })

    except httpx.TimeoutException:
        logger.warning("Timeout fetching latest tenders page")
    except httpx.HTTPStatusError as e:
        logger.warning(f"HTTP error fetching tenders: {e.response.status_code}")
    except Exception as e:
        logger.warning(f"Failed to fetch tenders page: {e}")

    return results


def run_scan() -> dict:
    """
    Fetch the latest active tenders listing from etenders.gov.in,
    filter by domain keywords client-side, and save new matches.
    No CAPTCHA required — browsing the listing page is open access.
    Completely isolated — failures do not affect the chatbot.
    """
    new_count = 0
    errors = []

    try:
        with httpx.Client(headers=HEADERS, follow_redirects=True) as client:
            tenders = _fetch_tenders_page(client, LATEST_TENDERS_URL)

            if not tenders:
                logger.warning("No tenders fetched — page may be empty or structure changed")

            for tender in tenders:
                try:
                    matched_keyword = _matches_keyword(tender["title"])
                    if not matched_keyword:
                        continue  # not relevant to JD's domain

                    if tender_exists(tender["tender_id"]):
                        continue  # already stored

                    save_tender(
                        tender_id=tender["tender_id"],
                        title=tender["title"],
                        department=tender["department"],
                        value=tender["value"],
                        deadline=tender["deadline"],
                        url=tender["url"],
                        keyword=matched_keyword,
                    )
                    new_count += 1

                except Exception as e:
                    errors.append(f"{tender.get('tender_id', '?')}: {str(e)}")
                    logger.warning(f"Error processing tender: {e}")

    except Exception as e:
        logger.error(f"Tender scan failed: {e}")
        return {
            "new_tenders_found": 0,
            "keywords_scanned": len(KEYWORDS),
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
