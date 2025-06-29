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
        features, labels = extract_features(df)
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(features, labels)
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        dump(model, MODEL_PATH)
        self.model = model
        print(f"BTCUSDT model trained and saved to {MODEL_PATH}")

    def predict(self):
        if self.model is None:
            raise ValueError("Model is not loaded. Please train or load the model first.")
        # Fetch latest live OHLCV data from Binance
        df = fetch_binance_ohlcv("BTCUSDT")
        df.columns = [c.lower() for c in df.columns]

        # Datetime columns are handled by extract_features -> preprocess_df
        # No need to drop them here explicitly.

        features, _ = extract_features(df)

        if features.empty:
            print("WARN: Feature extraction returned empty, cannot predict.")
            return None, 0.0 # Or raise an error, or handle as per system design

        latest = features.iloc[-1:]
        prediction = self.model.predict(latest)[0]
        confidence = max(self.model.predict_proba(latest)[0])
        return prediction, round(confidence, 4)


if __name__ == "__main__":
    agent = BTCUSDTAgent()
    # Pass CSV path for training
    agent.train("backtester/data/BTCUSDT_15m.csv")
