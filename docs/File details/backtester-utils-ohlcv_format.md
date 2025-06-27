# 📄 `ohlcv_format.md` — Format Pandas DataFrame to OHLCV JSON

This utility module provides a helper function to **convert a pandas DataFrame of candlestick (OHLCV) data** into a list of dictionaries compatible with frontend charting libraries (like Recharts or TradingView widgets).

---

## 🔧 Function: `df_to_ohlcv(df)`

**Purpose:**  
Convert a DataFrame with standard OHLCV columns and a time column into a list of JSON-style objects for frontend consumption.

---

## ✅ Expected Input:

A DataFrame (`df`) with these columns:

| Column     | Type            | Description                                      |
|------------|-----------------|--------------------------------------------------|
| Timestamp  | int/str/datetime| Unix timestamp in ms/s, ISO string, or datetime |
| Open       | float           | Opening price of the candle                      |
| High       | float           | Highest price during the candle                  |
| Low        | float           | Lowest price during the candle                   |
| Close      | float           | Closing price of the candle                      |
| Volume     | float           | Trade volume during the candle                   |

---

## 🔄 Logic Flow:

1. **Loop over each row** in the DataFrame.
2. **Convert `Timestamp`** to a clean epoch time in **seconds**:
   - If it's a string → parsed with `pd.to_datetime()` and converted.
   - If it's already a `datetime` object → converted directly.
   - If it's numeric (e.g., already epoch) → used as-is.
3. **Map the OHLCV fields** to a dictionary format with keys:
   - `"time"`, `"open"`, `"high"`, `"low"`, `"close"`, `"volume"`
4. Return a list of all formatted candle dictionaries.

---

## 📤 Output Format:

```json
[
  {
    "time": 1719426000,
    "open": 29250.0,
    "high": 29300.0,
    "low": 29100.0,
    "close": 29280.5,
    "volume": 123.45
  },
  ...
]
```

---

## 🧠 Why This Matters:

- Ensures **clean and consistent formatting** for candlestick charts.
- Normalizes time formats regardless of source (Binance, CSVs, etc.).
- Compatible with charting tools in your React frontend (`Recharts`, `TVChart`, etc.).

---

## 📌 Notes:

- Always assumes timestamps should be in **epoch seconds**.
- Expects `df` to be pre-validated or cleaned before conversion.
- This module is typically used right before sending data to the frontend from a backtest result or live fetch.