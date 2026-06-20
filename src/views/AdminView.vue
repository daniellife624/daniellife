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
        :rows="socialActivities.map(a => [a.name, a.esgType, a.organization, a.periodFrom, a.periodTo ?? ''])"
        :ids="socialActivities.map(a => a.id)"
        @add="openAdd"
        @edit="openEdit"
        @delete="deleteItem"
      />

      <AdminTable
        v-if="current === 'literature'"
        title="文學作品"
        :columns="['標題', '撰寫年齡', '期間', '得獎紀錄']"
        :rows="literatureWorks.map(w => [w.title, w.ageWritten ? w.ageWritten + '歲' : '', w.period ?? '', w.awards])"
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

      <AdminTable
        v-if="current === 'academic'"
        title="求學歷程"
        :columns="['學校', '科系', '期間', 'GPA', '排名', '順序']"
        :rows="academics.map(a => [a.school, a.major, a.period, a.gpa, a.rank, String(a.sortOrder ?? 0)])"
        :ids="academics.map(a => a.id)"
        @add="openAdd"
        @edit="openEdit"
        @delete="deleteItem"
      />

      <AdminTable
        v-if="current === 'futureplans'"
        title="未來規劃"
        :columns="['階段', '標題', '副標題', '順序']"
        :rows="futurePlans.map(p => [p.phase, p.title, p.subtitle, String(p.sortOrder ?? 0)])"
        :ids="futurePlans.map(p => p.id)"
        @add="openAdd"
        @edit="openEdit"
        @delete="deleteItem"
      />

      <AdminTable
        v-if="current === 'langcerts'"
        title="語言證照"
        :columns="['語言', '名稱', '成績', '進度%']"
        :rows="langCerts.map(c => [c.lang, c.name, c.score, String(c.pct)])"
        :ids="langCerts.map(c => c.id)"
        @add="openAdd"
        @edit="openEdit"
        @delete="deleteItem"
      />

      <AdminTable
        v-if="current === 'certgroups'"
        title="財會/資訊證照"
        :columns="['領域', '類別', '項目數', '順序']"
        :rows="certGroups.map(g => [g.domain, g.category, String(g.items.length), String(g.sortOrder)])"
        :ids="certGroups.map(g => g.id)"
        @add="openAdd"
        @edit="openEdit"
        @delete="deleteItem"
      />

      <AdminTable
        v-if="current === 'travel'"
        title="旅遊記錄"
        :columns="['國家', '城市', '洲', '日期']"
        :rows="travelEntries.map(t => [t.country, t.city, t.continent, t.visitedAt])"
        :ids="travelEntries.map(t => t.id)"
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
                :placeholder="field.placeholder ?? field.label"
              />
            </label>
          </div>
          <p v-if="saveError" class="modal__error">{{ saveError }}</p>
          <div class="modal__actions">
            <button class="modal__btn modal__btn--cancel" @click="modalOpen = false">取消</button>
            <button class="modal__btn modal__btn--save" :disabled="saving" @click="saveModal">
              {{ saving ? '儲存中…' : '儲存' }}
            </button>
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
import {
  getInternships, createInternship, updateInternship, deleteInternship,
  getProjects,    createProject,    updateProject,    deleteProject,
  getAcademicMilestones, createAcademicMilestone, updateAcademicMilestone, deleteAcademicMilestone,
  getFuturePlans, createFuturePlan, updateFuturePlan, deleteFuturePlan,
  getLangCerts,   createLangCert,   updateLangCert,   deleteLangCert,
  getCertGroups,  createCertGroup,  updateCertGroup,  deleteCertGroup,
} from '@/api/homepage'
import {
  getExperiences, createExperience, updateExperience, deleteExperience,
  getTravelEntries, createTravelEntry, updateTravelEntry, deleteTravelEntry,
} from '@/api/activities'
import {
  getSocialActivities, createSocialActivity, updateSocialActivity, deleteSocialActivity,
} from '@/api/social'
import {
  getLiteratureWorks, createLiteratureWork, updateLiteratureWork, deleteLiteratureWork,
} from '@/api/literature'
import {
  getThesisPapers, createThesisPaper, updateThesisPaper, deleteThesisPaper,
} from '@/api/thesis'
import {
  getHoldings, createHolding, updateHolding, deleteHolding,
} from '@/api/finance'
import type { Internship, Project, AcademicMilestone, FuturePlan, LangCertAdmin, CertGroupAdmin } from '@/types/homepage'
import type { Experience, TravelEntry } from '@/types/activities'
import type { SocialActivity } from '@/types/social'
import type { LiteratureWork } from '@/types/literature'
import type { ThesisPaper } from '@/types/thesis'
import type { Holding } from '@/types/finance'

const router = useRouter()
const auth = useAuthStore()

type SectionKey =
  | 'internships' | 'projects' | 'activities' | 'social'
  | 'literature' | 'papers' | 'holdings'
  | 'academic' | 'futureplans' | 'langcerts' | 'certgroups' | 'travel'

const sections: { key: SectionKey; label: string }[] = [
  { key: 'internships', label: '實習經歷' },
  { key: 'projects',    label: '作品集' },
  { key: 'activities',  label: '課外活動' },
  { key: 'social',      label: '社會參與' },
  { key: 'literature',  label: '文學作品' },
  { key: 'papers',      label: '論文文獻' },
  { key: 'holdings',    label: '持股明細' },
  { key: 'academic',    label: '求學歷程' },
  { key: 'futureplans', label: '未來規劃' },
  { key: 'langcerts',   label: '語言證照' },
  { key: 'certgroups',  label: '財會/資訊證照' },
  { key: 'travel',      label: '旅遊記錄' },
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
const academics        = ref<AcademicMilestone[]>([])
const futurePlans      = ref<FuturePlan[]>([])
const langCerts        = ref<LangCertAdmin[]>([])
const certGroups       = ref<CertGroupAdmin[]>([])
const travelEntries    = ref<TravelEntry[]>([])

onMounted(async () => {
  ;[
    interns.value,
    projects.value,
    experiences.value,
    socialActivities.value,
    literatureWorks.value,
    papers.value,
    holdings.value,
    academics.value,
    futurePlans.value,
    langCerts.value,
    certGroups.value,
    travelEntries.value,
  ] = await Promise.all([
    getInternships(),
    getProjects(),
    getExperiences(),
    getSocialActivities(),
    getLiteratureWorks(),
    getThesisPapers(),
    getHoldings(),
    getAcademicMilestones(),
    getFuturePlans(),
    getLangCerts(),
    getCertGroups(),
    getTravelEntries(),
  ])
})

// ── Modal state ──
const modalOpen = ref(false)
const modalMode = ref<'add' | 'edit'>('add')
const editId    = ref<number | null>(null)
const formData  = ref<Record<string, string>>({})
const saving    = ref(false)
const saveError = ref('')

type FieldDef = { key: string; label: string; type?: string; placeholder?: string }

const fieldMap: Record<SectionKey, FieldDef[]> = {
  internships: [
    { key: 'company',      label: '公司' },
    { key: 'dept',         label: '部門' },
    { key: 'role',         label: '職稱' },
    { key: 'period',       label: '期間', placeholder: 'YYYY/MM – YYYY/MM' },
    { key: 'contribution', label: '主要貢獻', type: 'textarea' },
  ],
  projects: [
    { key: 'name',       label: '名稱' },
    { key: 'type',       label: '類型', placeholder: 'code / uiux / finance' },
    { key: 'techLabel',  label: '技術標籤', placeholder: '使用技術 / 使用軟體' },
    { key: 'tech',       label: '技術/工具' },
    { key: 'members',    label: '成員人數', type: 'number' },
    { key: 'period',     label: '期間', placeholder: 'YYYY/MM – YYYY/MM' },
    { key: 'core',       label: '核心功能（20字）' },
    { key: 'githubUrl',  label: 'GitHub 連結（可空）' },
    { key: 'youtubeUrl', label: 'YouTube 連結（可空）' },
    { key: 'createdAt',  label: '建立日期', placeholder: 'YYYY-MM-DD' },
    { key: 'starS',      label: 'STAR — S 情境', type: 'textarea' },
    { key: 'starT',      label: 'STAR — T 任務', type: 'textarea' },
    { key: 'starA',      label: 'STAR — A 行動', type: 'textarea' },
    { key: 'starR',      label: 'STAR — R 結果', type: 'textarea' },
  ],
  activities: [
    { key: 'type',         label: '類型', placeholder: 'leadership / club' },
    { key: 'title',        label: '標題' },
    { key: 'organization', label: '組織' },
    { key: 'period',       label: '期間', placeholder: 'YYYY/MM – YYYY/MM' },
    { key: 'contribution', label: '主要貢獻', type: 'textarea' },
  ],
  social: [
    { key: 'name',         label: '名稱' },
    { key: 'organization', label: '組織' },
    { key: 'esgType',      label: 'ESG 類型', placeholder: 'Environmental / Social / Governance' },
    { key: 'sdgNumbers',   label: 'SDG 號碼（逗號分隔）', placeholder: '如 1,3,13' },
    { key: 'periodFrom',   label: '開始日期', placeholder: 'YYYY-MM-DD' },
    { key: 'periodTo',     label: '結束日期（可空）', placeholder: 'YYYY-MM-DD' },
    { key: 'contribution', label: '主要貢獻', type: 'textarea' },
    { key: 'reflection',   label: '心得', type: 'textarea' },
  ],
  literature: [
    { key: 'title',      label: '標題' },
    { key: 'ageWritten', label: '撰寫年齡', type: 'number' },
    { key: 'period',     label: '撰寫期間', placeholder: 'YYYY.MM' },
    { key: 'awards',     label: '得獎紀錄' },
    { key: 'summary',    label: '摘要', type: 'textarea' },
    { key: 'fullText',   label: '全文（可空）', type: 'textarea' },
  ],
  papers: [
    { key: 'topic',        label: '研究主題' },
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
    { key: 'currency',    label: '幣別', placeholder: 'TWD / USD' },
    { key: 'broker',      label: '券商' },
    { key: 'shares',      label: '股數', type: 'number' },
    { key: 'avgPrice',    label: '均價', type: 'number' },
    { key: 'marketPrice', label: '市價', type: 'number' },
    { key: 'dividend',    label: '股利', type: 'number' },
  ],
  academic: [
    { key: 'school',    label: '學校' },
    { key: 'major',     label: '科系' },
    { key: 'period',    label: '期間', placeholder: '2021 – 2024' },
    { key: 'gpa',       label: 'GPA', placeholder: '4.26/4.30' },
    { key: 'rank',      label: '排名', placeholder: '3/71' },
    { key: 'sortOrder', label: '顯示順序', type: 'number' },
    { key: 'facts',     label: '重點事蹟（每行一條）', type: 'textarea' },
  ],
  futureplans: [
    { key: 'phase',     label: '階段', placeholder: 'short / mid-short / mid' },
    { key: 'title',     label: '標題', placeholder: '短期' },
    { key: 'subtitle',  label: '副標題', placeholder: '近一年' },
    { key: 'sortOrder', label: '顯示順序', type: 'number' },
    { key: 'items',     label: '項目（每行一條）', type: 'textarea' },
  ],
  langcerts: [
    { key: 'lang',  label: '語言', placeholder: 'en / jp' },
    { key: 'name',  label: '名稱', placeholder: 'TOEIC / JLPT' },
    { key: 'score', label: '成績', placeholder: '865 / N4' },
    { key: 'pct',   label: '進度百分比 (0–100)', type: 'number' },
  ],
  certgroups: [
    { key: 'domain',    label: '領域', placeholder: 'finance / it' },
    { key: 'category',  label: '類別', placeholder: '國際證照' },
    { key: 'sortOrder', label: '顯示順序', type: 'number' },
    { key: 'items',     label: '證照項目（每行一條）', type: 'textarea' },
  ],
  travel: [
    { key: 'country',    label: '國家' },
    { key: 'city',       label: '城市' },
    { key: 'continent',  label: '洲', placeholder: 'Asia / Europe / Americas / Africa / Australia' },
    { key: 'visitedAt',  label: '造訪日期', placeholder: 'YYYY-MM-DD' },
    { key: 'companions', label: '同行者（可空）' },
    { key: 'activities', label: '活動（可空）' },
    { key: 'purchases',  label: '購物（可空）' },
    { key: 'journal',    label: '日記（可空）', type: 'textarea' },
  ],
}

const modalFields = computed<FieldDef[]>(() => fieldMap[current.value] ?? [])

// ── openAdd ──
function openAdd() {
  modalMode.value = 'add'
  editId.value = null
  saveError.value = ''
  formData.value = Object.fromEntries(fieldMap[current.value].map((f) => [f.key, '']))
  modalOpen.value = true
}

// ── openEdit ──
function openEdit(id: number) {
  modalMode.value = 'edit'
  editId.value = id
  saveError.value = ''
  const fd: Record<string, string> = {}

  if (current.value === 'internships') {
    const item = interns.value.find((i) => i.id === id)!
    Object.assign(fd, {
      company: item.company, dept: item.dept, role: item.role,
      period: item.period, contribution: item.contribution,
    })
  } else if (current.value === 'projects') {
    const item = projects.value.find((p) => p.id === id)!
    Object.assign(fd, {
      name: item.name, type: item.type,
      techLabel: item.techLabel, tech: item.tech,
      members: String(item.members), period: item.period, core: item.core,
      githubUrl: item.githubUrl ?? '', youtubeUrl: item.youtubeUrl ?? '',
      createdAt: item.createdAt,
      starS: item.star.find((s) => s.label === 'S')?.text ?? '',
      starT: item.star.find((s) => s.label === 'T')?.text ?? '',
      starA: item.star.find((s) => s.label === 'A')?.text ?? '',
      starR: item.star.find((s) => s.label === 'R')?.text ?? '',
    })
  } else if (current.value === 'activities') {
    const item = experiences.value.find((e) => e.id === id)!
    Object.assign(fd, {
      type: item.type, title: item.title, organization: item.organization,
      period: item.period, contribution: item.contribution,
    })
  } else if (current.value === 'social') {
    const item = socialActivities.value.find((a) => a.id === id)!
    Object.assign(fd, {
      name: item.name, organization: item.organization, esgType: item.esgType,
      sdgNumbers: item.sdgNumbers.join(', '),
      periodFrom: item.periodFrom, periodTo: item.periodTo ?? '',
      contribution: item.contribution, reflection: item.reflection,
    })
  } else if (current.value === 'literature') {
    const item = literatureWorks.value.find((w) => w.id === id)!
    Object.assign(fd, {
      title: item.title, ageWritten: item.ageWritten ? String(item.ageWritten) : '',
      period: item.period ?? '', awards: item.awards,
      summary: item.summary, fullText: item.fullText ?? '',
    })
  } else if (current.value === 'papers') {
    const item = papers.value.find((p) => p.id === id)!
    Object.assign(fd, {
      topic: item.topic, name: item.name, journal: item.journal,
      authors: item.authors, year: String(item.year),
      purpose: item.purpose, contribution: item.contribution,
    })
  } else if (current.value === 'holdings') {
    const item = holdings.value.find((h) => h.id === id)!
    Object.assign(fd, {
      symbol: item.symbol, name: item.name, currency: item.currency,
      broker: item.broker, shares: String(item.shares),
      avgPrice: String(item.avgPrice), marketPrice: String(item.marketPrice),
      dividend: String(item.dividend),
    })
  } else if (current.value === 'academic') {
    const item = academics.value.find((a) => a.id === id)!
    Object.assign(fd, {
      school: item.school, major: item.major, period: item.period,
      gpa: item.gpa, rank: item.rank,
      sortOrder: String(item.sortOrder ?? 0),
      facts: item.facts.join('\n'),
    })
  } else if (current.value === 'futureplans') {
    const item = futurePlans.value.find((p) => p.id === id)!
    Object.assign(fd, {
      phase: item.phase, title: item.title, subtitle: item.subtitle,
      sortOrder: String(item.sortOrder ?? 0),
      items: item.items.join('\n'),
    })
  } else if (current.value === 'langcerts') {
    const item = langCerts.value.find((c) => c.id === id)!
    Object.assign(fd, { lang: item.lang, name: item.name, score: item.score, pct: String(item.pct) })
  } else if (current.value === 'certgroups') {
    const item = certGroups.value.find((g) => g.id === id)!
    Object.assign(fd, {
      domain: item.domain, category: item.category,
      sortOrder: String(item.sortOrder),
      items: item.items.join('\n'),
    })
  } else if (current.value === 'travel') {
    const item = travelEntries.value.find((t) => t.id === id)!
    Object.assign(fd, {
      country: item.country, city: item.city, continent: item.continent,
      visitedAt: item.visitedAt, companions: item.companions ?? '',
      activities: item.activities ?? '', purchases: item.purchases ?? '',
      journal: item.journal ?? '',
    })
  }

  formData.value = fd
  modalOpen.value = true
}

// ── saveModal ──
async function saveModal() {
  saving.value = true
  saveError.value = ''
  const fd = formData.value
  const isEdit = modalMode.value === 'edit'

  try {
    if (current.value === 'internships') {
      const body = {
        company: fd.company, dept: fd.dept, role: fd.role,
        period: fd.period, contribution: fd.contribution,
        photoUrl: fd.photoUrl || undefined,
      }
      if (isEdit) {
        const updated = await updateInternship(editId.value!, body)
        replaceInList(interns.value, updated)
      } else {
        interns.value.push(await createInternship(body))
      }

    } else if (current.value === 'projects') {
      const star = (['S', 'T', 'A', 'R'] as const)
        .map((l) => ({ label: l, text: fd[`star${l}`] ?? '' }))
        .filter((s) => s.text.trim())
      const body = {
        name: fd.name, type: fd.type,
        techLabel: fd.techLabel || '使用技術', tech: fd.tech,
        members: Number(fd.members) || 1, period: fd.period, core: fd.core,
        githubUrl: fd.githubUrl || undefined, youtubeUrl: fd.youtubeUrl || undefined,
        star, createdAt: fd.createdAt,
      }
      if (isEdit) {
        const updated = await updateProject(editId.value!, body)
        replaceInList(projects.value, updated)
      } else {
        projects.value.push(await createProject(body))
      }

    } else if (current.value === 'activities') {
      const body = {
        type: fd.type as 'leadership' | 'club',
        title: fd.title, organization: fd.organization,
        period: fd.period, contribution: fd.contribution,
        photos: [],
      }
      if (isEdit) {
        const updated = await updateExperience(editId.value!, body)
        replaceInList(experiences.value, updated)
      } else {
        experiences.value.push(await createExperience(body))
      }

    } else if (current.value === 'social') {
      const sdgNumbers = fd.sdgNumbers
        .split(',').map((n) => parseInt(n.trim())).filter((n) => !isNaN(n) && n >= 1 && n <= 17)
      const body = {
        name: fd.name, organization: fd.organization,
        esgType: fd.esgType as SocialActivity['esgType'],
        sdgNumbers,
        periodFrom: fd.periodFrom, periodTo: fd.periodTo || undefined,
        contribution: fd.contribution, reflection: fd.reflection,
      }
      if (isEdit) {
        const updated = await updateSocialActivity(editId.value!, body)
        replaceInList(socialActivities.value, updated)
      } else {
        socialActivities.value.push(await createSocialActivity(body))
      }

    } else if (current.value === 'literature') {
      const body = {
        title: fd.title,
        ageWritten: fd.ageWritten ? Number(fd.ageWritten) : undefined,
        period: fd.period || undefined,
        awards: fd.awards, summary: fd.summary,
        fullText: fd.fullText || undefined,
      }
      if (isEdit) {
        const updated = await updateLiteratureWork(editId.value!, body)
        replaceInList(literatureWorks.value, updated)
      } else {
        literatureWorks.value.push(await createLiteratureWork(body))
      }

    } else if (current.value === 'papers') {
      const body = {
        topic: fd.topic, name: fd.name, journal: fd.journal,
        authors: fd.authors, year: Number(fd.year) || new Date().getFullYear(),
        purpose: fd.purpose, contribution: fd.contribution,
      }
      if (isEdit) {
        const updated = await updateThesisPaper(editId.value!, body)
        replaceInList(papers.value, updated)
      } else {
        papers.value.push(await createThesisPaper(body))
      }

    } else if (current.value === 'holdings') {
      const body = {
        symbol: fd.symbol, name: fd.name,
        currency: fd.currency as Holding['currency'],
        broker: fd.broker,
        shares: Number(fd.shares), avgPrice: Number(fd.avgPrice),
        marketPrice: Number(fd.marketPrice), dividend: Number(fd.dividend) || 0,
      }
      if (isEdit) {
        const updated = await updateHolding(editId.value!, body)
        replaceInList(holdings.value, updated)
      } else {
        holdings.value.push(await createHolding(body))
      }

    } else if (current.value === 'academic') {
      const body = {
        school: fd.school, major: fd.major, period: fd.period,
        gpa: fd.gpa, rank: fd.rank,
        facts: fd.facts.split('\n').map((s) => s.trim()).filter(Boolean),
        sortOrder: Number(fd.sortOrder) || 0,
      }
      if (isEdit) {
        const updated = await updateAcademicMilestone(editId.value!, body)
        replaceInList(academics.value, updated)
      } else {
        academics.value.push(await createAcademicMilestone(body))
      }

    } else if (current.value === 'futureplans') {
      const body = {
        phase: fd.phase as FuturePlan['phase'],
        title: fd.title, subtitle: fd.subtitle,
        items: fd.items.split('\n').map((s) => s.trim()).filter(Boolean),
        sortOrder: Number(fd.sortOrder) || 0,
      }
      if (isEdit) {
        const updated = await updateFuturePlan(editId.value!, body)
        replaceInList(futurePlans.value, updated)
      } else {
        futurePlans.value.push(await createFuturePlan(body))
      }

    } else if (current.value === 'langcerts') {
      const body = {
        lang: fd.lang as LangCertAdmin['lang'],
        name: fd.name, score: fd.score, pct: Number(fd.pct) || 0,
      }
      if (isEdit) {
        const updated = await updateLangCert(editId.value!, body)
        replaceInList(langCerts.value, updated)
      } else {
        langCerts.value.push(await createLangCert(body))
      }

    } else if (current.value === 'certgroups') {
      const body = {
        domain: fd.domain as CertGroupAdmin['domain'],
        category: fd.category,
        items: fd.items.split('\n').map((s) => s.trim()).filter(Boolean),
        sortOrder: Number(fd.sortOrder) || 0,
      }
      if (isEdit) {
        const updated = await updateCertGroup(editId.value!, body)
        replaceInList(certGroups.value, updated)
      } else {
        certGroups.value.push(await createCertGroup(body))
      }

    } else if (current.value === 'travel') {
      const body = {
        country: fd.country, city: fd.city, continent: fd.continent,
        visitedAt: fd.visitedAt,
        companions: fd.companions || undefined,
        activities: fd.activities || undefined,
        purchases: fd.purchases || undefined,
        journal: fd.journal || undefined,
        photos: [],
      }
      if (isEdit) {
        const updated = await updateTravelEntry(editId.value!, body)
        replaceInList(travelEntries.value, updated)
      } else {
        travelEntries.value.push(await createTravelEntry(body))
      }
    }

    modalOpen.value = false
  } catch {
    saveError.value = '儲存失敗，請確認欄位格式是否正確'
  } finally {
    saving.value = false
  }
}

function replaceInList<T extends { id: number }>(list: T[], updated: T) {
  const idx = list.findIndex((x) => x.id === updated.id)
  if (idx !== -1) list[idx] = updated
}

// ── deleteItem ──
async function deleteItem(id: number) {
  if (!confirm('確定刪除這筆資料？')) return
  try {
    if (current.value === 'internships') {
      await deleteInternship(id); interns.value = interns.value.filter((i) => i.id !== id)
    } else if (current.value === 'projects') {
      await deleteProject(id); projects.value = projects.value.filter((p) => p.id !== id)
    } else if (current.value === 'activities') {
      await deleteExperience(id); experiences.value = experiences.value.filter((e) => e.id !== id)
    } else if (current.value === 'social') {
      await deleteSocialActivity(id); socialActivities.value = socialActivities.value.filter((a) => a.id !== id)
    } else if (current.value === 'literature') {
      await deleteLiteratureWork(id); literatureWorks.value = literatureWorks.value.filter((w) => w.id !== id)
    } else if (current.value === 'papers') {
      await deleteThesisPaper(id); papers.value = papers.value.filter((p) => p.id !== id)
    } else if (current.value === 'holdings') {
      await deleteHolding(id); holdings.value = holdings.value.filter((h) => h.id !== id)
    } else if (current.value === 'academic') {
      await deleteAcademicMilestone(id); academics.value = academics.value.filter((a) => a.id !== id)
    } else if (current.value === 'futureplans') {
      await deleteFuturePlan(id); futurePlans.value = futurePlans.value.filter((p) => p.id !== id)
    } else if (current.value === 'langcerts') {
      await deleteLangCert(id); langCerts.value = langCerts.value.filter((c) => c.id !== id)
    } else if (current.value === 'certgroups') {
      await deleteCertGroup(id); certGroups.value = certGroups.value.filter((g) => g.id !== id)
    } else if (current.value === 'travel') {
      await deleteTravelEntry(id); travelEntries.value = travelEntries.value.filter((t) => t.id !== id)
    }
  } catch {
    alert('刪除失敗，請再試一次')
  }
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
  width: 560px;
  max-width: 92vw;
  max-height: 88vh;
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

.modal__error {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: #dc2626;
  background: #fef2f2;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
}

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
.modal__btn:disabled { opacity: 0.6; cursor: not-allowed; }
.modal__btn:not(:disabled):hover { opacity: 0.82; }
.modal__btn--cancel { background: var(--color-ink-4); color: var(--color-ink-1); }
.modal__btn--save   { background: var(--color-primary); color: var(--color-ink-1); }
</style>
