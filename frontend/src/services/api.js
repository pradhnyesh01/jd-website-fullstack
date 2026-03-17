const BASE_URL = import.meta.env.VITE_API_URL;

export async function sendMessage(message, userId = "user1") {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      user_id: userId,
      message: message
    })
  });

  return res.json();
}