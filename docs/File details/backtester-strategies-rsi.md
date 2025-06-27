# RSI Strategies (rsi.py)

This document outlines the logic behind the RSI (Relative Strength Index) trading strategies implemented in `backtester/strategies/rsi.py`.

---

## 📈 RSI Calculation

All strategies in this module use a shared `compute_rsi` function to calculate the RSI values:

```python
compute_rsi(prices, period=14)
```

**Steps:**

1. Calculate price changes (`delta`).
2. Separate gains and losses.
3. Compute average gain and loss over a `rolling(window=period)`.
4. Compute relative strength (RS) = avg\_gain / avg\_loss.
5. Calculate RSI = 100 - (100 / (1 + RS)).

This gives a standard RSI time series.

---

## ✅ `backtest_rsi_strategy(df, rsi_buy=30, rsi_sell=70)`

This is the default/backward-compatible version.

### Entry Conditions:

* **Buy** when RSI drops below 30 (oversold).
* **Sell** when RSI goes above 70 (overbought).

### Behavior:

* Uses an index loop to simulate trades.
* Tracks position and profit inline.
* Records both buy and sell trades as dictionaries.

### Example Output Format:

```json
{
  "type": "sell",
  "price": 24250.45,
  "index": 123,
  "profit": 120.55
}
```

---

## 🔁 `backtest_rsi_v1_strategy(df, rsi_buy=30, rsi_sell=70)`

An alternate version with slightly different structure.

### Differences:

* Still uses same RSI calc.
* Ensures all `price` and `profit` values are explicitly cast to `float` (may help frontend formatting).
* Still uses index-based loop with same logic.

### Output Format:

Same as above but enforces float format consistency in results.

---

## Usage

Both functions are accessible via dynamic routing with the `load_strategy()` method:

```python
load_strategy("rsi")      # maps to backtest_rsi_strategy
load_strategy("rsi_v1")   # maps to backtest_rsi_v1_strategy
```

You can call either by passing the correct strategy name in the config JSON when triggering a backtest.

---

## Summary

| Strategy Name | Function Name              | Float Outputs | Profit Tracking | Recommended Use   |
| ------------- | -------------------------- | ------------- | --------------- | ----------------- |
| `rsi`         | `backtest_rsi_strategy`    | No            | Yes             | Default           |
| `rsi_v1`      | `backtest_rsi_v1_strategy` | Yes           | Yes             | Consistent output |

Both strategies implement the same core logic, differing only in formatting precision and explicit type casting.
