from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

if not MONGODB_URI or not DB_NAME:
    raise ValueError("MONGODB_URI and DB_NAME must be set in the .env file")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

# Example collections
failed_trades = db["failed_trades"]
backtests = db["backtests"]
