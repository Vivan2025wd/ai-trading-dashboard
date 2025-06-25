// src/components/BacktestRunner.jsx
import React, { useState } from 'react';

function BacktestRunner() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  async function runBacktest() {
    const config = {
      symbol: "BTCUSDT",
      interval: "15m",
      strategy: "rsi",
      params: {}
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/backtest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(config),
      });

      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
      setError(null);
    } catch (err) {
      setError(err.message || "Failed to fetch");
      setResult(null);
    }
  }

  return (
    <div>
      <button onClick={runBacktest}>Run Backtest</button>
      {error && <div style={{color: 'red'}}>Error: {error}</div>}
      {result && (
        <div>
          <h3>Backtest Results:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}
const runBacktest = async () => {
  const response = await fetch("http://localhost:8000/backtest", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      symbol: "BTCUSDT",
      interval: "15m",
      strategy: "rsi", // or "macd"
      params: {} // Optional strategy parameters
    })
  });

  const data = await response.json();
  if (data.trades) {
    setTrades(data.trades);
    setMessage(data.message);
  } else {
    setError(data.error || "Unknown error");
  }
};


export default BacktestRunner;
