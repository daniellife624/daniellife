<template>
  <div class="exp-card">
    <div class="exp-card__left">
      <h3 class="exp-card__title">{{ item.title }}</h3>
      <p class="exp-card__info">服務機構：{{ item.organization }}</p>
      <p class="exp-card__info">服務期間：{{ item.period }}</p>
      <p class="exp-card__contrib">主要貢獻：{{ item.contribution }}</p>
    </div>
    <div class="exp-card__right">
      <div class="exp-card__photos">
        <template v-if="item.photos?.length">
          <img
            v-for="photo in item.photos.slice(0, 2)"
            :key="photo.url"
            :src="mediaUrl(photo.url)"
            class="exp-card__photo exp-card__photo--img"
            alt="活動照片"
            :style="{ objectPosition: photo.position || '50% 50%' }"
          />
          <div v-for="i in Math.max(0, 2 - item.photos.length)" :key="'p'+i" class="exp-card__photo"></div>
        </template>
        <template v-else>
          <div class="exp-card__photo"></div>
          <div class="exp-card__photo"></div>
        </template>
      </div>
      <button class="exp-card__btn" @click="$emit('view-more')">查看更多</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { mediaUrl } from '@/api/client'
import type { Experience } from '@/types/activities'

defineProps<{ item: Experience }>()
defineEmits<{ 'view-more': [] }>()
</script>

<style scoped>
.exp-card {
  display: flex;
  gap: var(--space-5);
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-md);
  padding: var(--space-5);
  background: var(--color-white);
}

.exp-card__left {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.exp-card__title {
  font-family: var(--font-cjk);
  font-size: 17px;
  font-weight: 700;
  color: var(--color-ink-1);
}

.exp-card__info {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
}

.exp-card__contrib {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
  line-height: 1.7;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  white-space: pre-wrap;
}

.exp-card__right {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  width: 260px;
}

.exp-card__photos {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-2);
}

.exp-card__photo {
  height: 100px;
  background-color: #f5efea;
  border-radius: var(--radius-sm);
}

.exp-card__photo--img {
  width: 100%;
  object-fit: cover;
  background-color: transparent;
}

.exp-card__btn {
  width: 100%;
  padding: var(--space-3) 0;
  background-color: var(--color-primary);
  color: var(--color-ink-1);
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 600;
  border-radius: var(--radius-sm);
  border: none;
  cursor: pointer;
  transition: opacity 0.2s;
}

.exp-card__btn:hover { opacity: 0.82; }

@media (max-width: 767px) {
  .exp-card { flex-direction: column; }
  .exp-card__right { width: 100%; }
}
</style>
