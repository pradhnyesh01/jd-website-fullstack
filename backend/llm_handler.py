import json
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # ← IMPORTANT

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def extract_user_info(user_input):
    prompt = f"""
You are an expert AI system for infrastructure planning.

Extract the following fields from the user query:

- facility (choose: school, college, office, auditorium, hospital, factory, stadium, retail, other)
- goal (choose: security, communication, av_experience, collaboration, full_integration)
- size (choose: small, medium, large)
- setup_type (choose: new, upgrade)
- budget_tier (choose: low, medium, high — low is under ₹2L, medium is ₹2–10L, high is above ₹10L)
- num_zones (choose: single, multiple — number of separate coverage areas)

Rules:
- Only extract a field if the user has EXPLICITLY stated or very strongly implied it
- If a field is not clearly present in the message, set it to null — do NOT guess or use defaults
- NEVER use "other", "full_integration", or "medium" as fallback values — use null instead
- Return ONLY valid JSON
- Do NOT explain anything

Examples:

Input: "CCTV for office"
Output: {{
  "facility": "office",
  "goal": "security",
  "size": null,
  "setup_type": null,
  "budget_tier": null,
  "num_zones": null
}}

Input: "Upgrade sound system in large auditorium, medium budget, multiple zones"
Output: {{
  "facility": "auditorium",
  "goal": "av_experience",
  "size": "large",
  "setup_type": "upgrade",
  "budget_tier": "medium",
  "num_zones": "multiple"
}}

Input: "I need help"
Output: {{
  "facility": null,
  "goal": null,
  "size": null,
  "setup_type": null,
  "budget_tier": null,
  "num_zones": null
}}

Input: "scratch"
Output: {{
  "facility": null,
  "goal": null,
  "size": null,
  "setup_type": "new",
  "budget_tier": null,
  "num_zones": null
}}

Input: "just one area"
Output: {{
  "facility": null,
  "goal": null,
  "size": null,
  "setup_type": null,
  "budget_tier": null,
  "num_zones": "single"
}}

Now extract:

User Query:
{user_input}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content