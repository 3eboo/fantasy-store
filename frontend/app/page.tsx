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
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [sortBy, setSortBy] = useState<'rating' | 'price' | ''>('')

  const apiBase = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000'

  const fetchProducts = async () => {
    if (!budget || budget <= 0) {
      setError("Please enter a valid budget greater than 0.")
      return
    }

    try {
      setError(null)
      setIsLoading(true)
      const res = await fetch(`${apiBase}/team-builder?budget=${budget}`)
      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.detail || "Something went wrong")
      }
      setProducts(data.products)
    } catch (err: any) {
      setProducts([])
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  const sortedProducts = [...products].sort((a, b) => {
    if (sortBy === 'price') return a.price - b.price
    if (sortBy === 'rating') return b.rating - a.rating
    return 0
  })

  return (
    <div style={{ padding: 24 }}>
      <h1>Fantasy Store Team Builder</h1>

      <input
        type="number"
        value={budget}
        onChange={(e) => setBudget(Number(e.target.value))}
        placeholder="Enter budget"
        style={{ marginRight: 12 }}
      />
      <button onClick={fetchProducts}>Build Team</button>

      {isLoading && <p>Loading team...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {products.length > 0 && (
        <>
          <label style={{ marginTop: 16 }}>
            Sort by:&nbsp;
            <select value={sortBy} onChange={(e) => setSortBy(e.target.value as 'rating' | 'price')}>
              <option value="">None</option>
              <option value="rating">Rating</option>
              <option value="price">Price</option>
            </select>
          </label>

          <table style={{ marginTop: 16, borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th>Name</th>
                <th>Category</th>
                <th>Price</th>
                <th>Rating</th>
              </tr>
            </thead>
            <tbody>
              {sortedProducts.map(p => (
                <tr key={p.id}>
                  <td>{p.name}</td>
                  <td>{p.category}</td>
                  <td>{p.price}</td>
                  <td>{p.rating}</td>
                </tr>
              ))}
            </tbody>
          </table>

          <p style={{ marginTop: 12, fontWeight: 'bold' }}>
            Total Cost: ${products.reduce((sum, p) => sum + p.price, 0).toFixed(2)}
          </p>
        </>
      )}
    </div>
  )
}
