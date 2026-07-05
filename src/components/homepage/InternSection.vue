<template>
  <section class="intern">
    <div class="intern__inner">
      <div class="intern__header">
        <div class="intern__header-left">
          <h2 class="section-title">實習經驗</h2>
          <span class="section-tag">金融業 X 四大事務所</span>
        </div>
      </div>
      <div class="intern__wrap">
        <div class="intern__list" ref="listEl">
          <article v-for="item in interns" :key="item.id" class="intern-card">
            <h3 class="intern-card__company">{{ item.company }}</h3>
            <p class="intern-card__dept">部門/職稱：{{ item.dept }}/{{ item.role }}</p>
            <div class="intern-card__photo">
              <img
                v-if="item.photoUrl"
                :src="mediaUrl(item.photoUrl)"
                :alt="item.company"
                class="intern-card__photo-img"
                :style="{ objectPosition: item.photoPosition || '50% 50%' }"
              />
              <span v-else class="intern-card__photo-hint">尚未上傳照片</span>
            </div>
            <p class="intern-card__contrib">主要貢獻：{{ item.contribution }}</p>
            <button class="intern-card__btn" @click="activeIntern = item">查看更多</button>
          </article>
        </div>
        <button class="intern__arrow" @click="scrollNext" aria-label="下一頁">›</button>
      </div>
    </div>
  </section>

  <!-- Detail Modal -->
  <Teleport to="body">
    <div v-if="activeIntern" class="intern-modal-backdrop" @click.self="activeIntern = null">
      <div class="intern-modal">
        <button class="intern-modal__close" @click="activeIntern = null">×</button>
        <h3 class="intern-modal__company">{{ activeIntern.company }}</h3>
        <p class="intern-modal__meta">部門：{{ activeIntern.dept }}　　職稱：{{ activeIntern.role }}</p>
        <p class="intern-modal__meta">實習期間：{{ activeIntern.period }}</p>
        <div class="intern-modal__photo">
          <img
            v-if="activeIntern.photoUrl"
            :src="mediaUrl(activeIntern.photoUrl)"
            :alt="activeIntern.company"
            class="intern-modal__photo-img"
            :style="{ objectPosition: activeIntern.photoPosition || '50% 50%' }"
          />
          <span v-else class="intern-modal__photo-hint">尚未上傳照片</span>
        </div>
        <div class="intern-modal__section">
          <p class="intern-modal__label">主要貢獻</p>
          <p class="intern-modal__text">{{ activeIntern.contribution }}</p>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getInternships } from '@/api/homepage'
import { mediaUrl } from '@/api/client'
import type { Internship } from '@/types/homepage'

const listEl = ref<HTMLElement | null>(null)
const interns = ref<Internship[]>([])
const activeIntern = ref<Internship | null>(null)

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
  justify-content: space-between;
  margin-bottom: var(--space-6);
}

.intern__header-left {
  display: flex;
  align-items: baseline;
  gap: var(--space-3);
}

.intern__sort {
  font-family: var(--font-cjk);
  font-size: 12px;
  color: #fff;
  background-color: var(--color-tertiary);
  padding: 3px 10px;
  border-radius: var(--radius-full);
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
  aspect-ratio: 4 / 3;
  background-color: var(--color-primary);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.intern-card__photo-hint {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-1);
}

.intern-card__photo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
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
  white-space: pre-wrap;
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

/* ── Intern Detail Modal ── */
.intern-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.intern-modal {
  background: var(--color-white);
  border-radius: var(--radius-md);
  padding: var(--space-6);
  width: 520px;
  max-width: 90vw;
  max-height: 85vh;
  overflow-y: auto;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.intern-modal__close {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  font-size: 20px;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-ink-3);
  line-height: 1;
  transition: color 0.2s;
}
.intern-modal__close:hover { color: var(--color-ink-1); }

.intern-modal__company {
  font-family: var(--font-cjk);
  font-size: 20px;
  font-weight: 700;
  color: var(--color-ink-1);
  padding-right: var(--space-6);
}

.intern-modal__meta {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
}

.intern-modal__photo {
  aspect-ratio: 4 / 3;
  background-color: var(--color-primary);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.intern-modal__photo-hint {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-1);
}

.intern-modal__photo-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: var(--radius-sm);
}

.intern-modal__section { display: flex; flex-direction: column; gap: var(--space-2); }

.intern-modal__label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--color-ink-3);
}

.intern-modal__text {
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-2);
  line-height: 1.8;
  white-space: pre-wrap;
}
</style>
