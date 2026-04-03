import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KB_PATH = os.path.join(BASE_DIR, "knowledge_base.json")

with open(KB_PATH) as f:
    kb = json.load(f)

# ================================
# STEP 3: CORE RECOMMENDATION LOGIC
# ================================

def get_systems(facility, goal):
    facility_systems = set()
    goal_systems = set()

    if facility in kb["facility_types"]:
        facility_systems = set(kb["facility_types"][facility]["systems"])

    if goal in kb["goals"]:
        goal_systems = set(kb["goals"][goal]["systems"])

    # 🔥 Priority logic
    if goal == "security":
        # Only include relevant systems
        return list(goal_systems.union({"Networking"}))

    if goal == "communication":
        return list(goal_systems.union({"Networking"}))

    if goal == "av_experience":
        return list(goal_systems)

    if goal == "full_integration":
        return list(goal_systems.union(facility_systems))

    # fallback
    return list(facility_systems.union(goal_systems))

def expand_systems(systems):
    detailed = {}

    for system in systems:
        if system in kb["system_details"]:
            detailed[system] = kb["system_details"][system]["components"]

    return detailed


# ================================
# STEP 4: CONTEXT LOGIC
# ================================

def apply_size_logic(size):
    if size in kb["size_rules"]:
        return kb["size_rules"][size]["approach"]
    return ""


def apply_setup_logic(setup_type):
    if setup_type in kb["setup_type"]:
        return kb["setup_type"][setup_type]["approach"]
    return ""


# ================================
# MAIN RECOMMENDATION FUNCTION
# ================================

def get_brands(system, budget_tier):
    brand_map = kb.get("brand_recommendations", {})
    if system in brand_map and budget_tier in brand_map[system]:
        return brand_map[system][budget_tier]
    return []


def generate_recommendation(data):
    facility = data.get("facility")
    goal = data.get("goal")
    size = data.get("size")
    setup_type = data.get("setup_type")
    budget_tier = data.get("budget_tier")
    num_zones = data.get("num_zones")

    # Step 1: Get systems
    systems = get_systems(facility, goal)

    # Step 2: Expand systems into components
    details = expand_systems(systems)

    # Step 3: Attach brand recommendations per system
    brands = {}
    if budget_tier:
        for system in details:
            recommended = get_brands(system, budget_tier)
            if recommended:
                brands[system] = recommended

    # Step 4: Apply context logic
    size_note = apply_size_logic(size)
    setup_note = apply_setup_logic(setup_type)

    return {
        "systems": details,
        "brands": brands,
        "size_note": size_note,
        "setup_note": setup_note,
        "facility": facility,
        "size": size,
        "setup_type": setup_type,
        "budget_tier": budget_tier,
        "num_zones": num_zones,
    }


# ================================
# STEP 5: OUTPUT FORMATTING
# ================================

def format_recommendation(result):
    output = "Based on your requirements, here’s a recommended setup:\n\n"

    # Systems + components + brands
    brands = result.get("brands", {})
    for system, components in result["systems"].items():
        if components:
            output += f"🔹 {system}\n"
            for comp in components:
                output += f"  - {comp}\n"
        else:
            output += f"🔹 {system} — contact us for detailed specification\n"
        if system in brands:
            output += f"  → Recommended brands: {', '.join(brands[system])}\n"
        output += "\n"

    # Size logic
    if result["size_note"]:
        output += f"📏 Deployment Approach:\n{result['size_note']}\n\n"

    # Setup logic
    if result["setup_note"]:
        output += f"⚙️ Setup Strategy:\n{result['setup_note']}\n\n"

    output += "Final configuration will be optimized after site evaluation."

    return output