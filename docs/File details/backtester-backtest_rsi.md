# RSI Backtest Script Documentation

This script performs a backtest of a simple RSI-based trading strategy using historical OHLCV data.

---

## File: `backtest_rsi.py`

### Purpose

This file:

* Loads historical candlestick (OHLCV) data from a CSV file
* Computes the RSI (Relative Strength Index)
* Executes a basic RSI trading strategy
* Outputs a list of simulated trades

---

## Imports

```python
import pandas as pd
import numpy as np
```

* **pandas**: For handling tabular data
* **numpy**: Required indirectly by pandas for numerical operations

---

## Load Dataset

```python
df = pd.read_csv('data/BTCUSDT_15m.csv')
```

* Loads Binance OHLCV data from a CSV file for the BTCUSDT trading pair on 15-minute intervals.

---

## Function: `compute_rsi`

```python
def compute_rsi(prices, period=14):
```

* **Input**: Pandas Series of prices (typically closing prices)
* **Output**: RSI values (0-100)

### Logic:

1. Calculate the price change (`delta`)
2. Separate `gain` (positive values) and `loss` (negative values)
3. Compute rolling averages of gains and losses
4. Calculate **Relative Strength (RS)**
5. Compute RSI using:

   ```
   RSI = 100 - (100 / (1 + RS))
   ```

---

## Function: `backtest_rsi_strategy`

```python
def backtest_rsi_strategy(df, rsi_buy=60, rsi_sell=61):
```

* **Input**: DataFrame with price data, Buy/Sell thresholds
* **Output**: A list of simulated trade dictionaries

### Strategy Logic:

* **Buy** if RSI drops below `rsi_buy` and you don't have an open position
* **Sell** if RSI rises above `rsi_sell` and you have a position

Each trade is recorded as a dictionary:

```python
{
    'type': 'buy' or 'sell',
    'price': float,
    'index': int (row index),
    'profit': optional (only on sell)
}
```

---

## Main Execution Block

```python
if __name__ == "__main__":
```

* Runs the backtest when executed directly
* Loads the data
* Executes the strategy
* Prints all trades

---

## Example Output

```bash
✅ CSV loaded with 500 rows
✅ Trades executed: 12
{'type': 'buy', 'price': 29105.12, 'index': 25}
{'type': 'sell', 'price': 29188.44, 'index': 36, 'profit': 83.32}
...
```

---

## Notes

* This is a simplified backtest without slippage, fees, or position sizing
* Ideal for testing strategy logic before integrating with a full pipeline
