<template>
  <div class="literature">
    <TrainTimeline :timeline="timeline" @click-work="scrollToWork" />

    <section class="works-section" ref="worksSectionEl">
      <div class="works-inner">
        <h2 class="page-title">文學作品</h2>
        <div class="works-grid">
          <WorkCard v-for="work in works" :key="work.id" :work="work" />
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getTimelineEvents, getLiteratureWorks } from '@/api/literature'
import type { TimelineEvent, LiteratureWork } from '@/types/literature'
import TrainTimeline from '@/components/literature/TrainTimeline.vue'
import WorkCard from '@/components/literature/WorkCard.vue'

const timeline = ref<TimelineEvent[]>([])
const works    = ref<LiteratureWork[]>([])
const worksSectionEl = ref<HTMLElement | null>(null)

function scrollToWork(workId: number) {
  if (!worksSectionEl.value) return
  const el = worksSectionEl.value.querySelector(`[data-work-id="${workId}"]`) as HTMLElement | null
  const target = el ?? worksSectionEl.value
  target.scrollIntoView({ behavior: 'smooth', block: 'center' })
  if (el) {
    el.classList.add('work-card--highlight')
    setTimeout(() => el.classList.remove('work-card--highlight'), 1800)
  }
}

onMounted(async () => {
  timeline.value = await getTimelineEvents()
  works.value    = await getLiteratureWorks()
})
</script>

<style scoped>
.literature { background: #faf9f7; }

.works-section {
  padding: var(--space-8) var(--space-6);
  background: #faf9f7;
}

.works-inner { max-width: var(--container-max); margin: 0 auto; }

.page-title {
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 400;
  color: var(--color-ink-3);
  margin-bottom: var(--space-5);
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.works-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }

@media (max-width: 900px) { :deep(.track-container) { overflow-x: auto; } }
@media (max-width: 767px) { .works-grid { grid-template-columns: 1fr; } }
</style>
