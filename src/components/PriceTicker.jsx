import { useEffect, useState } from "react"

export default function PriceTicker() {
  const [price, setPrice] = useState(null)

  useEffect(() => {
    const ws = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@trade")

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setPrice(parseFloat(data.p).toFixed(2))
    }

    return () => ws.close()
  }, [])

  return (
    <div className="bg-gray-800 p-4 rounded-xl shadow text-center">
      <h2 className="text-lg font-semibold mb-2">BTC/USDT (Live)</h2>
      <p className="text-2xl text-green-400 font-mono">
        {price ? `$${price}` : "Loading..."}
      </p>
    </div>
  )
}

