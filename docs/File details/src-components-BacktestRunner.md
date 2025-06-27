## Overview

`BacktestRunner` is a React component that allows users to run a trading strategy backtest on historical data, view the resulting trades, and visualize the price chart with buy/sell markers. It communicates with a backend API to perform the backtest, then renders detailed results and an interactive chart.

---

## What Does It Do?

- Provides a button to trigger a backtest for a selected trading symbol and strategy
- Calls the backend API to run the backtest and get trade results and price data
- Displays trade statistics and a detailed trade list
- Visualizes the price data along with buy/sell trade markers on a chart with tooltips

---

## Key Parts Explained

### 1. State Variables

```js
const [result, setResult] = useState(null);
const [error, setError] = useState(null);
const [loading, setLoading] = useState(false);
result: Stores backtest results and data received from the backend

error: Stores any error message encountered during API call

loading: Tracks whether the backtest is currently running

2. Running the Backtest
js
Copy code
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

    // Convert timestamps from seconds to milliseconds for charting
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
Defines a runBacktest async function triggered by the button

Sends a POST request to the backend /backtest endpoint with backtest config (symbol, interval, strategy)

Checks response status and handles errors

Converts timestamp format for frontend chart compatibility

Saves the result or error in state variables

3. UI: Button and Status
jsx
Copy code
<button onClick={runBacktest} disabled={loading}>
  {loading ? "Running Backtest..." : "Run Backtest"}
</button>
{error && <p className="text-red-500">Error: {error}</p>}
Button to start backtest, disabled during loading

Shows loading text or error message accordingly

4. Displaying Backtest Results
jsx
Copy code
{result && (
  <>
    <h3>Backtest Results</h3>
    <p>Total Trades: {result.trades.length}</p>
    <p>{result.message}</p>

    <table>
      {/* Trade details with columns: #, Type, Price, Profit, Index */}
    </table>

    {result.ohlcv && result.trades ? (
      <PriceChart ohlcvData={result.ohlcv} trades={result.trades} />
    ) : (
      <p>No chart data available.</p>
    )}
  </>
)}
Shows total number of trades and a summary message

Renders a styled table listing each trade’s details:

Trade number

Type (buy/sell)

Price at trade

Profit from trade

Index (position in the data)

Renders the PriceChart component to visualize price and trades

5. PriceChart Component (Visualization)
Uses Recharts to render a composed chart with:

X-axis: time (formatted)

Y-axis: price scale

Line chart of closing prices

Markers (ReferenceDot) for each trade on the chart:

Green dot for buy trades

Red dot for sell trades

Custom tooltip shows detailed info when hovering over points (price, trade type, profit, time)

Merges trade info into OHLCV data by matching indices to associate trades with price points

6. Static Test Chart
While no backtest has run yet, shows a static example chart with sample data and trades for UI testing

7. Error and Loading Handling
Displays user-friendly messages for errors or while loading

Prevents multiple backtests from running simultaneously by disabling the button

Where Does It Get Data and Logic From?
Calls your backend API at:

nginx
Copy code
POST http://127.0.0.1:8000/backtest
Sends configuration specifying:

symbol (e.g., BTCUSDT)

interval (e.g., 15 minutes)

strategy (e.g., RSI strategy)

Any additional parameters (empty in this example)

Backend runs the trading strategy on historical data and returns:

trades: Array of executed trades with type, price, profit, and index

ohlcv: Array of price candles with open/high/low/close/volume and timestamps

message: Summary or status message about the backtest

The frontend processes this data and visualizes it

Summary
Feature	Description
Backtest trigger button	Allows user to start backtest
API interaction	Sends config, receives backtest results
State management	Tracks loading, error, and backtest results
Results display	Shows total trades, detailed trade table
Chart visualization	Plots price and buy/sell trades with tooltips
Error & loading states	User feedback on process status
Static test chart	Example chart for UI verification before run

Next Steps
Extend backtest config with dynamic parameters and symbol selection

Add more strategies and customize trade table columns

Improve chart with additional indicators or zoom/pan functionality