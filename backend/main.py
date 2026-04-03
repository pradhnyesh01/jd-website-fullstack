import os
import time
from fastapi import FastAPI
from pydantic import BaseModel, Field
from conversation import next_question, update_state
from recommender import generate_recommendation, format_recommendation
from database import init_db, log_session, get_all_sessions, get_summary
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,https://jdenterprisespune.co.in,https://www.jdenterprisespune.co.in"
).split(",")
SESSION_TTL = 1800  # 30 minutes

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["Content-Type"],
)

sessions = {}

# Initialise database on startup
init_db()


class ChatRequest(BaseModel):
    user_id: str = "default"
    message: str = Field(..., min_length=1, max_length=2000)


def get_or_create_session(user_id: str) -> dict:
    now = time.time()
    # Purge expired sessions
    expired = [uid for uid, s in sessions.items() if now - s["last_active"] > SESSION_TTL]
    for uid in expired:
        del sessions[uid]

    if user_id not in sessions:
        sessions[user_id] = {
            "state": {"facility": None, "goal": None, "size": None, "setup_type": None,
                      "budget_tier": None, "num_zones": None},
            "last_active": now,
        }
    else:
        sessions[user_id]["last_active"] = now

    return sessions[user_id]["state"]


@app.post("/chat")
async def chat(data: ChatRequest):
    user_id = data.user_id
    user_input = data.message

    state = get_or_create_session(user_id)

    # Step 1: Update state
    state = update_state(state, user_input)
    sessions[user_id]["state"] = state

    # Step 2: Ask next question if state is incomplete
    question = next_question(state)
    if question:
        return {"type": "question", "message": question}

    # Step 3: Generate recommendation
    result = generate_recommendation(state)
    response = format_recommendation(result)

    # Log completed session to SQLite
    log_session(user_id, state, result)

    # Reset session
    sessions[user_id]["state"] = {"facility": None, "goal": None, "size": None, "setup_type": None,
                                   "budget_tier": None, "num_zones": None}

    return {
        "type": "result",
        "message": response,
        "quote_data": result,
    }


@app.get("/admin/sessions")
async def admin_sessions():
    return {"sessions": get_all_sessions()}


@app.get("/admin/summary")
async def admin_summary():
    return get_summary()
