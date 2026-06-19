// TODO: replace with real JWT auth — POST /api/auth/login → { token }
// Set VITE_ADMIN_EMAIL and VITE_ADMIN_PASSWORD in .env.local (not committed)
const ADMIN_EMAIL    = import.meta.env.VITE_ADMIN_EMAIL    ?? 'admin@daniellife.com'
const ADMIN_PASSWORD = import.meta.env.VITE_ADMIN_PASSWORD ?? 'changeme'

export async function mockLogin(
  email: string,
  password: string,
): Promise<{ ok: boolean; name: string; email: string }> {
  if (email === ADMIN_EMAIL && password === ADMIN_PASSWORD) {
    return { ok: true, name: '丹尼', email }
  }
  return { ok: false, name: '', email: '' }
}
