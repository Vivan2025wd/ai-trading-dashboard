
# `run_backtest.py` – Backtest Execution Script

This script runs trading strategy backtests based on historical OHLCV data. It supports RSI, MACD, and EMA strategies. It reads a configuration file, loads or fetches market data, applies the selected strategy, and outputs results in JSON.

---

## 📦 Imports

```python
import json
import sys
import pandas as pd
import traceback
from utils.fetch import fetch_ohlcv_data
from strategies import rsi, macd, ema
from utils.ohlcv_format import df_to_ohlcv
```

- `json`, `sys`, `traceback`: Core utilities for CLI + error handling.
- `pandas`: For reading and processing OHLCV data.
- `fetch_ohlcv_data`: Fetches market data from Binance or other sources.
- `rsi`, `macd`, `ema`: Strategy implementations.
- `df_to_ohlcv`: Converts DataFrame to a serializable OHLCV format.

---

## 🧠 Strategy Dispatcher

```python
STRATEGY_MAP = {
    "rsi": rsi.backtest_rsi_strategy,
    "macd": macd.backtest_macd_strategy,
    "ema": ema.backtest_ema_strategy,
}
```

- Maps strategy names (strings) to their actual backtest functions.

---

## ⚙️ `run_backtest(config)` Function

```python
def run_backtest(config):
    try:
        symbol = config["symbol"]
        interval = config["interval"]
        strategy = config["strategy"]
        params = config.get("params", {})
```

- Extracts values from `config`.

```python
        csv_path = f"data/{symbol}_{interval}.csv"
        try:
            df = pd.read_csv(csv_path)
        except FileNotFoundError:
            df = fetch_ohlcv_data(symbol, interval)
            df.to_csv(csv_path, index=False)
```

- Tries to load local CSV data.
- If not found, it fetches fresh data and caches it.

```python
        if df.empty:
            raise ValueError("No market data available for backtest")

        if strategy not in STRATEGY_MAP:
            raise ValueError(f"Strategy '{strategy}' not supported")
```

- Validates that data and strategy are usable.

```python
        trades = STRATEGY_MAP[strategy](df, **params)
        ohlcv = df_to_ohlcv(df)
```

- Runs the strategy and formats OHLCV data for the frontend.

```python
        return {
            "trades": trades,
            "ohlcv": ohlcv,
            "message": "✅ Backtest complete"
        }
```

- Returns results in JSON-serializable format.

```python
    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
```

- Catches and returns errors with stack traces.

---

## 🖥 CLI Entry Point

```python
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Missing config file path argument"}))
        sys.exit(1)
```

- Expects the path to a config JSON file as a command-line argument.

```python
    config_path = sys.argv[1]
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except Exception as e:
        print(json.dumps({"error": f"Failed to load config: {str(e)}"}))
        sys.exit(1)
```

- Loads the config file. If it fails, prints an error and exits.

```python
    result = run_backtest(config)
    print(json.dumps(result))
```

- Runs the backtest and prints the result to stdout in JSON format.

---

## 📝 Example Config File (JSON)

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

Save this as something like `rsi_config.json` and run:

```bash
python run_backtest.py rsi_config.json
```

---

## ✅ Output Format (Success)

```json
{
  "trades": [...],
  "ohlcv": [...],
  "message": "✅ Backtest complete"
}
```

---

## ❌ Output Format (Error)

```json
{
  "error": "Strategy 'xyz' not supported",
  "traceback": "Traceback (most recent call last): ..."
}
```

---

