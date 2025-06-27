from fastapi import FastAPI, Request, HTTPException, Query
import subprocess
import json
import uuid
import os
import tempfile
import sys
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from typing import Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your agents and mother AI
from backend.agents.btcusdt_agent import BTCUSDTAgent
from backend.agents.ethusdt_agent import ETHUSDTAgent
from backend.mother_ai.coordinator import MotherAI
from backend.strategy_registry import load_strategy

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Setup absolute paths for CSV data files ===
BASE_DIR = r"C:\Users\USER\Documents\GitHub\ai-trading-dashboard"

DATA_PATHS = {
    "BTCUSDT": os.path.join(BASE_DIR, "backtester", "data", "BTCUSDT_15m.csv"),
    "ETHUSDT": os.path.join(BASE_DIR, "backtester", "data", "ETHUSDT_15m.csv"),
}

# === /backtester/strategies ===
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
    print("Received backtest request")
    config = await request.json()
    print("Config received:", config)

    temp_dir = tempfile.gettempdir()
    config_path = os.path.join(temp_dir, f"config_{uuid.uuid4().hex}.json")

    with open(config_path, "w") as f:
        json.dump(config, f)
    print(f"Config written to {config_path}")

    try:
        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
        script_path = os.path.join(PROJECT_ROOT, "backtester", "runner.py")
        print(f"Running runner script at {script_path}")

        python_path = sys.executable

        result = subprocess.run(
            [python_path, script_path, config_path],
            capture_output=True,
            text=True,
            check=True,
            timeout=60,
        )
        print("Runner script completed")
        print("Stdout (first 500 chars):", result.stdout[:500])

        output = json.loads(result.stdout)
        return output

    except subprocess.TimeoutExpired:
        print("Runner script timed out")
        return {"error": "Backtest runner timed out"}

    except subprocess.CalledProcessError as e:
        print("Runner script error:", e)
        print("stderr:", e.stderr)
        print("stdout:", e.stdout)
        return {
            "error": "Backtest subprocess failed",
            "stderr": e.stderr,
            "stdout": e.stdout,
            "returncode": e.returncode,
        }

    except json.JSONDecodeError:
        print("JSON decode error with runner output:", result.stdout)
        return {
            "error": "Invalid JSON from runner",
            "raw_output": result.stdout,
        }

    finally:
        try:
            os.remove(config_path)
            print(f"Deleted temp config file {config_path}")
        except Exception as ex:
            print(f"Failed to delete temp config file: {ex}")

# === /agent/{symbol}/predict ===
@app.get("/agent/{symbol}/predict")
async def agent_predict(symbol: str):
    symbol = symbol.upper()
    data_path = DATA_PATHS.get(symbol)

    if not data_path or not os.path.exists(data_path):
        raise HTTPException(status_code=404, detail=f"No data file for symbol {symbol}")

    try:
        df = pd.read_csv(data_path)

        if symbol == "BTCUSDT":
            agent = BTCUSDTAgent()
            prediction, confidence = agent.predict(df)
            return {
                "symbol": symbol,
                "prediction": prediction,
                "confidence": confidence,
                "timestamp": pd.Timestamp.utcnow().isoformat()
            }

        elif symbol == "ETHUSDT":
            agent = ETHUSDTAgent()
            result: Dict[str, Any] = agent.predict(df)
            return {
                "symbol": symbol,
                "prediction": result["prediction"],
                "confidence": result["confidence"],
                "timestamp": pd.Timestamp.utcnow().isoformat()
            }

        else:
            raise HTTPException(status_code=404, detail=f"No agent available for symbol {symbol}")

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# === /mother-ai/decision ===
@app.get("/mother-ai/decision")
async def mother_decision():
    try:
        print("Mother AI decision triggered")
        decision = MotherAI().decide()
        return decision
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Mother AI decision error: {str(e)}")
