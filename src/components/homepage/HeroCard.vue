<template>
  <section class="hero">
    <div class="hero__inner">

      <!-- 左欄：個人資訊 -->
      <div class="hero__left">
        <div class="hero__name-row">
          <h1 class="hero__name">周彥廷 <span class="hero__age">(22)</span></h1>
          <p class="hero__meta">Taipei ／ 臺中人 ／ Male ／ <span class="hero__traits">沉穩、負責任、有企圖心</span></p>
        </div>
        <p class="hero__subtitle">NTU 臺大會計 ／ Financer ／ Web designer ／ Writer</p>
      </div>

      <!-- 中欄：社群帳號 -->
      <div class="hero__center">
        <div class="hero__social">
          <a href="https://www.instagram.com/daniellife_" target="_blank" class="hero__social-link">
            <!-- Instagram brand icon -->
            <svg class="hero__social-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <defs>
                <radialGradient id="ig-grad" cx="30%" cy="107%" r="150%">
                  <stop offset="0%" stop-color="#fdf497"/>
                  <stop offset="5%" stop-color="#fdf497"/>
                  <stop offset="45%" stop-color="#fd5949"/>
                  <stop offset="60%" stop-color="#d6249f"/>
                  <stop offset="90%" stop-color="#285AEB"/>
                </radialGradient>
              </defs>
              <rect width="24" height="24" rx="6" fill="url(#ig-grad)"/>
              <circle cx="12" cy="12" r="4.5" fill="none" stroke="#fff" stroke-width="1.8"/>
              <circle cx="17.5" cy="6.5" r="1.1" fill="#fff"/>
              <rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="#fff" stroke-width="1.6"/>
            </svg>
            _daniellife_
          </a>
          <a href="https://www.linkedin.com/in/yen-ting-chou" target="_blank" class="hero__social-link">
            <!-- LinkedIn brand icon -->
            <svg class="hero__social-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <rect width="24" height="24" rx="4" fill="#0A66C2"/>
              <path fill="#fff" d="M7.1 9.5H4.8v7.7h2.3V9.5zM5.95 8.5a1.35 1.35 0 1 0 0-2.7 1.35 1.35 0 0 0 0 2.7zM19.2 17.2h-2.3v-3.75c0-.9-.02-2.05-1.25-2.05-1.25 0-1.44.97-1.44 1.98v3.82h-2.3V9.5h2.2v1.05h.03c.31-.58 1.05-1.2 2.16-1.2 2.31 0 2.73 1.52 2.73 3.5v4.35z"/>
            </svg>
            Yen-Ting Chou
          </a>
        </div>
      </div>

      <!-- 右欄：座右銘 -->
      <div class="hero__right">
        <div class="hero__motto-card">
          <p class="hero__motto-label">人生座右銘</p>
          <p class="hero__motto-text">你不需要跟隨著才能開始<br>但至少要真心嘗試</p>
        </div>
      </div>

    </div>
  </section>
</template>

<script setup lang="ts">
</script>

<style scoped>
.hero {
  background-color: var(--color-white);
  padding: var(--space-6);
}

.hero__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  display: flex;
  align-items: center;
  gap: var(--space-6);
  background-color: var(--color-primary-bg);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-md);
  padding: var(--space-5) var(--space-6);
}

/* ── 左欄 ── */
.hero__left {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.hero__name-row {
  display: flex;
  align-items: baseline;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.hero__name {
  font-family: var(--font-cjk);
  font-size: 22px;
  font-weight: 700;
  color: var(--color-ink-1);
  white-space: nowrap;
}

.hero__age {
  font-size: 18px;
  font-weight: 400;
}

.hero__meta {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
  line-height: 1.5;
}

.hero__traits {
  text-decoration: underline;
  text-underline-offset: 2px;
}

.hero__subtitle {
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--color-ink-3);
}

/* ── 中欄 ── */
.hero__center {
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-4);
}


.hero__social {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: var(--space-5);
}

.hero__social-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  font-family: var(--font-body);
  font-size: 12px;
  color: var(--color-ink-2);
  transition: color 0.2s;
}

.hero__social-link:hover { color: var(--color-ink-1); }

.hero__social-icon {
  width: 28px;
  height: 28px;
  flex-shrink: 0;
}

/* ── 右欄 ── */
.hero__right {
  flex: 0 0 auto;
}

.hero__motto-card {
  background-color: var(--color-white);
  border-radius: var(--radius-md);
  padding: var(--space-4) var(--space-5);
  min-width: 180px;
  text-align: center;
}

.hero__motto-label {
  font-family: var(--font-cjk);
  font-size: 11px;
  color: var(--color-ink-3);
  margin-bottom: var(--space-3);
  letter-spacing: 0.04em;
}

.hero__motto-text {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-1);
  line-height: 1.9;
}

/* RWD */
@media (max-width: 900px) {
  .hero__center { display: none; }
}

@media (max-width: 767px) {
  .hero__inner { flex-direction: column; align-items: flex-start; }
  .hero__center { display: flex; align-self: center; }
  .hero__right { width: 100%; }
  .hero__motto-card { min-width: unset; }
}
</style>
