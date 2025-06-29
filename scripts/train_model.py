import os
import sys
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# Add project root to sys.path to allow backend imports
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from backend.ml_engine.feature_extractor import extract_features

def main():
    # Path to CSV data
    csv_path = os.path.join(project_root, "backtester", "data", "BTCUSDT_15m.csv")
    df = pd.read_csv(csv_path)

    # Normalize columns to lowercase & strip spaces
    df.columns = [col.lower().strip() for col in df.columns]

    # Validate required columns
    if "close" not in df.columns:
        raise ValueError("CSV is missing required column: 'close'")

    # Extract features and labels
    features, labels = extract_features(df)

    # Train Random Forest model
    model = RandomForestClassifier()
    model.fit(features, labels)

    # Save the trained model
    model_path = os.path.join(project_root, "backend", "models", "random_forest.pkl")
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)

    print(f"✅ Model trained and saved at: {model_path}")

if __name__ == "__main__":
    main()
