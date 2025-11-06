import React, { useState } from "react";
import { sendChat } from "../api";

function ChatbotUI({ context }) {
  const [question, setQuestion] = useState("");
  const [chat, setChat] = useState([]);

  const handleAsk = async () => {
    if (!question) return;
    const res = await sendChat(question, context);
    setChat([...chat, { q: question, a: res.response }]);
    setQuestion("");
  };

  return (
    <div className="chatbot-box">
      <h2>💬 Ask the AI Reporter</h2>
      <div className="chat-window">
        {chat.map((c, i) => (
          <div key={i} className="chat-msg">
            <p><b>You:</b> {c.q}</p>
            <p><b>AI:</b> {c.a}</p>
          </div>
        ))}
      </div>
      <input
        type="text"
        value={question}
        placeholder="Ask something..."
        onChange={(e) => setQuestion(e.target.value)}
      />
      <button onClick={handleAsk}>Send</button>
    </div>
  );
}

export default ChatbotUI;
