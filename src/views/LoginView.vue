<template>
  <div class="login">
    <div class="login__card">
      <div class="login__brand">
        <div class="login__logo">D</div>
        <p class="login__brand-name">Daniellife</p>
      </div>

      <h1 class="login__title">管理員登入</h1>

      <form class="login__form" @submit.prevent="submit">
        <label class="login__label">
          Email
          <input
            v-model="email"
            class="login__input"
            type="email"
            placeholder="your@email.com"
            autocomplete="email"
            required
          />
        </label>

        <label class="login__label">
          密碼
          <input
            v-model="password"
            class="login__input"
            type="password"
            placeholder="••••••••"
            autocomplete="current-password"
            required
          />
        </label>

        <p v-if="errorMsg" class="login__error">{{ errorMsg }}</p>

        <button class="login__btn" type="submit" :disabled="loading">
          <span v-if="loading">驗證中…</span>
          <span v-else>登入</span>
        </button>
      </form>

      <p class="login__back">
        <RouterLink to="/" class="login__back-link">← 回到首頁</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { login as apiLogin } from '@/api/auth'

const router = useRouter()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMsg = ref('')

async function submit() {
  errorMsg.value = ''
  loading.value = true
  const result = await apiLogin(email.value, password.value)
  loading.value = false

  if (result.ok) {
    auth.login({ name: result.name, email: result.email })
    router.push('/admin')
  } else {
    errorMsg.value = 'Email 或密碼錯誤，請再試一次'
  }
}
</script>

<style scoped>
.login {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary-bg);
  padding: var(--space-6);
}

.login__card {
  width: 100%;
  max-width: 400px;
  background: var(--color-white);
  border-radius: var(--radius-md);
  border: 1px solid var(--color-primary);
  padding: var(--space-7) var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
  box-shadow: var(--shadow-md);
}

.login__brand {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.login__logo {
  width: 40px;
  height: 40px;
  background: var(--color-primary);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  font-size: 20px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.login__brand-name {
  font-family: var(--font-cjk);
  font-size: 16px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.login__title {
  font-family: var(--font-cjk);
  font-size: 20px;
  font-weight: 700;
  color: var(--color-ink-1);
  margin-top: calc(-1 * var(--space-2));
}

.login__form {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.login__label {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  font-family: var(--font-cjk);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-ink-2);
}

.login__input {
  padding: var(--space-3) var(--space-3);
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm);
  font-family: var(--font-body);
  font-size: 14px;
  color: var(--color-ink-1);
  outline: none;
  transition: border-color 0.2s;
}

.login__input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(232, 193, 58, 0.15);
}

.login__error {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: #dc2626;
  text-align: center;
}

.login__btn {
  width: 100%;
  padding: var(--space-3) 0;
  background: var(--color-primary);
  color: var(--color-ink-1);
  border: none;
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 15px;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.2s;
  margin-top: var(--space-2);
}

.login__btn:hover:not(:disabled) { opacity: 0.85; }
.login__btn:disabled { opacity: 0.5; cursor: not-allowed; }

.login__back {
  text-align: center;
}

.login__back-link {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-3);
  transition: color 0.2s;
}

.login__back-link:hover { color: var(--color-ink-1); }
</style>
