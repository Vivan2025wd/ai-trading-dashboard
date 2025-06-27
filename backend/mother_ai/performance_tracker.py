# backend/mother_ai/performance_tracker.py

"""
Track agent performance metrics over time.
Store historical PnL, Sharpe ratios, accuracy, drawdowns.
This is a stub; extend with DB integration or file logging.
"""

from collections import defaultdict
import datetime

class PerformanceTracker:
    def __init__(self):
        # Example structure: {agent_name: [(date, pnl, sharpe, accuracy), ...]}
        self.performance_history = defaultdict(list)

    def log_performance(self, agent_name: str, pnl: float, sharpe: float, accuracy: float):
        entry = (datetime.datetime.utcnow(), pnl, sharpe, accuracy)
        self.performance_history[agent_name].append(entry)

    def get_latest(self, agent_name: str):
        if agent_name in self.performance_history and self.performance_history[agent_name]:
            return self.performance_history[agent_name][-1]
        return None

    def get_all_performance(self, agent_name: str):
        return self.performance_history.get(agent_name, [])
