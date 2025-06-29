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

    let isMounted = true; // cleanup flag

    setLoading(true);
    setError(null);

    fetch(`http://localhost:8000/agent/${symbol}/predict`)
      .then(async (res) => {
        if (!res.ok) {
          // Try to parse error message from JSON response
          let errorMessage = `API error: ${res.status} ${res.statusText}`;
          try {
            const errData = await res.json();
            if (errData.detail) errorMessage += ` - ${errData.detail}`;
            else if (errData.message) errorMessage += ` - ${errData.message}`;
          } catch {
            // ignore JSON parse errors
          }
          throw new Error(errorMessage);
        }
        return res.json();
      })
      .then((data) => {
        if (isMounted) {
          setPredictionData({
            prediction: data.prediction,
            confidence: data.confidence,
            timestamp: data.timestamp,
          });
        }
      })
      .catch((err) => {
        if (isMounted) {
          console.error("Fetch error:", err);
          setError(err.message);
        }
      })
      .finally(() => {
        if (isMounted) setLoading(false);
      });

    return () => {
      isMounted = false;
    };
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
        {typeof predictionData.confidence === "number"
          ? (predictionData.confidence * 100).toFixed(2) + "%"
          : "N/A"}
      </p>
      <p className="text-sm text-gray-400">
        <strong>Last updated:</strong>{" "}
        {predictionData.timestamp
          ? new Date(predictionData.timestamp).toLocaleString()
          : "N/A"}
      </p>
    </div>
  );
}

export default SymbolAgentCard;
