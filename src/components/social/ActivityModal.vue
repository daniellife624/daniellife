<template>
  <Teleport to="body">
    <div v-if="activity" class="modal-backdrop" @click.self="$emit('close')">
      <div class="modal">
        <button class="modal__close" @click="$emit('close')">×</button>
        <div class="modal__header">
          <h3 class="modal__title">{{ activity.name }}</h3>
          <div class="modal__badges">
            <a v-if="activity.youtubeUrl" :href="activity.youtubeUrl" target="_blank" class="modal__yt-icon" title="YouTube">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><path d="M23.5 6.2a3.02 3.02 0 0 0-2.12-2.14C19.54 3.6 12 3.6 12 3.6s-7.54 0-9.38.47A3.02 3.02 0 0 0 .5 6.2C0 8.05 0 12 0 12s0 3.95.5 5.8a3.02 3.02 0 0 0 2.12 2.14C4.46 20.4 12 20.4 12 20.4s7.54 0 9.38-.46a3.02 3.02 0 0 0 2.12-2.14C24 15.95 24 12 24 12s0-3.95-.5-5.8zM9.6 15.6V8.4l6.27 3.6-6.27 3.6z"/></svg>
            </a>
            <span v-if="activity.esgType" class="esg-badge" :class="`esg-badge--${activity.esgType.toLowerCase()}`">{{ activity.esgType }}</span>
            <template v-else>
              <span v-for="n in activity.sdgNumbers" :key="n" class="sdg-badge">SDG {{ n }}・{{ SDG_LABELS[n] }}</span>
            </template>
          </div>
        </div>
        <p class="modal__info">舉辦組織、單位：{{ activity.organization }}</p>
        <p class="modal__info">From {{ activity.periodFrom }}</p>
        <p class="modal__info">To {{ activity.periodTo }}</p>

        <div v-if="activity.photos.length" class="modal__photos modal__photos--real">
          <img
            v-for="photo in activity.photos"
            :key="photo.url"
            :src="mediaUrl(photo.url)"
            class="modal__photo-img"
            alt="活動照片"
            :style="{ objectPosition: photo.position || '50% 50%' }"
          />
        </div>
        <div v-else class="modal__photo"></div>

        <p class="modal__body-label">心得</p>
        <p class="modal__body-text">{{ activity.reflection }}</p>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { mediaUrl } from '@/api/client'
import type { SocialActivity } from '@/types/social'
import { SDG_LABELS } from '@/data/sdgLabels'

defineProps<{ activity: SocialActivity | null }>()
defineEmits<{ close: [] }>()
</script>

<style scoped>
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.45); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: var(--color-white); border-radius: var(--radius-md); padding: var(--space-6); width: 560px; max-width: 90vw; max-height: 80vh; overflow-y: auto; position: relative; display: flex; flex-direction: column; gap: var(--space-3); }
.modal__close { position: absolute; top: var(--space-4); right: var(--space-4); font-size: 20px; background: none; border: none; cursor: pointer; color: var(--color-ink-3); }
.modal__header { display: flex; flex-direction: column; gap: var(--space-2); }
.modal__title { font-family: var(--font-cjk); font-size: 18px; font-weight: 700; color: var(--color-ink-1); padding-right: var(--space-6); }
.modal__badges { display: flex; align-items: center; gap: var(--space-2); flex-wrap: wrap; }
.modal__info { font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-2); }

.modal__photo { height: 200px; background-color: #f5efea; border-radius: var(--radius-sm); }
.modal__photos {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: var(--space-3);
}
.modal__photo-img {
  width: 100%;
  height: 160px;
  object-fit: cover;
  border-radius: var(--radius-sm);
  display: block;
}

.modal__body-label {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--color-ink-3);
}
.modal__body-text { font-family: var(--font-cjk); font-size: 14px; color: var(--color-ink-2); line-height: 1.8; white-space: pre-wrap; }

.modal__yt-icon {
  width: 26px; height: 26px; flex-shrink: 0;
  border: 1px solid var(--color-ink-4); border-radius: var(--radius-sm);
  display: flex; align-items: center; justify-content: center;
  color: var(--color-ink-2); transition: color 0.2s, border-color 0.2s;
}
.modal__yt-icon:hover { color: var(--color-ink-1); border-color: var(--color-ink-2); }

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
</style>
