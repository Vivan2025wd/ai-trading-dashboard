import pandas as pd

# Adjust the path if needed
csv_path = "backtester/data/BTCUSDT_15m.csv"

df = pd.read_csv(csv_path)
print("Columns in CSV:")
print(df.columns.tolist())
