<template>
  <Teleport to="body">
    <div v-if="experience" class="modal-backdrop" @click.self="$emit('close')">
      <div class="modal">
        <button class="modal__close" @click="$emit('close')">×</button>
        <h3 class="modal__title">{{ experience.title }}</h3>
        <p class="modal__info">服務機構：{{ experience.organization }}</p>
        <p class="modal__info">服務期間：{{ experience.period }}</p>
        <div v-if="experience.photos?.length" class="modal__photos modal__photos--real">
          <img
            v-for="url in experience.photos"
            :key="url"
            :src="mediaUrl(url)"
            class="modal__photo-img"
            alt="活動照片"
          />
        </div>
        <div v-else class="modal__photos">
          <div class="modal__photo"></div>
          <div class="modal__photo"></div>
        </div>
        <p class="modal__contrib">{{ experience.contribution }}</p>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { mediaUrl } from '@/api/client'
import type { Experience } from '@/types/activities'

defineProps<{ experience: Experience | null }>()
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

.modal__info {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
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

.modal__contrib {
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-2);
  line-height: 1.8;
}
</style>
