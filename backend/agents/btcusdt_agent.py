import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load
from backend.ml_engine.feature_extractor import extract_features
from backend.utils.binance_data import fetch_binance_ohlcv

MODEL_PATH = "backend/agents/models/btcusdt_model.pkl"

class BTCUSDTAgent:
    def __init__(self):
        if os.path.exists(MODEL_PATH):
            self.model = load(MODEL_PATH)
        else:
            self.model = None
            print(f"Model file not found at {MODEL_PATH}")

    def train(self, csv_path: str):
        df = pd.read_csv(csv_path)
        df.columns = [c.lower() for c in df.columns]

        result = extract_features(df)
        if result is None or not isinstance(result, (list, tuple)) or len(result) != 2:
            raise ValueError("extract_features must return (features, labels).")
        features, labels = result
        if features is None or labels is None:
            raise ValueError("Features or labels are None.")

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(features, labels)

        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        dump(model, MODEL_PATH)
        self.model = model
        print(f"BTCUSDT model trained and saved to {MODEL_PATH}")

    def predict(self):
        if self.model is None:
            raise ValueError("Model is not loaded. Train or load the model first.")

        # Fetch live OHLCV from Binance
        data = fetch_binance_ohlcv("BTCUSDT")
        df = pd.DataFrame(data, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
        ])

        # Keep only needed numeric columns
        numeric_cols = ["open", "high", "low", "close", "volume"]
        df = df[numeric_cols].apply(pd.to_numeric, errors="coerce").dropna()

        # Extract features
        result = extract_features(df)
        if result is None or not isinstance(result, (list, tuple)) or len(result) == 0:
            raise ValueError("extract_features returned invalid features.")
        features = result[0]

        latest_features = features.iloc[-1:]
        prediction = self.model.predict(latest_features)[0]
        confidence = max(self.model.predict_proba(latest_features)[0])

        return prediction, round(confidence, 4)


if __name__ == "__main__":
    agent = BTCUSDTAgent()
    agent.train("backtester/data/BTCUSDT_15m.csv")
