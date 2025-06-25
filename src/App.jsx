// src/App.jsx
import Navbar from "./components/Navbar.jsx";
import { Routes, Route } from "react-router-dom";
import Dashboard from "./pages/Dashboard.jsx";
import BacktestRunner from "./components/BacktestRunner.jsx";

export default function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Navbar />
      <div className="p-4 max-w-7xl mx-auto">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/backtest" element={<BacktestRunner />} />
        </Routes>
      </div>
    </div>
  );
}
