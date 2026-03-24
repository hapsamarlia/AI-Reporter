import React, { useState } from "react";
import UploadAudio from "./components/UploadAudio";
import ReportDisplay from "./components/ReportDisplay";
import ChatbotUI from "./components/ChatbotUI";
import "./App.css";

function App() {
  const [reportData, setReportData] = useState(null);
  const [language, setLanguage] = useState("French"); // ✅ fixed

  return (
    <div className="app-container">
      <h1>🤖 Multilingual AI Reporter</h1>

      <div className="language-select">
        <label>Select Translation Language: </label>
        <select
          value={language}
          onChange={(e) => setLanguage(e.target.value)}
        >
          <option value="Hindi">Hindi</option>
          <option value="Tamil">Tamil</option>
          <option value="Spanish">Spanish</option>
          <option value="German">German</option>
          <option value="French">French</option>
        </select>
      </div>

      <UploadAudio setReportData={setReportData} language={language} />

      <ReportDisplay data={reportData} />

      {reportData && <ChatbotUI context={reportData.report} />}
    </div>
  );
}

export default App;