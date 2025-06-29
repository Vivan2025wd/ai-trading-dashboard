import requests
import pandas as pd
import csv
import sys
import os

def fetch_binance_ohlcv(symbol="BTCUSDT", interval="15m", limit=500) -> pd.DataFrame:
    """
    Fetch OHLCV data from Binance API and return as a cleaned pandas DataFrame.
    """
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Binance returns data as list of lists:
    # [Open time, Open, High, Low, Close, Volume, Close time,
    # Quote asset volume, Number of trades, Taker buy base asset volume,
    # Taker buy quote asset volume, Ignore]

    columns = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ]

    df = pd.DataFrame(data, columns=columns)

    # Convert numeric columns explicitly
    numeric_cols = [
        "open", "high", "low", "close", "volume",
        "quote_asset_volume", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume"
    ]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Convert time columns to datetime objects (milliseconds to datetime)
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')

    # Drop columns not needed for modeling
    df.drop(columns=['ignore'], inplace=True)

    # Drop rows with missing numeric data after conversion
    df.dropna(subset=numeric_cols, inplace=True)

    return df

def save_to_csv(df: pd.DataFrame, filename: str):
    """
    Save OHLCV DataFrame to CSV with selected columns.
    """
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    # Select columns for CSV output
    csv_columns = ['open_time', 'open', 'high', 'low', 'close', 'volume']
    df_to_save = df[csv_columns].copy()

    df_to_save.to_csv(filename, index=False)
    print(f"✅ Saved {len(df_to_save)} rows to {filename}")

if __name__ == "__main__":
    symbol = sys.argv[1] if len(sys.argv) > 1 else "BTCUSDT"
    interval = sys.argv[2] if len(sys.argv) > 2 else "15m"
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 1000

    print(f"⏳ Fetching {limit} candles for {symbol} at {interval} resolution...")
    df = fetch_binance_ohlcv(symbol, interval, limit)

    output_file = f"data/{symbol}_{interval}.csv"
    save_to_csv(df, output_file)
