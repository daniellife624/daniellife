<template>
  <section class="hero">
    <div class="hero__inner">

      <!-- 左側：個人資訊 -->
      <div class="hero__left">
        <div class="hero__info-card">
          <h1 class="hero__name">周彥廷 <span class="hero__age">(22)</span></h1>
          <p class="hero__meta">Taipei / 臺中人 ／ Male ／ 沉穩、負責任、有企圖心</p>
          <p class="hero__subtitle">NTU 臺大會計 ／ Financer ／ Web designer ／ Writer</p>
          <div class="hero__social">
            <a href="https://www.instagram.com/daniellife_" target="_blank" class="hero__social-link">
              <span class="hero__icon-placeholder"></span>
              _daniellife_
            </a>
            <a href="https://www.linkedin.com/in/yen-ting-chou" target="_blank" class="hero__social-link">
              <span class="hero__icon-placeholder"></span>
              Yen-Ting Chou
            </a>
          </div>
        </div>
      </div>

      <!-- 右側：座右銘 -->
      <div class="hero__right">
        <div class="hero__motto-card">
          <p class="hero__motto-label">人生座右銘</p>
          <p class="hero__motto-text">每一件事都要嘗試做<br>但至少要勇於嘗試</p>
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
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-6);
  background-color: var(--color-primary-bg);
  border: 1px solid var(--color-primary);
  border-radius: var(--radius-md);
  padding: var(--space-6);
}

.hero__left {
  flex: 1;
}

.hero__info-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.hero__name {
  font-family: var(--font-cjk);
  font-size: 28px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.hero__age {
  font-size: 22px;
  font-weight: 400;
}

.hero__meta {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
}

.hero__subtitle {
  font-family: var(--font-body);
  font-size: 13px;
  color: var(--color-ink-2);
}

.hero__social {
  display: flex;
  gap: var(--space-5);
  margin-top: var(--space-2);
}

.hero__social-link {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-size: 13px;
  color: var(--color-ink-2);
  transition: color 0.2s;
}

.hero__social-link:hover {
  color: var(--color-primary);
}

.hero__social-link img {
  width: 18px;
  height: 18px;
}

/* 右側座右銘 */
.hero__right {
  flex-shrink: 0;
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
}

.hero__motto-text {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-1);
  line-height: 1.8;
}

/* RWD */
@media (max-width: 767px) {
  .hero__inner {
    flex-direction: column;
  }

  .hero__right {
    width: 100%;
  }
}
</style>