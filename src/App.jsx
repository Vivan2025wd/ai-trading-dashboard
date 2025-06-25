import Navbar from "./components/Navbar.jsx"
import Dashboard from "./pages/Dashboard.jsx"
import BacktestRunner from "./components/BacktestRunner";
export default function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Navbar />
      <Dashboard />
      <h1 className="text-2xl font-bold mb-6">AI Trading Dashboard</h1>
      <BacktestRunner />
    </div>
  )
}

