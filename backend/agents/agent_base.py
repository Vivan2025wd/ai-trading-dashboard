### backend/agents/agent_base.py

from abc import ABC, abstractmethod

class TradingAgent(ABC):
    @abstractmethod
    def train(self, data):
        pass

    @abstractmethod
    def predict(self, market_data):
        pass

    @abstractmethod
    def evaluate(self):
        pass