// src/components/Navbar.jsx
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-gray-800 p-4 flex justify-between items-center">
      <h1 className="text-xl font-bold">🧠 AI Trader</h1>
      <div className="space-x-4 text-sm">
        <Link to="/" className="hover:underline">Dashboard</Link>
        <Link to="/backtest" className="hover:underline">Backtest</Link>
      </div>
    </nav>
  );
}
