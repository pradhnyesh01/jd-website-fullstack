import os
import json
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = os.getenv("DATABASE_URL")


def get_conn():
    return psycopg2.connect(DATABASE_URL)


def init_db():
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
    conn.commit()
    cur.close()
    conn.close()


def log_session(user_id: str, state: dict, result: dict):
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


def get_all_sessions() -> list:
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM chat_sessions ORDER BY timestamp DESC")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [dict(row) for row in rows]


def get_summary() -> dict:
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
