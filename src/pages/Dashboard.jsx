// src/pages/Dashboard.jsx
import AISuggestionBox from "../components/AISuggestionBox";
import MarketTable from "../components/MarketTable";
import PriceTicker from "../components/PriceTicker";
import TradingViewChart from "../components/TradingViewChart";
import BacktestRunner from "../components/BacktestRunner";

export default function Dashboard() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 p-6">
      <div className="space-y-4">
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

