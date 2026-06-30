import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getToken, clearToken } from '@/api/client'

export const useAuthStore = defineStore('auth', () => {
  const isLoggedIn = ref(false)
  const user = ref<{ name: string; email: string } | null>(null)

  // Restore session from localStorage on app boot
  function init() {
    const token = getToken()
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1] ?? ''))
        const now = Math.floor(Date.now() / 1000)
        if (payload.exp && payload.exp > now) {
          isLoggedIn.value = true
          user.value = { name: 'Daniel', email: payload.sub }
        } else {
          clearToken()
        }
      } catch {
        clearToken()
      }
    }
  }

  function login(userData: { name: string; email: string }) {
    isLoggedIn.value = true
    user.value = userData
  }

  function logout() {
    isLoggedIn.value = false
    user.value = null
    clearToken()
  }

  return { isLoggedIn, user, init, login, logout }
})
