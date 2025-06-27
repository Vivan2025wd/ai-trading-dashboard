Ai trading dashboard
|-venv
|-.vscode
|-backend-|-__pycache_
|                  |-db-|-_init_.py
|                  |        |-mongo.py
|                  |-models-|-init.py
|                  |                  |-trade.py
|                  |                       
|                  |-.env
|                  |-main.py
|                  |-strategy_registry.py 
|
|-backtester-|-data-|-BTCUSDT_15m.csv
|                     |-_pycache_
|                     |    
|                     |-strategies-|-_pycache_
|                     |                    |-ema.py
|                     |                    |-init.py
|                     |                    |-macd.py
|                     |                    |-rsi.py
|                     | -utils-|-_pycache_
|                     |           |-fetch.py
|                     |           |-init.py
|                     |           |-ohlcv_format.py
|                     |           
|                     |-backtest_rsi.py
|                     |config.json
|                     |-fetch_binance_data_py
|                     |-requirement.txt
|                     |-run_backtest.py
|                     |-runner.py  
|
|-data-|- BTCUSDT_15m.csv
|
|-node_modules
|
|-public-|-vite.svg
|
|-server-|-node_modules
|              |-package-lock.json
|              |-package.json
|              |-server.js
|
|
|-src-|-assets-|-react.svg
|        |
|        |-components-|-AISuggestionBox.jsx
|        |                          |-BacktestRunner.jsx
|        |                          |-MarketTable.jsx
|        |                          |-Navbar.jsx
|        |                          |-PriceTicker.jsx
|        |                          |-SymbolPicker.jsx
|        |                          |-TradingViewChart.jsx     
|        |
|        |-pages-|-Dashboard.jsx
|        |
|        |-App.jsx
|        |-index.css
|        |-main.jsx
|
|-gitattributes
|-gitignore
|-index.html
|-package-lock.json
|-package.json
|-postcss.config.js
|-tailwind.config.jsx
|-test_config.json
|-vite.config.js  
