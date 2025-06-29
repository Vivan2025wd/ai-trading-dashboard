import pandas as pd
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
from ta.volatility import BollingerBands

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # If there's a datetime column, convert it to numeric or drop
    datetime_cols = df.select_dtypes(include=['datetime64[ns]', 'datetime64']).columns
    for col in datetime_cols:
        # Convert datetime to POSIX timestamp float seconds
        df[col] = pd.to_datetime(df[col], errors='coerce')
        df[col] = df[col].astype('int64') / 1e9
    return df

def extract_features(df: pd.DataFrame):
    df = preprocess_df(df)
    
    # Calculate indicators
    df['RSI'] = RSIIndicator(df['close']).rsi()
    macd = MACD(df['close'])
    df['MACD'] = macd.macd()
    df['EMA'] = EMAIndicator(df['close']).ema_indicator()
    bb = BollingerBands(df['close'])
    df['BB_upper'] = bb.bollinger_hband()
    df['BB_middle'] = bb.bollinger_mavg()
    df['BB_lower'] = bb.bollinger_lband()

    # Drop rows with NaN values after indicator calculations
    df.dropna(inplace=True)

    # Features: indicator columns only
    features = df[['RSI', 'MACD', 'EMA', 'BB_upper', 'BB_middle', 'BB_lower']]

    # Label: next close price direction
    labels = ((df['close'].shift(-1) > df['close']) * 1).fillna(0).astype(int)
    labels = labels.map({1: 'Buy', 0: 'Sell'})

    return features, labels
