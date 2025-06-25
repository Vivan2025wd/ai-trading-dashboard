import json
import sys
import os
import pandas as pd
from strategies import rsi, macd, ema
from utils.fetch import fetch_ohlcv_data

STRATEGY_MAP = {
    "rsi": rsi.backtest_rsi_strategy,
    "macd": macd.backtest_macd_strategy,
    "ema": ema.backtest_ema_strategy,
}

def run_backtest(config):
    symbol = config["symbol"]
    interval = config.get("interval", "15m")
    strategy = config["strategy"]
    params = config.get("params", {})

    # Prepare data folder and CSV path
    os.makedirs("data", exist_ok=True)
    csv_path = f"data/{symbol}_{interval}.csv"

    # Load cached data or fetch new from Binance
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"⚡ Fetching new OHLCV data for {symbol} {interval} ...")
        df = fetch_ohlcv_data(symbol, interval)
        df.to_csv(csv_path, index=False)

    if strategy not in STRATEGY_MAP:
        output = {"error": f"Strategy '{strategy}' not supported"}
        print(json.dumps(output))
        return

    trades = STRATEGY_MAP[strategy](df, **params)

    # Convert numpy types to native Python types for JSON serialization
    def convert_trade(trade):
        return {k: (float(v) if hasattr(v, 'item') else v) for k, v in trade.items()}

    trades = [convert_trade(t) for t in trades]

    output = {"trades": trades, "message": "✅ Backtest complete"}
    print(json.dumps(output))

if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else "temp_config.json"
    with open(config_path) as f:
        config = json.load(f)
    run_backtest(config)
