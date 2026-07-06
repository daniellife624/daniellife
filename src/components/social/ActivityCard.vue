<template>
  <div class="activity-card">
    <div class="activity-card__left">
      <div class="activity-card__header">
        <h3 class="activity-card__name">{{ act.name }}</h3>
        <a v-if="act.youtubeUrl" :href="act.youtubeUrl" target="_blank" class="activity-card__yt-icon" title="YouTube">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M23.5 6.2a3.02 3.02 0 0 0-2.12-2.14C19.54 3.6 12 3.6 12 3.6s-7.54 0-9.38.47A3.02 3.02 0 0 0 .5 6.2C0 8.05 0 12 0 12s0 3.95.5 5.8a3.02 3.02 0 0 0 2.12 2.14C4.46 20.4 12 20.4 12 20.4s7.54 0 9.38-.46a3.02 3.02 0 0 0 2.12-2.14C24 15.95 24 12 24 12s0-3.95-.5-5.8zM9.6 15.6V8.4l6.27 3.6-6.27 3.6z"/></svg>
        </a>
        <span v-if="act.esgType" class="esg-badge" :class="`esg-badge--${act.esgType.toLowerCase()}`">{{ act.esgType }}</span>
        <template v-else>
          <span v-for="n in act.sdgNumbers" :key="n" class="sdg-badge">SDG {{ n }}・{{ SDG_LABELS[n] }}</span>
        </template>
      </div>
      <p class="activity-card__org">舉辦組織、單位：{{ act.organization }}</p>
      <p class="activity-card__contrib">心得：{{ act.reflection }}</p>
    </div>
    <div class="activity-card__right">
      <div
        class="activity-card__photo"
        :style="act.photos[0] ? `background-image:url(${mediaUrl(act.photos[0].url)});background-size:cover;background-position:${act.photos[0].position || '50% 50%'}` : ''"
      ></div>
      <p class="activity-card__period">
        From {{ act.periodFrom }}<br>To {{ act.periodTo }}
      </p>
      <button class="activity-card__btn" @click="$emit('view-more')">查看更多</button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { mediaUrl } from '@/api/client'
import type { SocialActivity } from '@/types/social'
import { SDG_LABELS } from '@/data/sdgLabels'

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

.activity-card__yt-icon {
  width: 22px; height: 22px; flex-shrink: 0;
  border: 1px solid var(--color-ink-4); border-radius: var(--radius-sm);
  display: flex; align-items: center; justify-content: center;
  color: var(--color-ink-2); transition: color 0.2s, border-color 0.2s;
}
.activity-card__yt-icon:hover { color: var(--color-ink-1); border-color: var(--color-ink-2); }

.esg-badge { padding: 2px var(--space-2); border-radius: var(--radius-sm); font-size: 12px; font-weight: 600; }
.esg-badge--environmental { background: #E8C13A; color: var(--color-ink-1); }
.esg-badge--social        { background: #7A8C6E; color: #fff; }
.esg-badge--governance    { background: #C17055; color: #fff; }

.sdg-badge {
  padding: 2px var(--space-2);
  border-radius: var(--radius-sm);
  font-size: 12px;
  font-weight: 600;
  background: var(--color-primary);
  color: var(--color-ink-1);
}

.activity-card__org { font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-2); }
.activity-card__contrib {
  font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-2); line-height: 1.7;
  display: -webkit-box; -webkit-line-clamp: 6; -webkit-box-orient: vertical; overflow: hidden;
  white-space: pre-wrap;
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
