import React from "react";

function ReportDisplay({ data }) {
  if (!data) return null;

  return (
    <div className="report-box">
      <h2>📊 AI Reporter — Business Analysis</h2>
      <p><b>🗣️ Transcription:</b> {data.transcription}</p>
      <p><b>🧠 Report:</b> {data.report}</p>
      <p><b>🌍 Translated Report (French):</b> {data.translated_report}</p>
    </div>
  );
}

export default ReportDisplay;
