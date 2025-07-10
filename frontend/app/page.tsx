'use client'

import { useState } from 'react'

type Product = {
  id: number
  name: string
  category: string
  price: number
  rating: number
}

export default function Page() {
  const [budget, setBudget] = useState<number>(0)
  const [products, setProducts] = useState<Product[]>([])
  const [error, setError] = useState<string | null>(null)

  const fetchProducts = async () => {
    try {
      setError(null)
      const res = await fetch(`http://localhost:8000/team-builder?budget=${budget}`)
      if (!res.ok) {
        const data = await res.json()
        throw new Error(data.detail || 'Request failed')
      }
      const data = await res.json()
      setProducts(data.products)
    } catch (err: any) {
      setProducts([])
      setError(err.message)
    }
  }

  return (
    <div style={{ padding: 24 }}>
      <h1>Fantasy Store Team Builder</h1>

      <input
        type="number"
        placeholder="Enter budget"
        value={budget}
        onChange={(e) => setBudget(Number(e.target.value))}
        style={{ marginRight: 12 }}
      />
      <button onClick={fetchProducts}>Build Team</button>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {products.length > 0 && (
        <table style={{ marginTop: 24, borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th>Name</th>
              <th>Category</th>
              <th>Price</th>
              <th>Rating</th>
            </tr>
          </thead>
          <tbody>
            {products.map((p) => (
              <tr key={p.id}>
                <td>{p.name}</td>
                <td>{p.category}</td>
                <td>{p.price}</td>
                <td>{p.rating}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
