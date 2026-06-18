<template>
  <section class="academic" ref="sectionEl">
    <div class="academic__inner">
      <div class="academic__header">
        <h2 class="section-title">求學歷程</h2>
      </div>

      <div class="academic__chart-wrap">
        <svg class="academic__svg" viewBox="0 0 900 300" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
          <path
            class="academic__path"
            :class="{ 'academic__path--drawn': isVisible }"
            d="M 50,270 C 120,260 200,200 290,165 C 380,130 440,110 510,80 C 580,50 680,30 860,18"
            fill="none"
            stroke="#E8C13A"
            stroke-width="3"
            stroke-linecap="round"
          />
          <circle
            v-for="(m, i) in milestones"
            :key="i"
            :cx="m.cx"
            :cy="m.cy"
            r="9"
            fill="#E8C13A"
            stroke="#fff"
            stroke-width="3"
            class="academic__dot"
            :class="{ 'academic__dot--visible': isVisible }"
            :style="{ transitionDelay: `${0.5 + i * 0.4}s` }"
          />
        </svg>

        <div class="academic__car" :class="{ 'academic__car--moving': isVisible }">🚗</div>
      </div>

      <div class="academic__cards">
        <div
          v-for="(m, i) in milestones"
          :key="`card-${m.id}`"
          class="academic-card"
          :class="{ 'academic-card--visible': isVisible }"
          :style="{ transitionDelay: `${0.7 + i * 0.25}s` }"
        >
          <div class="academic-card__school">{{ m.school }}</div>
          <div class="academic-card__major">{{ m.major }}</div>
          <div class="academic-card__period">{{ m.period }}</div>
          <div class="academic-card__divider"></div>
          <p class="academic-card__label">重點事蹟</p>
          <ul class="academic-card__list">
            <li v-for="fact in m.facts" :key="fact">{{ fact }}</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getAcademicMilestones } from '@/api/homepage'
import type { AcademicMilestone } from '@/types/homepage'

const sectionEl = ref<HTMLElement | null>(null)
const isVisible = ref(false)
const milestones = ref<(AcademicMilestone & { cx: number; cy: number })[]>([])

const positions = [
  { cx: 290, cy: 165 },
  { cx: 510, cy: 80 },
  { cx: 860, cy: 18 },
]

onMounted(async () => {
  const data = await getAcademicMilestones()
  milestones.value = data.map((m, i) => ({ ...m, ...positions[i] }))

  const observer = new IntersectionObserver(
    (entries) => {
      if (entries[0].isIntersecting) {
        isVisible.value = true
        observer.disconnect()
      }
    },
    { threshold: 0.2 },
  )
  if (sectionEl.value) observer.observe(sectionEl.value)
})
</script>

<style scoped>
.academic {
  padding: var(--space-8) var(--space-6);
  background-color: var(--color-white);
  border-top: 1px solid var(--color-ink-4);
  overflow: hidden;
}

.academic__inner {
  max-width: var(--container-max);
  margin: 0 auto;
}

.academic__header {
  margin-bottom: var(--space-5);
}

.section-title {
  font-family: var(--font-cjk);
  font-size: 22px;
  font-weight: 700;
  color: var(--color-ink-1);
}

/* SVG wrap */
.academic__chart-wrap {
  position: relative;
  width: 100%;
  height: 300px;
  margin-bottom: var(--space-5);
}

.academic__svg {
  width: 100%;
  height: 100%;
}

/* 曲線繪製動畫 */
.academic__path {
  stroke-dasharray: 1500;
  stroke-dashoffset: 1500;
  transition: stroke-dashoffset 2s cubic-bezier(0.4, 0, 0.2, 1);
}

.academic__path--drawn {
  stroke-dashoffset: 0;
}

/* 圓點 */
.academic__dot {
  opacity: 0;
  transform-origin: center;
  transform: scale(0);
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.academic__dot--visible {
  opacity: 1;
  transform: scale(1);
}

/* 汽車 */
.academic__car {
  position: absolute;
  bottom: 8%;
  left: 3%;
  font-size: 20px;
  transition: left 2s cubic-bezier(0.4, 0, 0.2, 1), bottom 2s cubic-bezier(0.4, 0, 0.2, 1);
}

.academic__car--moving {
  left: 92%;
  bottom: 88%;
}

/* 三欄卡片 */
.academic__cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-5);
}

.academic-card {
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-md);
  padding: var(--space-4) var(--space-5);
  opacity: 0;
  transform: translateY(16px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}

.academic-card--visible {
  opacity: 1;
  transform: translateY(0);
}

.academic-card__school {
  font-family: var(--font-cjk);
  font-size: 15px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.academic-card__major {
  font-size: 13px;
  color: var(--color-ink-3);
  margin-top: 2px;
}

.academic-card__period {
  font-size: 12px;
  color: var(--color-ink-3);
  margin-top: 2px;
  font-family: var(--font-body);
}

.academic-card__divider {
  height: 1px;
  background: var(--color-ink-4);
  margin: var(--space-3) 0;
}

.academic-card__label {
  font-size: 11px;
  font-weight: 700;
  color: var(--color-ink-3);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: var(--space-2);
}

.academic-card__list {
  display: flex;
  flex-direction: column;
  gap: 4px;
  list-style: none;
}

.academic-card__list li {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
  padding-left: var(--space-3);
  position: relative;
  line-height: 1.6;
}

.academic-card__list li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: var(--color-primary);
}

@media (max-width: 767px) {
  .academic__cards { grid-template-columns: 1fr; }
  .academic__chart-wrap { height: 160px; }
}
</style>
