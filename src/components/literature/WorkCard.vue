<template>
  <div class="work-card" :data-work-id="work.id">
    <div class="work-card__header">
      <h3 class="work-card__title">{{ work.title }}</h3>
      <button v-if="work.fullText" class="work-card__read-btn" @click="showFull = true">閱讀全文</button>
    </div>
    <div class="work-card__row">
      <span class="work-card__label">幾歲撰寫的作品</span>
      <span class="work-card__val work-card__val--yellow">{{ work.ageWritten }}歲</span>
    </div>
    <div class="work-card__row">
      <span class="work-card__label">撰寫期間</span>
      <span class="work-card__val work-card__val--yellow">{{ work.period }}</span>
    </div>
    <div class="work-card__row">
      <span class="work-card__label">得獎紀錄</span>
      <span class="work-card__val work-card__val--green">{{ work.awards }}</span>
    </div>
    <div class="work-card__row">
      <span class="work-card__label">摘要文字</span>
      <span class="work-card__val work-card__val--green">{{ work.summary }}</span>
    </div>
  </div>

  <Teleport to="body">
    <div v-if="showFull" class="fulltext-backdrop" @click.self="showFull = false">
      <div class="fulltext-modal">
        <div class="fulltext-modal__header">
          <h3 class="fulltext-modal__title">{{ work.title }}</h3>
          <button class="fulltext-modal__close" @click="showFull = false">×</button>
        </div>
        <div class="fulltext-modal__body">
          <pre class="fulltext-modal__text">{{ work.fullText }}</pre>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { LiteratureWork } from '@/types/literature'
defineProps<{ work: LiteratureWork }>()
const showFull = ref(false)
</script>

<style scoped>
.work-card {
  background: #ffffff;
  border: 1px solid #e0d8cc;
  border-radius: 3px;
  overflow: hidden;
  transition: border-color 0.25s, box-shadow 0.25s;
}

.work-card--highlight {
  border-color: #22c55e;
  box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.18);
}

.work-card__header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 10px var(--space-4);
  background: var(--color-primary);
  border-bottom: 1px solid rgba(0, 0, 0, 0.08);
  border-left: 3px solid rgba(0, 0, 0, 0.2);
}

.work-card__title {
  flex: 1;
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 700;
  color: #1a1000;
  letter-spacing: 0.04em;
}

.work-card__read-btn {
  padding: 3px 10px;
  background: transparent;
  color: #15803d;
  border: 1px solid #15803d;
  border-radius: 2px;
  font-family: 'Courier New', monospace;
  font-size: 11px;
  cursor: pointer;
  letter-spacing: 0.06em;
  transition: background 0.2s;
  white-space: nowrap;
}
.work-card__read-btn:hover { background: rgba(21, 128, 61, 0.1); }

.work-card__row {
  display: flex;
  align-items: stretch;
  border-bottom: 1px solid #f0ece6;
}
.work-card__row:last-child { border-bottom: none; }

.work-card__label {
  width: 108px;
  flex-shrink: 0;
  padding: 8px var(--space-3);
  font-family: var(--font-cjk);
  font-size: 11px;
  color: var(--color-ink-3);
  display: flex;
  align-items: center;
  background: #f5f0e8;
  border-right: 1px solid #e0d8cc;
}

.work-card__val {
  flex: 1;
  padding: 8px var(--space-3);
  font-family: 'Courier New', monospace;
  font-size: 13px;
  font-weight: 600;
  display: flex;
  align-items: center;
  background: #ffffff;
  min-height: 36px;
  word-break: break-all;
}

.work-card__val--yellow { color: #7a5800; }
.work-card__val--green  { color: #166534; }

.fulltext-backdrop {
  position: fixed; inset: 0; background: rgba(0,0,0,0.5);
  display: flex; align-items: center; justify-content: center; z-index: 1000;
}
.fulltext-modal {
  background: #fff; border-radius: 4px; width: 680px; max-width: 92vw;
  max-height: 80vh; display: flex; flex-direction: column; overflow: hidden;
}
.fulltext-modal__header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 20px; background: var(--color-primary);
  border-bottom: 1px solid rgba(0,0,0,0.08);
}
.fulltext-modal__title {
  font-family: var(--font-cjk); font-size: 16px; font-weight: 700; color: #1a1000;
}
.fulltext-modal__close {
  background: none; border: none; font-size: 20px; cursor: pointer; color: #555; line-height: 1;
}
.fulltext-modal__body { flex: 1; overflow-y: auto; padding: 20px; }
.fulltext-modal__text {
  font-family: var(--font-cjk); font-size: 14px; color: var(--color-ink-1);
  line-height: 2; white-space: pre-wrap; word-break: break-word; margin: 0;
}
</style>
