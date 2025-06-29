import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load
from backend.ml_engine.feature_extractor import extract_features
from backend.utils.binance_data import fetch_binance_ohlcv

MODEL_PATH = "backend/agents/models/ethusdt_model.pkl"

class ETHUSDTAgent:
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
        print(f"ETHUSDT model trained and saved to {MODEL_PATH}")

    def predict(self):
        if self.model is None:
            raise ValueError("Model is not loaded. Please train or load the model first.")
        # Fetch latest live OHLCV data from Binance
        df = fetch_binance_ohlcv("ETHUSDT")
        df.columns = [c.lower() for c in df.columns]

        # Debug print: show column dtypes before cleaning
        print("Columns and dtypes before dropping datetime:")
        print(df.dtypes)

        # Drop datetime columns that may cause issues
        datetime_cols = df.select_dtypes(include=['datetime64[ns]']).columns
        df = df.drop(columns=datetime_cols)

        # Also drop common timestamp columns if they exist
        for col in ['open_time', 'timestamp']:
            if col in df.columns:
                df = df.drop(columns=[col])

        features, _ = extract_features(df)
        latest = features.iloc[-1:]
        prediction = self.model.predict(latest)[0]
        confidence = max(self.model.predict_proba(latest)[0])
        return prediction, round(confidence, 4)


if __name__ == "__main__":
    agent = ETHUSDTAgent()
    # Pass CSV path for training
    agent.train("backtester/data/ETHUSDT_15m.csv")
