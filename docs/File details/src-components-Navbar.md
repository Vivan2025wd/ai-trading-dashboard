## Overview

The `Navbar` component provides the top navigation bar for your AI Trading Dashboard application. It includes branding and navigation links to different routes like the **Dashboard** and **Backtest** pages.

This component is built using **React** and **React Router DOM**, and styled with **TailwindCSS** for a clean, responsive layout.

---

## What Does It Do?

✅ Displays your app name: **🧠 AI Trader**  
✅ Renders navigation links to internal pages:  
&nbsp;&nbsp;&nbsp;&nbsp;🔹 `/` → Dashboard  
&nbsp;&nbsp;&nbsp;&nbsp;🔹 `/backtest` → Backtest  
✅ Uses React Router for seamless in-app navigation (no page reloads)  
✅ Uses TailwindCSS to style the navigation bar and hover effects

---

## Where Does the Logic Come From?

### 1. React Router DOM

```js
import { Link } from "react-router-dom";
Link is a component provided by React Router DOM.

It works like an <a> tag but without reloading the page.

It allows for fast, client-side routing between pages/components.

Component Breakdown
jsx
Copy code
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
1. <nav> Container
html
Copy code
<nav className="bg-gray-800 p-4 flex justify-between items-center">
bg-gray-800: Sets the background color to dark gray

p-4: Adds padding on all sides

flex justify-between items-center: Uses Flexbox to space elements (logo left, links right) and align them vertically

2. App Title
jsx
Copy code
<h1 className="text-xl font-bold">🧠 AI Trader</h1>
Large, bold title for your app with an emoji for personality

3. Navigation Links
jsx
Copy code
<div className="space-x-4 text-sm">
  <Link to="/" className="hover:underline">Dashboard</Link>
  <Link to="/backtest" className="hover:underline">Backtest</Link>
</div>
space-x-4: Adds horizontal space between the links

text-sm: Makes the text slightly smaller

hover:underline: Adds an underline when you hover over each link

to="/": Navigates to the homepage (Dashboard)

to="/backtest": Navigates to the backtest view

Summary
Feature	Description
App Branding	Displays title “🧠 AI Trader”
Routing	Uses Link from react-router-dom
Links	/ for Dashboard, /backtest for Backtest
Styling	Dark background, flex layout, hover effect

Prerequisites
Make sure you have react-router-dom installed and properly configured in your app:

bash
Copy code
npm install react-router-dom
And in your App.jsx or equivalent:

jsx
Copy code
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/backtest" element={<Backtest />} />
      </Routes>
    </BrowserRouter>
  );
}
Next Steps
Add more links like “AI Suggestions”, “Trade History”, or “Settings”

Make the navbar responsive for mobile using Tailwind’s responsive classes

Highlight the active route using NavLink from react-router-dom