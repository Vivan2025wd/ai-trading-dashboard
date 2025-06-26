import json
import sys
import pandas as pd
import traceback
from utils.fetch import fetch_ohlcv_data
from strategies import rsi, macd, ema
from utils.ohlcv_format import df_to_ohlcv  # you need this module

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
        csv_path = f"data/{symbol}_{interval}.csv"
        try:
            df = pd.read_csv(csv_path)
        except FileNotFoundError:
            df = fetch_ohlcv_data(symbol, interval)
            df.to_csv(csv_path, index=False)

        if df.empty:
            raise ValueError("No market data available for backtest")

        if strategy not in STRATEGY_MAP:
            raise ValueError(f"Strategy '{strategy}' not supported")

        trades = STRATEGY_MAP[strategy](df, **params)
        ohlcv = df_to_ohlcv(df)

        return {
            "trades": trades,
            "ohlcv": ohlcv,
            "message": "✅ Backtest complete"
        }

    except Exception as e:
        return {
            "error": str(e),
            "traceback": traceback.format_exc()
        }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Missing config file path argument"}))
        sys.exit(1)

    config_path = sys.argv[1]
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except Exception as e:
        print(json.dumps({"error": f"Failed to load config: {str(e)}"}))
        sys.exit(1)

    result = run_backtest(config)
    print(json.dumps(result))
