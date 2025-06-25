import json
import sys
import pandas as pd
from utils.fetch import fetch_ohlcv_data
from strategies import rsi, macd, ema


STRATEGY_MAP = {
    "rsi": rsi.backtest_rsi_strategy,
    "macd": macd.backtest_macd_strategy,
    "ema": ema.backtest_ema_strategy,
}
def run_backtest(config):
    try:
        symbol = config["symbol"]
        interval = config["interval"]
        strategy = config["strategy"]
        params = config.get("params", {})

        # Load CSV or fetch new data
        try:
            df = pd.read_csv(f"data/{symbol}_{interval}.csv")
        except FileNotFoundError:
            df = fetch_ohlcv_data(symbol, interval)
            df.to_csv(f"data/{symbol}_{interval}.csv", index=False)

        # Validate dataframe
        if df.empty:
            raise ValueError("No market data available for backtest")

        # Execute strategy
        if strategy in STRATEGY_MAP:
            trades = STRATEGY_MAP[strategy](df, **params)
            print(json.dumps({"trades": trades, "message": "✅ Backtest complete"}))
        else:
            raise ValueError(f"Strategy '{strategy}' not supported")

    except Exception as e:
        print(json.dumps({"error": str(e)}))
