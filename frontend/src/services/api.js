export async function sendMessage(message, userId = "user1") {
  const res = await fetch("http://127.0.0.1:8000/chat", {
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