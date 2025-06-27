## 📈 `ema.py` – Exponential Moving Average Strategy

### 🔍 Description:

This strategy simulates trades based on **EMA crossovers**, a classic trend-following technique:

* 📈 **Buy** when the **short-term EMA** crosses **above** the long-term EMA.
* 📉 **Sell** when the **short-term EMA** crosses **below** the long-term EMA.

---

### ⚙️ Parameters:

| Name           | Type        | Default | Description                                      |
| -------------- | ----------- | ------- | ------------------------------------------------ |
| `df`           | `DataFrame` | —       | OHLCV price data. Must contain a `Close` column. |
| `short_period` | `int`       | 12      | Period for the short-term EMA (fast)             |
| `long_period`  | `int`       | 26      | Period for the long-term EMA (slow)              |

---

### 📀 Strategy Logic *(to be implemented)*:

1. Compute `EMA_short` and `EMA_long` from `df["Close"]`.
2. If `EMA_short` crosses **above** `EMA_long`, simulate a **Buy**.
3. If `EMA_short` crosses **below** `EMA_long`, simulate a **Sell**.
4. Record each entry/exit trade, including index and profit.

---

### 🔁 Expected Return Format:

```json
[
  {
    "type": "buy",
    "price": 29400.5,
    "index": 150
  },
  {
    "type": "sell",
    "price": 29875.3,
    "index": 175,
    "profit": 474.8
  }
]
```

> 📝 **Note**: Logic not yet implemented. The function currently returns an empty list (`[]`). Add logic before use.

---

### 🔢 Strategy Entry Point

```python
def backtest_ema_strategy(df, short_period=12, long_period=26):
```

For multiple versions:

```python
def backtest_ema_strategy_v1(df, short_period=12, long_period=26): ...
def backtest_ema_strategy_v2(df, short_period=9, long_period=21): ...
```

Then reflect that in your strategy registry like:

```python
"ema_v1": "backtester.strategies.ema",
"ema_v2": "backtester.strategies.ema",
```
