import React, { useEffect, useState } from "react";

function SymbolAgentCard({ symbol }) {
  const [predictionData, setPredictionData] = useState({
    prediction: null,
    confidence: null,
    timestamp: null,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!symbol) return;

    setLoading(true);
    setError(null);

    fetch(`http://localhost:8000/agent/${symbol}/predict`)
      .then((res) => {
        if (!res.ok) {
          throw new Error(`API error: ${res.statusText}`);
        }
        return res.json();
      })
      .then((data) => {
        setPredictionData({
          prediction: data.prediction,
          confidence: data.confidence,
          timestamp: data.timestamp,
        });
      })
      .catch((err) => {
        console.error("Fetch error:", err);
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [symbol]);

  if (loading)
    return (
      <div className="p-4 rounded shadow bg-gray-900 text-white text-center">
        Loading prediction...
      </div>
    );

  if (error)
    return (
      <div className="p-4 rounded shadow bg-red-700 text-white text-center">
        Error loading prediction: {error}
      </div>
    );

  return (
    <div className="p-6 rounded-lg shadow-lg bg-gray-900 text-white hover:bg-gray-800 transition-colors duration-300">
      <h3 className="text-2xl font-bold mb-3">{symbol}</h3>
      <p className="mb-1">
        <strong>Prediction:</strong> {predictionData.prediction}
      </p>
      <p className="mb-1">
        <strong>Confidence:</strong>{" "}
        {(predictionData.confidence * 100).toFixed(2)}%
      </p>
      <p className="text-sm text-gray-400">
        <strong>Last updated:</strong>{" "}
        {new Date(predictionData.timestamp).toLocaleString()}
      </p>
    </div>
  );
}

export default SymbolAgentCard;
