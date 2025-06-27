import os
from typing import Optional
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load
from backend.ml_engine.feature_extractor import extract_features
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

class ETHUSDTAgent:
    def __init__(self):
        # Resolve model path relative to this file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.model_path = os.path.join(base_dir, "models", "ethusdt_model.pkl")
        self.model: Optional[RandomForestClassifier] = None

    def train(self, data_path: str):
        """
        Train the model on historical OHLCV data and save it.
        """
        df = pd.read_csv(data_path)
        df.columns = [c.lower() for c in df.columns]

        features, labels = extract_features(df)

        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(features, labels)

        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        dump(self.model, self.model_path)
        print(f"ETHUSDT model trained on {len(df)} rows and saved to {self.model_path}")

    def load_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        self.model = load(self.model_path)

    def predict(self, df: pd.DataFrame):
        if self.model is None:
            self.load_model()

        assert self.model is not None, "Model is not loaded"

        df.columns = [c.lower() for c in df.columns]
        features, _ = extract_features(df)
        latest = features.iloc[-1:]

        prediction = self.model.predict(latest)[0]
        confidence = max(self.model.predict_proba(latest)[0])

        return {
            "symbol": "ETHUSDT",
            "prediction": prediction,
            "confidence": round(confidence, 4),
        }

if __name__ == "__main__":
    agent = ETHUSDTAgent()

    # Dynamically resolve path for standalone run
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.abspath(os.path.join(current_dir, "..", "..", "backtester", "data", "ETHUSDT_15m.csv"))

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"ETHUSDT CSV not found at {data_path}")

    agent.train(data_path)
