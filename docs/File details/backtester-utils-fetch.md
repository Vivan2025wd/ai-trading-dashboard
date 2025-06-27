# Data Pipeline: Binance OHLCV Fetching

## Purpose

The `fetch_ohlcv_data` function in `fetch.py` is responsible for retrieving historical OHLCV (Open, High, Low, Close, Volume) data from Binance's REST API. This data is essential for running backtests on trading strategies using historical price movement.

---

## File: `backtester/utils/fetch.py`

### Function: `fetch_ohlcv_data(symbol, interval="15m", limit=500)`

#### Description:

Fetches candlestick data for a specific trading pair (symbol) and interval from Binance.

#### Parameters:

* `symbol` *(str)*: Trading pair symbol (e.g., `BTCUSDT`, `ETHUSDT`).
* `interval` *(str)*: Candlestick interval (e.g., `1m`, `5m`, `15m`, `1h`, `1d`).
* `limit` *(int)*: Number of data points to fetch (default is 500, max is 1000).

#### Returns:

A **Pandas DataFrame** with the following columns:

* `Timestamp`: Epoch time in milliseconds (open time of candle)
* `Open`: Opening price of the candle
* `High`: Highest price of the candle
* `Low`: Lowest price of the candle
* `Close`: Closing price of the candle
* `Volume`: Trading volume during the candle

#### Usage:

```python
from backtester.utils.fetch import fetch_ohlcv_data

df = fetch_ohlcv_data("BTCUSDT", interval="15m")
print(df.head())
```

---

## How It Works

1. **API Call:**
   Sends a `GET` request to Binance's `/api/v3/klines` endpoint with the desired `symbol`, `interval`, and `limit`.

2. **Data Parsing:**
   Binance returns raw data as an array of arrays:

   ```
   [
     [OpenTime, Open, High, Low, Close, Volume, ...],
     [...],
     ...
   ]
   ```

   The function extracts only the relevant fields and converts them into floats for numerical operations.

3. **Return:**
   Creates a DataFrame from the cleaned data and returns it to the caller.

---

## Dependencies

* `requests`: Used for making HTTP API requests.
* `pandas`: Used to structure and manipulate tabular data returned from Binance.

---

## Notes

* This data is typically cached in `/backtester/data/` as CSVs for reuse.
* This module is used directly in `runner.py` when backtests are executed.
* Binance API has rate limits. Ensure you don’t hit those if scaling usage.

---

## Future Enhancements

* Add retry logic on API failure.
* Parameterize the endpoint base URL for testnet/mainnet flexibility.
* Add support for other exchanges or centralized data fetching.
