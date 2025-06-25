from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json
from pymongo import MongoClient, errors
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env file contents into environment variables

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client.ai_trading
failed_trades = db.failed_trades

@app.post("/backtest")
async def run_backtest_api(request: Request):
    config = await request.json()
    symbol = config.get("symbol")
    interval = config.get("interval")
    strategy = config.get("strategy")

    temp_config_path = "temp_config.json"
    with open(temp_config_path, "w") as f:
        json.dump(config, f)

    result = subprocess.run(
        ["python", "backtester/runner.py", temp_config_path],
        capture_output=True,
        text=True
    )

    # Optional cleanup
    try:
        os.remove(temp_config_path)
    except Exception:
        pass  # ignore errors here

    if result.returncode != 0:
        return {"error": "Runner failed", "stderr": result.stderr}

    try:
        output = json.loads(result.stdout)
        for trade in output.get("trades", []):
            if trade["type"] == "sell" and trade.get("profit", 0) < 0:
                try:
                    failed_trades.insert_one({
                        "symbol": symbol,
                        "strategy": strategy,
                        "price": trade["price"],
                        "index": trade["index"],
                        "profit": trade["profit"]
                    })
                except errors.PyMongoError as e:
                    # Log the error or handle it appropriately
                    print(f"MongoDB insert error: {e}")

        return output
    except json.JSONDecodeError:
        return {"error": "Failed to parse runner output", "log": result.stdout}
