<template>
  <div class="admin">

    <!-- Sidebar -->
    <aside class="admin__sidebar">
      <p class="admin__sidebar-title">資料管理</p>
      <button
        v-for="sec in sections"
        :key="sec.key"
        class="admin__sidebar-item"
        :class="{ 'admin__sidebar-item--active': current === sec.key }"
        @click="current = sec.key"
      >
        {{ sec.label }}
      </button>
      <div class="admin__sidebar-divider"></div>
      <button class="admin__logout" @click="logout">登出</button>
    </aside>

    <!-- Main Content -->
    <main class="admin__main">

      <AdminTable
        v-if="current === 'internships'"
        title="實習經歷"
        :columns="['公司', '部門', '職稱', '期間']"
        :rows="interns.map(i => [i.company, i.dept, i.role, i.period])"
        :ids="interns.map(i => i.id)"
        @add="openAdd"
        @edit="openEdit"
        @delete="deleteItem"
      />

      <AdminTable
        v-if="current === 'projects'"
        title="作品集"
        :columns="['名稱', '類型', '技術', '人數', '期間']"
        :rows="projects.map(p => [p.name, p.type, p.tech, String(p.members), p.period])"
        :ids="projects.map(p => p.id)"
        @add="openAdd"
        @edit="openEdit"
        @delete="deleteItem"
      />

      <AdminTable
        v-if="current === 'activities'"
        title="課外活動"
        :columns="['標題', '組織', '類型', '期間']"
        :rows="experiences.map(e => [e.title, e.organization, e.type, e.period])"
        :ids="experiences.map(e => e.id)"
        @add="openAdd"
        @edit="openEdit"
        @delete="deleteItem"
      />

      <AdminTable
        v-if="current === 'social'"
        title="社會參與"
        :columns="['名稱', 'ESG', '組織', '開始', '結束']"
        :rows="socialActivities.map(a => [a.name, a.esgType, a.organization, a.periodFrom, a.periodTo])"
        :ids="socialActivities.map(a => a.id)"
        @add="openAdd"
        @edit="openEdit"
        @delete="deleteItem"
      />

      <AdminTable
        v-if="current === 'literature'"
        title="文學作品"
        :columns="['標題', '撰寫年齡', '期間', '得獎紀錄']"
        :rows="literatureWorks.map(w => [w.title, w.ageWritten + '歲', w.period, w.awards])"
        :ids="literatureWorks.map(w => w.id)"
        @add="openAdd"
        @edit="openEdit"
        @delete="deleteItem"
      />

      <AdminTable
        v-if="current === 'papers'"
        title="論文文獻"
        :columns="['主題', '期刊', '作者', '年份']"
        :rows="papers.map(p => [p.topic, p.journal, p.authors, String(p.year)])"
        :ids="papers.map(p => p.id)"
        @add="openAdd"
        @edit="openEdit"
        @delete="deleteItem"
      />

      <AdminTable
        v-if="current === 'holdings'"
        title="持股明細"
        :columns="['股票代碼', '名稱', '幣別', '券商', '股數', '均價', '市價']"
        :rows="holdings.map(h => [h.symbol, h.name, h.currency, h.broker, String(h.shares), String(h.avgPrice), String(h.marketPrice)])"
        :ids="holdings.map(h => h.id)"
        @add="openAdd"
        @edit="openEdit"
        @delete="deleteItem"
      />

    </main>

    <!-- Edit / Add Modal -->
    <Teleport to="body">
      <div v-if="modalOpen" class="modal-backdrop" @click.self="modalOpen = false">
        <div class="modal">
          <button class="modal__close" @click="modalOpen = false">×</button>
          <h3 class="modal__title">
            {{ modalMode === 'add' ? '新增' : '編輯' }}：{{ currentSectionLabel }}
          </h3>
          <div class="modal__fields">
            <label v-for="field in modalFields" :key="field.key" class="modal__label">
              {{ field.label }}
              <textarea
                v-if="field.type === 'textarea'"
                v-model="formData[field.key]"
                class="modal__textarea"
                rows="3"
              ></textarea>
              <input
                v-else
                v-model="formData[field.key]"
                class="modal__input"
                :type="field.type ?? 'text'"
                :placeholder="field.label"
              />
            </label>
          </div>
          <div class="modal__actions">
            <button class="modal__btn modal__btn--cancel" @click="modalOpen = false">取消</button>
            <button class="modal__btn modal__btn--save" @click="saveModal">儲存</button>
          </div>
        </div>
      </div>
    </Teleport>

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AdminTable from '@/components/admin/AdminTable.vue'
import { getInternships, getProjects } from '@/api/homepage'
import { getExperiences } from '@/api/activities'
import { getSocialActivities } from '@/api/social'
import { getLiteratureWorks } from '@/api/literature'
import { getThesisPapers } from '@/api/thesis'
import { getHoldings } from '@/api/finance'
import type { Internship, Project } from '@/types/homepage'
import type { Experience } from '@/types/activities'
import type { SocialActivity } from '@/types/social'
import type { LiteratureWork } from '@/types/literature'
import type { ThesisPaper } from '@/types/thesis'
import type { Holding } from '@/types/finance'

const router = useRouter()
const auth = useAuthStore()

type SectionKey = 'internships' | 'projects' | 'activities' | 'social' | 'literature' | 'papers' | 'holdings'

const sections: { key: SectionKey; label: string }[] = [
  { key: 'internships', label: '實習經歷' },
  { key: 'projects',    label: '作品集' },
  { key: 'activities',  label: '課外活動' },
  { key: 'social',      label: '社會參與' },
  { key: 'literature',  label: '文學作品' },
  { key: 'papers',      label: '論文文獻' },
  { key: 'holdings',    label: '持股明細' },
]

const current = ref<SectionKey>('internships')
const currentSectionLabel = computed(() => sections.find((s) => s.key === current.value)?.label ?? '')

// ── Data ──
const interns          = ref<Internship[]>([])
const projects         = ref<Project[]>([])
const experiences      = ref<Experience[]>([])
const socialActivities = ref<SocialActivity[]>([])
const literatureWorks  = ref<LiteratureWork[]>([])
const papers           = ref<ThesisPaper[]>([])
const holdings         = ref<Holding[]>([])

onMounted(async () => {
  ;[
    interns.value,
    projects.value,
    experiences.value,
    socialActivities.value,
    literatureWorks.value,
    papers.value,
    holdings.value,
  ] = await Promise.all([
    getInternships(),
    getProjects(),
    getExperiences(),
    getSocialActivities(),
    getLiteratureWorks(),
    getThesisPapers(),
    getHoldings(),
  ])
})

// ── Modal ──
const modalOpen = ref(false)
const modalMode = ref<'add' | 'edit'>('add')
const editId    = ref<number | null>(null)
const formData  = ref<Record<string, string>>({})

type FieldDef = { key: string; label: string; type?: string }

const fieldMap: Record<SectionKey, FieldDef[]> = {
  internships: [
    { key: 'company',      label: '公司' },
    { key: 'dept',         label: '部門' },
    { key: 'role',         label: '職稱' },
    { key: 'period',       label: '期間' },
    { key: 'contribution', label: '主要貢獻', type: 'textarea' },
  ],
  projects: [
    { key: 'name',    label: '名稱' },
    { key: 'type',    label: '類型 (code / uiux / finance)' },
    { key: 'tech',    label: '技術' },
    { key: 'members', label: '成員人數', type: 'number' },
    { key: 'period',  label: '期間' },
    { key: 'core',    label: '核心功能', type: 'textarea' },
  ],
  activities: [
    { key: 'title',        label: '標題' },
    { key: 'organization', label: '組織' },
    { key: 'type',         label: '類型 (leadership / club)' },
    { key: 'period',       label: '期間' },
    { key: 'contribution', label: '主要貢獻', type: 'textarea' },
  ],
  social: [
    { key: 'name',         label: '名稱' },
    { key: 'esgType',      label: 'ESG (Environmental / Social / Governance)' },
    { key: 'organization', label: '組織' },
    { key: 'periodFrom',   label: '開始日期' },
    { key: 'periodTo',     label: '結束日期' },
    { key: 'contribution', label: '主要貢獻', type: 'textarea' },
  ],
  literature: [
    { key: 'title',      label: '標題' },
    { key: 'ageWritten', label: '撰寫年齡', type: 'number' },
    { key: 'period',     label: '撰寫期間' },
    { key: 'awards',     label: '得獎紀錄' },
    { key: 'summary',    label: '摘要', type: 'textarea' },
  ],
  papers: [
    { key: 'topic',        label: '主題' },
    { key: 'name',         label: '論文名稱', type: 'textarea' },
    { key: 'journal',      label: '期刊' },
    { key: 'authors',      label: '作者' },
    { key: 'year',         label: '年份', type: 'number' },
    { key: 'purpose',      label: '研究目的', type: 'textarea' },
    { key: 'contribution', label: '主要貢獻', type: 'textarea' },
  ],
  holdings: [
    { key: 'symbol',      label: '股票代碼' },
    { key: 'name',        label: '名稱' },
    { key: 'currency',    label: '幣別 (TWD / USD)' },
    { key: 'broker',      label: '券商' },
    { key: 'shares',      label: '股數', type: 'number' },
    { key: 'avgPrice',    label: '均價', type: 'number' },
    { key: 'marketPrice', label: '市價', type: 'number' },
  ],
}

const modalFields = computed<FieldDef[]>(() => fieldMap[current.value] ?? [])

function openAdd() {
  modalMode.value = 'add'
  editId.value = null
  formData.value = Object.fromEntries(fieldMap[current.value].map((f) => [f.key, '']))
  modalOpen.value = true
}

function openEdit(id: number) {
  modalMode.value = 'edit'
  editId.value = id
  const dataMap: Record<SectionKey, { id: number }[]> = {
    internships: interns.value,
    projects:    projects.value,
    activities:  experiences.value,
    social:      socialActivities.value,
    literature:  literatureWorks.value,
    papers:      papers.value,
    holdings:    holdings.value,
  }
  const item = dataMap[current.value].find((x) => x.id === id) as Record<string, unknown> | undefined
  if (item) {
    formData.value = Object.fromEntries(
      fieldMap[current.value].map((f) => [f.key, String(item[f.key] ?? '')])
    )
  }
  modalOpen.value = true
}

function saveModal() {
  // TODO: call apiFetch PUT / POST with formData when backend is ready
  console.log('[Admin] save', current.value, modalMode.value, formData.value)
  modalOpen.value = false
}

function deleteItem(id: number) {
  if (!confirm('確定刪除這筆資料？')) return
  // TODO: call apiFetch DELETE when backend is ready
  console.log('[Admin] delete', current.value, id)
}

function logout() {
  auth.logout()
  router.push('/')
}
</script>

<style scoped>
.admin {
  display: flex;
  min-height: 100vh;
}

/* ── Sidebar ── */
.admin__sidebar {
  flex-shrink: 0;
  width: 200px;
  background: var(--color-ink-1);
  padding: var(--space-6) var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  position: sticky;
  top: var(--navbar-height);
  height: calc(100vh - var(--navbar-height));
  overflow-y: auto;
}

.admin__sidebar-title {
  font-family: var(--font-cjk);
  font-size: 11px;
  font-weight: 700;
  color: var(--color-ink-3);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: var(--space-2) var(--space-3);
  margin-bottom: var(--space-2);
}

.admin__sidebar-item {
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
  background: none;
  border: none;
  font-family: var(--font-cjk);
  font-size: 14px;
  color: var(--color-ink-3);
  cursor: pointer;
  text-align: left;
  transition: background 0.15s, color 0.15s;
}

.admin__sidebar-item:hover { background: rgba(255,255,255,0.06); color: #fff; }
.admin__sidebar-item--active { background: var(--color-primary); color: var(--color-ink-1); font-weight: 700; }

.admin__sidebar-divider {
  height: 1px;
  background: rgba(255,255,255,0.1);
  margin: var(--space-4) 0;
}

.admin__logout {
  padding: var(--space-2) var(--space-3);
  background: none;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-3);
  cursor: pointer;
  text-align: left;
  transition: border-color 0.2s, color 0.2s;
  margin-top: auto;
}
.admin__logout:hover { border-color: #dc2626; color: #dc2626; }

/* ── Main ── */
.admin__main {
  flex: 1;
  padding: var(--space-7) var(--space-6);
  background: #f7f7f5;
  overflow-y: auto;
}

/* ── Modal ── */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.45);
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
  max-height: 85vh;
  overflow-y: auto;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
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

.modal__fields { display: flex; flex-direction: column; gap: var(--space-3); }

.modal__label {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  font-family: var(--font-cjk);
  font-size: 13px;
  font-weight: 600;
  color: var(--color-ink-2);
}

.modal__input,
.modal__textarea {
  padding: var(--space-2) var(--space-3);
  border: 1px solid var(--color-ink-4);
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  width: 100%;
  box-sizing: border-box;
}
.modal__input:focus,
.modal__textarea:focus { border-color: var(--color-primary); }
.modal__textarea { resize: vertical; }

.modal__actions { display: flex; gap: var(--space-2); justify-content: flex-end; }

.modal__btn {
  padding: var(--space-2) var(--space-5);
  border: none;
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}
.modal__btn:hover { opacity: 0.82; }
.modal__btn--cancel { background: var(--color-ink-4); color: var(--color-ink-1); }
.modal__btn--save   { background: var(--color-primary); color: var(--color-ink-1); }
</style>
