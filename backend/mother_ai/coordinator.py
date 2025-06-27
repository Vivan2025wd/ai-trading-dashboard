import os
import pandas as pd
from backend.agents.btcusdt_agent import BTCUSDTAgent
from backend.agents.ethusdt_agent import ETHUSDTAgent

class MotherAI:
    def __init__(self):
        self.agents = {
            "BTCUSDT": BTCUSDTAgent(),
            "ETHUSDT": ETHUSDTAgent(),
            # Add more agents here as needed
        }
        # Paths for data CSVs (adjust as needed)
        base_dir = r"C:\Users\USER\Documents\GitHub\ai-trading-dashboard"
        self.data_paths = {
            "BTCUSDT": os.path.join(base_dir, "backtester", "data", "BTCUSDT_15m.csv"),
            "ETHUSDT": os.path.join(base_dir, "backtester", "data", "ETHUSDT_15m.csv"),
        }

    def decide(self):
        predictions = []

        for symbol, agent in self.agents.items():
            data_path = self.data_paths.get(symbol)
            if not data_path:
                continue
            df = pd.read_csv(data_path)

            result = agent.predict(df)

            if isinstance(result, dict):
                # For agents returning dict (e.g. ETHUSDTAgent)
                prediction = result.get("prediction")
                confidence = result.get("confidence")
            elif isinstance(result, tuple) and len(result) == 2:
                # For agents returning tuple (e.g. BTCUSDTAgent)
                prediction, confidence = result
            else:
                # Unexpected format; skip this agent's output
                continue

            predictions.append({
                "symbol": symbol,
                "prediction": prediction,
                "confidence": confidence,
            })

        # Filter out agents with no predictions (if any)
        predictions = [p for p in predictions if p["prediction"] is not None]

        # Capital allocation logic example:
        # We allocate capital proportional to confidence, only for 'Buy' signals
        buy_signals = [p for p in predictions if p["prediction"].lower() == "buy"]

        if not buy_signals:
            # No buy signals, no allocation
            return {
                "decision": "hold",
                "allocations": [],
                "message": "No buy signals from agents"
            }

        total_confidence = sum(p["confidence"] for p in buy_signals)
        allocations = []
        for p in buy_signals:
            allocation_pct = (p["confidence"] / total_confidence) * 100
            allocations.append({
                "symbol": p["symbol"],
                "allocation_pct": round(allocation_pct, 2),
                "confidence": round(p["confidence"], 4),
            })

        # Sort descending allocation for clarity
        allocations.sort(key=lambda x: x["allocation_pct"], reverse=True)

        # Return top candidate plus allocation info
        top_candidate = allocations[0]

        return {
            "decision": "buy",
            "top_candidate": top_candidate["symbol"],
            "allocation_pct": top_candidate["allocation_pct"],
            "confidence": top_candidate["confidence"],
            "allocations": allocations,
        }
