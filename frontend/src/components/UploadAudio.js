import React, { useState } from "react";
import { uploadAudio } from "../api";
import Loader from "./Loader";

function UploadAudio({ setReportData }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return alert("Please select an audio file!");
    setLoading(true);
    try {
      const data = await uploadAudio(file);
      setReportData(data);
    } catch (error) {
      alert("⚠️ Error processing audio! Check if backend is running.");
    }
    setLoading(false);
  };

  return (
    <div className="upload-box">
      <h2>🎙️ Upload Audio for Analysis</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="audio/*"
          onChange={(e) => setFile(e.target.files[0])}
        />
        <button type="submit">Generate Report</button>
      </form>
      {loading && <Loader />}
    </div>
  );
}

export default UploadAudio;
