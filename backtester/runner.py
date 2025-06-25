# backtester/runner.py
import sys
import json
import pandas as pd
from strategies import rsi, macd
from utils.fetch import fetch_ohlcv_data

STRATEGY_MAP = {
    "rsi": rsi.backtest_rsi_strategy,
    "macd": macd.backtest_macd_strategy,
    # more strategies here...
}

def run_backtest(config):
    symbol = config["symbol"]
    interval = config.get("interval", "15m")
    strategy = config["strategy"]
    params = config.get("params", {})

    try:
        df = pd.read_csv(f"data/{symbol}_{interval}.csv")
    except FileNotFoundError:
        df = fetch_ohlcv_data(symbol, interval)
        df.to_csv(f"data/{symbol}_{interval}.csv", index=False)

    if strategy not in STRATEGY_MAP:
        print(json.dumps({"error": f"Strategy '{strategy}' not supported"}))
        sys.exit(1)

    trades = STRATEGY_MAP[strategy](df, **params)
    print(json.dumps({"trades": trades, "message": "✅ Backtest complete"}))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Config file path required"}))
        sys.exit(1)
    config_path = sys.argv[1]
    with open(config_path, "r") as f:
        config = json.load(f)
    run_backtest(config)
