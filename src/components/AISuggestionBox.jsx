import React, { useEffect, useState } from "react";
import SymbolPicker from "./SymbolPicker";

const SYMBOLS = ["BTCUSDT", "ETHUSDT"];

export default function AISuggestionBox() {
  const [symbol, setSymbol] = useState("BTCUSDT");
  const [suggestion, setSuggestion] = useState("Loading...");
  const [indicators, setIndicators] = useState(null);

  useEffect(() => {
    const controller = new AbortController();

    setSuggestion("Loading...");
    setIndicators(null);

    fetch(`http://localhost:8000/backtester/strategies?symbol=${symbol}`, {
      signal: controller.signal,
      // You generally don't need to set Origin or Accept explicitly for local fetch
      headers: {
        "Accept": "application/json",
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error(`HTTP error! Status: ${res.status}`);
        return res.json();
      })
      .then((data) => {
        // Adjust this part based on your backend's exact response structure
        // Assuming data looks like { suggestion: "...", latest: { close, rsi, ema, macd, bb } }
        setSuggestion(data.suggestion || "No suggestion available");
        setIndicators(data.latest || null);
      })
      .catch((err) => {
        if (err.name !== "AbortError") {
          console.error("Fetch error:", err);
          setSuggestion("Error loading suggestion");
        }
      });

    return () => controller.abort();
  }, [symbol]);

  return (
    <div className="bg-gray-800 p-4 rounded-xl shadow text-center max-w-md mx-auto">
      <h2 className="text-lg font-semibold mb-2">🧠 AI Trade Suggestion</h2>

      <SymbolPicker symbols={SYMBOLS} selected={symbol} onChange={setSymbol} />

      {indicators ? (
        <>
          <p>Close: {indicators.close}</p>
          <p>RSI: {indicators.rsi}</p>
          <p>EMA: {indicators.ema}</p>
          <p>
            MACD: {indicators.macd?.MACD?.toFixed(2)} | Signal:{" "}
            {indicators.macd?.signal?.toFixed(2)}
          </p>
          <p>
            Bollinger Bands: Lower: {indicators.bb?.lower?.toFixed(2)}, Middle:{" "}
            {indicators.bb?.middle?.toFixed(2)}, Upper: {indicators.bb?.upper?.toFixed(2)}
          </p>
          <p className="mt-2 text-xl">{suggestion}</p>
        </>
      ) : (
        <p>Loading indicators...</p>
      )}
    </div>
  );
}
