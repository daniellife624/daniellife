<template>
  <Teleport to="body">
    <div v-if="activity" class="modal-backdrop" @click.self="$emit('close')">
      <div class="modal">
        <button class="modal__close" @click="$emit('close')">×</button>
        <div class="modal__header">
          <h3 class="modal__title">{{ activity.name }}</h3>
          <span class="esg-badge" :class="`esg-badge--${activity.esgType.toLowerCase()}`">{{ activity.esgType }}</span>
        </div>
        <p class="modal__info">舉辦組織、單位：{{ activity.organization }}</p>
        <p class="modal__info">期間：From {{ activity.periodFrom }} To {{ activity.periodTo }}</p>
        <img v-if="activity.photoUrl" :src="mediaUrl(activity.photoUrl)" class="modal__photo modal__photo--img" alt="活動照片" />
        <div v-else class="modal__photo"></div>
        <p class="modal__body-text">主要貢獻&心得：</p>
        <p class="modal__body-text">{{ activity.contribution }}</p>
        <p class="modal__body-text">{{ activity.reflection }}</p>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { mediaUrl } from '@/api/client'
import type { SocialActivity } from '@/types/social'

defineProps<{ activity: SocialActivity | null }>()
defineEmits<{ close: [] }>()
</script>

<style scoped>
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.45); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: var(--color-white); border-radius: var(--radius-md); padding: var(--space-6); width: 560px; max-width: 90vw; max-height: 80vh; overflow-y: auto; position: relative; display: flex; flex-direction: column; gap: var(--space-3); }
.modal__close { position: absolute; top: var(--space-4); right: var(--space-4); font-size: 20px; background: none; border: none; cursor: pointer; color: var(--color-ink-3); }
.modal__header { display: flex; align-items: center; gap: var(--space-3); }
.modal__title { font-family: var(--font-cjk); font-size: 18px; font-weight: 700; color: var(--color-ink-1); }
.modal__info { font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-2); }
.modal__photo { height: 200px; background-color: #f5efea; border-radius: var(--radius-sm); }
.modal__photo--img { width: 100%; object-fit: cover; display: block; }
.modal__body-text { font-family: var(--font-cjk); font-size: 14px; color: var(--color-ink-2); line-height: 1.8; }

.esg-badge { padding: 2px var(--space-2); border-radius: var(--radius-sm); font-size: 12px; font-weight: 600; }
.esg-badge--environmental { background: #E8C13A; color: var(--color-ink-1); }
.esg-badge--social        { background: #7A8C6E; color: #fff; }
.esg-badge--governance    { background: #C17055; color: #fff; }
</style>
