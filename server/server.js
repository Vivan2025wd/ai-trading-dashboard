import express from "express"
import cors from "cors"
import axios from "axios"
import { RSI, MACD, EMA, BollingerBands } from "technicalindicators"

const app = express()
app.use(cors())

app.get("/api/suggestions", async (req, res) => {
  try {
    const symbol = req.query.symbol || "BTCUSDT"
    const { data } = await axios.get("https://api.binance.com/api/v3/klines", {
      params: { symbol, interval: "15m", limit: 100 }
    })

    const closes = data.map(k => parseFloat(k[4]))
    const highs = data.map(k => parseFloat(k[2]))
    const lows = data.map(k => parseFloat(k[3]))

    const rsi = RSI.calculate({ period: 14, values: closes })
    const macd = MACD.calculate({
      values: closes,
      fastPeriod: 12,
      slowPeriod: 26,
      signalPeriod: 9,
      SimpleMAOscillator: false,
      SimpleMASignal: false
    })
    const ema = EMA.calculate({ period: 14, values: closes })
    const bb = BollingerBands.calculate({
      period: 20,
      values: closes,
      stdDev: 2
    })

    const latest = {
      rsi: rsi[rsi.length - 1]?.toFixed(2),
      macd: macd[macd.length - 1] || null,
      ema: ema[ema.length - 1]?.toFixed(2),
      bb: bb[bb.length - 1] || null,
      close: closes[closes.length - 1]
    }

    // Basic suggestion logic example
    let suggestion = "Hold"
    if (latest.rsi < 30) suggestion = "Buy (RSI Oversold)"
    else if (latest.rsi > 70) suggestion = "Sell (RSI Overbought)"
    else if (latest.macd?.MACD > latest.macd?.signal) suggestion = "Buy (MACD crossover)"
    else if (latest.macd?.MACD < latest.macd?.signal) suggestion = "Sell (MACD crossover)"

    res.json({ latest, suggestion, symbol })
  } catch (err) {
    res.status(500).json({ error: "Suggestion engine failed", details: err.message })
  }
})

app.listen(5000, () => console.log("✅ Suggestion server running on http://localhost:5000"))
