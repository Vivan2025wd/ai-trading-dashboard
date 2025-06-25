import { ComposedChart, XAxis, YAxis, Tooltip, CartesianGrid, Bar, Line } from 'recharts';

// OHLCV and trades are props or state
function PriceChart({ ohlcvData, trades }) {
  // Map trades to markers with colors/icons based on type
  const markers = trades.map(trade => ({
    x: trade.index, 
    y: trade.price, 
    type: trade.type,
  }));

  return (
    <ComposedChart width={800} height={400} data={ohlcvData}>
      <XAxis dataKey="time" />
      <YAxis domain={['auto', 'auto']} />
      <Tooltip />
      <CartesianGrid stroke="#f5f5f5" />
      {/* Candlesticks: Use Bar or customized components */}
      {/* Markers */}
      {markers.map((m, i) => (
        <circle
          key={i}
          cx={m.x}  // calculate pixel position for x from data index/time
          cy={m.y}  // similarly for y
          r={5}
          fill={m.type === 'buy' ? 'green' : 'red'}
        />
      ))}
    </ComposedChart>
  );
}
