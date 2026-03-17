# conversation.py

from extract_pipeline import process_query


# ================================
# STEP 4.1: Decide next question
# ================================

def next_question(state):
    if not state["facility"]:
        return "What type of facility is this for? (e.g., school, office, hospital)"

    if not state["goal"]:
        return "What is your main objective? (security, communication, AV experience, full integration)"

    if not state["size"]:
        return "How large is the space? (small, medium, large or describe)"

    if not state["setup_type"]:
        return "Are you setting this up from scratch or upgrading an existing system?"

    return None


# ================================
# STEP 4.2: Update state
# ================================

def update_state(state, user_input):
    user_input_lower = user_input.lower()

    # 🔥 Step 1: Try direct keyword matching FIRST

    # Facility
    if not state["facility"]:
        if any(word in user_input_lower for word in ["school", "college", "office", "hospital", "auditorium", "factory", "stadium"]):
            state["facility"] = next(
                word for word in ["school", "college", "office", "hospital", "auditorium", "factory", "stadium"]
                if word in user_input_lower
            )
            return state

    # Goal
    if not state["goal"]:
        if any(word in user_input_lower for word in ["security", "communication", "av", "integration"]):
            if "security" in user_input_lower:
                state["goal"] = "security"
            elif "communication" in user_input_lower:
                state["goal"] = "communication"
            elif "av" in user_input_lower:
                state["goal"] = "av_experience"
            elif "integration" in user_input_lower:
                state["goal"] = "full_integration"
            return state

    # Size
    if not state["size"]:
        if any(word in user_input_lower for word in ["small", "medium", "large", "campus"]):
            if "small" in user_input_lower:
                state["size"] = "small"
            elif "medium" in user_input_lower:
                state["size"] = "medium"
            else:
                state["size"] = "large"
            return state

    # Setup type
    if not state["setup_type"]:
        if any(word in user_input_lower for word in ["new", "upgrade"]):
            if "upgrade" in user_input_lower:
                state["setup_type"] = "upgrade"
            else:
                state["setup_type"] = "new"
            return state

    # 🔥 Step 2: fallback to LLM ONLY if needed
    from extract_pipeline import process_query
    extracted = process_query(user_input)

    for key in ["facility", "goal", "size", "setup_type"]:
        if not state.get(key) and extracted.get(key):
            state[key] = extracted[key]
            break

    return state