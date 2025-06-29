import pandas as pd
import numpy as np
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
 fix/numeric-feature-casting
    features = df[['RSI', 'MACD', 'EMA', 'BB_upper', 'BB_middle', 'BB_lower']]

    # Safeguard: Ensure only numeric columns are in features.
    # This will drop any non-numeric columns, including a stray datetime 'timestamp' column if it exists.
    if not features.empty:
        features = features.select_dtypes(include=np.number)

    # Features: indicator columns only
    potential_feature_names = ['RSI', 'MACD', 'EMA', 'BB_upper', 'BB_middle', 'BB_lower']
    # Ensure all potential features are present in df before selection
    # This can happen if indicator calculation failed for some reason and produced all NaNs for a column
    # which was then dropped by df.dropna()
    existing_potential_features = [col for col in potential_feature_names if col in df.columns]

    if not existing_potential_features:
        # Handle the case where no feature columns exist, perhaps return empty DataFrame or raise error
        # For now, let's assume this means features cannot be extracted.
        # This could happen if df is too short for any indicators or all indicator columns were dropped.
        print("WARN: No potential feature columns exist in DataFrame after indicator calculation and dropna.")
        # Depending on requirements, either return empty dataframes or raise
        return pd.DataFrame(), pd.Series()


    selected_features_df = df[existing_potential_features]

    # Ensure only numeric features are passed
    numeric_features_df = selected_features_df.select_dtypes(include='number')

    # Log columns that were in potential_feature_names but not in numeric_features_df.columns
    # This could be due to them being non-numeric OR not existing in df after indicator calculation
    dropped_or_missing_cols = set(potential_feature_names) - set(numeric_features_df.columns)
    if dropped_or_missing_cols:
        # A more specific check for truly non-numeric among selected
        non_numeric_in_selected = set(selected_features_df.columns) - set(numeric_features_df.columns)
        if non_numeric_in_selected:
            print(f"INFO: Selected non-numeric columns (will be excluded): {list(non_numeric_in_selected)}")

        # Columns that were in potential_feature_names but not even in selected_features_df (e.g. all NaN and dropped)
        missing_from_selected = set(potential_feature_names) - set(selected_features_df.columns)
        if missing_from_selected:
             print(f"INFO: Potential features not found in DataFrame (likely all NaN and dropped): {list(missing_from_selected)}")


    features = numeric_features_df

    # Label: next close price direction
    # Ensure 'close' column is present for labels
    if 'close' not in df.columns or df['close'].isnull().all():
        print("WARN: 'close' column missing or all NaN, cannot generate labels.")
        return features, pd.Series() # Return features but empty labels
     main

    labels = ((df['close'].shift(-1) > df['close']) * 1).fillna(0).astype(int)
    labels = labels.map({1: 'Buy', 0: 'Sell'})

    return features, labels
