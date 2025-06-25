from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/backtest")
async def run_backtest_api(request: Request):
    config = await request.json()
    with open("temp_config.json", "w") as f:
        json.dump(config, f)

    result = subprocess.run(
        ["python", "backtester/runner.py", "temp_config.json"],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {"error": "Runner failed", "stderr": result.stderr}

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": "Failed to parse runner output", "log": result.stdout}
