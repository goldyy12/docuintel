import { useState } from "react";
import axios from "axios";
import "./App.css"; // Importing the new CSS file

// Fallback to localhost if env is not defined
const API_BASE_URL = import.meta.env.VITE_API_URL;

export default function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [filename, setFilename] = useState("");

  const search = async () => {
    if (!query) return;

    setLoading(true);
    setAnswer("");
    setResults([]);

    try {
      const res = await axios.get(`${API_BASE_URL}/search`, {
        params: { query, filename },
      });

      setAnswer(res.data.answer);
      setResults(res.data.results);
    } catch (err) {
      console.error(err);
      setAnswer("Error fetching results");
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
      alert("Error uploading file");
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
        <button className="btn-primary" onClick={search} disabled={!filename}>
          Search
        </button>
      </div>

      {loading && <p>Loading...</p>}

      {answer && (
        <div className="answer-section">
          <h2>Answer</h2>
          <p className="answer-text">{answer}</p>
        </div>
      )}

      <div className="upload-section">
        <h2>Upload Source Document</h2>
        <input
          type="file"
          className="file-input"
          onChange={(e) => {
            const file = e.target.files[0];
            if (!file) return;
            setFilename(file.name);
            uploadFile(file);
          }}
        />
      </div>

      {results && results.length > 0 && (
        <div className="sources-section">
          <h2>Sources</h2>
          {results.map((r) => (
            <div key={r.id} className="result-card">
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
