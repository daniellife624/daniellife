<template>
  <div class="donut-wrap">
    <svg class="donut" viewBox="0 0 120 120">
      <circle class="donut__track" cx="60" cy="60" r="46" />
      <circle
        class="donut__slice"
        :style="{ stroke: slices[0].color }"
        cx="60" cy="60" r="46"
        :stroke-dasharray="`${arc0} ${circumference - arc0}`"
        stroke-dashoffset="0"
      />
      <circle
        class="donut__slice"
        :style="{ stroke: slices[1].color }"
        cx="60" cy="60" r="46"
        :stroke-dasharray="`${arc1} ${circumference - arc1}`"
        :stroke-dashoffset="-(arc0)"
      />
    </svg>
    <div class="donut-legend">
      <div v-for="(s, i) in slices" :key="i" class="donut-legend__item">
        <span class="donut-legend__dot" :style="{ background: s.color }"></span>
        <span>{{ s.label }} {{ s.pct }}%</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  slices: { label: string; pct: number; color: string }[]
}>()

const circumference = 2 * Math.PI * 46
const arc0 = computed(() => (props.slices[0].pct / 100) * circumference)
const arc1 = computed(() => (props.slices[1].pct / 100) * circumference)
</script>

<style scoped>
.donut-wrap { display: flex; flex-direction: column; align-items: center; gap: var(--space-3); }
.donut { width: 120px; height: 120px; transform: rotate(-90deg); }

.donut__track { fill: none; stroke: var(--color-ink-4); stroke-width: 16; }
.donut__slice { fill: none; stroke-width: 16; stroke-linecap: butt; transition: stroke-dasharray 0.8s ease; }

.donut-legend { display: flex; flex-direction: column; gap: var(--space-2); align-self: flex-start; padding-left: var(--space-2); }
.donut-legend__item { display: flex; align-items: center; gap: var(--space-2); font-size: 13px; color: var(--color-ink-2); }
.donut-legend__dot { width: 10px; height: 10px; border-radius: 2px; flex-shrink: 0; }
</style>
