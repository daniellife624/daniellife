import { apiFetch, setToken, clearToken } from './client'

interface TokenResponse {
  access_token: string
  name: string
  email: string
}

export async function googleLogin(
  credential: string,
): Promise<{ ok: boolean; name: string; email: string; error?: string }> {
  try {
    const res = await apiFetch<TokenResponse>('/api/auth/google', {
      method: 'POST',
      body: JSON.stringify({ credential }),
    })
    setToken(res.access_token)
    return { ok: true, name: res.name, email: res.email }
  } catch (e) {
    return { ok: false, name: '', email: '', error: e instanceof Error ? e.message : '登入失敗' }
  }
}

export function logout() {
  clearToken()
}
