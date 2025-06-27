# fetch_binance_data.py

This script fetches historical OHLCV (Open, High, Low, Close, Volume) candlestick data from the Binance API for a specified trading symbol and interval, then saves the data as a CSV file.

---

## Functions

### `fetch_binance_ohlcv(symbol="BTCUSDT", interval="15m", limit=500)`

- Fetches OHLCV candlestick data from Binance.
- **Parameters:**
  - `symbol` (str): Trading pair symbol (default `"BTCUSDT"`).
  - `interval` (str): Candle interval, e.g., `"15m"`, `"1h"`, etc. (default `"15m"`).
  - `limit` (int): Number of candles to fetch (default `500`).
- **Returns:**
  - JSON response from Binance API containing OHLCV data as a list of arrays.

---

### `save_to_csv(klines, filename)`

- Saves fetched candlestick data to a CSV file.
- **Parameters:**
  - `klines` (list): List of candlestick arrays from Binance API.
  - `filename` (str): Output CSV file path.
- The CSV has columns: `Timestamp, Open, High, Low, Close, Volume`.

---

## Main script execution

- Takes optional command-line arguments:
  - `symbol` (default: `"BTCUSDT"`)
  - `interval` (default: `"15m"`)
  - `limit` (default: `1000`)
- Fetches OHLCV data from Binance for the given parameters.
- Saves the data to `data/{symbol}_{interval}.csv`.
- Prints progress and success messages.

---

## Example usage

```bash
python fetch_binance_data.py BTCUSDT 15m 1000
