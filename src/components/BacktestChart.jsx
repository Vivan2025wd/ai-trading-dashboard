import React, { useState } from "react";
import {
  ComposedChart,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Line,
  ReferenceDot,
} from "recharts";

function PriceChart({ ohlcvData, trades }) {
  // Map trades to markers with colors/icons based on type
  const markers = trades.map(trade => ({
    x: trade.index, 
    y: trade.price, 
    type: trade.type,
  }));

  return (
    <ComposedChart
      width={800}
      height={400}
      data={ohlcvData}
      margin={{ top: 20, right: 30, bottom: 20, left: 20 }}
    >
      <XAxis dataKey="time" />
      <YAxis domain={["auto", "auto"]} />
      <Tooltip />
      <CartesianGrid stroke="#f5f5f5" />

      {/* Closing price line */}
      <Line type="monotone" dataKey="close" stroke="#8884d8" dot={false} />

      {/* Buy/Sell markers */}
      {trades?.map((trade, index) => (
        <ReferenceDot
          key={index}
          x={ohlcvData[trade.index]?.time}
          y={trade.price}
          r={6}
          fill={trade.type === "buy" ? "green" : "red"}
          stroke="none"
          label={{ position: "top", value: trade.type.toUpperCase() }}
          isFront={true}
        />
      ))}
    </ComposedChart>
  );
}

function BacktestRunner() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function runBacktest() {
    setLoading(true);
    setError(null);
    setResult(null);

    const config = {
      symbol: "BTCUSDT",
      interval: "15m",
      strategy: "rsi",
      params: {},
    };

    try {
      const response = await fetch("http://127.0.0.1:8000/backtest", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(config),
      });

      if (!response.ok) {
        throw new Error(`Server responded with ${response.status}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || "Failed to fetch");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <button onClick={runBacktest} disabled={loading}>
        {loading ? "Running Backtest..." : "Run Backtest"}
      </button>

      {loading && <p>Loading... please wait.</p>}

      {error && <div style={{ color: "red" }}>Error: {error}</div>}

      {result && (
        <>
          <h3>Backtest Results:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>

          {/* Render chart if OHLCV data and trades exist */}
          {result.ohlcvData && result.trades ? (
            <PriceChart ohlcvData={result.ohlcvData} trades={result.trades} />
          ) : (
            <p>Chart data not available.</p>
          )}
        </>
      )}
    </div>
  );
}

export default BacktestRunner;
