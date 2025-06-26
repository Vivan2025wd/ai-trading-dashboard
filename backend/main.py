from fastapi import FastAPI, Request, HTTPException, Query
import subprocess
import json
import uuid
import os
import tempfile
import sys
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

        python_path = sys.executable  # Use current Python executable

        result = subprocess.run(
            [python_path, script_path, config_path],
            capture_output=True,
            text=True,
            check=True,
            timeout=60,  # timeout in seconds
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


@app.get("/backtester/strategies")
async def get_strategies(symbol: str = Query(..., description="Trading pair symbol like BTCUSDT")):
    """
    Return mock or real strategy suggestions for given symbol.
    Replace the mock response below with your actual logic or subprocess call.
    """

    # Added BNBUSDT and ADAUSDT entries without touching your existing ones
    strategies_data = {
        "BTCUSDT": {
            "suggestion": "Buy",
            "latest": {
                "close": 30000.25,
                "rsi": 45.6,
                "ema": 29900.15,
                "macd": {"MACD": 0.5, "signal": 0.45},
                "bb": {"lower": 29500.0, "middle": 30000.0, "upper": 30500.0},
            },
        },
        "ETHUSDT": {
            "suggestion": "Sell",
            "latest": {
                "close": 2000.5,
                "rsi": 70.2,
                "ema": 1985.0,
                "macd": {"MACD": -0.3, "signal": -0.25},
                "bb": {"lower": 1900.0, "middle": 2000.0, "upper": 2100.0},
            },
        },
        "BNBUSDT": {
            "suggestion": "Hold",
            "latest": {
                "close": 320.45,
                "rsi": 55.0,
                "ema": 315.0,
                "macd": {"MACD": 0.1, "signal": 0.05},
                "bb": {"lower": 300.0, "middle": 320.0, "upper": 340.0},
            },
        },
        "ADAUSDT": {
            "suggestion": "Buy",
            "latest": {
                "close": 1.15,
                "rsi": 40.5,
                "ema": 1.10,
                "macd": {"MACD": 0.25, "signal": 0.20},
                "bb": {"lower": 1.0, "middle": 1.15, "upper": 1.30},
            },
        },
    }

    result = strategies_data.get(symbol.upper())
    if not result:
        raise HTTPException(status_code=404, detail=f"No strategies found for symbol {symbol}")

    return result
