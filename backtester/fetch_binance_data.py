import requests
import csv
import sys

def fetch_binance_ohlcv(symbol="BTCUSDT", interval="15m", limit=500):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def save_to_csv(klines, filename):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "Open", "High", "Low", "Close", "Volume"])
        for k in klines:
            writer.writerow([k[0], k[1], k[2], k[3], k[4], k[5]])

if __name__ == "__main__":
    symbol = sys.argv[1] if len(sys.argv) > 1 else "BTCUSDT"
    interval = sys.argv[2] if len(sys.argv) > 2 else "15m"
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 1000

    print(f"⏳ Fetching {limit} candles for {symbol} at {interval} resolution...")
    klines = fetch_binance_ohlcv(symbol, interval, limit)

    output_file = f"data/{symbol}_{interval}.csv"
    save_to_csv(klines, output_file)
    print(f"✅ Saved {len(klines)} rows to {output_file}")
