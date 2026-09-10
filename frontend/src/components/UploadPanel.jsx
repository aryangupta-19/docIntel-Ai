import { useState } from "react";
import axios from "axios";

function UploadPanel({ setResult, setLoading, setError }) {
  const [file, setFile] = useState(null);
  const [analysisType, setAnalysisType] = useState("summary");

  const handleSubmit = async () => {
    if (!file) return alert("Please select a PDF document.");

    const formData = new FormData();
    formData.append("file", file);

    // Keeping this so backend won't break for now
    formData.append("project_type", analysisType);
    formData.append("city_tier", "general");

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await axios.post(
        "http://localhost:8000/analyze",
        formData
      );

      setResult(response.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        background: "#f8f9fa",
        padding: "1.8rem",
        borderRadius: "12px",
        marginBottom: "2rem",
      }}
    >
      <h2 style={{ marginTop: 0 }}>Upload Documents</h2>

      <p style={{ color: "#666", marginTop: "-5px", marginBottom: "25px" }}>
        Upload a PDF document and let AI generate summaries, insights,
        compliance checks and document intelligence.
      </p>

      <div
        style={{
          display: "flex",
          gap: "1rem",
          flexWrap: "wrap",
          alignItems: "flex-end",
        }}
      >
        <div>
          <label
            style={{
              display: "block",
              marginBottom: "4px",
              fontWeight: "bold",
            }}
          >
            PDF Document
          </label>

          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
          />
        </div>

        <div>
          <label
            style={{
              display: "block",
              marginBottom: "4px",
              fontWeight: "bold",
            }}
          >
            Analysis Type
          </label>

          <select
            value={analysisType}
            onChange={(e) => setAnalysisType(e.target.value)}
            style={{
              padding: "6px",
              borderRadius: "4px",
              border: "1px solid #ccc",
            }}
          >
            <option value="summary">Executive Summary</option>
            <option value="compliance">Compliance Analysis</option>
            <option value="risk">Risk Assessment</option>
            <option value="insights">Key Insights</option>
            <option value="comparison">Document Comparison</option>
          </select>
        </div>

        <button
          onClick={handleSubmit}
          style={{
            padding: "8px 20px",
            background: "#4F9DFF",
            color: "white",
            border: "none",
            borderRadius: "6px",
            cursor: "pointer",
            fontWeight: "bold",
          }}
        >
          Analyze Document
        </button>
      </div>
    </div>
  );
}

export default UploadPanel;