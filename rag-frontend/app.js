import React, { useState } from "react";
import axios from "axios";

const BACKEND_URL = "http://127.0.0.1:5000";

function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [document, setDocument] = useState("");

  const handleSearch = async () => {
    try {
      const response = await axios.post(`${BACKEND_URL}/rag`, { query });
      setResults(response.data.documents);
      alert(`Resposta gerada: ${response.data.answer}`);
    } catch (error) {
      console.error("Error during RAG:", error);
    }
  };
  

  const handleIndex = async () => {
    try {
      const response = await axios.post(`${BACKEND_URL}/index`, { text: document });
      alert("Document indexed successfully!");
      setDocument("");
    } catch (error) {
      console.error("Error indexing:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>RAG Example</h1>
      <div>
        <h2>Index Document</h2>
        <textarea
          value={document}
          onChange={(e) => setDocument(e.target.value)}
          placeholder="Enter document text here..."
          rows="4"
          cols="50"
        />
        <br />
        <button onClick={handleIndex}>Index Document</button>
      </div>
      <div>
        <h2>Search</h2>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter your query here..."
        />
        <button onClick={handleSearch}>Search</button>
      </div>
      <div>
        <h2>Results</h2>
        <ul>
          {results.map((result) => (
            <li key={result.id}>
              <p>Text: {result.text}</p>
              <p>Score: {result.score}</p>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default App;
