
# `main.py` – FastAPI Backend for Trading Strategy Backtests 🧠📊

This file is your backend **API server** built with [FastAPI](https://fastapi.tiangolo.com/). It exposes two endpoints:

- `POST /backtest`: Runs a strategy backtest with given settings
- `GET /backtester/strategies`: Returns mock strategy suggestions for symbols like BTCUSDT

This guide explains every part in simple terms for beginners, including where data and logic come from.

---

## 🔧 What This Backend Does

- Accepts backtest configuration from a frontend (e.g., React).
- Saves it as a temporary config file.
- Runs a Python script (`runner.py`) in a subprocess to perform the backtest.
- Collects and returns the output as JSON.

---

## 🚀 FastAPI Setup

```python
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
```

- `FastAPI`: The core web framework.
- `CORSMiddleware`: Allows the frontend (on port 5173 or 5174) to call this API.

```python
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This sets up **CORS** to let the React frontend talk to this backend without browser security errors.

---

## 📬 POST `/backtest`

### What It Does

1. Accepts a JSON config from the frontend.
2. Writes it to a temporary `.json` file.
3. Calls `runner.py` using `subprocess`.
4. Reads the result and returns it.

### Code Breakdown

```python
@app.post("/backtest")
async def run_backtest(request: Request):
    config = await request.json()
```

Receives a config like:

```json
{
  "symbol": "BTCUSDT",
  "interval": "15m",
  "strategy": "rsi",
  "params": {
    "rsi_period": 14,
    "overbought": 70,
    "oversold": 30
  }
}
```

---

### Save Config to Temp File

```python
temp_dir = tempfile.gettempdir()
config_path = os.path.join(temp_dir, f"config_{uuid.uuid4().hex}.json")
with open(config_path, "w") as f:
    json.dump(config, f)
```

- Saves the config to a unique file like `/tmp/config_abc123.json`.

---

### Run the Backtest Script

```python
script_path = os.path.join(PROJECT_ROOT, "backtester", "runner.py")

result = subprocess.run(
    [python_path, script_path, config_path],
    capture_output=True,
    text=True,
    check=True,
    timeout=60,
)
```

- Calls `runner.py` and passes the config path.
- The runner script reads price data, runs the strategy, and returns the result as JSON.

---

### Parse and Return Output

```python
output = json.loads(result.stdout)
return output
```

If it works, this sends back:

```json
{
  "trades": [...],
  "ohlcv": [...],
  "message": "✅ Backtest complete"
}
```

---

### Error Handling

Handles things like:
- Script timeout
- Script failure (return code != 0)
- Invalid JSON output

---

### Clean Up

```python
os.remove(config_path)
```

- Deletes the temp config file to keep your system clean.

---

## 📊 GET `/backtester/strategies`

### Purpose

Returns mock strategy suggestions for specific symbols like `BTCUSDT` or `ETHUSDT`.

```python
@app.get("/backtester/strategies")
async def get_strategies(symbol: str)
```

### Example Response

```json
{
  "suggestion": "Buy",
  "latest": {
    "close": 30000.25,
    "rsi": 45.6,
    "ema": 29900.15,
    "macd": {"MACD": 0.5, "signal": 0.45},
    "bb": {"lower": 29500.0, "middle": 30000.0, "upper": 30500.0}
  }
}
```

- Used to power strategy previews or recommendation panels in the UI.

---

### Where the Data Comes From

Right now, this is **hardcoded** in the file:

```python
strategies_data = {
  "BTCUSDT": { ... },
  ...
}
```

Later, you can replace it with real-time indicators from your backend engine.

---

## 🛠 Example Frontend Request

### POST `/backtest`

```js
fetch("http://localhost:8000/backtest", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    symbol: "BTCUSDT",
    interval: "15m",
    strategy: "rsi",
    params: {
      rsi_period: 14,
      overbought: 70,
      oversold: 30
    }
  })
})
.then(res => res.json())
.then(data => console.log(data))
```

---

## ✅ Summary

- `main.py` = FastAPI backend with 2 endpoints
- `/backtest`: Runs the real backtest using `runner.py`
- `/backtester/strategies`: Returns mock strategy indicators
- Uses temporary files and subprocesses to decouple strategy logic

---