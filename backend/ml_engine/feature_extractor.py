import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
from ta.volatility import BollingerBands

def extract_features(df: pd.DataFrame):
    df = df.copy()
    df['RSI'] = RSIIndicator(df['close']).rsi()
    macd = MACD(df['close'])
    df['MACD'] = macd.macd()
    df['EMA'] = EMAIndicator(df['close']).ema_indicator()
    bb = BollingerBands(df['close'])
    df['BB_upper'] = bb.bollinger_hband()
    df['BB_middle'] = bb.bollinger_mavg()
    df['BB_lower'] = bb.bollinger_lband()

    df.dropna(inplace=True)

    features = df[['RSI', 'MACD', 'EMA', 'BB_upper', 'BB_middle', 'BB_lower']]
    labels = ((df['close'].shift(-1) > df['close']) * 1).fillna(0).astype(int)
    labels = labels.map({1: 'Buy', 0: 'Sell'})
    return features, labels
