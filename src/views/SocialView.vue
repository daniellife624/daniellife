<template>
  <div class="social">
    <div class="social__inner">

      <!-- Stage 1 + Stage 2 tabs — stacked vertically -->
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
        <!-- 活動列表 -->
        <div class="social__list">
          <div v-for="act in filteredActivities" :key="act.id" class="activity-card">
            <div class="activity-card__left">
              <div class="activity-card__header">
                <h3 class="activity-card__name">{{ act.name }}</h3>
                <span class="esg-badge" :class="`esg-badge--${act.esgType.toLowerCase()}`">{{ act.esgType }}</span>
              </div>
              <p class="activity-card__org">舉辦組織、單位：{{ act.organization }}</p>
              <p class="activity-card__contrib">主要貢獻&心得：{{ act.contribution }}</p>
            </div>
            <div class="activity-card__right">
              <div class="activity-card__photo"></div>
              <p class="activity-card__period">
                期間<br>From {{ act.periodFrom }}<br>To {{ act.periodTo }}
              </p>
              <button class="activity-card__btn" @click="openModal(act)">查看更多</button>
            </div>
          </div>
          <div v-if="!filteredActivities.length" class="social__empty">暫無符合條件的活動</div>
        </div>

        <!-- 右側 Filter Sidebar -->
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
          <button class="sidebar__btn" @click="applyFilter">篩選</button>
        </aside>
      </div>
    </div>

    <!-- Modal -->
    <Teleport to="body">
      <div v-if="activeModal" class="modal-backdrop" @click.self="closeModal">
        <div class="modal">
          <button class="modal__close" @click="closeModal">×</button>
          <div class="modal__header">
            <h3 class="modal__title">{{ activeModal.name }}</h3>
            <span class="esg-badge" :class="`esg-badge--${activeModal.esgType.toLowerCase()}`">{{ activeModal.esgType }}</span>
          </div>
          <p class="modal__info">舉辦組織、單位：{{ activeModal.organization }}</p>
          <p class="modal__info">期間：From {{ activeModal.periodFrom }} To {{ activeModal.periodTo }}</p>
          <div class="modal__photo"></div>
          <p class="modal__body-text">主要貢獻&心得：</p>
          <p class="modal__body-text">{{ activeModal.contribution }}</p>
          <p class="modal__body-text">{{ activeModal.reflection }}</p>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getSocialActivities } from '@/api/social'
import type { SocialActivity, EsgType } from '@/types/social'

const stage1 = ref<'esg' | 'sdgs'>('esg')
const esgSub = ref<'E' | 'S' | 'G'>('E')
const selectedEsg = ref<EsgType[]>([])
const selectedSdg = ref<number[]>([])
const appliedEsg = ref<EsgType[]>([])
const appliedSdg = ref<number[]>([])
const activities = ref<SocialActivity[]>([])
const activeModal = ref<SocialActivity | null>(null)

const stage1Tabs = [
  { key: 'esg', label: 'ESG分類' },
  { key: 'sdgs', label: 'SDGs分類' },
]

const esgOptions: EsgType[] = ['Environmental', 'Social', 'Governance']

const esgSubMap: Record<'E' | 'S' | 'G', EsgType> = {
  E: 'Environmental',
  S: 'Social',
  G: 'Governance',
}

const totalCount = computed(() => activities.value.length)

const filteredActivities = computed(() => {
  let list = activities.value
  if (stage1.value === 'esg') {
    const t = esgSubMap[esgSub.value]
    list = list.filter((a) => a.esgType === t)
  }
  if (appliedEsg.value.length) list = list.filter((a) => appliedEsg.value.includes(a.esgType))
  if (appliedSdg.value.length) list = list.filter((a) => a.sdgNumbers.some((n) => appliedSdg.value.includes(n)))
  return list
})

function applyFilter() {
  appliedEsg.value = [...selectedEsg.value]
  appliedSdg.value = [...selectedSdg.value]
}

function openModal(act: SocialActivity) { activeModal.value = act }
function closeModal() { activeModal.value = null }

onMounted(async () => {
  activities.value = await getSocialActivities()
})
</script>

<style scoped>
.social { padding: var(--space-6) var(--space-6) var(--space-8); }
.social__inner { max-width: var(--container-max); margin: 0 auto; }

/* Tabs */
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

/* Body */
.social__body { display: flex; gap: var(--space-6); align-items: flex-start; }
.social__list { flex: 1; display: flex; flex-direction: column; gap: var(--space-4); }
.social__empty { font-family: var(--font-cjk); font-size: 14px; color: var(--color-ink-3); text-align: center; padding: var(--space-8) 0; }

/* Activity card */
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

/* Sidebar */
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

/* Modal */
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.45); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: var(--color-white); border-radius: var(--radius-md); padding: var(--space-6); width: 560px; max-width: 90vw; max-height: 80vh; overflow-y: auto; position: relative; display: flex; flex-direction: column; gap: var(--space-3); }
.modal__close { position: absolute; top: var(--space-4); right: var(--space-4); font-size: 20px; background: none; border: none; cursor: pointer; color: var(--color-ink-3); }
.modal__header { display: flex; align-items: center; gap: var(--space-3); }
.modal__title { font-family: var(--font-cjk); font-size: 18px; font-weight: 700; color: var(--color-ink-1); }
.modal__info { font-family: var(--font-cjk); font-size: 13px; color: var(--color-ink-2); }
.modal__photo { height: 200px; background-color: #f5efea; border-radius: var(--radius-sm); }
.modal__body-text { font-family: var(--font-cjk); font-size: 14px; color: var(--color-ink-2); line-height: 1.8; }

@media (max-width: 767px) {
  .social__body { flex-direction: column; }
  .sidebar { width: 100%; }
  .activity-card { flex-direction: column; }
  .activity-card__right { width: 100%; }
}
</style>
