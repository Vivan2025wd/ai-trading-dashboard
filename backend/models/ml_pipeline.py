import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
from backend.ml_engine.feature_extractor import extract_features
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/models
MODEL_PATH = os.path.join(BASE_DIR, "random_forest.pkl")

class TradingModel:
    def __init__(self):
        self.model = None

    def train(self, df: pd.DataFrame):
        X, y = extract_features(df)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        clf = RandomForestClassifier(n_estimators=100, random_state=42)
        clf.fit(X_train, y_train)

        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print(f"Model trained with accuracy: {acc:.4f}")

        self.model = clf
        joblib.dump(self.model, MODEL_PATH)
        return acc

    def load(self):
        self.model = joblib.load(MODEL_PATH)

    def predict(self, df: pd.DataFrame):
        if self.model is None:
            self.load()
        if self.model is None:
            raise ValueError("Model is not trained or could not be loaded.")

        X, _ = extract_features(df)
        preds_proba = self.model.predict_proba(X)
        preds = self.model.predict(X)

        # Take last prediction for latest timestamp
        last_pred = preds[-1]
        last_pred_proba = preds_proba[-1].max()

        # Get timestamp from df (last row)
        timestamp = df.index[-1] if df.index.dtype.kind in 'M' else None

        return {
            "prediction": last_pred,
            "confidence": float(last_pred_proba),
            "timestamp": timestamp
        }
