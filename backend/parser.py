import json

VALID_FACILITIES = ["school", "college", "office", "auditorium", "hospital", "factory", "stadium", "retail", "other"]
VALID_GOALS = ["security", "communication", "av_experience", "collaboration", "full_integration"]
VALID_SIZES = ["small", "medium", "large"]
VALID_SETUP = ["new", "upgrade"]
VALID_BUDGET = ["low", "medium", "high"]
VALID_ZONES = ["single", "multiple"]

def normalize_output(raw_output):
    try:
        data = json.loads(raw_output)
    except:
        return None

    return {
        "facility":    data.get("facility")    if data.get("facility")    in VALID_FACILITIES else None,
        "goal":        data.get("goal")        if data.get("goal")        in VALID_GOALS      else None,
        "size":        data.get("size")        if data.get("size")        in VALID_SIZES      else None,
        "setup_type":  data.get("setup_type")  if data.get("setup_type")  in VALID_SETUP      else None,
        "budget_tier": data.get("budget_tier") if data.get("budget_tier") in VALID_BUDGET     else None,
        "num_zones":   data.get("num_zones")   if data.get("num_zones")   in VALID_ZONES      else None,
    }