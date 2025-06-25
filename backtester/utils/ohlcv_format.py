def df_to_ohlcv(df):
    return [
        [
  { "time": 1687603200, "open": 105000, "high": 105500, "low": 104500, "close": 105100, "volume": 1000 },
  ...
]
        for _, row in df.iterrows()
    ]
