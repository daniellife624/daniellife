const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export function getToken(): string | null {
  return localStorage.getItem('dl_token')
}

export function setToken(token: string) {
  localStorage.setItem('dl_token', token)
}

export function clearToken() {
  localStorage.removeItem('dl_token')
}

export async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const token = getToken()
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options?.headers as Record<string, string>),
  }
  if (token) headers['Authorization'] = `Bearer ${token}`

  const res = await fetch(`${BASE_URL}${path}`, { ...options, headers })
  if (!res.ok) throw new Error(`API error ${res.status}: ${path}`)
  return res.json() as Promise<T>
}
