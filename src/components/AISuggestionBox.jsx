import React, { useEffect, useState } from "react"
import SymbolPicker from "./SymbolPicker"

const SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT"]

export default function AISuggestionBox() {
  const [symbol, setSymbol] = useState("BTCUSDT")
  const [suggestion, setSuggestion] = useState("Loading...")
  const [indicators, setIndicators] = useState(null)

  useEffect(() => {
    setSuggestion("Loading...")
    fetch(`http://localhost:5000/api/suggestions?symbol=${symbol}`)
      .then(res => res.json())
      .then(data => {
        setSuggestion(data.suggestion)
        setIndicators(data.latest)
      })
      .catch(() => setSuggestion("Error loading suggestion"))
  }, [symbol])

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
            MACD: {indicators.macd?.MACD.toFixed(2)} | Signal:{" "}
            {indicators.macd?.signal.toFixed(2)}
          </p>
          <p>
            Bollinger Bands: Lower: {indicators.bb?.lower.toFixed(2)}, Middle:{" "}
            {indicators.bb?.middle.toFixed(2)}, Upper: {indicators.bb?.upper.toFixed(2)}
          </p>
          <p className="mt-2 text-xl">{suggestion}</p>
        </>
      ) : (
        <p>Loading indicators...</p>
      )}
    </div>
  )
}

