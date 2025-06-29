import { useEffect, useState, useRef } from "react";

export default function PriceTicker() {
  const [price, setPrice] = useState(null);
  const ws = useRef(null);

  useEffect(() => {
    // Prevent multiple WebSocket instances in React Strict Mode (dev)
    if (ws.current) return;

    ws.current = new WebSocket("wss://stream.binance.com:9443/ws/btcusdt@trade");

    ws.current.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.p) {
        // parseFloat + toFixed returns string, so keep it as string for display
        setPrice(parseFloat(data.p).toFixed(2));
      }
    };

    ws.current.onerror = (err) => {
      console.error("WebSocket error:", err);
    };

    ws.current.onclose = (event) => {
      console.log("WebSocket closed:", event.code, event.reason);
      ws.current = null; // Clear ref on close
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  return (
    <div className="bg-gray-800 p-4 rounded-xl shadow text-center">
      <h2 className="text-lg font-semibold mb-2">BTC/USDT (Live)</h2>
      <p className="text-2xl text-green-400 font-mono">
        {price ? `$${price}` : "Loading..."}
      </p>
    </div>
  );
}
