from fastapi import FastAPI
from conversation import next_question, update_state
from recommender import generate_recommendation, format_recommendation
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all (dev mode)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sessions = {}

@app.post("/chat")
async def chat(data: dict):
    user_id = data.get("user_id", "default")
    user_input = data.get("message")

    # Initialize session
    if user_id not in sessions:
        sessions[user_id] = {
            "facility": None,
            "goal": None,
            "size": None,
            "setup_type": None
        }

    state = sessions[user_id]

    # 🔥 Step 1: Update state
    state = update_state(state, user_input)

    # 🔥 Step 2: Ask next question IF incomplete
    question = next_question(state)

    if question:
        return {
            "type": "question",
            "message": question
        }

    # 🔥 Step 3: Only now generate recommendation
    result = generate_recommendation(state)
    response = format_recommendation(result)

    # Reset session (optional)
    sessions[user_id] = {
        "facility": None,
        "goal": None,
        "size": None,
        "setup_type": None
    }

    return {
        "type": "result",
        "message": response
    }