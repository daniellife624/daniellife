import { apiFetch, setToken, clearToken } from './client'

interface LoginResponse {
  access_token: string
  token_type: string
  name: string
  email: string
}

export async function login(
  email: string,
  password: string,
): Promise<{ ok: boolean; name: string; email: string }> {
  try {
    const res = await apiFetch<LoginResponse>('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    })
    setToken(res.access_token)
    return { ok: true, name: res.name, email: res.email }
  } catch {
    return { ok: false, name: '', email: '' }
  }
}

export function logout() {
  clearToken()
}
