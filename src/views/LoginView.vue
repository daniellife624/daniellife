<template>
  <div class="login">
    <div class="login__card">
      <div class="login__brand">
        <div class="login__logo">D</div>
        <p class="login__brand-name">Daniellife</p>
      </div>

      <h1 class="login__title">管理員登入</h1>
      <p class="login__desc">僅限授權帳號，透過 Google 驗證登入</p>

      <p v-if="errorMsg" class="login__error">{{ errorMsg }}</p>

      <div class="login__google-wrap">
        <div ref="googleBtnEl"></div>
        <p v-if="loading" class="login__loading">驗證中…</p>
      </div>

      <p class="login__back">
        <RouterLink to="/" class="login__back-link">← 回到首頁</RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { googleLogin } from '@/api/auth'

const router = useRouter()
const auth = useAuthStore()
const googleBtnEl = ref<HTMLElement | null>(null)
const errorMsg = ref('')
const loading = ref(false)

onMounted(() => {
  const script = document.createElement('script')
  script.src = 'https://accounts.google.com/gsi/client'
  script.onload = initGoogle
  script.onerror = () => { errorMsg.value = '無法載入 Google 登入，請確認網路連線' }
  document.head.appendChild(script)
})

function initGoogle() {
  // @ts-ignore
  window.google.accounts.id.initialize({
    client_id: import.meta.env.VITE_GOOGLE_CLIENT_ID as string,
    callback: handleCredential,
    auto_select: false,
  })
  // @ts-ignore
  window.google.accounts.id.renderButton(googleBtnEl.value!, {
    theme: 'outline',
    size: 'large',
    type: 'standard',
    text: 'signin_with',
    shape: 'rectangular',
    logo_alignment: 'left',
    width: 280,
  })
}

async function handleCredential(response: { credential: string }) {
  errorMsg.value = ''
  loading.value = true
  const result = await googleLogin(response.credential)
  loading.value = false

  if (result.ok) {
    auth.login({ name: result.name, email: result.email })
    router.push('/admin')
  } else {
    errorMsg.value = result.error?.includes('403')
      ? '此 Google 帳號沒有存取權限'
      : '登入失敗，請再試一次'
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

.login__desc {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-3);
  margin-top: calc(-1 * var(--space-3));
}

.login__error {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: #dc2626;
  text-align: center;
  padding: var(--space-2) var(--space-3);
  background: #fef2f2;
  border-radius: var(--radius-sm);
}

.login__google-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) 0;
}

.login__loading {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-3);
}

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
