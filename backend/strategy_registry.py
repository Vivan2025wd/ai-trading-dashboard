# backend/strategy_registry.py
import importlib
from backtester.strategies import rsi, macd, ema


STRATEGY_MODULES = {
    "ema": "backtester.strategies.ema",
    "macd": "backtester.strategies.macd",
    "rsi": "backtester.strategies.rsi",       # Maps to default `backtest_rsi_strategy`
    "rsi_v1": "backtester.strategies.rsi",    # Variant 1 support
}


def load_strategy(strategy_name):
    module_path = STRATEGY_MODULES.get(strategy_name.lower())
    if not module_path:
        raise ValueError(f"Unknown strategy: {strategy_name}")
    
    module = importlib.import_module(module_path)
    
    # Normalize strategy function name
    base = strategy_name.lower().replace("_", "")
    if base == "rsiv1":
        strategy_func_name = "backtest_rsi_v1_strategy"
    else:
        strategy_func_name = f"backtest_{strategy_name.lower()}_strategy"
    
    if not hasattr(module, strategy_func_name):
        raise AttributeError(f"{module_path} does not implement {strategy_func_name}")
    
    return getattr(module, strategy_func_name)
