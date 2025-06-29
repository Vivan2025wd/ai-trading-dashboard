import requests
import pandas as pd

def fetch_binance_ohlcv(symbol="BTCUSDT", interval="15m", limit=500) -> pd.DataFrame:
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    columns = [
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ]

    df = pd.DataFrame(data, columns=columns)

    # Convert time columns to datetime
    df['open_time'] = pd.to_datetime(df['open_time'], unit='ms')
    df['close_time'] = pd.to_datetime(df['close_time'], unit='ms')

    # Convert numeric columns to floats (only these)
    numeric_cols = [
        "open", "high", "low", "close", "volume",
        "quote_asset_volume", "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume"
    ]
    df[numeric_cols] = df[numeric_cols].astype(float)

    # Drop 'ignore' column as it's unused
    df.drop(columns=['ignore'], inplace=True)

    # Optionally drop rows with missing data (if any)
    df.dropna(inplace=True)

    return df
