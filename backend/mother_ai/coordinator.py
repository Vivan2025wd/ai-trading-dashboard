import os
from backend.agents.btcusdt_agent import BTCUSDTAgent
from backend.agents.ethusdt_agent import ETHUSDTAgent

class MotherAI:
    def __init__(self):
        self.agents = {
            "BTCUSDT": BTCUSDTAgent(),
            "ETHUSDT": ETHUSDTAgent(),
            # Add more agents here as needed
        }

    def decide(self):
        predictions = []

        for symbol, agent in self.agents.items():
            try:
                # Call predict with no arguments; agent fetches data internally
                prediction, confidence = agent.predict()
            except Exception as e:
                print(f"Error predicting for {symbol}: {e}")
                continue

            predictions.append({
                "symbol": symbol,
                "prediction": prediction,
                "confidence": confidence,
            })

        # Filter out agents with no valid predictions
        predictions = [p for p in predictions if p["prediction"] is not None]

        # Capital allocation logic: allocate proportional to confidence for Buy signals only
        buy_signals = [p for p in predictions if str(p["prediction"]).lower() == "buy"]

        if not buy_signals:
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

        # Sort allocations descending by allocation_pct
        allocations.sort(key=lambda x: x["allocation_pct"], reverse=True)

        top_candidate = allocations[0]

        return {
            "decision": "buy",
            "top_candidate": top_candidate["symbol"],
            "allocation_pct": top_candidate["allocation_pct"],
            "confidence": top_candidate["confidence"],
            "allocations": allocations,
        }
