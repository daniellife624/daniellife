<template>
  <section class="academic" ref="sectionEl">
    <div class="academic__inner">
      <div class="academic__header">
        <h2 class="section-title">求學歷程</h2>
      </div>

      <div class="academic__chart-wrap">
        <svg
          ref="svgEl"
          class="academic__svg"
          viewBox="0 0 900 300"
          preserveAspectRatio="none"
          xmlns="http://www.w3.org/2000/svg"
        >
          <path
            ref="pathEl"
            class="academic__path"
            d="M 50,265 C 95,248 140,200 182,210 C 224,220 265,265 314,250 C 363,235 403,152 455,140 C 507,128 540,172 588,158 C 636,144 706,50 768,36 C 818,22 850,14 884,12"
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
            :style="{ transitionDelay: `${0.6 + i * 0.4}s` }"
          />
        </svg>

        <!-- Car follows path via JS; no CSS transition -->
        <div ref="carEl" class="academic__car">🚗</div>
      </div>

      <div class="academic__cards">
        <div
          v-for="(m, i) in milestones"
          :key="`card-${m.id}`"
          class="academic-card"
          :class="{ 'academic-card--visible': isVisible }"
          :style="{ transitionDelay: `${0.8 + i * 0.25}s` }"
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
import { ref, onMounted, onUnmounted } from 'vue'
import { getAcademicMilestones } from '@/api/homepage'
import type { AcademicMilestone } from '@/types/homepage'

const sectionEl = ref<HTMLElement | null>(null)
const svgEl     = ref<SVGSVGElement | null>(null)
const pathEl    = ref<SVGPathElement | null>(null)
const carEl     = ref<HTMLElement | null>(null)
const isVisible = ref(false)

const milestones = ref<(AcademicMilestone & { cx: number; cy: number })[]>([])

// Milestone positions — each is the endpoint of a path segment
const positions = [
  { cx: 455, cy: 140 },
  { cx: 768, cy:  36 },
  { cx: 884, cy:  12 },
]

const DURATION = 2600   // ms — matches visual expectation

let rafId     = 0
let animStart: number | null = null
let observer: IntersectionObserver | null = null

function easeInOut(t: number): number {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2
}

function resetAnimation() {
  cancelAnimationFrame(rafId)
  rafId = 0
  animStart = null
  isVisible.value = false

  const path = pathEl.value
  if (path) {
    const len = path.getTotalLength()
    path.style.strokeDasharray  = `${len}`
    path.style.strokeDashoffset = `${len}`
  }
  const car = carEl.value
  if (car) {
    car.style.opacity   = '0'
    car.style.left      = '5.56%'   // 50/900*100
    car.style.top       = '88.33%'  // 265/300*100
    car.style.transform = 'translate(-50%, -50%)'
  }
}

function tick(ts: number) {
  if (animStart === null) animStart = ts
  const t     = Math.min((ts - animStart) / DURATION, 1)
  const eased = easeInOut(t)

  const path = pathEl.value
  const car  = carEl.value
  const svg  = svgEl.value
  if (!path || !car || !svg) return

  const totalLen    = path.getTotalLength()
  const currentLen  = eased * totalLen

  // Animate path drawing (replaces CSS transition)
  path.style.strokeDashoffset = `${totalLen - currentLen}`

  // Car position in SVG user units → CSS percentage of container
  const pt     = path.getPointAtLength(currentLen)
  const ptNext = path.getPointAtLength(Math.min(currentLen + 5, totalLen))

  // Visual angle: account for preserveAspectRatio="none" stretching
  const wrap  = svg.parentElement as HTMLElement
  const wrapW = wrap.clientWidth  || 900
  const wrapH = wrap.clientHeight || 300
  const dx    = (ptNext.x - pt.x) * (wrapW / 900)
  const dy    = (ptNext.y - pt.y) * (wrapH / 300)
  const angle = Math.atan2(dy, dx) * 180 / Math.PI

  car.style.left      = `${(pt.x / 900) * 100}%`
  car.style.top       = `${(pt.y / 300) * 100}%`
  car.style.transform = `translate(-50%, -50%) rotate(${angle}deg) scaleX(-1)`

  if (t < 1) {
    rafId = requestAnimationFrame(tick)
  }
}

function startAnimation() {
  cancelAnimationFrame(rafId)
  animStart = null

  const path = pathEl.value
  if (path) {
    const len = path.getTotalLength()
    path.style.strokeDasharray  = `${len}`
    path.style.strokeDashoffset = `${len}`
  }
  const car = carEl.value
  if (car) car.style.opacity = '1'

  isVisible.value = true          // reveals dots + cards via CSS
  rafId = requestAnimationFrame(tick)
}

onMounted(async () => {
  const data = await getAcademicMilestones()
  milestones.value = data.map((m, i) => ({ ...m, cx: positions[i]?.cx ?? 0, cy: positions[i]?.cy ?? 0 }))

  // Initialise path to hidden (getTotalLength available after mount)
  const path = pathEl.value
  if (path) {
    const len = path.getTotalLength()
    path.style.strokeDasharray  = `${len}`
    path.style.strokeDashoffset = `${len}`
  }

  observer = new IntersectionObserver(
    (entries) => {
      if (entries[0]?.isIntersecting) {
        startAnimation()
      } else {
        resetAnimation()
      }
    },
    { threshold: 0.2 },
  )
  if (sectionEl.value) observer.observe(sectionEl.value)
})

onUnmounted(() => {
  cancelAnimationFrame(rafId)
  observer?.disconnect()
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
  display: flex;
  align-items: baseline;
  gap: var(--space-4);
}

.academic__subtitle {
  font-family: var(--font-cjk);
  font-size: 12px;
  color: var(--color-ink-3);
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

/* Path — dasharray/dashoffset set by JS; no CSS transition needed */
.academic__path {
  stroke-dasharray: 3000;   /* fallback until JS overrides */
  stroke-dashoffset: 3000;
}

/* Milestone dots */
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

/* Car — positioned and rotated entirely by JS */
.academic__car {
  position: absolute;
  left: 5.56%;
  top: 88.33%;
  transform: translate(-50%, -50%);
  font-size: 22px;
  opacity: 0;
  pointer-events: none;
  user-select: none;
  line-height: 1;
}

/* Cards */
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
  .academic__cards      { grid-template-columns: 1fr; }
  .academic__chart-wrap { height: 160px; }
}
</style>
