
# `runner.py` 

This script is designed to **run a trading backtest** using one of your predefined strategies (like RSI or MACD). It reads configuration from a JSON file, loads or fetches price data, runs the strategy logic, and prints the result in JSON format.

This guide explains each part of the script in plain English, including where data comes from and how the logic flows.

---

## 📂 Project Structure Expectations

Before using this script, make sure your project is structured like this:

```
your-project/
│
├── backend/
│   └── strategy_registry.py
│
├── backtester/
│   ├── strategies/
│   │   ├── rsi.py
│   │   └── macd.py
│   └── utils/
│       └── fetch.py
│
├── data/              <-- This is where price data CSVs are stored
│
├── runner.py          <-- This script
└── config.json        <-- A sample config file
```

---

## 💡 What This Script Does

1. Loads a JSON config file.
2. Reads historical price data (from a local CSV or the internet).
3. Applies the chosen trading strategy (e.g. RSI).
4. Formats the result and prints it as JSON.

---

## 📥 Step-by-Step Code Walkthrough

### 1. Imports and Setup

```python
import sys, json, os, traceback
import pandas as pd
```

- **Core utilities** for reading configs and handling errors.
- **Pandas** is used to read/write CSVs and process OHLCV data.

### 2. Set Up Import Paths

```python
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
```

- Adds your project root to Python's import path so you can use modules like `backend.strategy_registry`.

---

### 3. Load Functions

```python
from backend.strategy_registry import load_strategy
from backtester.strategies import rsi, macd
from backtester.utils.fetch import fetch_ohlcv_data
```

- Imports:
  - `load_strategy()`: Dynamically loads a strategy from the registry.
  - Fallback strategy functions like `rsi.backtest_rsi_strategy`.
  - `fetch_ohlcv_data()`: Pulls price data from Binance or similar.

---

### 4. Strategy Fallback Map

```python
STRATEGY_MAP = {
    "rsi": rsi.backtest_rsi_strategy,
    "macd": macd.backtest_macd_strategy
}
```

- If dynamic loading fails, this dictionary is used to fall back to known strategy functions.

---

## 🧠 The Main Logic: `run_backtest(config)`

### 5. Read Config

```python
symbol = config["symbol"]
strategy = config["strategy"]
interval = config.get("interval", "15m")
params = config.get("params", {})
```

- Config values: Which symbol, strategy, and parameters to use.
- Example:
```json
{
  "symbol": "BTCUSDT",
  "interval": "15m",
  "strategy": "rsi",
  "params": {
    "rsi_period": 14,
    "overbought": 70,
    "oversold": 30
  }
}
```

---

### 6. Load or Fetch Price Data

```python
csv_path = os.path.join(data_dir, f"{symbol}_{interval}.csv")
```

- This checks if historical price data already exists as a CSV.
- If not:
```python
df = fetch_ohlcv_data(symbol, interval)
df.to_csv(csv_path, index=False)
```

- `fetch_ohlcv_data()` gets OHLCV candlestick data from Binance API.

---

### 7. Clean the Data

```python
df.rename(columns={...}, inplace=True)
```

- Makes sure column names match expected format: `Open`, `High`, `Low`, `Close`, `Volume`, `Timestamp`.

---

### 8. Load the Strategy

```python
strategy_func = load_strategy(strategy)
```

- Tries to dynamically load a strategy using a registry.
- If it fails, uses fallback:
```python
strategy_func = STRATEGY_MAP[strategy]
```

---

### 9. Run the Strategy

```python
trades = strategy_func(df, **params)
```

- Passes OHLCV data and parameters to the strategy function.
- Output: a list of trades like:
```json
[
  {"type": "buy", "time": 1729453200, "price": 29000},
  {"type": "sell", "time": 1729460400, "price": 29350}
]
```

---

### 10. Prepare Data for Frontend

```python
for _, row in df.iterrows():
    ...
```

- Converts each row of the OHLCV DataFrame to a clean JSON format.
- Timestamps are normalized to seconds.

Example output format:
```json
{
  "time": 1729453200,
  "open": 28800,
  "high": 29000,
  "low": 28700,
  "close": 28900,
  "volume": 100.2
}
```

---

## 🏁 Command Line Execution

### 11. CLI Interface

```python
if __name__ == "__main__":
    ...
```

- Reads config from command-line argument:
```bash
python runner.py config.json
```

- Runs the backtest and prints the result as JSON.
- On error, returns a JSON error object with a traceback.

---

## ✅ Success Output Example

```json
{
  "trades": [...],
  "ohlcv": [...],
  "message": "✅ Backtest complete"
}
```

---

## ❌ Error Output Example

```json
{
  "error": "Strategy 'xyz' not supported",
  "traceback": "Traceback (most recent call last): ..."
}
```

---

## 🧪 Testing It Out

1. Create a file named `config.json`:
```json
{
  "symbol": "BTCUSDT",
  "interval": "15m",
  "strategy": "rsi",
  "params": {
    "rsi_period": 14,
    "overbought": 70,
    "oversold": 30
  }
}
```

2. Run:
```bash
python runner.py config.json
```

-