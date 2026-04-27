import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_BASE_URL = import.meta.env.VITE_API_URL;

export default function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filename, setFilename] = useState("");
  const [error, setError] = useState("");
  const [searchAll, setSearchAll] = useState(false);

  const search = async () => {
    // 🔴 Safety check (even if button is disabled)
    if (!searchAll && !filename) {
      setError("Please upload a document first.");
      return;
    }

    if (!query) {
      setError("Please enter a query.");
      return;
    }

    setLoading(true);
    setAnswer("");
    setResults([]);
    setError("");

    try {
      const res = await axios.get(`${API_BASE_URL}/search`, {
        params: { query, filename: searchAll ? "" : filename },
      });

      setAnswer(res.data.answer || "No answer found.");
      setResults(res.data.results || []);
    } catch (err) {
      console.error(err);
      setError("Error fetching results");
    } finally {
      setLoading(false);
    }
  };

  const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post(`${API_BASE_URL}/upload`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("File uploaded successfully");
    } catch (err) {
      console.error(err);
      setError("Error uploading file");
    }
  };

  return (
    <div className="container">
      <h1>AI Search</h1>

      <div className="search-section">
        <input
          className="search-input"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask something..."
        />

        <button
          className="btn-primary"
          onClick={search}
          disabled={!searchAll && !filename}
        >
          Search
        </button>
      </div>

      {/* 🔥 Toggle */}
      <div style={{ marginTop: "10px" }}>
        <label>
          <input
            type="checkbox"
            checked={searchAll}
            onChange={() => setSearchAll(!searchAll)}
          />{" "}
          Search all documents
        </label>
      </div>

      {/* 📄 Current file */}
      {filename && !searchAll && (
        <p style={{ marginTop: "10px", opacity: 0.7 }}>
          Using document: <strong>{filename}</strong>
        </p>
      )}

      {/* ❌ Error */}
      {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}

      {loading && <p>Loading...</p>}

      {/* ✅ Answer */}
      {answer && (
        <div className="answer-section">
          <h2>Answer</h2>
          <p className="answer-text">{answer}</p>
        </div>
      )}

      {/* 📤 Upload */}
      <div className="upload-section">
        <h2>Upload Source Document</h2>
        <input
          type="file"
          className="file-input"
          onChange={(e) => {
            const file = e.target.files[0];
            if (!file) return;
            setFilename(file.name);
            setError("");
            uploadFile(file);
          }}
        />
      </div>

      {/* 📚 Sources */}
      {results.length > 0 && (
        <div className="sources-section">
          <h2>Sources</h2>
          {results.map((r, i) => (
            <div key={i} className="result-card">
              <p>{r.content}</p>
              <small className="similarity-text">
                Similarity: {(r.similarity * 100).toFixed(2)}%
              </small>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
