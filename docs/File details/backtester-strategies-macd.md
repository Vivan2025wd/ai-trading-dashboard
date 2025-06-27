# MACD Strategy Documentation

## Overview

This document explains how the **MACD-based trading strategy** implemented in `macd.py` works. The strategy uses the Moving Average Convergence Divergence (MACD) indicator to determine entry and exit points for trades.

---

## 1. Indicator: MACD

**MACD (Moving Average Convergence Divergence)** is calculated using two exponential moving averages (EMAs):

* **Fast EMA**: 12-period EMA
* **Slow EMA**: 26-period EMA
* **MACD Line**: Difference between Fast EMA and Slow EMA
* **Signal Line**: 9-period EMA of the MACD Line

```python
exp1 = df['Close'].ewm(span=fast, adjust=False).mean()
exp2 = df['Close'].ewm(span=slow, adjust=False).mean()
macd = exp1 - exp2
signal_line = macd.ewm(span=signal, adjust=False).mean()
```

---

## 2. Strategy Logic

The strategy works by detecting **MACD crossovers**:

### Buy Signal:

Occurs when:

```
MACD crosses above the Signal Line (bullish crossover)
```

Translated to code:

```python
macd[i] > signal[i] and macd[i-1] <= signal[i-1]
```

### Sell Signal:

Occurs when:

```
MACD crosses below the Signal Line (bearish crossover)
```

Translated to code:

```python
macd[i] < signal[i] and macd[i-1] >= signal[i-1]
```

---

## 3. Trade Execution

* The system opens a position on a **buy signal**.
* It **closes the position and records profit** on a **sell signal**.

Each trade is saved as a dictionary with:

```python
{
  "type": "buy" or "sell",
  "price": float,           # price at the signal
  "index": int,            # index of the candle
  "profit": float (optional)  # only in sell trades
}
```

### Example Flow:

1. Buy at index 10, price = 27000
2. Sell at index 25, price = 27500 → Profit = 500

---

## 4. Return Value

Returns a list of trade dictionaries:

```python
[
  {"type": "buy", "price": 27000.0, "index": 10},
  {"type": "sell", "price": 27500.0, "index": 25, "profit": 500.0},
  ...
]
```

This can be visualized on the frontend with price charts and markers.

---

## 5. Usage

This strategy can be executed via:

* The backtester runner using strategy name `macd`
* API route `/backtest` with config:

```json
{
  "symbol": "BTCUSDT",
  "strategy": "macd",
  "interval": "15m"
}
```

---

## Summary

* Indicator: MACD & Signal Line
* Logic: Detects bullish/bearish crossovers
* Goal: Capture short-to-mid-term momentum shifts
* Easy to parameterize for fast/slow/signal tuning

---

> ⚠️ This is a trend-following strategy. Avoids chop but may lag during fast reversals.
