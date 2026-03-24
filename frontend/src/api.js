import axios from "axios";

const API_URL = process.env.REACT_APP_BACKEND_URL || "http://127.0.0.1:5000";

// 🎧 Upload Audio and Analyze
export const uploadAudio = async (file, language) => {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("language", language);   // ✅ send selected language

  const res = await axios.post(`${API_URL}/analyze_audio`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return res.data;
};

// 💬 Chat with the AI Reporter (optional)
export const sendChat = async (question, context) => {
  const res = await axios.post(`${API_URL}/chat`, { question, context });
  return res.data;
};