import React, { useState } from "react";
import UploadAudio from "./components/UploadAudio";
import ReportDisplay from "./components/ReportDisplay";
import ChatbotUI from "./components/ChatbotUI";
import "./App.css";

function App() {
  const [reportData, setReportData] = useState(null);

  return (
    <div className="app-container">
      <h1>🤖 Multilingual AI Reporter</h1>
      <UploadAudio setReportData={setReportData} />
      <ReportDisplay data={reportData} />
      {reportData && <ChatbotUI context={reportData.report} />}
    </div>
  );
}

export default App;
