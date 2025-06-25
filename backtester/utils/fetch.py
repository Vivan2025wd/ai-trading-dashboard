import requests
import pandas as pd
import time

def fetch_ohlcv_data(symbol, interval="15m", limit=500):
    """
    Fetch OHLCV data from Binance REST API.
    Returns a DataFrame with columns: Timestamp, Open, High, Low, Close, Volume
    """
    base_url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "limit": limit
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    # Binance returns array of arrays:
    # [Open time, Open, High, Low, Close, Volume, ... other fields]
    # We extract relevant fields and convert types
    ohlcv = []
    for d in data:
        ohlcv.append({
            "Timestamp": d[0],
            "Open": float(d[1]),
            "High": float(d[2]),
            "Low": float(d[3]),
            "Close": float(d[4]),
            "Volume": float(d[5]),
        })

    df = pd.DataFrame(ohlcv)
    return df


