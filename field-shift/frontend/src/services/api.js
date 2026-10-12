const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  })

  if (!response.ok) {
    const detail = await response.json().catch(() => null)
    throw new Error(detail?.detail?.[0]?.msg || detail?.detail || `API request failed (${response.status})`)
  }
  return response.json()
}

export const checkHealth = () => request('/health')

export async function analyzeFarm(farm) {
  const options = { method: 'POST', body: JSON.stringify(farm) }
  const [analysis, rotation] = await Promise.all([
    request('/farm/analyze', options),
    request('/rotation/suggest', options),
  ])
  return { analysis, rotation }
}

