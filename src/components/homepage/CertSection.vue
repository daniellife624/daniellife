<template>
  <section class="cert" ref="sectionEl">
    <div class="cert__inner">
      <div class="cert__header">
        <h2 class="section-title">專業證照與資格</h2>
      </div>

      <div v-if="certData" class="cert__grid">
        <!-- 語言領域 -->
        <div class="cert-col">
          <h3 class="cert-col__title">語言領域</h3>
          <div class="cert-col__body">
            <p class="cert-col__sub">英文</p>
            <div v-for="lang in certData.language.en" :key="lang.name" class="cert-bar-item">
              <div class="cert-bar-item__info">
                <span class="cert-bar-item__name">{{ lang.name }}</span>
                <span class="cert-bar-item__score">{{ lang.score }}</span>
              </div>
              <div class="cert-bar-item__track">
                <div
                  class="cert-bar-item__fill"
                  :class="{ 'cert-bar-item__fill--animate': animateBars }"
                  :style="{ width: animateBars ? lang.pct + '%' : '0%' }"
                ></div>
              </div>
            </div>

            <p class="cert-col__sub cert-col__sub--mt">日文</p>
            <div v-for="jp in certData.language.jp" :key="jp.name" class="cert-bar-item">
              <div class="cert-bar-item__info">
                <span class="cert-bar-item__name">{{ jp.name }}</span>
                <span class="cert-bar-item__score">{{ jp.score }}</span>
              </div>
              <div class="cert-bar-item__track">
                <div
                  class="cert-bar-item__fill"
                  :class="{ 'cert-bar-item__fill--animate': animateBars }"
                  :style="{ width: animateBars ? jp.pct + '%' : '0%' }"
                ></div>
              </div>
            </div>
          </div>
        </div>

        <div class="cert-col__divider"></div>

        <!-- 財會領域 -->
        <div class="cert-col">
          <h3 class="cert-col__title">財會領域</h3>
          <div class="cert-col__body">
            <div v-for="cat in certData.finance" :key="cat.category" class="cert-list-group">
              <p class="cert-list-group__title">{{ cat.category }}</p>
              <ul class="cert-list">
                <li v-for="item in cat.items" :key="item" class="cert-list__item">
                  <span class="cert-list__dot" :class="item !== '待補充' ? 'cert-list__dot--filled' : ''"></span>
                  {{ item }}
                </li>
              </ul>
            </div>
          </div>
        </div>

        <div class="cert-col__divider"></div>

        <!-- 資訊領域 -->
        <div class="cert-col">
          <h3 class="cert-col__title">資訊領域</h3>
          <div class="cert-col__body">
            <div v-for="cat in certData.it" :key="cat.category" class="cert-list-group">
              <p class="cert-list-group__title">{{ cat.category }}</p>
              <ul class="cert-list">
                <li v-for="item in cat.items" :key="item" class="cert-list__item">
                  <span class="cert-list__dot" :class="item !== '待補充' ? 'cert-list__dot--filled' : ''"></span>
                  {{ item }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getCertData } from '@/api/homepage'
import type { CertData } from '@/types/homepage'

const sectionEl = ref<HTMLElement | null>(null)
const certData = ref<CertData | null>(null)
const animateBars = ref(false)

onMounted(async () => {
  certData.value = await getCertData()

  const observer = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting) {
        animateBars.value = true
      } else {
        animateBars.value = false
      }
    },
    { threshold: 0.3 },
  )
  if (sectionEl.value) observer.observe(sectionEl.value)
})
</script>

<style scoped>
.cert {
  padding: var(--space-8) var(--space-6);
  background-color: var(--color-white);
  border-top: 1px solid var(--color-ink-4);
}

.cert__inner {
  max-width: var(--container-max);
  margin: 0 auto;
}

.cert__header { margin-bottom: var(--space-6); }

.section-title {
  font-family: var(--font-cjk);
  font-size: 22px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.cert__grid {
  display: flex;
  gap: 0;
}

.cert-col {
  flex: 1;
  padding: 0 var(--space-6);
}

.cert-col:first-child { padding-left: 0; }
.cert-col:last-child  { padding-right: 0; }

.cert-col__divider {
  width: 1px;
  background-color: var(--color-ink-4);
  flex-shrink: 0;
}

.cert-col__title {
  font-family: var(--font-cjk);
  font-size: 15px;
  font-weight: 700;
  color: var(--color-ink-1);
  margin-bottom: var(--space-4);
}

.cert-col__body {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.cert-col__sub {
  font-family: var(--font-cjk);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-ink-2);
}

.cert-col__sub--mt { margin-top: var(--space-3); }

/* Progress bars */
.cert-bar-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.cert-bar-item__info {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}

.cert-bar-item__name { font-size: 13px; color: var(--color-ink-2); }
.cert-bar-item__score { font-size: 13px; font-weight: 700; color: var(--color-ink-1); }

.cert-bar-item__track {
  height: 8px;
  background-color: var(--color-ink-4);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.cert-bar-item__fill {
  height: 100%;
  background-color: var(--color-ink-1);
  border-radius: var(--radius-full);
  width: 0;
  transition: none;
}

.cert-bar-item__fill--animate {
  transition: width 1.2s cubic-bezier(0.22, 0.61, 0.36, 1);
}

/* Cert list */
.cert-list-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.cert-list-group__title {
  font-size: 12px;
  font-weight: 600;
  color: var(--color-ink-3);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.cert-list { display: flex; flex-direction: column; gap: 4px; list-style: none; }

.cert-list__item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
}

.cert-list__dot {
  width: 8px;
  height: 8px;
  border-radius: 2px;
  border: 1px solid var(--color-ink-4);
  flex-shrink: 0;
}

.cert-list__dot--filled {
  background-color: var(--color-secondary);
  border-color: var(--color-secondary);
}

@media (max-width: 767px) {
  .cert__grid { flex-direction: column; }
  .cert-col { padding: var(--space-4) 0; }
  .cert-col__divider { width: 100%; height: 1px; }
}
</style>
