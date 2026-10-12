Here is the corrected and properly formatted `README.md` file. You can copy the content below and save it as `README.md` in your project root.

```markdown
# 🧠 AI Trading Dashboard

A full-stack AI-powered trading platform that combines real-time market data, technical analysis, strategy backtesting, and AI-driven trade suggestions.

---

## 📋 Table of Contents

- Overview
- Features
- Architecture
- Tech Stack
- Project Structure
- Installation
- Configuration
- Running the Application
- API Endpoints
- Components
- Backtesting Strategies
- Data Pipeline
- Database Setup
- Development Workflow
- Troubleshooting
- Scripts Reference
- Contributing
- License
- Resources
- Authors

---

## 🎯 Overview

The AI Trading Dashboard is a comprehensive trading platform that provides:

- Real-time price tracking via Binance WebSocket
- AI-generated trade suggestions based on technical indicators (RSI, MACD, EMA, Bollinger Bands)
- Strategy backtesting with historical OHLCV data
- Interactive charts powered by TradingView and Recharts
- Market analysis with top USDT trading pairs

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📈 Live Price Ticker | Real-time BTC/USDT price via WebSocket |
| 🧠 AI Suggestions | Buy/Sell/Hold signals based on technical indicators |
| 📊 Backtesting Engine | Test RSI, MACD, and EMA strategies on historical data |
| 📉 Interactive Charts | TradingView widgets + custom Recharts visualizations |
| 💹 Market Table | Top 10 USDT pairs ranked by 24h volume |
| 🔄 Multi-Symbol Support | BTCUSDT, ETHUSDT, BNBUSDT, ADAUSDT |

---

## 🏗 Architecture

```text
┌─────────────────────────────────────────────────────────────────┐
│                         Frontend (React + Vite)                  │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌───────────┐  │
│  │ PriceTicker │ │AISuggestion │ │BacktestRun  │ │MarketTable│  │
│  │ (WebSocket) │ │    Box      │ │    ner      │ │           │  │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └─────┬─────┘  │
└─────────┼───────────────┼───────────────┼──────────────┼────────┘
          │               │               │              │
          ▼               ▼               ▼              ▼
    ┌──────────┐   ┌─────────────┐  ┌───────────┐  ┌───────────┐
    │ Binance  │   │  Express    │  │  FastAPI  │  │  Binance  │
    │WebSocket │   │  Server     │  │  Backend  │  │  REST API │
    │          │   │ (Port 5000) │  │(Port 8000)│  │           │
    └──────────┘   └──────┬──────┘  └─────┬─────┘  └───────────┘
                          │               │
                          ▼               ▼
                   ┌─────────────┐  ┌───────────┐
                   │ Technical   │  │ Backtester│
                   │ Indicators  │  │  Engine   │
                   └─────────────┘  └─────┬─────┘
                                          │
                                          ▼
                                    ┌───────────┐
                                    │  MongoDB  │
                                    └───────────┘
```

---

## 🛠 Tech Stack

### Frontend

| Technology | Version | Purpose |
|------------|---------|---------|
| React | ^19.1.0 | UI framework |
| Vite | ^7.0.0 | Build tool & dev server |
| TailwindCSS | ^3.4.17 | Utility-first CSS |
| React Router | ^7.6.2 | Client-side routing |
| Recharts | ^3.0.0 | Chart visualization |
| Lightweight Charts | ^5.0.7 | TradingView-like charts |
| date-fns | ^4.1.0 | Date formatting |

### Backend (FastAPI)

| Technology | Purpose |
|------------|---------|
| FastAPI | REST API framework |
| Uvicorn | ASGI server |
| Pandas | Data manipulation |
| PyMongo | MongoDB driver |
| python-dotenv | Environment variables |

### Backend (Express)

| Technology | Purpose |
|------------|---------|
| Express | Suggestion engine API |
| Axios | HTTP client |
| technicalindicators | Technical analysis |
| CORS | Cross-origin support |

---

## 📁 Project Structure

```text
ai-trading-dashboard/
├── backend/                      # FastAPI Backend
│   ├── db/
│   │   ├── __init__.py
│   │   └── mongo.py              # MongoDB connection
│   ├── models/
│   │   ├── __init__.py
│   │   └── trade.py              # Trade data model
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── agent_base.py
│   │   ├── btcusdt_agent.py
│   │   └── ethusdt_agent.py
│   ├── ml_engine/
│   │   ├── __init__.py
│   │   ├── feature_extractor.py
│   │   └── module_utils.py
│   ├── mother_ai/
│   │   ├── __init__.py
│   │   ├── coordinator.py
│   │   └── performance_tracker.py
│   ├── .env                      # Environment variables
│   ├── main.py                   # FastAPI app entry
│   └── strategy_registry.py      # Dynamic strategy loader
│
├── backtester/                   # Backtesting Engine
│   ├── data/
│   │   └── BTCUSDT_15m.csv       # Cached OHLCV data
│   ├── strategies/
│   │   ├── __init__.py
│   │   ├── ema.py                # EMA strategy
│   │   ├── macd.py               # MACD strategy
│   │   └── rsi.py                # RSI strategy
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── fetch.py              # Binance data fetcher
│   │   └── ohlcv_format.py       # DataFrame to JSON converter
│   ├── backtest_rsi.py           # Standalone RSI backtest
│   ├── config.json               # Sample config
│   ├── fetch_binance_data.py     # CLI data fetcher
│   ├── requirements.txt
│   ├── run_backtest.py           # Main backtest runner
│   └── runner.py                 # Subprocess runner
│
├── server/                       # Express Suggestion Engine
│   ├── node_modules/
│   ├── package.json
│   ├── package-lock.json
│   └── server.js                 # Express server
│
├── src/                          # React Frontend
│   ├── assets/
│   │   └── react.svg
│   ├── components/
│   │   ├── AISuggestionBox.jsx   # AI trade suggestions
│   │   ├── BacktestRunner.jsx    # Backtest UI
│   │   ├── MarketTable.jsx       # Top pairs table
│   │   ├── Navbar.jsx            # Navigation
│   │   ├── PriceTicker.jsx       # Live price
│   │   ├── SymbolPicker.jsx      # Symbol dropdown
│   │   ├── TradingViewChart.jsx  # TradingView widget
│   │   ├── MotherAIdecisionBox.jsx
│   │   └── symbolAgentCard.jsx
│   ├── pages/
│   │   └── Dashboard.jsx         # Main dashboard
│   ├── App.jsx                   # Routes & layout
│   ├── index.css                 # Tailwind imports
│   └── main.jsx                  # React entry point
│
├── public/
│   └── vite.svg
│
├── data/
│   └── BTCUSDT_15m.csv           # Cached market data
│
├── .env                          # Root environment variables
├── .gitattributes
├── .gitignore
├── index.html                    # HTML template
├── package.json                  # Frontend dependencies
├── package-lock.json
├── postcss.config.js             # PostCSS config
├── tailwind.config.jsx           # Tailwind config
├── test_config.json              # Test backtest config
└── vite.config.js                # Vite config
```

---

## 🚀 Installation

### Prerequisites

- Node.js (v18 or higher)
- Python (v3.9 or higher)
- MongoDB (local or Atlas cloud)
- npm or yarn

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd ai-trading-dashboard
```

### Step 2: Install Frontend Dependencies

```bash
npm install
```

### Step 3: Install Backend Dependencies (FastAPI)

```bash
cd backend
pip install -r requirements.txt
# Or manually:
pip install fastapi uvicorn pymongo python-dotenv pandas
```

### Step 4: Install Suggestion Engine Dependencies (Express)

```bash
cd server
npm install
```

### Step 5: Install Backtester Dependencies

```bash
cd backtester
pip install -r requirements.txt
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# MongoDB Configuration
MONGODB_URI=mongodb+srv://username:password@cluster0.mongodb.net
DB_NAME=ai_trading_dashboard
```

### Tailwind Configuration

`tailwind.config.js`:

```javascript
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: { extend: {} },
  plugins: []
}
```

### Vite Configuration

`vite.config.js`:

```javascript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
```

---

## 🏃 Running the Application

### Start All Services

You need to run **three separate services**:

#### 1. FastAPI Backend (Port 8000)

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

#### 2. Express Suggestion Engine (Port 5000)

```bash
cd server
npm start
# Or: node server.js
```

#### 3. React Frontend (Port 5173)

```bash
npm run dev
```

### Access the Application

Open your browser and navigate to:

```text
http://localhost:5173
```

---

## 📡 API Endpoints

### FastAPI Backend (Port 8000)

#### `POST /backtest`

Run a strategy backtest.

**Request Body:**

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

**Response:**

```json
{
  "trades": [
    {"type": "buy", "price": 29105.12, "index": 25},
    {"type": "sell", "price": 29188.44, "index": 36, "profit": 83.32}
  ],
  "ohlcv": [],
  "message": "✅ Backtest complete"
}
```

#### `GET /backtester/strategies?symbol=BTCUSDT`

Get AI trading suggestions.

**Response:**

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

### Express Suggestion Engine (Port 5000)

#### `GET /api/suggestions?symbol=BTCUSDT`

Get real-time trading suggestions.

---

## 🧩 Components

### Frontend Components

| Component | File | Description |
|-----------|------|-------------|
| Navbar | `Navbar.jsx` | Top navigation with routes |
| PriceTicker | `PriceTicker.jsx` | Live BTC/USDT price via WebSocket |
| AISuggestionBox | `AISuggestionBox.jsx` | AI trade signals with indicators |
| BacktestRunner | `BacktestRunner.jsx` | Run and visualize backtests |
| MarketTable | `MarketTable.jsx` | Top 10 USDT pairs by volume |
| SymbolPicker | `SymbolPicker.jsx` | Reusable symbol dropdown |
| TradingViewChart | `TradingViewChart.jsx` | Embedded TradingView widget |

### Data Sources

| Component | Data Source |
|-----------|-------------|
| PriceTicker | `wss://stream.binance.com:9443/ws/btcusdt@trade` |
| AISuggestionBox | `http://localhost:5000/api/suggestions` |
| BacktestRunner | `http://127.0.0.1:8000/backtest` |
| TradingViewChart | TradingView Widget |
| MarketTable | `https://api.binance.com/api/v3/ticker/24hr` |

---

## 📊 Backtesting Strategies

### RSI Strategy

**File:** `backtester/strategies/rsi.py`

**Logic:**

- Buy when RSI < 30 (oversold)
- Sell when RSI > 70 (overbought)

```python
def backtest_rsi_strategy(df, rsi_buy=30, rsi_sell=70):
    # Compute RSI
    # Buy on oversold, Sell on overbought
    # Return list of trades
```

### MACD Strategy

**File:** `backtester/strategies/macd.py`

**Logic:**

- Buy when MACD crosses above Signal Line (bullish crossover)
- Sell when MACD crosses below Signal Line (bearish crossover)

```python
def backtest_macd_strategy(df, fast=12, slow=26, signal=9):
    # Calculate MACD and Signal Line
    # Detect crossovers
    # Return list of trades
```

### EMA Strategy

**File:** `backtester/strategies/ema.py`

**Logic:**

- Buy when short EMA crosses above long EMA
- Sell when short EMA crosses below long EMA

```python
def backtest_ema_strategy(df, short_period=12, long_period=26):
    # Calculate EMAs
    # Detect crossovers
    # Return list of trades
```

### Strategy Registry

**File:** `backend/strategy_registry.py`

Dynamically loads strategies by name:

```python
STRATEGY_MODULES = {
    "ema": "backtester.strategies.ema",
    "macd": "backtester.strategies.macd",
    "rsi": "backtester.strategies.rsi",
    "rsi_v1": "backtester.strategies.rsi",
}

def load_strategy(strategy_name):
    module_path = STRATEGY_MODULES.get(strategy_name.lower())
    module = importlib.import_module(module_path)
    # Returns the strategy function
```

---

## 📥 Data Pipeline

### Fetching OHLCV Data

**File:** `backtester/utils/fetch.py`

```python
def fetch_ohlcv_data(symbol, interval="15m", limit=500):
    # Fetches from Binance API
    # Returns pandas DataFrame with columns:
    # Timestamp, Open, High, Low, Close, Volume
```

### CLI Data Fetcher

**File:** `backtester/fetch_binance_data.py`

```bash
python fetch_binance_data.py BTCUSDT 15m 1000
```

This saves data to `data/BTCUSDT_15m.csv`.

### OHLCV Formatting

**File:** `backtester/utils/ohlcv_format.py`

Converts DataFrame to JSON-serializable format for frontend:

```python
def df_to_ohlcv(df):
    # Returns list of dicts:
    # [{"time": 1719426000, "open": 29250.0, "high": 29300.0, ...}]
```

---

## 🗄 Database Setup

### MongoDB Configuration

**File:** `backend/db/mongo.py`

```python
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

# Collections
failed_trades = db["failed_trades"]
backtests = db["backtests"]
```

### Trade Model

**File:** `backend/models/trade.py`

```python
def trade_to_dict(trade):
    return {
        "symbol": trade.get("symbol"),
        "strategy": trade.get("strategy"),
        "price": trade.get("price"),
        "index": trade.get("index"),
        "profit": trade.get("profit", 0),
        "timestamp": trade.get("timestamp")
    }
```

---

## 🔄 Development Workflow

1. **Start MongoDB** – Ensure MongoDB is running (local or Atlas).
2. **Start FastAPI Backend**

   ```bash
   python -m uvicorn backend.main:app --reload --port 8000
   ```

3. **Start Express Suggestion Engine**

   ```bash
   cd server
   npm start
   ```

4. **Start React Frontend**

   ```bash
   npm run dev
   ```

5. **Access Dashboard** – Open `http://localhost:5173` in your browser.

---

## 🧪 Testing

### Run Frontend Linter

```bash
npm run lint
```

### Build for Production

```bash
npm run build
npm run preview
```

### Test Backtest Manually

```bash
cd backtester
python run_backtest.py config.json
```

---

## 🐛 Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| CORS errors | Ensure both frontend ports (5173, 5174) are allowed in FastAPI CORS config |
| MongoDB connection failed | Check `.env` file has correct `MONGODB_URI` and `DB_NAME` |
| Binance API rate limit | Reduce request frequency or cache data locally |
| WebSocket disconnects | Check internet connection; Binance WebSocket may have downtime |
| Backtest timeout | Increase timeout value in `main.py` subprocess call |

### Port Conflicts

If ports are in use:

- **FastAPI:** Change `--port 8000` to another port
- **Express:** Change `app.listen(5000)` in `server.js`
- **Vite:** Vite will auto-select next available port

---

## 📝 Scripts Reference

### Frontend (`package.json`)

| Command | Description |
|---------|-------------|
| `npm run dev` | Start dev server on localhost:5173 |
| `npm run build` | Create production build |
| `npm run preview` | Preview production build |
| `npm run lint` | Run ESLint |

### Backend Commands

| Command | Description |
|---------|-------------|
| `python -m uvicorn backend.main:app --reload --port 8000` | Start FastAPI |
| `cd server && npm start` | Start Express suggestion engine |
| `python backtester/run_backtest.py config.json` | Run backtest manually |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the ISC License.

---

## 🔗 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [TailwindCSS Documentation](https://tailwindcss.com/docs)
- [Binance API Documentation](https://binance-docs.github.io/apidocs/)
- [TradingView Widget Documentation](https://www.tradingview.com/widget/)
- [Recharts Documentation](https://recharts.org/)

---

## 👥 Authors

- AI Trading Dashboard Team

---

> ⚠️ **Disclaimer:** This software is for educational purposes only. Trading cryptocurrencies involves significant risk. Always do your own research before making investment decisions.
```