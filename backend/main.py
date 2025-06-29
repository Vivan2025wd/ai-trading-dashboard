from fastapi import FastAPI, Request, HTTPException, Query
import subprocess
import json
import uuid
import os
import tempfile
import sys
import pandas as pd
from typing import Dict, Any, List, Optional
from fastapi.middleware.cors import CORSMiddleware

# Setup path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# === Imports ===
from backend.agents.btcusdt_agent import BTCUSDTAgent
from backend.agents.ethusdt_agent import ETHUSDTAgent
from backend.mother_ai.coordinator import MotherAI
from backend.strategy_registry import load_strategy
from backend.models.ml_pipeline import TradingModel
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === In-Memory ML Model ===
model = TradingModel()
model.load()

# === /backtester/strategies ===
BASE_DIR = r"C:\Users\USER\Documents\GitHub\ai-trading-dashboard"
DATA_PATHS = {
    "BTCUSDT": os.path.join(BASE_DIR, "backtester", "data", "BTCUSDT_15m.csv"),
    "ETHUSDT": os.path.join(BASE_DIR, "backtester", "data", "ETHUSDT_15m.csv"),
}

@app.get("/backtester/strategies")
async def get_strategies(symbol: str = Query(..., description="Trading pair symbol like BTCUSDT")):
    symbol = symbol.upper()
    data_path = DATA_PATHS.get(symbol)
    if not data_path or not os.path.exists(data_path):
        raise HTTPException(status_code=404, detail=f"No data file for symbol {symbol}")

    df = pd.read_csv(data_path)
    df.columns = [col.lower() for col in df.columns]

    strategy_names = ["rsi", "macd", "ema"]
    indicators = {}
    suggestions = []

    for strat_name in strategy_names:
        try:
            strategy_func = load_strategy(strat_name)
            result = strategy_func(df)

            for key, value in result.get("indicators", {}).items():
                indicators[key] = value

            if "suggestion" in result:
                suggestions.append(result["suggestion"].lower())
        except Exception as e:
            print(f"Error running strategy {strat_name} for {symbol}: {e}")

    if suggestions:
        buy_count = suggestions.count("buy")
        sell_count = suggestions.count("sell")

        if buy_count > sell_count:
            combined_suggestion = "Buy"
        elif sell_count > buy_count:
            combined_suggestion = "Sell"
        else:
            combined_suggestion = "Hold"
    else:
        combined_suggestion = "Hold"

    indicators["close"] = df["close"].iloc[-1]

    return {
        "suggestion": combined_suggestion,
        "latest": indicators,
    }

# === /backtest ===
@app.post("/backtest")
async def run_backtest(request: Request):
    config = await request.json()
    temp_dir = tempfile.gettempdir()
    config_path = os.path.join(temp_dir, f"config_{uuid.uuid4().hex}.json")

    with open(config_path, "w") as f:
        json.dump(config, f)

    try:
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
        script_path = os.path.join(PROJECT_ROOT, "backtester", "runner.py")

        result = subprocess.run(
            [sys.executable, script_path, config_path],
            capture_output=True,
            text=True,
            check=True,
            timeout=60,
        )

        output = json.loads(result.stdout)
        return output

    except subprocess.TimeoutExpired:
        return {"error": "Backtest runner timed out"}

    except subprocess.CalledProcessError as e:
        return {
            "error": "Backtest subprocess failed",
            "stderr": e.stderr,
            "stdout": e.stdout,
            "returncode": e.returncode,
        }

    except json.JSONDecodeError:
        return {
            "error": "Invalid JSON from runner",
            "raw_output": result.stdout,
        }

    finally:
        try:
            os.remove(config_path)
        except Exception as ex:
            print(f"Failed to delete temp config file: {ex}")

# === /agent/{symbol}/predict ===
@app.get("/agent/{symbol}/predict")
async def agent_predict(symbol: str):
    symbol = symbol.upper()

    try:
        if symbol == "BTCUSDT":
            agent = BTCUSDTAgent()
            prediction, confidence = agent.predict()
        elif symbol == "ETHUSDT":
            agent = ETHUSDTAgent()
            prediction, confidence = agent.predict()
        else:
            raise HTTPException(status_code=404, detail=f"No agent available for symbol {symbol}")

        return {
            "symbol": symbol,
            "prediction": prediction,
            "confidence": confidence,
            "timestamp": pd.Timestamp.utcnow().isoformat()
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# === /mother-ai/decision ===
@app.get("/mother-ai/decision")
async def mother_decision():
    try:
        decision = MotherAI().decide()
        return decision
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Mother AI decision error: {str(e)}")

# === ML /predict from OHLCV JSON ===
class OHLCV(BaseModel):
    timestamp: Optional[str]
    open: float
    high: float
    low: float
    close: float
    volume: float

class OHLCVRequest(BaseModel):
    symbol: str
    data: List[OHLCV]

@app.post("/predict")
async def predict_from_ohlcv(request: OHLCVRequest):
    try:
        data_dicts = [d.dict() for d in request.data]
        df = pd.DataFrame(data_dicts)

        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df.set_index('timestamp', inplace=True)

        result = model.predict(df)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# Duplicate /agent/{symbol}/predict endpoint removed to resolve function name conflict.
