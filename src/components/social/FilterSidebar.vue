<template>
  <aside class="sidebar">
    <h4 class="sidebar__title">類別</h4>

    <p class="sidebar__sub">ESG 分類</p>
    <label v-for="esg in esgOptions" :key="esg" class="sidebar__label">
      <input type="checkbox" v-model="selectedEsg" :value="esg" class="sidebar__checkbox" />
      {{ esg }}
    </label>

    <p class="sidebar__sub sidebar__sub--mt">SDGs 分類</p>
    <label v-for="n in 5" :key="n" class="sidebar__label">
      <input type="checkbox" v-model="selectedSdg" :value="n" class="sidebar__checkbox" />
      {{ n }}
    </label>

    <div class="sidebar__count-row">
      <span class="sidebar__count">總共有<br>{{ totalCount }} 個</span>
    </div>
    <button class="sidebar__btn" @click="apply">篩選</button>
  </aside>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { EsgType } from '@/types/social'

defineProps<{ totalCount: number }>()
const emit = defineEmits<{ apply: [esg: EsgType[], sdg: number[]] }>()

const esgOptions: EsgType[] = ['Environmental', 'Social', 'Governance']
const selectedEsg = ref<EsgType[]>([])
const selectedSdg = ref<number[]>([])

function apply() {
  emit('apply', [...selectedEsg.value], [...selectedSdg.value])
}
</script>

<style scoped>
.sidebar {
  flex-shrink: 0; width: 180px; border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-md); padding: var(--space-4); display: flex; flex-direction: column; gap: var(--space-2);
}
.sidebar__title { font-family: var(--font-cjk); font-size: 14px; font-weight: 700; color: var(--color-ink-1); }
.sidebar__sub { font-family: var(--font-cjk); font-size: 12px; font-weight: 600; color: var(--color-ink-2); }
.sidebar__sub--mt { margin-top: var(--space-2); }
.sidebar__label { display: flex; align-items: center; gap: var(--space-2); font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-2); cursor: pointer; }
.sidebar__checkbox { accent-color: var(--color-primary); }
.sidebar__count-row { margin-top: var(--space-2); display: flex; justify-content: flex-end; }
.sidebar__count { background: #ef4444; color: #fff; font-size: 12px; font-weight: 700; padding: var(--space-2); border-radius: var(--radius-sm); text-align: center; line-height: 1.4; }
.sidebar__btn {
  width: 100%; padding: var(--space-2) 0; background: var(--color-primary); border: none;
  border-radius: var(--radius-full); font-family: var(--font-cjk); font-size: 14px; font-weight: 600;
  cursor: pointer; transition: opacity 0.2s; margin-top: var(--space-2);
}
.sidebar__btn:hover { opacity: 0.82; }

@media (max-width: 767px) { .sidebar { width: 100%; } }
</style>
