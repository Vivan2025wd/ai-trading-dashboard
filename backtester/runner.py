# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import subprocess
import os
import json

app = FastAPI()

# Allow frontend CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class BacktestRequest(BaseModel):
    symbol: str
    interval: str = "15m"
    strategy: str
    params: Optional[dict] = {}

class Trade(BaseModel):
    type: str
    price: float
    index: int
    profit: Optional[float] = None

class BacktestResponse(BaseModel):
    trades: List[Trade]
    message: str

@app.get("/")
def root():
    return {"message": "AI Trading API Running"}

@app.post("/backtest", response_model=BacktestResponse)
def run_backtest(request: BacktestRequest):
    # Write config to a temp file
    config_path = "temp_config.json"
    with open(config_path, "w") as f:
        json.dump(request.dict(), f)

    # Call the Python backtest script
    process = subprocess.run(
        ["python", "backtester/runner.py", config_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    if process.returncode != 0:
        raise HTTPException(status_code=500, detail=process.stderr)

    try:
        trades = json.loads(process.stdout)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Invalid output from backtest runner")

    return BacktestResponse(trades=trades, message="✅ Backtest complete")
