// src/components/MotherAIdecisionBox.jsx

import React from "react";

export default function MotherAIdecisionBox({ decisionData }) {
  // decisionData = {
  //   symbol: "BTCUSDT",
  //   action: "Buy",
  //   confidence: 0.87,
  //   capitalAllocation: 0.3,
  //   notes: "Strong momentum with low volatility"
  // }

  if (!decisionData) {
    return (
      <div className="p-4 bg-gray-100 rounded shadow text-center text-gray-500">
        No decision data available
      </div>
    );
  }

  const { symbol, action, confidence, capitalAllocation, notes } = decisionData;

  return (
    <div className="p-4 bg-white rounded shadow space-y-2 border border-gray-300">
      <h2 className="text-xl font-semibold">Mother AI Decision</h2>
      <div>
        <strong>Symbol:</strong> {symbol}
      </div>
      <div>
        <strong>Action:</strong>{" "}
        <span
          className={`font-bold ${
            action === "Buy"
              ? "text-green-600"
              : action === "Sell"
              ? "text-red-600"
              : "text-gray-700"
          }`}
        >
          {action}
        </span>
      </div>
      <div>
        <strong>Confidence:</strong> {(confidence * 100).toFixed(1)}%
      </div>
      <div>
        <strong>Capital Allocation:</strong> {(capitalAllocation * 100).toFixed(1)}%
      </div>
      {notes && (
        <div>
          <strong>Notes:</strong> {notes}
        </div>
      )}
    </div>
  );
}
