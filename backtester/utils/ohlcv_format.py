import pandas as pd

def df_to_ohlcv(df):
    time_col = 'Timestamp'

    ohlcv = []
    for _, row in df.iterrows():
        # Convert Timestamp to epoch seconds
        if isinstance(row[time_col], str):
            dt = pd.to_datetime(row[time_col])
            epoch_time = int(dt.timestamp())
        elif pd.api.types.is_datetime64_any_dtype(type(row[time_col])):
            epoch_time = int(row[time_col].timestamp())
        else:
            # fallback if already numeric timestamp (assumed in seconds)
            epoch_time = int(row[time_col])

        candle = {
            "time": epoch_time,
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": float(row["Volume"]),
        }
        ohlcv.append(candle)

    return ohlcv
