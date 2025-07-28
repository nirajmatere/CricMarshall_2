import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!query.trim()) return;

    setLoading(true);
    setAnswer("Thinking...");

    try {
      const res = await fetch("http://localhost:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();
      setAnswer(data.answer);
    } catch (err) {
      setAnswer("Error: Could not get answer.");
      console.error(err);
    }

    setLoading(false);
  };

  return (
    <div className="App">
      <h2>Cric-Marshall</h2>
      <div className="input-container">
        
      <textarea
        placeholder="Type your question..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault(); // prevent newline on Enter
            handleSubmit();
          }
        }}
      />
      

        <button onClick={handleSubmit} disabled={loading}>Ask</button>
      </div>
      <div className="answer">
        <h3>Answer:</h3>
        <p>{answer}</p>
      </div>
    </div>
  );
}

export default App;
