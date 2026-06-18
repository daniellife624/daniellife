<template>
  <section class="intern">
    <div class="intern__inner">
      <div class="intern__header">
        <h2 class="section-title">實習經驗</h2>
        <span class="section-tag">金融業 X 四大事務所</span>
      </div>
      <div class="intern__wrap">
        <div class="intern__list" ref="listEl">
          <article v-for="item in interns" :key="item.id" class="intern-card">
            <h3 class="intern-card__company">{{ item.company }}</h3>
            <p class="intern-card__dept">部門/職稱：{{ item.dept }}/{{ item.role }}</p>
            <div class="intern-card__photo"></div>
            <p class="intern-card__contrib">主要貢獻：{{ item.contribution }}</p>
            <button class="intern-card__btn">查看更多</button>
          </article>
        </div>
        <button class="intern__arrow" @click="scrollNext" aria-label="下一頁">›</button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getInternships } from '@/api/homepage'
import type { Internship } from '@/types/homepage'

const listEl = ref<HTMLElement | null>(null)
const interns = ref<Internship[]>([])

onMounted(async () => {
  interns.value = await getInternships()
})

function scrollNext() {
  listEl.value?.scrollBy({ left: 320, behavior: 'smooth' })
}
</script>

<style scoped>
.intern {
  padding: var(--space-8) var(--space-6);
  background-color: var(--color-white);
  border-top: 1px solid var(--color-ink-4);
}

.intern__inner {
  max-width: var(--container-max);
  margin: 0 auto;
}

.intern__header {
  display: flex;
  align-items: baseline;
  gap: var(--space-3);
  margin-bottom: var(--space-6);
}

.section-title {
  font-family: var(--font-cjk);
  font-size: 22px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.section-tag {
  font-size: 13px;
  color: var(--color-ink-3);
}

.intern__wrap {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.intern__list {
  display: flex;
  gap: var(--space-5);
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  -ms-overflow-style: none;
  scrollbar-width: none;
  flex: 1;
}

.intern__list::-webkit-scrollbar { display: none; }

.intern-card {
  flex: 0 0 calc(33.333% - 14px);
  min-width: 240px;
  scroll-snap-align: start;
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.intern-card__company {
  font-family: var(--font-cjk);
  font-size: 18px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.intern-card__dept {
  font-size: 13px;
  color: var(--color-ink-2);
}

.intern-card__photo {
  height: 140px;
  background-color: #f2ebe4;
  border-radius: var(--radius-sm);
}

.intern-card__contrib {
  font-size: 13px;
  color: var(--color-ink-2);
  line-height: 1.7;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  flex: 1;
}

.intern-card__btn {
  padding: var(--space-3) 0;
  width: 100%;
  background-color: var(--color-primary);
  color: var(--color-ink-1);
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 600;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: opacity 0.2s;
  border: none;
}

.intern-card__btn:hover { opacity: 0.82; }

.intern__arrow {
  font-size: 28px;
  color: var(--color-ink-3);
  padding: var(--space-2) var(--space-1);
  cursor: pointer;
  background: none;
  border: none;
  flex-shrink: 0;
  transition: color 0.2s;
}

.intern__arrow:hover { color: var(--color-ink-1); }

@media (max-width: 767px) {
  .intern-card { flex: 0 0 85%; }
}
</style>
