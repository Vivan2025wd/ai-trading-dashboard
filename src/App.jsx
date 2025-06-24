import Navbar from "./components/Navbar.jsx"
import Dashboard from "./pages/Dashboard.jsx"

export default function App() {
  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <Navbar />
      <Dashboard />
    </div>
  )
}
