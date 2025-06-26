import React, { useState } from "react";
import {
  ComposedChart,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Line,
  ReferenceDot,
  ResponsiveContainer,
} from "recharts";
import { format } from "date-fns";

// Custom tooltip for showing trade details on hover
function CustomTooltip({ active, payload, label }) {
  if (!active || !payload || payload.length === 0) return null;

  const data = payload[0].payload;

  return (
    <div className="bg-gray-900 text-gray-200 border border-gray-700 p-2 rounded">
      <p><strong>Time:</strong> {format(new Date(label), "PPpp")}</p>
      <p><strong>Close Price:</strong> {data.close}</p>
      {data.trade && (
        <>
          <p><strong>Trade Type:</strong> {data.trade.type.toUpperCase()}</p>
          {data.trade.profit !== undefined && (
            <p><strong>Profit:</strong> {data.trade.profit.toFixed(2)}</p>
          )}
          <p><strong>Trade Price:</strong> {data.trade.price}</p>
        </>
      )}
    </div>
  );
}

// PriceChart component to visualize live backtest data with enhanced tooltip
function PriceChart({ ohlcvData, trades }) {
  if (!ohlcvData || !trades) return <p>No chart data available.</p>;

  // Merge trades info into ohlcv points by matching index, for tooltip access
  const dataWithTrades = ohlcvData.map((candle, i) => {
    const trade = trades.find((t) => t.index === i);
    return { ...candle, trade };
  });

  return (
    <ResponsiveContainer width="100%" height={400}>
      <ComposedChart data={dataWithTrades} margin={{ top: 20, right: 30, bottom: 40, left: 20 }}>
        <XAxis
          dataKey="time"
          tickFormatter={(time) => format(new Date(time), "MM-dd HH:mm")}
          angle={-30}
          textAnchor="end"
          tick={{ fontSize: 12, fill: "#ddd" }}
          stroke="#444"
        />
        <YAxis domain={["auto", "auto"]} tick={{ fontSize: 12, fill: "#ddd" }} stroke="#444" />
        <Tooltip content={<CustomTooltip />} />
        <CartesianGrid stroke="#444" />
        <Line type="monotone" dataKey="close" stroke="#6366f1" dot={false} strokeWidth={2} />

        {trades.map((trade, index) => {
          const point = ohlcvData[trade.index];
          if (!point) return null;

          return (
            <ReferenceDot
              key={index}
              x={point.time}
              y={trade.price}
              r={6}
              fill={trade.type === "buy" ? "#22c55e" : "#ef4444"}
              stroke="#fff"
              label={{
                value: trade.type.toUpperCase(),
                position: "top",
                fontSize: 10,
                fill: trade.type === "buy" ? "#22c55e" : "#ef4444",
              }}
              isFront
            />
          );
        })}
      </ComposedChart>
    </ResponsiveContainer>
  );
}

// Static test chart with sample data to verify chart UI works
const testOhlcv = [
  { time: 1680000000000, open: 100, high: 105, low: 99, close: 102, volume: 10 },
  { time: 1680000900000, open: 102, high: 106, low: 101, close: 104, volume: 12 },
  { time: 1680001800000, open: 104, high: 108, low: 103, close: 107, volume: 15 },
];
const testTrades = [
  { index: 1, price: 104, type: "buy", profit: 10 },
  { index: 2, price: 107, type: "sell", profit: -5 },
];
function TestPriceChart() {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <ComposedChart data={testOhlcv} margin={{ top: 20, right: 30, bottom: 40, left: 20 }}>
        <XAxis
          dataKey="time"
          tickFormatter={(t) => format(new Date(t), "MM-dd HH:mm")}
          angle={-30}
          textAnchor="end"
          tick={{ fontSize: 12, fill: "#ddd" }}
          stroke="#444"
        />
        <YAxis domain={["auto", "auto"]} tick={{ fontSize: 12, fill: "#ddd" }} stroke="#444" />
        <Tooltip
          labelFormatter={(label) => format(new Date(label), "PPpp")}
          formatter={(value, name) => [value, name.toUpperCase()]}
          contentStyle={{ backgroundColor: "#1f2937", borderColor: "#374151", color: "#ddd" }}
          labelStyle={{ color: "#ddd" }}
        />
        <CartesianGrid stroke="#444" strokeDasharray="3 3" />
        <Line type="monotone" dataKey="close" stroke="#6366f1" dot={false} strokeWidth={2} />
        {testTrades.map((trade, i) => (
          <ReferenceDot
            key={i}
            x={testOhlcv[trade.index]?.time}
            y={trade.price}
            r={6}
            fill={trade.type === "buy" ? "#22c55e" : "#ef4444"}
            stroke="#fff"
            label={{
              value: trade.type.toUpperCase(),
              position: "top",
              fontSize: 10,
              fill: trade.type === "buy" ? "#22c55e" : "#ef4444",
            }}
            isFront
          />
        ))}
      </ComposedChart>
    </ResponsiveContainer>
  );
}

// Main BacktestRunner component
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

      if (!response.ok) throw new Error(`Server responded with ${response.status}`);

      const data = await response.json();

      if (data.error) throw new Error(data.error);

      // Convert timestamps to ms for Recharts
      const ohlcvWithMs = (data.ohlcv || []).map((candle) => ({
        ...candle,
        time: candle.time * 1000,
      }));

      setResult({ ...data, ohlcv: ohlcvWithMs });
    } catch (err) {
      setError(err.message || "Failed to fetch");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-3xl mx-auto p-5 bg-gray-900 rounded-md text-gray-200">
      <button
        onClick={runBacktest}
        disabled={loading}
        className={`px-5 py-2 mb-5 text-lg rounded border transition-colors 
          ${loading ? "cursor-not-allowed bg-gray-700 text-gray-400 border-gray-600" : "cursor-pointer bg-gray-800 hover:bg-gray-700 border-gray-600 text-gray-200"}`}
      >
        {loading ? "Running Backtest..." : "Run Backtest"}
      </button>

      {error && <p className="text-red-500 mb-4">Error: {error}</p>}

      {result ? (
        <>
          <h3 className="text-xl font-semibold mb-2">Backtest Results</h3>
          <p>Total Trades: {result.trades.length}</p>
          <p className="mb-4">{result.message}</p>

          {/* Trade Details Table with Tailwind Dark Styling */}
          <div className="overflow-x-auto mb-10">
            <table className="min-w-full border-collapse border border-gray-700 rounded-md">
              <thead className="bg-gray-800">
                <tr>
                  {["#", "Type", "Price", "Profit", "Index"].map((header) => (
                    <th
                      key={header}
                      className="border border-gray-700 px-4 py-2 text-center text-gray-300"
                    >
                      {header}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {result.trades.map((trade, i) => (
                  <tr
                    key={i}
                    className={i % 2 === 0 ? "bg-gray-800" : "bg-gray-700"}
                  >
                    <td className="border border-gray-700 px-4 py-2 text-center">{i + 1}</td>
                    <td
                      className={`border border-gray-700 px-4 py-2 text-center font-bold capitalize ${
                        trade.type === "buy" ? "text-green-400" : "text-red-400"
                      }`}
                    >
                      {trade.type}
                    </td>
                    <td className="border border-gray-700 px-4 py-2 text-center">
                      {trade.price.toFixed(2)}
                    </td>
                    <td className="border border-gray-700 px-4 py-2 text-center">
                      {trade.profit !== undefined ? trade.profit.toFixed(2) : "—"}
                    </td>
                    <td className="border border-gray-700 px-4 py-2 text-center">
                      {trade.index}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {result.ohlcv && result.trades ? (
            <PriceChart ohlcvData={result.ohlcv} trades={result.trades} />
          ) : (
            <p>No chart data available.</p>
          )}
        </>
      ) : (
        <>
          <h3 className="text-xl font-semibold mb-2">Static Test Chart</h3>
          <TestPriceChart />
        </>
      )}
    </div>
  );
}

export default BacktestRunner;
