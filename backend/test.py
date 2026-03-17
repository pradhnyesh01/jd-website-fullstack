import requests

url = "http://localhost:8000/chat"

user_id = "test_user"

messages = [
    "I need CCTV for a college",
    "security",
    "large campus",
    "new setup"
]

for msg in messages:
    res = requests.post(url, json={
        "user_id": user_id,
        "message": msg
    })

    print("\nUser:", msg)
    print("Bot:", res.json()["message"])