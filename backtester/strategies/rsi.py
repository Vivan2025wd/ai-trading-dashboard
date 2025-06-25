import pandas as pd

def compute_rsi(prices, period=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def backtest_rsi_strategy(df, rsi_buy=30, rsi_sell=70):
    df['RSI'] = compute_rsi(df['Close'])
    position = 0
    entry_price = 0
    trades = []

    for i in range(len(df)):
        if position == 0 and df['RSI'].iloc[i] < rsi_buy:
            position = 1
            entry_price = df['Close'].iloc[i]
            trades.append({"type": "buy", "price": entry_price, "index": i})
        elif position == 1 and df['RSI'].iloc[i] > rsi_sell:
            exit_price = df['Close'].iloc[i]
            profit = exit_price - entry_price
            trades.append({"type": "sell", "price": exit_price, "index": i, "profit": profit})
            position = 0
    return trades

