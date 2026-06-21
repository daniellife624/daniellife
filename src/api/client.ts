const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export function mediaUrl(path: string): string {
  if (!path) return ''
  return path.startsWith('http') ? path : `${BASE_URL}${path}`
}

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
  if (!res.ok) {
    let msg = `API error ${res.status}`
    try {
      const body = await res.json()
      const detail = body?.detail
      if (typeof detail === 'string') {
        msg = detail
      } else if (Array.isArray(detail) && detail.length > 0) {
        msg = detail.map((e: { msg?: string }) => e.msg?.replace(/^Value error, /, '') ?? '').filter(Boolean).join('；')
      }
    } catch { /* ignore parse errors */ }
    throw new Error(msg)
  }
  return res.json() as Promise<T>
}
