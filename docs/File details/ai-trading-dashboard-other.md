# ⚙️ Frontend Configuration Guide – AI Trading Dashboard

This markdown explains all config files in your frontend project. These files together define how your React app builds, styles, lints, and runs in development.

---

## 📦 1. `package.json` – Project Metadata & Scripts

### 🔍 What It Does

Defines:
- The app name & version
- Dependencies (what your project needs to run)
- Dev dependencies (tools used during development)
- Useful commands (`npm run dev`, `npm run build`, etc.)

### 📄 Breakdown

```json
{
  "name": "ai-trading-dashboard",
  "type": "module",
  "scripts": {
    "dev": "vite",             // Starts development server
    "build": "vite build",     // Bundles app for production
    "preview": "vite preview", // Previews production build locally
    "lint": "eslint ."         // Runs ESLint for code checking
  },
  "dependencies": {
    "react": "^19.1.0",        // React core library
    "react-dom": "^19.1.0",    // DOM renderer for React
    "react-router-dom": "^7.6.2", // Routing system
    "recharts": "^3.0.0",      // Chart library used in backtest visuals
    "technicalindicators": "^3.1.0", // Technical analysis indicators (RSI, MACD, etc.)
    "date-fns": "^4.1.0",      // Utility library for formatting dates
    "lightweight-charts": "^5.0.7" // Optional: for TradingView-like charts
  },
  "devDependencies": {
    "vite": "^7.0.0",          // Build tool
    "eslint": "^9.29.0",       // JS/React code linter
    "tailwindcss": "^3.4.17",  // Utility-first CSS framework
    "prettier": "^3.6.0",      // Code formatter
    "autoprefixer": "^10.4.21",// Adds browser-specific prefixes
    "@vitejs/plugin-react": "^4.5.2" // React plugin for Vite
  }
}
🧪 How to Use
Command	Description
npm install	Installs all dependencies
npm run dev	Starts dev server on localhost:5173
npm run build	Creates production build
npm run preview	Serves the build (like in real deployment)
npm run lint	Checks code quality

🎨 2. tailwind.config.js – TailwindCSS Setup
js
Copy code
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: { extend: {} },
  plugins: []
}
🔍 What It Does
Tells Tailwind which files to scan for class names (HTML/JSX)

Enables customization via theme.extend

You can add Tailwind plugins here (e.g., @tailwindcss/forms)

🔁 3. postcss.config.js – PostCSS Processing
js
Copy code
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
🔍 What It Does
tailwindcss: Loads Tailwind utilities

autoprefixer: Adds vendor prefixes for cross-browser support

PostCSS is the system that compiles @tailwind directives from index.css into real CSS.

⚡ 4. vite.config.js – Vite Configuration
js
Copy code
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
🔍 What It Does
Vite is your frontend dev/build tool (faster than Webpack)

@vitejs/plugin-react adds React Fast Refresh, JSX support, etc.

✅ With this setup, your React app starts instantly, supports hot-reloading, and builds quickly.

🧪 5. test.config.json – Sample Backtest Config
json
Copy code
{
  "symbol": "BTCUSDT",
  "strategy": "rsi",
  "interval": "15m",
  "params": {}
}
🔍 What It Does
Represents a backtest job you send to the FastAPI backend

Used by BacktestRunner.jsx when you click "Run Backtest"

Field	Purpose
symbol	Which market pair to simulate
strategy	Which trading logic to use (rsi, macd)
interval	Candle timeframe (e.g. 15m, 1h)
params	Optional: pass strategy-specific inputs

This JSON config is sent via fetch() to:

bash
Copy code
POST http://localhost:8000/backtest
🌐 File & Tool Summary
Tool	Role
React	Component-based UI system
Vite	Fast dev server & bundler
TailwindCSS	Utility-based CSS styling
Recharts	Visualize backtest trades as charts
TechnicalIndicators	Calculate RSI, MACD, EMA for analysis
React Router	Handles page routing (e.g. /, /backtest)
ESLint	Lints code for errors and consistency
Prettier	Auto-formats your JS and CSS

🛠️ Dev Workflow
Start your backend (FastAPI + Mongo)

Start suggestion engine (Express server on port 5000)

Run the frontend:

bash
Copy code
npm install       # First time setup
npm run dev       # Start Vite dev server on localhost:5173
🧠 Tips for Beginners
Want to test a different strategy? Change strategy in test.config.json

Want to add new pages? Add a new React component and a <Route />

Want to style anything? Use Tailwind utility classes in JSX (p-4, bg-gray-800, etc.)

