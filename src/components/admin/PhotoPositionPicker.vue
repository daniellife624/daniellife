<template>
  <div class="ppp" @click="handleClick">
    <img :src="src" class="ppp__img" :style="{ objectPosition: position || '50% 50%' }" alt="" />
    <div class="ppp__hint">點擊調整焦點</div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ src: string; position: string }>()
const emit = defineEmits<{ 'update:position': [position: string] }>()

function handleClick(e: MouseEvent) {
  const target = e.currentTarget as HTMLElement
  const rect = target.getBoundingClientRect()
  const clamp = (n: number) => Math.min(100, Math.max(0, n))
  const x = clamp(Math.round(((e.clientX - rect.left) / rect.width) * 100))
  const y = clamp(Math.round(((e.clientY - rect.top) / rect.height) * 100))
  emit('update:position', `${x}% ${y}%`)
}
</script>

<style scoped>
.ppp {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
  cursor: crosshair;
}

.ppp__img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.ppp__hint {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  color: #fff;
  font-size: 10px;
  text-align: center;
  padding: 2px 0;
  font-family: var(--font-cjk);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.15s;
}

.ppp:hover .ppp__hint { opacity: 1; }
</style>
