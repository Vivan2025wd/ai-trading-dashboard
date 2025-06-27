// src/pages/Dashboard.jsx
import { useEffect, useState } from "react";
import AISuggestionBox from "../components/AISuggestionBox";
import MarketTable from "../components/MarketTable";
import PriceTicker from "../components/PriceTicker";
import TradingViewChart from "../components/TradingViewChart";
import BacktestRunner from "../components/BacktestRunner";
import SymbolAgentCard from "../components/SymbolAgentCard";

export default function Dashboard() {
  const [motherAiDecision, setMotherAiDecision] = useState(null);
  const [aiError, setAiError] = useState(null);

  useEffect(() => {
    const fetchDecision = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/mother-ai/decision");
        if (!res.ok) throw new Error("Failed to fetch Mother AI decision");
        const data = await res.json();
        setMotherAiDecision(data);
      } catch (err) {
        console.error("Mother AI fetch error:", err);
        setAiError(err.message);
      }
    };

    fetchDecision();
  }, []);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 p-6">
      <div className="space-y-4">
        {/* Mother AI Summary Card */}
        {motherAiDecision && (
          <div className="p-4 border border-gray-700 rounded bg-gray-800 text-white shadow">
            <h3 className="text-xl font-semibold mb-2">Mother AI Trade Decision</h3>
            <p><strong>Symbol:</strong> {motherAiDecision?.symbol ?? "N/A"}</p>
            <p><strong>Action:</strong> {motherAiDecision?.action ?? "N/A"}</p>
            <p>
              <strong>Allocation %:</strong>{" "}
              {typeof motherAiDecision?.allocation === "number"
                ? (motherAiDecision.allocation * 100).toFixed(2) + "%"
                : "N/A"}
            </p>
            <p>
              <strong>Confidence:</strong>{" "}
              {typeof motherAiDecision?.confidence === "number"
                ? (motherAiDecision.confidence * 100).toFixed(2) + "%"
                : "N/A"}
            </p>
          </div>
        )}

        {/* Optional error display */}
        {aiError && (
          <div className="p-4 border border-red-600 bg-red-900 text-red-200 rounded">
            Error fetching Mother AI decision: {aiError}
          </div>
        )}

        {/* Agent predictions for symbols */}
        <SymbolAgentCard symbol="BTCUSDT" />
        <SymbolAgentCard symbol="ETHUSDT" />

        <PriceTicker />
        <AISuggestionBox />
        <BacktestRunner />
      </div>

      <div className="space-y-4">
        <TradingViewChart />
        <MarketTable />
      </div>
    </div>
  );
}
