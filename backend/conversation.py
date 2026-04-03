# conversation.py

from llm_handler import extract_user_info
from parser import normalize_output


# ================================
# STEP 4.1: Decide next question
# ================================

def next_question(state):
    if not state.get("facility"):
        return "What type of facility is this for? (e.g., school, office, hospital)"

    if not state.get("goal"):
        return "What is your main objective? (security, communication, AV experience, full integration)"

    if not state.get("size"):
        return "How large is the space? (small, medium, large or describe)"

    if not state.get("setup_type"):
        return "Are you setting this up from scratch or upgrading an existing system?"

    if not state.get("budget_tier"):
        return "What is your approximate budget range? (low: under ₹2L / medium: ₹2–10L / high: above ₹10L)"

    if not state.get("num_zones"):
        return "How many separate areas or zones need coverage? (single / multiple)"

    return None


# ================================
# STEP 4.2: Update state
# ================================

def update_state(state, user_input):
    user_input_lower = user_input.lower()

    # Step 1: Try direct keyword matching across ALL fields (no early returns)

    # Facility
    if not state["facility"]:
        if any(word in user_input_lower for word in ["school", "college", "office", "hospital", "auditorium", "factory", "stadium"]):
            state["facility"] = next(
                word for word in ["school", "college", "office", "hospital", "auditorium", "factory", "stadium"]
                if word in user_input_lower
            )

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

    # Size
    large_words = ["large", "big", "campus", "huge", "massive", "wide"]
    small_words = ["small", "tiny", "single room", "compact"]
    if not state["size"]:
        if any(w in user_input_lower for w in large_words + small_words + ["medium"]):
            if any(w in user_input_lower for w in small_words):
                state["size"] = "small"
            elif "medium" in user_input_lower:
                state["size"] = "medium"
            elif any(w in user_input_lower for w in large_words):
                state["size"] = "large"

    # Setup type
    upgrade_words = ["upgrade", "existing", "already have", "replace", "retrofit"]
    new_words = ["new", "scratch", "fresh", "brand new", "greenfield"]
    if not state["setup_type"]:
        if any(w in user_input_lower for w in upgrade_words + new_words):
            if any(w in user_input_lower for w in upgrade_words):
                state["setup_type"] = "upgrade"
            else:
                state["setup_type"] = "new"

    # Budget tier
    # Use budget-specific context words as primary triggers to avoid
    # colliding with "medium"/"low"/"high" answers meant for size.
    # Bare low/medium/high only apply once setup_type is filled
    # (i.e., the size question is already answered).
    budget_context_words = ["budget", "cost", "price", "affordable", "cheap", "premium", "expensive", "₹", "lakh"]
    if not state.get("budget_tier"):
        if any(w in user_input_lower for w in budget_context_words):
            if any(w in user_input_lower for w in ["low", "cheap", "affordable"]):
                state["budget_tier"] = "low"
            elif any(w in user_input_lower for w in ["high", "premium", "expensive"]):
                state["budget_tier"] = "high"
            else:
                state["budget_tier"] = "medium"
        elif state.get("setup_type") and any(w in user_input_lower for w in ["low", "medium", "high"]):
            # Safe to use bare words here — size is already answered
            if "low" in user_input_lower:
                state["budget_tier"] = "low"
            elif "high" in user_input_lower:
                state["budget_tier"] = "high"
            elif "medium" in user_input_lower:
                state["budget_tier"] = "medium"

    # Number of zones
    if not state.get("num_zones"):
        if any(word in user_input_lower for word in ["single", "one", "multiple", "several", "many", "zones", "areas"]):
            if any(w in user_input_lower for w in ["multiple", "several", "many", "zones", "areas"]):
                state["num_zones"] = "multiple"
            elif any(w in user_input_lower for w in ["single", "one"]):
                state["num_zones"] = "single"

    # Step 2: fallback to LLM for any still-missing fields
    all_fields = ["facility", "goal", "size", "setup_type", "budget_tier", "num_zones"]
    missing_fields = [f for f in all_fields if not state.get(f)]

    if missing_fields:
        extracted = normalize_output(extract_user_info(user_input))

        if extracted:
            # Short replies (≤ 3 words) are answering one specific question —
            # only apply the result to the first missing field to prevent
            # the LLM from filling unrelated fields with guesses.
            word_count = len(user_input.strip().split())
            fields_to_apply = [missing_fields[0]] if word_count <= 3 else missing_fields

            for key in fields_to_apply:
                if not state.get(key) and extracted.get(key):
                    state[key] = extracted[key]

    return state