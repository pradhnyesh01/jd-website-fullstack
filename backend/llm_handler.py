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
- Infer intelligently if not explicitly mentioned
- Return ONLY valid JSON
- Do NOT explain anything

Examples:

Input: "CCTV for office"
Output: {{
  "facility": "office",
  "goal": "security",
  "size": "medium",
  "setup_type": "new"
}}

Input: "Upgrade sound system in auditorium"
Output: {{
  "facility": "auditorium",
  "goal": "av_experience",
  "size": "medium",
  "setup_type": "upgrade"
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