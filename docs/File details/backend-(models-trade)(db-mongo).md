
This documentation explains two key backend components of your trading platform:

1. **Trade Model (`trade.py`)** — Responsible for standardizing trade data into a consistent dictionary format.
2. **MongoDB Database Setup (`mongo.py`)** — Handles connection to your MongoDB database, reading environment variables for credentials, and initializing collections used by your app.

---

## 1. Trade Model: `trade_to_dict` function

### File Location

`backend/models/trade.py`

### Purpose

The `trade_to_dict` function takes a trade represented as a Python dictionary (usually from your backtesting or live trading engine) and normalizes it into a consistent dictionary format with expected keys.

### Why normalize?

- Different parts of your system may produce trade data with slightly different fields or missing optional fields.
- Normalizing ensures downstream code (like database saving or API responses) always get a predictable structure.

### Function Details

```python
def trade_to_dict(trade): 
    return {
        "symbol": trade.get("symbol"),
        "strategy": trade.get("strategy"),
        "price": trade.get("price"),
        "index": trade.get("index"),
        "profit": trade.get("profit", 0),
        "timestamp": trade.get("timestamp")
    }
trade is expected to be a dictionary with keys like "symbol", "strategy", "price", etc.

The function uses .get() to safely access keys; if a key is missing, it returns None (except "profit" which defaults to 0).

Returns a new dictionary with exactly these keys, ready to be saved or processed further.

Example Usage
python
Copy
Edit
raw_trade = {
    "symbol": "BTCUSDT",
    "strategy": "ema",
    "price": 30000,
    "index": 45,
    "timestamp": 1688000000
    # 'profit' key missing
}

normalized_trade = trade_to_dict(raw_trade)
# Result:
# {
#   "symbol": "BTCUSDT",
#   "strategy": "ema",
#   "price": 30000,
#   "index": 45,
#   "profit": 0,            # default applied
#   "timestamp": 1688000000
# }
2. MongoDB Database Setup: mongo.py
File Location
backend/db/mongo.py

Purpose
This module connects your backend application to a MongoDB database using environment variables for secure credentials. It initializes important collections your app will use.

How it works
Uses the pymongo library to interact with MongoDB.

Reads MongoDB connection details from a .env file using dotenv.

Creates a client connection to the MongoDB server.

Sets up handles for specific collections like "failed_trades" and "backtests".

Code Breakdown
python
Copy
Edit
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

MONGODB_URI = os.getenv("MONGODB_URI")  # MongoDB connection string
DB_NAME = os.getenv("DB_NAME")          # Database name

if not MONGODB_URI or not DB_NAME:
    raise ValueError("MONGODB_URI and DB_NAME must be set in the .env file")

client = MongoClient(MONGODB_URI)  # Connect to MongoDB
db = client[DB_NAME]               # Select the database

# Example collections used by the app
failed_trades = db["failed_trades"]
backtests = db["backtests"]
What goes in .env file?
env
Copy
Edit
MONGODB_URI=mongodb+srv://username:password@cluster0.mongodb.net
DB_NAME=your_database_name
What are collections?
Collections in MongoDB are like tables in relational databases.

"failed_trades" could store trade data that failed processing or execution.

"backtests" might store results or metadata of your trading strategy backtests.

Example Usage
Elsewhere in your backend, you can import and use these collections to insert or query data:

python
Copy
Edit
from backend.db.mongo import failed_trades

# Insert a failed trade record
failed_trades.insert_one({
    "symbol": "BTCUSDT",
    "error": "Order rejected",
    "timestamp": 1688000000
})
Summary
Component	Purpose	Inputs	Outputs
trade_to_dict	Normalize trade data into a consistent dictionary	Raw trade dictionary	Standardized trade dictionary
mongo.py	Connect to MongoDB, initialize collections	Environment variables	MongoDB client and collections

