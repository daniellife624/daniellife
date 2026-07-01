<template>
  <section class="market__section">
    <h2 class="market__section-title">利率與殖利率 Yield</h2>
    <p class="market__section-sub">資料來源：<a href="https://fred.stlouisfed.org/" target="_blank" rel="noopener">FRED · St. Louis Fed</a></p>
    <div class="market__grid market__grid--2">
      <div class="market__chart-wrap">
        <p class="market__chart-label">Fed 基準利率（聯邦基金目標利率）</p>
        <div class="market__chart market__chart--fred">
          <iframe
            src="https://fred.stlouisfed.org/graph/?id=FEDFUNDS&cosd=2010-01-01"
            width="100%" height="100%"
            frameborder="0"
            title="Federal Funds Rate — FRED"
          ></iframe>
        </div>
      </div>
      <div class="market__chart-wrap">
        <p class="market__chart-label">美國10年期公債殖利率</p>
        <div class="market__chart market__chart--fred">
          <iframe
            src="https://fred.stlouisfed.org/graph/?id=DGS10&cosd=2010-01-01"
            width="100%" height="100%"
            frameborder="0"
            title="US 10-Year Treasury Yield — FRED"
          ></iframe>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
</script>

<style scoped>
.market__section { display: flex; flex-direction: column; gap: var(--space-4); }
.market__section-title { font-family: var(--font-cjk); font-size: 20px; font-weight: 700; color: var(--color-ink-1); }
.market__section-sub { font-family: var(--font-cjk); font-size: 12px; color: var(--color-ink-3); margin-top: -8px; }
.market__section-sub a { color: var(--color-secondary); text-decoration: none; }
.market__section-sub a:hover { text-decoration: underline; }
.market__grid { display: grid; gap: var(--space-5); }
.market__grid--2 { grid-template-columns: 1fr 1fr; }
.market__chart-wrap { display: flex; flex-direction: column; gap: var(--space-2); }
.market__chart-label { font-family: var(--font-cjk); font-size: 14px; font-weight: 600; color: var(--color-ink-2); text-align: center; }
.market__chart { width: 100%; border: 1px solid var(--color-ink-4); border-radius: var(--radius-md); overflow: hidden; }
.market__chart--fred { height: 520px; }

@media (max-width: 767px) { .market__grid--2 { grid-template-columns: 1fr; } }
</style>
