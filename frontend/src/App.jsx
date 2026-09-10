import { useState } from "react";
import HomePage from "./pages/HomePage";
import UploadPage from "./pages/UploadPage";
import AnalysisPage from "./pages/AnalysisPage";

function App() {
  // Controls which page is currently visible
  const [page, setPage] = useState("home");

  // Stores the AI analysis result returned from backend
  const [analysisResult, setAnalysisResult] = useState(null);

  return (
    <div className="min-h-screen bg-gray-950">
      {/* Landing Page */}
      {page === "home" && (
        <HomePage
          onStart={() => setPage("upload")}
        />
      )}

      {/* Upload Document Page */}
      {page === "upload" && (
        <UploadPage
          onResult={(data) => {
            setAnalysisResult(data);
            setPage("analysis");
          }}
          onBack={() => setPage("home")}
        />
      )}

      {/* AI Analysis Results */}
      {page === "analysis" && (
        <AnalysisPage
          result={analysisResult}
          onBack={() => setPage("upload")}
        />
      )}
    </div>
  );
}

export default App;