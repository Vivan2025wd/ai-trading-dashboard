import PriceTicker from "../components/PriceTicker"
import MarketTable from "../components/MarketTable"
import AISuggestionBox from "../components/AISuggestionBox"
import TradingViewChart from "../components/TradingViewChart"

export default function Dashboard() {
  return (
    <div className="p-6 space-y-6">
      <h2 className="text-2xl font-semibold">Market Intelligence Dashboard</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <PriceTicker />
        <AISuggestionBox />
      </div>

      <TradingViewChart />

      <MarketTable />
    </div>
  )
}
