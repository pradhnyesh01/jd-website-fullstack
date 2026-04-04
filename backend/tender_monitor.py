import logging
from datetime import datetime

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

SEARCH_URL = "https://tenders.gov.in/tenders/advancedsearchlist.aspx"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-IN,en;q=0.9",
}


def _search_keyword(client: httpx.Client, keyword: str) -> list[dict]:
    """Search tenders.gov.in for a single keyword and return parsed rows."""
    results = []
    try:
        params = {
            "searchkeyword": keyword,
            "tendertype": "",
            "state": "",
            "dept": "",
        }
        response = client.get(SEARCH_URL, params=params, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # tenders.gov.in renders results in a table with class "table"
        table = soup.find("table", {"class": "table"})
        if not table:
            return results

        rows = table.find_all("tr")[1:]  # skip header row
        for row in rows:
            cols = row.find_all("td")
            if len(cols) < 5:
                continue

            # Extract fields from table columns
            tender_id = cols[0].get_text(strip=True)
            title = cols[1].get_text(strip=True)
            department = cols[2].get_text(strip=True)
            value = cols[3].get_text(strip=True) if len(cols) > 3 else ""
            deadline = cols[4].get_text(strip=True) if len(cols) > 4 else ""

            # Build detail URL if anchor exists
            anchor = cols[1].find("a")
            detail_url = ""
            if anchor and anchor.get("href"):
                href = anchor["href"]
                detail_url = href if href.startswith("http") else f"https://tenders.gov.in{href}"

            if tender_id:
                results.append({
                    "tender_id": tender_id,
                    "title": title,
                    "department": department,
                    "value": value,
                    "deadline": deadline,
                    "url": detail_url,
                    "keyword": keyword,
                })
    except httpx.TimeoutException:
        logger.warning(f"Timeout while searching keyword: {keyword}")
    except httpx.HTTPStatusError as e:
        logger.warning(f"HTTP error for keyword '{keyword}': {e.response.status_code}")
    except Exception as e:
        logger.warning(f"Failed to scrape keyword '{keyword}': {e}")

    return results


def run_scan() -> dict:
    """
    Run a full tender scan across all keywords.
    Returns a dict with counts and any error message.
    Completely isolated — failures do not affect the chatbot.
    """
    new_count = 0
    errors = []

    try:
        with httpx.Client(headers=HEADERS, follow_redirects=True) as client:
            for keyword in KEYWORDS:
                try:
                    rows = _search_keyword(client, keyword)
                    for row in rows:
                        if not tender_exists(row["tender_id"]):
                            save_tender(
                                tender_id=row["tender_id"],
                                title=row["title"],
                                department=row["department"],
                                value=row["value"],
                                deadline=row["deadline"],
                                url=row["url"],
                                keyword=row["keyword"],
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
