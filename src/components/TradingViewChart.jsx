import { useEffect, useRef } from "react"

export default function TradingViewChart() {
  const containerRef = useRef(null)

  useEffect(() => {
    if (!window.TradingView) return

    new window.TradingView.widget({
      autosize: true,
      symbol: "BINANCE:BTCUSDT",
      interval: "1",
      timezone: "Etc/UTC",
      theme: "dark",
      style: "1",
      locale: "en",
      toolbar_bg: "#1e293b",
      enable_publishing: false,
      allow_symbol_change: true,
      container_id: containerRef.current.id
    })
  }, [])

  return (
    <div className="h-[500px] rounded-xl overflow-hidden" id="tv-container" ref={containerRef}></div>
  )
}
