import sys
import json
import pandas as pd
import os
import traceback

# --- Ensure root is in sys.path for clean imports ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.strategy_registry import load_strategy
from backtester.strategies import rsi, macd
from backtester.utils.fetch import fetch_ohlcv_data

# Map strategy names to functions (fallback if registry fails)
STRATEGY_MAP = {
    "rsi": rsi.backtest_rsi_strategy,
    "macd": macd.backtest_macd_strategy,
    # Add more strategies here
}

def run_backtest(config):
    symbol = config["symbol"]
    strategy = config["strategy"]
    interval = config.get("interval", "15m")
    params = config.get("params", {})

    try:
        # Prepare data directory
        data_dir = os.path.join(PROJECT_ROOT, "data")
        os.makedirs(data_dir, exist_ok=True)

        csv_path = os.path.join(data_dir, f"{symbol}_{interval}.csv")

        # Load or fetch OHLCV data
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        else:
            df = fetch_ohlcv_data(symbol, interval)
            df.to_csv(csv_path, index=False)

        # Normalize column names
        df.rename(columns={
            "timestamp": "Timestamp",
            "open": "Open",
            "high": "High",
            "low": "Low",
            "close": "Close",
            "volume": "Volume"
        }, inplace=True)

        try:
            strategy_func = load_strategy(strategy)
        except Exception:
            # Fallback to STRATEGY_MAP if registry fails or doesn't have it
            if strategy not in STRATEGY_MAP:
                return {"error": f"Strategy '{strategy}' not supported"}
            strategy_func = STRATEGY_MAP[strategy]

        trades = strategy_func(df, **params)

        # Format OHLCV data for frontend
        ohlcv = []
        for _, row in df.iterrows():
            timestamp = int(row["Timestamp"])
            if timestamp > 1e12:  # convert ms → s
                timestamp = timestamp // 1000

            ohlcv.append({
                "time": timestamp,
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
                "volume": float(row["Volume"]),
            })

        return {
            "trades": trades,
            "ohlcv": ohlcv,
            "message": "✅ Backtest complete"
        }

    except Exception as e:
        return {
            "error": "Exception during backtest",
            "details": str(e),
            "traceback": traceback.format_exc()
        }

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            raise ValueError("Missing config file path argument")
        config_path = sys.argv[1]
        with open(config_path, "r") as f:
            config = json.load(f)

        result = run_backtest(config)
        print(json.dumps(result))

    except Exception as e:
        print(json.dumps({
            "error": "Critical runner failure",
            "details": str(e),
            "traceback": traceback.format_exc()
        }))
        sys.exit(1)
