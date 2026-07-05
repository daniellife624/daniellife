<template>
  <div class="activity-card">
    <div class="activity-card__left">
      <div class="activity-card__header">
        <h3 class="activity-card__name">{{ act.name }}</h3>
        <span class="esg-badge" :class="`esg-badge--${act.esgType.toLowerCase()}`">{{ act.esgType }}</span>
      </div>
      <p class="activity-card__org">舉辦組織、單位：{{ act.organization }}</p>
      <p class="activity-card__contrib">主要貢獻&心得：{{ act.contribution }}</p>
    </div>
    <div class="activity-card__right">
      <div
        class="activity-card__photo"
        :style="act.photoUrl ? `background-image:url(${mediaUrl(act.photoUrl)});background-size:cover;background-position:${act.photoPosition || '50% 50%'}` : ''"
      ></div>
      <p class="activity-card__period">
        期間<br>From {{ act.periodFrom }}<br>To {{ act.periodTo }}
      </p>
      <button class="activity-card__btn" @click="$emit('view-more')">查看更多</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { mediaUrl } from '@/api/client'
import type { SocialActivity } from '@/types/social'

defineProps<{ act: SocialActivity }>()
defineEmits<{ 'view-more': [] }>()
</script>

<style scoped>
.activity-card {
  display: flex;
  gap: var(--space-5);
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-md);
  padding: var(--space-4) var(--space-5);
  background: var(--color-white);
}

.activity-card__left { flex: 1; display: flex; flex-direction: column; gap: var(--space-2); }
.activity-card__header { display: flex; align-items: center; gap: var(--space-3); flex-wrap: wrap; }
.activity-card__name { font-family: var(--font-cjk); font-size: 16px; font-weight: 700; color: var(--color-ink-1); }

.esg-badge { padding: 2px var(--space-2); border-radius: var(--radius-sm); font-size: 12px; font-weight: 600; }
.esg-badge--environmental { background: #E8C13A; color: var(--color-ink-1); }
.esg-badge--social        { background: #7A8C6E; color: #fff; }
.esg-badge--governance    { background: #C17055; color: #fff; }

.activity-card__org { font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-2); }
.activity-card__contrib {
  font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-2); line-height: 1.7;
  display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}

.activity-card__right { flex-shrink: 0; width: 160px; display: flex; flex-direction: column; gap: var(--space-2); }
.activity-card__photo { height: 90px; background-color: #f5efea; border-radius: var(--radius-sm); }
.activity-card__period { font-size: 12px; color: var(--color-ink-3); line-height: 1.6; text-align: right; }

.activity-card__btn {
  width: 100%; padding: var(--space-2) 0; background: var(--color-primary); border: none;
  border-radius: var(--radius-sm); font-family: var(--font-cjk); font-size: 13px; font-weight: 600;
  cursor: pointer; transition: opacity 0.2s;
}
.activity-card__btn:hover { opacity: 0.82; }

@media (max-width: 767px) {
  .activity-card { flex-direction: column; }
  .activity-card__right { width: 100%; }
}
</style>
