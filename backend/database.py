import os
import json
import logging
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")

logger = logging.getLogger(__name__)


def get_conn():
    import psycopg2
    # Supabase requires SSL — append sslmode if not already present
    url = DATABASE_URL
    if url and "sslmode" not in url:
        url += "?sslmode=require"
    return psycopg2.connect(url)


def init_db():
    if not DATABASE_URL:
        logger.warning("DATABASE_URL not set — session logging disabled.")
        return
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS chat_sessions (
                id          SERIAL PRIMARY KEY,
                user_id     TEXT,
                facility    TEXT,
                goal        TEXT,
                size        TEXT,
                setup_type  TEXT,
                budget_tier TEXT,
                num_zones   TEXT,
                systems     TEXT,
                brands      TEXT,
                timestamp   TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS tenders (
                id              SERIAL PRIMARY KEY,
                tender_id       TEXT UNIQUE,
                title           TEXT,
                department      TEXT,
                value           TEXT,
                deadline        TEXT,
                url             TEXT,
                matched_keyword TEXT,
                found_at        TEXT
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
        logger.info("Database initialised successfully.")
    except Exception as e:
        logger.error(f"Database init failed: {e} — session logging disabled.")


def log_session(user_id: str, state: dict, result: dict):
    if not DATABASE_URL:
        return
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO chat_sessions
            (user_id, facility, goal, size, setup_type, budget_tier, num_zones, systems, brands, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id,
            state.get("facility"),
            state.get("goal"),
            state.get("size"),
            state.get("setup_type"),
            state.get("budget_tier"),
            state.get("num_zones"),
            json.dumps(list(result.get("systems", {}).keys())),
            json.dumps(result.get("brands", {})),
            datetime.utcnow().isoformat(),
        ))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logger.error(f"Failed to log session: {e}")


def get_all_sessions() -> list:
    if not DATABASE_URL:
        return []
    try:
        import psycopg2.extras
        conn = get_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM chat_sessions ORDER BY timestamp DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"Failed to fetch sessions: {e}")
        return []


def tender_exists(tender_id: str) -> bool:
    if not DATABASE_URL:
        return False
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM tenders WHERE tender_id = %s LIMIT 1", (tender_id,))
        exists = cur.fetchone() is not None
        cur.close()
        conn.close()
        return exists
    except Exception as e:
        logger.error(f"tender_exists check failed: {e}")
        return False


def save_tender(tender_id: str, title: str, department: str, value: str,
                deadline: str, url: str, keyword: str):
    if not DATABASE_URL:
        return
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO tenders (tender_id, title, department, value, deadline, url, matched_keyword, found_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (tender_id) DO NOTHING
        """, (
            tender_id, title, department, value, deadline, url, keyword,
            datetime.utcnow().isoformat(),
        ))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        logger.error(f"save_tender failed: {e}")


def get_tenders() -> list:
    if not DATABASE_URL:
        return []
    try:
        import psycopg2.extras
        conn = get_conn()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM tenders ORDER BY found_at DESC")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"get_tenders failed: {e}")
        return []


def get_summary() -> dict:
    if not DATABASE_URL:
        return {"error": "DATABASE_URL not configured"}
    try:
        conn = get_conn()
        cur = conn.cursor()

        cur.execute("SELECT COUNT(*) FROM chat_sessions")
        total = cur.fetchone()[0]

        cur.execute("SELECT facility, COUNT(*) FROM chat_sessions GROUP BY facility ORDER BY COUNT(*) DESC")
        facility_counts = dict(cur.fetchall())

        cur.execute("SELECT goal, COUNT(*) FROM chat_sessions GROUP BY goal ORDER BY COUNT(*) DESC")
        goal_counts = dict(cur.fetchall())

        cur.execute("SELECT budget_tier, COUNT(*) FROM chat_sessions GROUP BY budget_tier ORDER BY COUNT(*) DESC")
        budget_counts = dict(cur.fetchall())

        cur.close()
        conn.close()
        return {
            "total_sessions": total,
            "by_facility": facility_counts,
            "by_goal": goal_counts,
            "by_budget": budget_counts,
        }
    except Exception as e:
        logger.error(f"Failed to get summary: {e}")
        return {"error": str(e)}
