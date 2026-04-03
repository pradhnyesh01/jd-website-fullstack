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

Rules:
- Only extract a field if the user has clearly stated or strongly implied it
- If a field cannot be confidently determined from the query, set it to null
- Return ONLY valid JSON
- Do NOT explain anything

Examples:

Input: "CCTV for office"
Output: {{
  "facility": "office",
  "goal": "security",
  "size": null,
  "setup_type": null
}}

Input: "Upgrade sound system in auditorium"
Output: {{
  "facility": "auditorium",
  "goal": "av_experience",
  "size": null,
  "setup_type": "upgrade"
}}

Input: "I need help"
Output: {{
  "facility": null,
  "goal": null,
  "size": null,
  "setup_type": null
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