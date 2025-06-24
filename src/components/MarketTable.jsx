import { useEffect, useState } from "react"

export default function MarketTable() {
  const [topPairs, setTopPairs] = useState([])

  useEffect(() => {
    fetch("https://api.binance.com/api/v3/ticker/24hr")
      .then(res => res.json())
      .then(data => {
        const usdtPairs = data
          .filter(item => item.symbol.endsWith("USDT") && !item.symbol.includes("UP") && !item.symbol.includes("DOWN"))
          .sort((a, b) => b.quoteVolume - a.quoteVolume)
          .slice(0, 10)
        setTopPairs(usdtPairs)
      })
  }, [])

  return (
    <div className="bg-gray-800 p-4 rounded-xl shadow">
      <h2 className="text-lg font-semibold mb-4">🔥 Top 10 USDT Pairs</h2>
      <table className="w-full text-sm">
        <thead>
          <tr className="text-gray-400 border-b border-gray-700">
            <th className="text-left py-1">Pair</th>
            <th className="text-right py-1">Price</th>
            <th className="text-right py-1">% Change</th>
            <th className="text-right py-1">Volume</th>
          </tr>
        </thead>
        <tbody>
          {topPairs.map((pair) => (
            <tr key={pair.symbol} className="border-b border-gray-700">
              <td>{pair.symbol}</td>
              <td className="text-right">${parseFloat(pair.lastPrice).toFixed(2)}</td>
              <td className={`text-right ${parseFloat(pair.priceChangePercent) > 0 ? "text-green-400" : "text-red-400"}`}>
                {parseFloat(pair.priceChangePercent).toFixed(2)}%
              </td>
              <td className="text-right">{parseFloat(pair.quoteVolume).toFixed(0)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
