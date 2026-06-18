<template>
  <div class="news-view">
    <div class="news-view__inner">

      <!-- Section: 股市行情 -->
      <section class="news-section">
        <h2 class="section-title">股市行情</h2>
        <div class="widget-row">
          <!-- TradingView Ticker Tape placeholder -->
          <div class="widget-placeholder widget-placeholder--wide">
            <span class="widget-placeholder__label">TradingView · 股票走勢圖</span>
            <span class="widget-placeholder__hint">（整合後將顯示 K 線圖）</span>
          </div>
          <div class="widget-placeholder widget-placeholder--wide">
            <span class="widget-placeholder__label">TradingView · 台股走勢圖</span>
            <span class="widget-placeholder__hint">（整合後將顯示 K 線圖）</span>
          </div>
        </div>
      </section>

      <!-- Section: 外匯 / 利率 / 總經指標 -->
      <section class="news-section">
        <h2 class="section-title">總體經濟指標</h2>
        <div class="macro-grid">

          <!-- Forex -->
          <div class="macro-card">
            <h3 class="macro-card__title">外匯 Forex</h3>
            <div class="macro-card__body">
              <div v-for="pair in forexPairs" :key="pair.symbol" class="macro-row">
                <span class="macro-row__symbol">{{ pair.symbol }}</span>
                <span class="macro-row__value" :class="pair.change >= 0 ? 'macro-row__value--up' : 'macro-row__value--down'">
                  {{ pair.value }}
                  <span class="macro-row__change">{{ pair.change >= 0 ? '+' : '' }}{{ pair.change }}%</span>
                </span>
              </div>
            </div>
          </div>

          <!-- Yield -->
          <div class="macro-card">
            <h3 class="macro-card__title">美債殖利率</h3>
            <div class="macro-card__body">
              <div v-for="bond in yieldCurve" :key="bond.maturity" class="macro-row">
                <span class="macro-row__symbol">{{ bond.maturity }}</span>
                <span class="macro-row__value" :class="bond.change >= 0 ? 'macro-row__value--up' : 'macro-row__value--down'">
                  {{ bond.yield }}%
                  <span class="macro-row__change">{{ bond.change >= 0 ? '+' : '' }}{{ bond.change }}bp</span>
                </span>
              </div>
            </div>
          </div>

          <!-- GDP -->
          <div class="macro-card">
            <h3 class="macro-card__title">GDP 成長率</h3>
            <div class="macro-card__body">
              <div v-for="g in gdpData" :key="g.country" class="macro-row">
                <span class="macro-row__symbol">{{ g.country }}</span>
                <span class="macro-row__value" :class="g.pct >= 0 ? 'macro-row__value--up' : 'macro-row__value--down'">
                  {{ g.pct >= 0 ? '+' : '' }}{{ g.pct }}%
                </span>
              </div>
            </div>
          </div>

          <!-- CPI -->
          <div class="macro-card">
            <h3 class="macro-card__title">CPI 通膨率</h3>
            <div class="macro-card__body">
              <div v-for="c in cpiData" :key="c.country" class="macro-row">
                <span class="macro-row__symbol">{{ c.country }}</span>
                <span class="macro-row__value" :class="c.pct >= 2 ? 'macro-row__value--up' : 'macro-row__value--down'">
                  {{ c.pct }}%
                </span>
              </div>
            </div>
          </div>

        </div>
      </section>

      <!-- Note -->
      <p class="news-view__note">
        ＊ 以上數據為 Mock 資料，實際整合 TradingView Widget 與總經 API 後將顯示即時資訊。
      </p>

    </div>
  </div>
</template>

<script setup lang="ts">
const forexPairs = [
  { symbol: 'USD/TWD', value: '32.45', change: 0.12 },
  { symbol: 'USD/JPY', value: '157.82', change: -0.35 },
  { symbol: 'EUR/USD', value: '1.0831', change: 0.07 },
  { symbol: 'USD/CNH', value: '7.2540', change: 0.04 },
]

const yieldCurve = [
  { maturity: '2Y', yield: '4.82', change: 3 },
  { maturity: '5Y', yield: '4.51', change: -1 },
  { maturity: '10Y', yield: '4.28', change: 2 },
  { maturity: '30Y', yield: '4.47', change: 1 },
]

const gdpData = [
  { country: '美國 US', pct: 2.8 },
  { country: '台灣 TW', pct: 3.1 },
  { country: '日本 JP', pct: 0.6 },
  { country: '中國 CN', pct: 4.7 },
]

const cpiData = [
  { country: '美國 US', pct: 3.2 },
  { country: '台灣 TW', pct: 2.1 },
  { country: '日本 JP', pct: 2.8 },
  { country: '中國 CN', pct: 0.4 },
]
</script>

<style scoped>
.news-view {
  padding: var(--space-7) var(--space-6) var(--space-8);
  background: var(--color-white);
}

.news-view__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
}

/* Section */
.news-section { display: flex; flex-direction: column; gap: var(--space-5); }

.section-title {
  font-family: var(--font-cjk);
  font-size: 20px;
  font-weight: 700;
  color: var(--color-ink-1);
}

/* Widget row */
.widget-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-5);
}

.widget-placeholder {
  height: 260px;
  border: 1px dashed var(--color-ink-4);
  border-radius: var(--radius-md);
  background: #fafafa;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
}

.widget-placeholder__label {
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 600;
  color: var(--color-ink-2);
}

.widget-placeholder__hint {
  font-family: var(--font-cjk);
  font-size: 12px;
  color: var(--color-ink-4);
}

/* Macro grid */
.macro-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-4);
}

.macro-card {
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.macro-card__title {
  padding: var(--space-3) var(--space-4);
  background: var(--color-primary-bg);
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 700;
  color: var(--color-ink-1);
  border-bottom: 1px solid var(--color-ink-4);
}

.macro-card__body {
  padding: var(--space-3) var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.macro-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.macro-row__symbol {
  font-size: 13px;
  color: var(--color-ink-2);
  font-family: var(--font-body);
}

.macro-row__value {
  font-size: 13px;
  font-weight: 700;
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.macro-row__value--up   { color: #16a34a; }
.macro-row__value--down { color: #dc2626; }

.macro-row__change {
  font-size: 11px;
  font-weight: 400;
  opacity: 0.8;
}

/* Note */
.news-view__note {
  font-family: var(--font-cjk);
  font-size: 12px;
  color: var(--color-ink-4);
}

@media (max-width: 900px) {
  .macro-grid { grid-template-columns: 1fr 1fr; }
  .widget-row { grid-template-columns: 1fr; }
}

@media (max-width: 600px) {
  .macro-grid { grid-template-columns: 1fr; }
}
</style>
