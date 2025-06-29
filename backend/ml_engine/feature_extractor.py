import pandas as pd
import numpy as np
from ta.momentum import RSIIndicator
from ta.trend import MACD, EMAIndicator
from ta.volatility import BollingerBands

def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Convert datetime columns to numeric POSIX timestamps (float)
    datetime_cols = df.select_dtypes(include=['datetime64[ns]', 'datetime64']).columns
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        df[col] = df[col].astype('int64') / 1e9  # convert to seconds float
    return df

def extract_features(df: pd.DataFrame):
    df = preprocess_df(df)

    # Calculate technical indicators
    df['RSI'] = RSIIndicator(df['close']).rsi()
    macd = MACD(df['close'])
    df['MACD'] = macd.macd()
    df['EMA'] = EMAIndicator(df['close']).ema_indicator()
    bb = BollingerBands(df['close'])
    df['BB_upper'] = bb.bollinger_hband()
    df['BB_middle'] = bb.bollinger_mavg()
    df['BB_lower'] = bb.bollinger_lband()

    # Drop rows with NaNs after indicator calculations
    df.dropna(inplace=True)

    # Define potential feature columns
    potential_feature_names = ['RSI', 'MACD', 'EMA', 'BB_upper', 'BB_middle', 'BB_lower']
    existing_potential_features = [col for col in potential_feature_names if col in df.columns]

    if not existing_potential_features:
        print("WARN: No potential feature columns exist after indicator calc and dropna.")
        return pd.DataFrame(), pd.Series()

    selected_features_df = df[existing_potential_features]
    numeric_features_df = selected_features_df.select_dtypes(include='number')

    # Debug log: which columns were dropped or not numeric
    dropped_or_missing_cols = set(potential_feature_names) - set(numeric_features_df.columns)
    if dropped_or_missing_cols:
        non_numeric_in_selected = set(selected_features_df.columns) - set(numeric_features_df.columns)
        if non_numeric_in_selected:
            print(f"INFO: Dropped non-numeric columns: {list(non_numeric_in_selected)}")
        missing_from_selected = set(potential_feature_names) - set(selected_features_df.columns)
        if missing_from_selected:
            print(f"INFO: Missing indicator columns (all NaN or failed): {list(missing_from_selected)}")

    features = numeric_features_df

    # Label: Buy if next candle is higher, else Sell
    if 'close' not in df.columns or df['close'].isnull().all():
        print("WARN: 'close' column missing or all NaN. Cannot generate labels.")
        return features, pd.Series()

    labels = ((df['close'].shift(-1) > df['close']) * 1).fillna(0).astype(int)
    labels = labels.map({1: 'Buy', 0: 'Sell'})

    return features, labels
