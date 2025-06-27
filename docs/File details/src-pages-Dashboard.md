
## 🧠 What Is This?

The `Dashboard.jsx` file defines the **main page** of your AI-powered trading platform. It assembles several functional components into a clean, responsive layout that provides:

- 📈 Live price tracking
- 🧠 AI-based trade suggestions
- 💹 Backtest result visualization
- 📊 Interactive TradingView chart
- 🔥 Top USDT pair market data

---

## 🗂 Components Used

| Component           | Purpose                                                                 |
|---------------------|-------------------------------------------------------------------------|
| `PriceTicker`       | Displays **live BTC/USDT price** from Binance WebSocket                 |
| `AISuggestionBox`   | Shows AI-generated trading signal based on technical indicators         |
| `BacktestRunner`    | Runs and visualizes trading strategy backtests with charts and tables   |
| `TradingViewChart`  | Embeds a **TradingView** candlestick chart widget                       |
| `MarketTable`       | Lists the top 10 high-volume **USDT trading pairs** from Binance        |

---

## 🧩 Page Layout

The layout uses **TailwindCSS grid** to structure the dashboard:

```jsx
<div className="grid grid-cols-1 lg:grid-cols-2 gap-6 p-6">
On mobile: 1 column layout

On large screens (lg): 2-column layout

Adds padding (p-6) and spacing between elements (gap-6)

🧠 Code Summary
jsx
Copy code
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
📦 Where Does the Data Come From?
Component	Data Source
PriceTicker	Binance WebSocket: wss://stream.binance.com/...@trade
AISuggestionBox	Your Express API (port 5000): Calculates RSI, MACD, EMA, BB
BacktestRunner	FastAPI backend (port 8000): Runs Python strategy backtests
TradingViewChart	TradingView Widget: Live data from Binance
MarketTable	Binance REST API: /api/v3/ticker/24hr

🔍 Component Breakdown
🔹 PriceTicker
Connects to Binance WebSocket for real-time BTC price

Updates price dynamically using React state

Styled with Tailwind for a modern look

🔹 AISuggestionBox
Sends HTTP request to http://localhost:5000/api/suggestions

Receives:

RSI, MACD, EMA, Bollinger Bands

Trade suggestion (Buy/Sell/Hold)

Displays them clearly in a dark-styled box

🔹 BacktestRunner
Sends POST request to your FastAPI /backtest endpoint

Runs selected strategy on Binance OHLCV data

Returns:

Trades with index, price, profit

OHLCV time series

Visualized using:

A table for trades

A Recharts line chart with buy/sell markers

🔹 TradingViewChart
Injects a 3rd-party TradingView chart

Configured for symbol BINANCE:BTCUSDT

1-minute candlesticks, dark theme

No coding needed for live charting—fully managed by TradingView

🔹 MarketTable
Fetches 24h stats for all pairs from Binance

Filters to show only USDT pairs (excluding leveraged tokens)

Sorts by quoteVolume

Displays price, % change, volume

✨ Styling
Uses TailwindCSS for utility-first styling

Consistent dark theme across all components

Responsive layout that adjusts for mobile and desktop

🛠 How to Extend
Goal	Suggestion
Make symbol selectable globally	Lift symbol state to Dashboard.jsx and pass as prop
Add account info or portfolio stats	Create a PortfolioSummary component
Show alerts or news	Add a NewsFeed or AlertsPanel
Save backtest results to DB	Modify BacktestRunner to POST to MongoDB