# Strategy Registry Module Documentation

## Overview

`strategy_registry.py` is a utility module designed to **dynamically load and provide access to different trading strategy implementations** in your backtesting system. It acts as a centralized registry and loader for your trading strategies, allowing you to easily plug in various strategies by name without manually importing each one everywhere.

---

## Why do we need a Strategy Registry?

When building a backtester or trading system, you might have multiple strategies implemented, for example:

- EMA (Exponential Moving Average) strategy
- MACD (Moving Average Convergence Divergence) strategy
- RSI (Relative Strength Index) strategy

Instead of importing these strategy functions manually wherever needed, the registry provides:

- **A single place to map strategy names to their implementations**
- **Dynamic importing based on strategy name strings** (helps in making the backtester extensible)
- **An easy way to add variants of strategies** without changing the core backtesting code

---

## How does it work?

### 1. Mapping Strategy Names to Python Modules

```python
STRATEGY_MODULES = {
    "ema": "backtester.strategies.ema",
    "macd": "backtester.strategies.macd",
    "rsi": "backtester.strategies.rsi",
    "rsi_v1": "backtester.strategies.rsi",
}
This dictionary links strategy name keys (like "ema", "macd") to the Python module paths where the strategy logic is implemented.

For example, the "ema" strategy is found inside the backtester/strategies/ema.py file.

2. Loading the Strategy Function Dynamically
python
Copy
Edit
def load_strategy(strategy_name):
    module_path = STRATEGY_MODULES.get(strategy_name.lower())
    if not module_path:
        raise ValueError(f"Unknown strategy: {strategy_name}")

    module = importlib.import_module(module_path)
The function load_strategy takes a string strategy_name (like "ema" or "rsi_v1") as input.

It uses the dictionary above to get the corresponding Python module path.

It imports the module dynamically using Python’s importlib.import_module.

If the strategy name is not found, it raises an error.

3. Determining the Function to Call
Each strategy module can have multiple functions or versions. The registry decides which function to call based on the strategy_name.

python
Copy
Edit
base = strategy_name.lower().replace("_", "")
if base == "rsiv1":
    strategy_func_name = "backtest_rsi_v1_strategy"
else:
    strategy_func_name = f"backtest_{strategy_name.lower()}_strategy"
For example:

"ema" → function name: backtest_ema_strategy

"rsi_v1" → function name: backtest_rsi_v1_strategy

This naming convention helps in maintaining multiple versions of strategies in the same module.

4. Returning the Strategy Function
python
Copy
Edit
if not hasattr(module, strategy_func_name):
    raise AttributeError(f"{module_path} does not implement {strategy_func_name}")

return getattr(module, strategy_func_name)
The code checks if the module has the required function.

If yes, it returns the function object.

This function can then be called by your backtesting engine with the required data inputs.

Where does it get data and logic from?
Data:
The registry itself does not fetch or handle any trading data (like price candles, indicators). It only loads the strategy code.

Logic:
The actual trading logic is implemented inside the strategy modules like:

backtester/strategies/ema.py

backtester/strategies/macd.py

backtester/strategies/rsi.py

Each of these modules exports one or more functions that apply the strategy’s rules to trading data. The load_strategy function simply provides a way to get the right function so the backtester can execute the strategy.

Example Usage
python
Copy
Edit
from strategy_registry import load_strategy

# Load the EMA strategy function dynamically
ema_strategy_func = load_strategy("ema")

# Assuming you have OHLCV (Open, High, Low, Close, Volume) data
ohlcv_data = [...]

# Run the strategy logic on your data
trades = ema_strategy_func(ohlcv_data)

# 'trades' contains buy/sell signals based on the EMA strategy logic
Summary
Purpose: Centralize and manage loading of multiple trading strategies by name.

Input: Strategy name as a string.

Output: Strategy function you can call with market data.

Extensible: Easily add new strategies or versions without changing core code.

Does not handle data fetching: Only loads strategy logic modules.