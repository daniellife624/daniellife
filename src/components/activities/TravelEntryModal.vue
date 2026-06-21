<template>
  <Teleport to="body">
    <div v-if="entry" class="modal-backdrop" @click.self="$emit('close')">
      <div class="modal travel-modal">
        <button class="modal__close" @click="$emit('close')">×</button>
        <div class="travel-modal__header">
          <span class="travel-modal__pin">📍</span>
          <h3 class="modal__title">{{ entry.country }}</h3>
        </div>
        <div class="travel-modal__meta-row">
          <span class="travel-modal__meta-item">城市：{{ entry.city }}</span>
          <span class="travel-modal__meta-item">洲別：{{ entry.continent }}</span>
          <span class="travel-modal__meta-item">造訪：{{ entry.visitedAt }}</span>
        </div>
        <div v-if="entry.photos?.length" class="modal__photos modal__photos--real">
          <img
            v-for="url in entry.photos"
            :key="url"
            :src="mediaUrl(url)"
            class="modal__photo-img"
            alt="旅行照片"
          />
        </div>
        <div v-else class="modal__photos">
          <div class="modal__photo"></div>
          <div class="modal__photo"></div>
        </div>
        <template v-if="entry.journal || entry.companions || entry.activities || entry.purchases">
          <div v-if="entry.companions" class="travel-modal__field">
            <span class="travel-modal__field-label">旅伴</span>
            <span class="travel-modal__field-value">{{ entry.companions }}</span>
          </div>
          <div v-if="entry.activities" class="travel-modal__field">
            <span class="travel-modal__field-label">主要活動</span>
            <span class="travel-modal__field-value">{{ entry.activities }}</span>
          </div>
          <div v-if="entry.purchases" class="travel-modal__field">
            <span class="travel-modal__field-label">購物清單</span>
            <span class="travel-modal__field-value">{{ entry.purchases }}</span>
          </div>
          <div v-if="entry.journal" class="travel-modal__journal">
            <p class="travel-modal__field-label">旅行日記</p>
            <p class="travel-modal__journal-text">{{ entry.journal }}</p>
          </div>
        </template>
        <p v-else class="travel-modal__empty">尚未填寫旅行見聞，可至後台新增。</p>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { mediaUrl } from '@/api/client'
import type { TravelEntry } from '@/types/activities'

defineProps<{ entry: TravelEntry | null }>()
defineEmits<{ close: [] }>()
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: var(--color-white);
  border-radius: var(--radius-md);
  padding: var(--space-6);
  width: 540px;
  max-width: 90vw;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.modal__close {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  font-size: 20px;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-ink-3);
}

.modal__title {
  font-family: var(--font-cjk);
  font-size: 18px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.modal__photos {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3);
  margin: var(--space-2) 0;
}

.modal__photos--real {
  grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
}

.modal__photo {
  height: 140px;
  background-color: #f5efea;
  border-radius: var(--radius-sm);
}

.modal__photo-img {
  width: 100%;
  height: 140px;
  object-fit: cover;
  border-radius: var(--radius-sm);
  display: block;
}

.travel-modal { gap: var(--space-4); }

.travel-modal__header {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.travel-modal__pin { font-size: 20px; }

.travel-modal__meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-4);
}

.travel-modal__meta-item {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-3);
}

.travel-modal__field {
  display: flex;
  gap: var(--space-3);
  align-items: baseline;
}

.travel-modal__field-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--color-ink-3);
  flex-shrink: 0;
  min-width: 60px;
}

.travel-modal__field-value {
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-2);
}

.travel-modal__journal {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.travel-modal__journal-text {
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-2);
  line-height: 1.8;
}

.travel-modal__empty {
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-3);
  font-style: italic;
}
</style>
