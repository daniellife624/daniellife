<template>
  <div class="social">
    <div class="social__inner">

      <div class="tab-row">
        <div class="tab-group">
          <button
            v-for="t in stage1Tabs"
            :key="t.key"
            class="tab-pill"
            :class="{ 'tab-pill--active-yellow': stage1 === t.key }"
            @click="stage1 = t.key as typeof stage1"
          >{{ t.label }}</button>
        </div>

        <div v-if="stage1 === 'esg'" class="tab-group">
          <button class="tab-pill" :class="{ 'tab-pill--active-yellow': esgSub === 'E' }" @click="esgSub = 'E'">E</button>
          <button class="tab-pill" :class="{ 'tab-pill--active-green': esgSub === 'S' }"  @click="esgSub = 'S'">S</button>
          <button class="tab-pill" :class="{ 'tab-pill--active-terra': esgSub === 'G' }"  @click="esgSub = 'G'">G</button>
        </div>
      </div>

      <div class="social__body">
        <div class="social__list">
          <ActivityCard
            v-for="act in filteredActivities"
            :key="act.id"
            :act="act"
            @view-more="activeModal = act"
          />
          <div v-if="!filteredActivities.length" class="social__empty">暫無符合條件的活動</div>
        </div>

        <FilterSidebar :total-count="totalCount" @apply="onApplyFilter" />
      </div>
    </div>

    <ActivityModal :activity="activeModal" @close="activeModal = null" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getSocialActivities } from '@/api/social'
import type { SocialActivity, EsgType } from '@/types/social'
import ActivityCard from '@/components/social/ActivityCard.vue'
import ActivityModal from '@/components/social/ActivityModal.vue'
import FilterSidebar from '@/components/social/FilterSidebar.vue'

const stage1 = ref<'all' | 'esg' | 'sdgs'>('all')
const esgSub = ref<'E' | 'S' | 'G'>('E')
const appliedEsg = ref<EsgType[]>([])
const appliedSdg = ref<number[]>([])
const activities = ref<SocialActivity[]>([])
const activeModal = ref<SocialActivity | null>(null)

const stage1Tabs = [
  { key: 'all', label: '全部' },
  { key: 'esg', label: 'ESG分類' },
  { key: 'sdgs', label: 'SDGs分類' },
]

const esgSubMap: Record<'E' | 'S' | 'G', EsgType> = {
  E: 'Environmental', S: 'Social', G: 'Governance',
}

const totalCount = computed(() => activities.value.length)

const filteredActivities = computed(() => {
  let list = activities.value
  if (stage1.value === 'esg') {
    const t = esgSubMap[esgSub.value]
    list = list.filter((a) => a.esgType === t)
  } else if (stage1.value === 'sdgs') {
    list = list.filter((a) => a.sdgNumbers.length > 0)
  }
  if (appliedEsg.value.length) list = list.filter((a) => a.esgType && appliedEsg.value.includes(a.esgType))
  if (appliedSdg.value.length) list = list.filter((a) => a.sdgNumbers.some((n) => appliedSdg.value.includes(n)))
  return list
})

function onApplyFilter(esg: EsgType[], sdg: number[]) {
  appliedEsg.value = esg
  appliedSdg.value = sdg
}

onMounted(async () => {
  activities.value = await getSocialActivities()
})
</script>

<style scoped>
.social { padding: var(--space-6) var(--space-6) var(--space-8); }
.social__inner { max-width: var(--container-max); margin: 0 auto; }

.tab-row {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: var(--space-2);
  margin-bottom: var(--space-5);
}

.tab-group {
  display: inline-flex;
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.tab-pill {
  padding: var(--space-2) var(--space-5);
  font-family: var(--font-cjk);
  font-size: 14px;
  background: transparent;
  border: none;
  cursor: pointer;
  color: var(--color-ink-2);
  transition: background 0.2s, color 0.2s;
}
.tab-pill--active-yellow { background: var(--color-primary); color: var(--color-ink-1); font-weight: 600; }
.tab-pill--active-green  { background: var(--color-secondary); color: #fff; font-weight: 600; }
.tab-pill--active-terra  { background: var(--color-tertiary); color: #fff; font-weight: 600; }

.social__body { display: flex; gap: var(--space-6); align-items: flex-start; }
.social__list { flex: 1; display: flex; flex-direction: column; gap: var(--space-4); }
.social__empty { font-family: var(--font-cjk); font-size: 14px; color: var(--color-ink-3); text-align: center; padding: var(--space-8) 0; }

@media (max-width: 767px) { .social__body { flex-direction: column; } }
</style>
