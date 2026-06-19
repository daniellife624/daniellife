<template>
  <section class="plan">
    <div class="plan__inner">
      <div class="plan__header">
        <h2 class="section-title">未來規劃</h2>
        <p class="plan__subtitle">由於 AI 時代迭代迅速，先以近 5 年規劃為主</p>
      </div>

      <div class="plan__body">
        <div class="plan__pyramid">
          <div
            v-for="(p, i) in plans"
            :key="p.id"
            class="plan-row"
          >
            <div class="plan-row__block" :class="`plan-row__block--${p.phase}`">
              <span class="plan-row__title">{{ p.title }}</span>
              <span class="plan-row__sub">{{ p.subtitle }}</span>
            </div>
            <div class="plan-row__line" :class="`plan-row__line--${p.phase}`"></div>
            <ul class="plan-row__items">
              <li v-for="item in p.items" :key="item">{{ item }}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getFuturePlans } from '@/api/homepage'
import type { FuturePlan } from '@/types/homepage'

const plans = ref<FuturePlan[]>([])

onMounted(async () => {
  plans.value = await getFuturePlans()
})
</script>

<style scoped>
.plan {
  padding: var(--space-8) var(--space-6);
  background-color: var(--color-white);
  border-top: 1px solid var(--color-ink-4);
}

.plan__inner {
  max-width: var(--container-max);
  margin: 0 auto;
}

.plan__header {
  margin-bottom: var(--space-6);
}

.section-title {
  font-family: var(--font-cjk);
  font-size: 22px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.plan__subtitle {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-3);
  margin-top: var(--space-2);
}

/* 金字塔列 */
.plan__pyramid {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.plan-row {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

/* 每層 block 的寬度遞減（從上到下：中期最寬） */
.plan-row:nth-child(1) .plan-row__block { width: 340px; }
.plan-row:nth-child(2) .plan-row__block { width: 260px; margin-left: 40px; }
.plan-row:nth-child(3) .plan-row__block { width: 180px; margin-left: 80px; }

.plan-row__block {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-sm);
  flex-shrink: 0;
  min-height: 60px;
}

.plan-row__block--mid {
  background-color: #fdf8d8;
  border: 1px solid #E8C13A;
}

.plan-row__block--mid-short {
  background-color: #eef1ec;
  border: 1px solid #7A8C6E;
}

.plan-row__block--short {
  background-color: #f8eee9;
  border: 1px solid #C17055;
}

.plan-row__title {
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.plan-row__sub {
  font-family: var(--font-cjk);
  font-size: 12px;
  color: var(--color-ink-3);
  margin-top: 2px;
}

/* 連接線 */
.plan-row__line {
  height: 1px;
  width: 40px;
  flex-shrink: 0;
}

.plan-row__line--mid       { background-color: #E8C13A; }
.plan-row__line--mid-short { background-color: #7A8C6E; }
.plan-row__line--short     { background-color: #C17055; }

/* 項目文字 */
.plan-row__items {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.plan-row__items li {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
  line-height: 1.6;
  padding-left: var(--space-3);
  position: relative;
}

.plan-row__items li::before {
  content: '·';
  position: absolute;
  left: 0;
  color: var(--color-ink-3);
}

@media (max-width: 767px) {
  .plan-row { flex-direction: column; align-items: flex-start; }
  .plan-row:nth-child(1) .plan-row__block,
  .plan-row:nth-child(2) .plan-row__block,
  .plan-row:nth-child(3) .plan-row__block {
    width: 100%;
    margin-left: 0;
  }
  .plan-row__line { display: none; }
}
</style>
