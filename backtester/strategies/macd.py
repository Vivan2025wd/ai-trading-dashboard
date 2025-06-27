import pandas as pd

# --- MACD Calculation ---
def compute_macd(df, fast=12, slow=26, signal=9):
    exp1 = df['Close'].ewm(span=fast, adjust=False).mean()
    exp2 = df['Close'].ewm(span=slow, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return macd, signal_line

# --- MACD Strategy ---
def backtest_macd_strategy(df):
    macd, signal = compute_macd(df)
    position = 0
    entry_price = 0
    trades = []

    for i in range(1, len(df)):
        if position == 0 and macd.iloc[i] > signal.iloc[i] and macd.iloc[i-1] <= signal.iloc[i-1]:
            position = 1
            entry_price = df['Close'].iloc[i]
            trades.append({"type": "buy", "price": entry_price, "index": i})
        elif position == 1 and macd.iloc[i] < signal.iloc[i] and macd.iloc[i-1] >= signal.iloc[i-1]:
            exit_price = df['Close'].iloc[i]
            profit = exit_price - entry_price
            trades.append({"type": "sell", "price": exit_price, "index": i, "profit": profit})
            position = 0

    return trades
