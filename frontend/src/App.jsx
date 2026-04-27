import { useState } from "react";
import axios from "axios";

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
      const res = await axios.get("http://localhost:8000/search", {
        params: { query, filename },
      });
      console.log(res.data);

      setAnswer(res.data.answer);
      setResults(res.data.results);
    } catch (err) {
      console.error(err);
      setAnswer("Error fetching results");
    }

    setLoading(false);
  };
  const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post("http://localhost:8000/upload ", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      alert("File uploaded successfully");
    } catch (err) {
      console.error(err);
      alert("Error uploading file");
    }
  };

  return (
    <div style={{ maxWidth: 800, margin: "50px auto", fontFamily: "Arial" }}>
      <h1>AI Search</h1>

      <div style={{ display: "flex", gap: 10 }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask something..."
          style={{ flex: 1, padding: 10 }}
        />

        <button onClick={search} style={{ padding: "10px 20px" }}>
          Search
        </button>
      </div>

      {loading && <p>Loading...</p>}

      {answer && (
        <div style={{ marginTop: 20 }}>
          <h2>Answer</h2>
          <p>{answer}</p>
        </div>
      )}
      <div>
        <h2>Upload File</h2>
        <input
          type="file"
          onChange={(e) => {
            const file = e.target.files[0];
            if (!file) return;

            setFilename(file.name);
            uploadFile(file);
          }}
        />{" "}
      </div>

      {results && results.length > 0 && (
        <div style={{ marginTop: 20 }}>
          <h2>Sources</h2>

          {results.map((r) => (
            <div
              key={r.id}
              style={{
                border: "1px solid #ddd",
                padding: 10,
                marginBottom: 10,
              }}
            >
              <p>{r.content}</p>
              <small>Similarity: {r.similarity}</small>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
