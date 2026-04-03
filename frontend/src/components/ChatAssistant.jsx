import { useState, useEffect, useRef } from "react";
import { sendMessage } from "../services/api";

// Maps system names from quote_data to QuoteModal service options
const SYSTEM_TO_SERVICE = {
  "CCTV": "CCTV Surveillance",
  "Perimeter Security": "CCTV Surveillance",
  "Access Control": "CCTV Surveillance",
  "Sound System": "Audio Systems",
  "PA System": "Audio Systems",
  "AV Systems": "Audio Systems",
  "Video Conferencing": "Audio Systems",
  "Stage Lighting": "Lighting Systems",
  "Lighting": "Lighting Systems",
  "Projection": "LCD Projectors",
  "LED Display": "LCD Projectors",
};

export default function ChatAssistant({ isOpen, setIsOpen, onOpenQuote }) {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "Hi! I'll help you design the right system.\n\nTell me what you're planning 🙂"
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [lastQuoteData, setLastQuoteData] = useState(null);

  const messagesEndRef = useRef(null);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userText = input;
    setMessages(prev => [...prev, { sender: "user", text: userText }]);
    setInput("");
    setLoading(true);

    try {
      const response = await sendMessage(userText);

      setMessages(prev => [...prev, { sender: "bot", text: response.message }]);

      if (response.type === "result" && response.quote_data) {
        setLastQuoteData(response.quote_data);
      }
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { sender: "bot", text: "Something went wrong. Please try again." }
      ]);
    }

    setLoading(false);
  };

  // Auto-scroll
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  if (!isOpen) return null;

  return (
    <div className="fixed bottom-6 right-6 w-[360px] h-[560px] bg-white rounded-2xl shadow-2xl flex flex-col overflow-hidden border z-50">

      {/* Header */}
      <div className="bg-black text-white px-4 py-3 flex justify-between items-center">
        <span className="font-semibold">AI Assistant</span>
        <button onClick={() => setIsOpen(false)}>×</button>
      </div>

      {/* Messages */}
      <div className="flex-1 p-4 overflow-y-auto space-y-3 bg-gray-50">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`max-w-[75%] px-4 py-2 rounded-2xl text-sm whitespace-pre-line ${
              msg.sender === "user"
                ? "ml-auto bg-blue-600 text-white"
                : "bg-white border shadow-sm"
            }`}
          >
            {msg.text}
          </div>
        ))}

        {/* Typing indicator */}
        {loading && (
          <div className="text-sm text-gray-500">AI is thinking...</div>
        )}

        {/* Get Quote button — shown after recommendation is delivered */}
        {lastQuoteData && !loading && (
          <div className="flex justify-center pt-1">
            <button
              onClick={() => onOpenQuote && onOpenQuote(lastQuoteData)}
              className="bg-green-600 hover:bg-green-700 text-white text-sm font-medium px-4 py-2 rounded-xl transition"
            >
              📋 Get Quote for This Setup
            </button>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="flex border-t">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Type your answer..."
          className="flex-1 px-3 py-2 outline-none text-sm"
        />
        <button
          onClick={handleSend}
          className="bg-blue-600 text-white px-4 hover:bg-blue-700 transition"
        >
          Send
        </button>
      </div>
    </div>
  );
}
