import React from "react"

export default function SymbolPicker({ symbols, selected, onChange }) {
  return (
    <select
      value={selected}
      onChange={e => onChange(e.target.value)}
      className="p-2 rounded border bg-gray-900 text-white"
    >
      {symbols.map(sym => (
        <option key={sym} value={sym}>
          {sym}
        </option>
      ))}
    </select>
  )
}
