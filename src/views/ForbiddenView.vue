<template>
  <div class="forbidden">
    <div class="forbidden__card">
      <div class="forbidden__code">403</div>
      <h1 class="forbidden__title">需要管理員權限</h1>
      <p class="forbidden__desc">此頁面為私人區域，請登入後再試。</p>
      <div class="forbidden__actions">
        <RouterLink to="/danieladmin" class="forbidden__btn forbidden__btn--primary">
          前往登入
        </RouterLink>
        <RouterLink to="/" class="forbidden__btn forbidden__btn--ghost">
          回到首頁
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.forbidden {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-primary-bg);
  padding: var(--space-6);
}

.forbidden__card {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-4);
  max-width: 400px;
}

.forbidden__code {
  font-family: var(--font-display);
  font-size: 96px;
  font-weight: 700;
  color: var(--color-primary);
  line-height: 1;
  letter-spacing: -4px;
}

.forbidden__title {
  font-family: var(--font-cjk);
  font-size: 22px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.forbidden__desc {
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-3);
}

.forbidden__actions {
  display: flex;
  gap: var(--space-3);
  margin-top: var(--space-2);
}

.forbidden__btn {
  padding: var(--space-3) var(--space-6);
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 700;
  transition: opacity 0.2s;
  display: inline-block;
}

.forbidden__btn:hover { opacity: 0.8; }

.forbidden__btn--primary {
  background: var(--color-primary);
  color: var(--color-ink-1);
}

.forbidden__btn--ghost {
  background: transparent;
  border: 1px solid var(--color-ink-4);
  color: var(--color-ink-2);
}
</style>
