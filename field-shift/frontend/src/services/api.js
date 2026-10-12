const LOCAL_API_URL = 'http://localhost:8000/api'
const configuredApiUrl = import.meta.env.VITE_API_URL?.trim()

if (import.meta.env.PROD && !configuredApiUrl) {
  throw new Error('Missing VITE_API_URL for production build/runtime. Set VITE_API_URL to your deployed FastAPI /api base URL.')
}

const API_URL = configuredApiUrl || LOCAL_API_URL

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
