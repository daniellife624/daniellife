<template>
  <div class="market">
    <div class="market__inner">

      <section class="market__section">
        <h2 class="market__section-title">股票市場 Stock Market</h2>
        <div class="market__grid market__grid--2">
          <MarketOverviewPanel default-tab="TW" />
          <MarketOverviewPanel default-tab="US" />
        </div>
      </section>

      <ForexSection />
      <YieldSection />
      <WorldBankSection />

    </div>
  </div>
</template>

<script setup lang="ts">
import MarketOverviewPanel from '@/components/market/MarketOverviewPanel.vue'
import ForexSection from '@/components/market/ForexSection.vue'
import YieldSection from '@/components/market/YieldSection.vue'
import WorldBankSection from '@/components/market/WorldBankSection.vue'
</script>

<style scoped>
.market { background: var(--color-white); min-height: 100vh; }

.market__inner {
  max-width: var(--container-max);
  margin: 0 auto;
  padding: var(--space-8) var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-7);
}

.market__section { display: flex; flex-direction: column; gap: var(--space-4); }
.market__section-title { font-family: var(--font-cjk); font-size: 20px; font-weight: 700; color: var(--color-ink-1); }
.market__grid { display: grid; gap: var(--space-5); }
.market__grid--2 { grid-template-columns: 1fr 1fr; }

@media (max-width: 767px) { .market__grid--2 { grid-template-columns: 1fr; } }
</style>
