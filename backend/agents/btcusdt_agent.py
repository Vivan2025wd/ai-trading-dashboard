import pandas as pd
import os
from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load
from backend.ml_engine.feature_extractor import extract_features

MODEL_PATH = "backend/agents/models/btcusdt_model.pkl"
DATA_PATH = "backtester/data/BTCUSDT_15m.csv"

class BTCUSDTAgent:
    def __init__(self):
        # Load model once when agent instance is created
        if os.path.exists(MODEL_PATH):
            self.model = load(MODEL_PATH)
        else:
            self.model = None
            print(f"Model file not found at {MODEL_PATH}")

    def train(self):
        df = pd.read_csv(DATA_PATH)
        df.columns = [c.lower() for c in df.columns]

        features, labels = extract_features(df)

        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(features, labels)

        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        dump(model, MODEL_PATH)
        print(f"BTCUSDT model trained and saved to {MODEL_PATH}")

        self.model = model  # update model in instance

    def predict(self, df: pd.DataFrame):
        if self.model is None:
            raise ValueError("Model is not loaded. Train the model first or load a saved model.")

        df.columns = [c.lower() for c in df.columns]
        features, _ = extract_features(df)
        latest = features.iloc[-1:]

        prediction = self.model.predict(latest)[0]
        confidence = max(self.model.predict_proba(latest)[0])

        return prediction, round(confidence, 4)


if __name__ == "__main__":
    agent = BTCUSDTAgent()
    agent.train()
