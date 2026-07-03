<template>
  <div class="admin">

    <AdminSidebar
      :sections="sections"
      :current-section="current"
      @select="current = $event as SectionKey"
      @logout="logout"
    />

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

      <div v-if="current === 'papers'" class="notion-sync-bar">
        <button class="notion-sync-btn" :disabled="notionSyncing" @click="runNotionSync">
          {{ notionSyncing ? '同步中…' : '🔄 同步 Notion 筆記' }}
        </button>
        <span v-if="notionSyncMsg" class="notion-sync-msg">{{ notionSyncMsg }}</span>
      </div>

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
        :columns="['學校', '科系', '期間', 'GPA', '排名']"
        :rows="academics.map(a => [a.school, a.major, a.period, a.gpa, a.rank])"
        :ids="academics.map(a => a.id)"
        draggable
        @add="openAdd"
        @edit="openEdit"
        @delete="deleteItem"
        @reorder="handleReorder"
      />

      <AdminTable
        v-if="current === 'futureplans'"
        title="未來規劃"
        :columns="['階段', '標題', '副標題']"
        :rows="futurePlans.map(p => [p.phase, p.title, p.subtitle])"
        :ids="futurePlans.map(p => p.id)"
        draggable
        @add="openAdd"
        @edit="openEdit"
        @delete="deleteItem"
        @reorder="handleReorder"
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
        :columns="['領域', '類別', '證照名稱']"
        :rows="certGroups.map(g => [g.domain, g.category, g.items.at(0) ?? ''])"
        :ids="certGroups.map(g => g.id)"
        draggable
        @add="openAdd"
        @edit="openEdit"
        @delete="deleteItem"
        @reorder="handleReorder"
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

    <AdminModal
      :open="modalOpen"
      :mode="modalMode"
      :section-label="currentSectionLabel"
      :fields="modalFields"
      :initial-form-data="modalInitialFormData"
      :current="current"
      :saving="saving"
      :save-error="saveError"
      :editing-photos="editingPhotos"
      :editing-photo-url="editingPhotoUrl"
      :photo-uploading="photoUploading"
      @close="modalOpen = false"
      @save="handleModalSave"
      @upload-multi="uploadAdminPhoto"
      @delete-multi="deleteAdminPhoto"
      @upload-single-edit="handleUploadSingleEdit"
      @delete-single-edit="handleDeleteSingleEdit"
    />

  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import AdminTable from '@/components/admin/AdminTable.vue'
import AdminSidebar from '@/components/admin/AdminSidebar.vue'
import AdminModal, { type FieldDef } from '@/components/admin/AdminModal.vue'
import {
  getInternships, createInternship, updateInternship, deleteInternship,
  uploadInternshipPhoto, deleteInternshipPhoto,
  getProjects,    createProject,    updateProject,    deleteProject,
  getAcademicMilestones, createAcademicMilestone, updateAcademicMilestone, deleteAcademicMilestone,
  reorderAcademic,
  getFuturePlans, createFuturePlan, updateFuturePlan, deleteFuturePlan,
  reorderFuturePlans,
  getLangCerts,   createLangCert,   updateLangCert,   deleteLangCert,
  getCertGroups,  createCertGroup,  updateCertGroup,  deleteCertGroup,
  reorderCertGroups,
} from '@/api/homepage'
import {
  getExperiences, createExperience, updateExperience, deleteExperience,
  getTravelEntries, createTravelEntry, updateTravelEntry, deleteTravelEntry,
  uploadExperiencePhoto, deleteExperiencePhoto, uploadTravelPhoto, deleteTravelPhoto,
} from '@/api/activities'
import {
  getSocialActivities, createSocialActivity, updateSocialActivity, deleteSocialActivity,
  uploadSocialPhoto, deleteSocialPhoto,
} from '@/api/social'
import {
  getLiteratureWorks, createLiteratureWork, updateLiteratureWork, deleteLiteratureWork,
} from '@/api/literature'
import {
  getThesisPapers, createThesisPaper, updateThesisPaper, deleteThesisPaper, syncNotionPapers,
} from '@/api/thesis'
import {
  getHoldings, createHolding, updateHolding, deleteHolding,
} from '@/api/finance'
import type { Internship, Project, AcademicMilestone, FuturePlan, LangCertAdmin, CertGroupAdmin } from '@/types/homepage'
import type { Experience, TravelEntry } from '@/types/activities'
import type { SocialActivity, SdgNumber } from '@/types/social'
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
const notionSyncing    = ref(false)
const notionSyncMsg    = ref('')

async function runNotionSync() {
  notionSyncing.value = true
  notionSyncMsg.value = ''
  try {
    const result = await syncNotionPapers()
    papers.value = await getThesisPapers()
    const parts = [`成功同步 ${result.synced.length} 篇`]
    if (result.failed.length) {
      parts.push(`失敗 ${result.failed.length} 篇：${result.failed.map((f) => `${f.name}（${f.error}）`).join('；')}`)
    }
    notionSyncMsg.value = parts.join('，')
  } catch (e) {
    notionSyncMsg.value = e instanceof Error ? e.message : '同步失敗'
  } finally {
    notionSyncing.value = false
  }
}
const holdings         = ref<Holding[]>([])
const academics        = ref<AcademicMilestone[]>([])
const futurePlans      = ref<FuturePlan[]>([])
const langCerts        = ref<LangCertAdmin[]>([])
const certGroups       = ref<CertGroupAdmin[]>([])
const travelEntries    = ref<TravelEntry[]>([])

// ── Edit-mode photo state (passed as props to AdminModal) ──
const editingPhotos   = ref<string[]>([])
const editingPhotoUrl = ref<string>('')
const photoUploading  = ref(false)

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
const modalOpen            = ref(false)
const modalMode            = ref<'add' | 'edit'>('add')
const editId               = ref<number | null>(null)
const modalInitialFormData = ref<Record<string, string>>({})
const saving               = ref(false)
const saveError            = ref('')

const fieldMap: Record<SectionKey, FieldDef[]> = {
  internships: [
    { key: 'company',      label: '公司' },
    { key: 'dept',         label: '部門' },
    { key: 'role',         label: '職稱' },
    { key: 'periodFrom',   label: '開始年月', placeholder: '例：2025/07' },
    { key: 'periodTo',     label: '結束年月（留空視為「至今」）', placeholder: '例：2025/08 或 至今' },
    { key: 'contribution', label: '主要貢獻', type: 'textarea' },
  ],
  projects: [
    { key: 'name',       label: '名稱' },
    { key: 'type',       label: '類型（可複選）', options: ['code', 'uiux', 'finance'], multi: true },
    { key: 'tech',       label: '使用技術/工具' },
    { key: 'responsibility', label: '主要職責（100字以內）', type: 'textarea', placeholder: '例：負責前端全站開發與 UI/UX 設計', maxLength: 100 },
    { key: 'members',    label: '成員人數', type: 'number' },
    { key: 'periodFrom', label: '開始年月', placeholder: '例：2025/07' },
    { key: 'periodTo',   label: '結束年月（留空視為「至今」）', placeholder: '例：2025/08 或 至今' },
    { key: 'core',       label: '核心功能（20字）' },
    { key: 'githubUrl',  label: 'GitHub 連結（可空）' },
    { key: 'youtubeUrl', label: 'YouTube 連結（可空）' },
    { key: 'otherUrl',   label: '其他連結（可空，如 PDF / 網頁）' },
    { key: 'createdAt',  label: '建立日期', placeholder: 'YYYY-MM-DD（用於排序：由新到舊）' },
    { key: 'starS',      label: 'STAR — S 情境（150字以內）', type: 'textarea', maxLength: 150 },
    { key: 'starT',      label: 'STAR — T 任務（150字以內）', type: 'textarea', maxLength: 150 },
    { key: 'starA',      label: 'STAR — A 行動（150字以內）', type: 'textarea', maxLength: 150 },
    { key: 'starR',      label: 'STAR — R 結果（150字以內）', type: 'textarea', maxLength: 150 },
  ],
  activities: [
    { key: 'type',         label: '類型', placeholder: 'leadership / club' },
    { key: 'title',        label: '標題' },
    { key: 'organization', label: '組織' },
    { key: 'periodFrom',   label: '開始年月', placeholder: '例：2025/07' },
    { key: 'periodTo',     label: '結束年月（留空視為「至今」）', placeholder: '例：2025/08 或 至今' },
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
    { key: 'notionUrl',    label: 'Notion 筆記頁面連結（可空）', placeholder: 'https://notion.so/...' },
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
    { key: 'school',     label: '學校' },
    { key: 'major',      label: '科系' },
    { key: 'periodFrom', label: '入學年月', placeholder: '例：2021/09' },
    { key: 'periodTo',   label: '畢業年月（留空視為「至今」）', placeholder: '例：2025/06 或 至今' },
    { key: 'gpa',        label: 'GPA', placeholder: '4.26/4.30' },
    { key: 'rank',       label: '排名', placeholder: '3/71' },
    { key: 'facts',      label: '重點事蹟（每行一條）', type: 'textarea' },
  ],
  futureplans: [
    { key: 'phase',    label: '階段', placeholder: 'short / mid-short / mid' },
    { key: 'title',    label: '標題', placeholder: '短期' },
    { key: 'subtitle', label: '副標題', placeholder: '近一年' },
    { key: 'items',    label: '項目（每行一條）', type: 'textarea' },
  ],
  langcerts: [
    { key: 'lang',  label: '語言', placeholder: 'en / jp' },
    { key: 'name',  label: '名稱', placeholder: 'TOEIC / JLPT' },
    { key: 'score', label: '成績', placeholder: '865 / N4' },
    { key: 'pct',   label: '進度百分比 (0–100)', type: 'number' },
  ],
  certgroups: [
    { key: 'domain',   label: '領域', options: ['財會', '資訊'] },
    { key: 'category', label: '類別', options: ['國內', '國外'] },
    { key: 'name',     label: '證照名稱' },
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

function parsePeriod(period: string): { from: string; to: string } {
  const parts = period.split('–').map((p) => p.trim())
  return { from: parts[0] || '', to: parts[1] || '' }
}

function replaceInList<T extends { id: number }>(list: T[], updated: T) {
  const idx = list.findIndex((x) => x.id === updated.id)
  if (idx !== -1) list[idx] = updated
}

// ── openAdd ──
function openAdd() {
  modalMode.value = 'add'
  editId.value = null
  saveError.value = ''
  modalInitialFormData.value = Object.fromEntries(fieldMap[current.value].map((f) => [f.key, '']))
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
    const p = parsePeriod(item.period)
    Object.assign(fd, {
      company: item.company, dept: item.dept, role: item.role,
      periodFrom: p.from, periodTo: p.to, contribution: item.contribution,
    })
  } else if (current.value === 'projects') {
    const item = projects.value.find((p) => p.id === id)!
    const period = parsePeriod(item.period)
    Object.assign(fd, {
      name: item.name, type: item.type,
      techLabel: item.techLabel, tech: item.tech,
      responsibility: item.responsibility,
      members: String(item.members),
      periodFrom: period.from, periodTo: period.to,
      core: item.core,
      githubUrl: item.githubUrl ?? '', youtubeUrl: item.youtubeUrl ?? '',
      otherUrl: item.otherUrl ?? '',
      createdAt: item.createdAt,
      starS: item.star.find((s) => s.label === 'S')?.text ?? '',
      starT: item.star.find((s) => s.label === 'T')?.text ?? '',
      starA: item.star.find((s) => s.label === 'A')?.text ?? '',
      starR: item.star.find((s) => s.label === 'R')?.text ?? '',
    })
  } else if (current.value === 'activities') {
    const item = experiences.value.find((e) => e.id === id)!
    const p = parsePeriod(item.period)
    Object.assign(fd, {
      type: item.type, title: item.title, organization: item.organization,
      periodFrom: p.from, periodTo: p.to, contribution: item.contribution,
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
      notionUrl: item.notionUrl ?? '',
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
    const p = parsePeriod(item.period)
    Object.assign(fd, {
      school: item.school, major: item.major,
      periodFrom: p.from, periodTo: p.to,
      gpa: item.gpa, rank: item.rank,
      _sortOrder: String(item.sortOrder ?? 0),
      facts: item.facts.join('\n'),
    })
  } else if (current.value === 'futureplans') {
    const item = futurePlans.value.find((p) => p.id === id)!
    Object.assign(fd, {
      phase: item.phase, title: item.title, subtitle: item.subtitle,
      _sortOrder: String(item.sortOrder ?? 0),
      items: item.items.join('\n'),
    })
  } else if (current.value === 'langcerts') {
    const item = langCerts.value.find((c) => c.id === id)!
    Object.assign(fd, { lang: item.lang, name: item.name, score: item.score, pct: String(item.pct) })
  } else if (current.value === 'certgroups') {
    const item = certGroups.value.find((g) => g.id === id)!
    const domainLabel = item.domain === 'finance' ? '財會' : item.domain === 'it' ? '資訊' : item.domain
    Object.assign(fd, {
      domain: domainLabel, category: item.category,
      _sortOrder: String(item.sortOrder),
      name: item.items.at(0) ?? '',
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

  // populate edit-mode photo refs
  editingPhotos.value = []
  editingPhotoUrl.value = ''
  if (current.value === 'activities') {
    editingPhotos.value = [...(experiences.value.find((e) => e.id === id)?.photos ?? [])]
  } else if (current.value === 'travel') {
    editingPhotos.value = [...(travelEntries.value.find((t) => t.id === id)?.photos ?? [])]
  } else if (current.value === 'social') {
    editingPhotoUrl.value = socialActivities.value.find((a) => a.id === id)?.photoUrl ?? ''
  } else if (current.value === 'internships') {
    editingPhotoUrl.value = interns.value.find((i) => i.id === id)?.photoUrl ?? ''
  }

  modalInitialFormData.value = fd
  modalOpen.value = true
}

// ── validateForm ──
function validateForm(fd: Record<string, string>): string {
  const s = (k: string): string => fd[k] ?? ''
  const MONTH = /^\d{4}\/(0[1-9]|1[0-2])$/
  const MONTH_OR_JIUJIN = (v: string) => !v.trim() || v.trim() === '至今' || MONTH.test(v.trim())
  const YEAR = /^\d{4}$/
  const DATE = /^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/

  if (current.value === 'internships') {
    if (!s('company').trim()) return '「公司」不可空白'
    if (!s('dept').trim()) return '「部門」不可空白'
    if (!s('role').trim()) return '「職稱」不可空白'
    if (!MONTH.test(s('periodFrom'))) return '「開始年月」格式須為 YYYY/MM（例：2025/07）'
    if (!MONTH_OR_JIUJIN(s('periodTo'))) return '「結束年月」格式須為 YYYY/MM，或填「至今」，或留空'
    if (!s('contribution').trim()) return '「主要貢獻」不可空白'
  } else if (current.value === 'projects') {
    if (!s('name').trim()) return '「名稱」不可空白'
    {
      const types = s('type').split(',').map((t) => t.trim()).filter(Boolean)
      if (types.length === 0 || !types.every((t) => ['code', 'uiux', 'finance'].includes(t)))
        return '「類型」至少選擇一項，且須為 code / uiux / finance'
    }
    if (!Number.isInteger(Number(s('members'))) || Number(s('members')) < 1) return '「成員人數」須為正整數'
    if (!MONTH.test(s('periodFrom'))) return '「開始年月」格式須為 YYYY/MM（例：2025/07）'
    if (!MONTH_OR_JIUJIN(s('periodTo'))) return '「結束年月」格式須為 YYYY/MM，或填「至今」，或留空'
    if (!s('core').trim()) return '「核心功能」不可空白'
    if (s('responsibility').length > 100) return '「主要職責」不可超過 100 字'
    if (s('createdAt') && !DATE.test(s('createdAt'))) return '「建立日期」格式須為 YYYY-MM-DD（例：2025-07-01）'
    for (const [key, label] of [['starS', 'S 情境'], ['starT', 'T 任務'], ['starA', 'A 行動'], ['starR', 'R 結果']] as const) {
      if (s(key).length > 150) return `「STAR — ${label}」不可超過 150 字`
    }
  } else if (current.value === 'activities') {
    if (!['leadership', 'club'].includes(s('type'))) return '「類型」須為 leadership 或 club'
    if (!s('title').trim()) return '「標題」不可空白'
    if (!s('organization').trim()) return '「組織」不可空白'
    if (!MONTH.test(s('periodFrom'))) return '「開始年月」格式須為 YYYY/MM（例：2025/07）'
    if (!MONTH_OR_JIUJIN(s('periodTo'))) return '「結束年月」格式須為 YYYY/MM，或填「至今」，或留空'
    if (!s('contribution').trim()) return '「主要貢獻」不可空白'
  } else if (current.value === 'social') {
    if (!s('name').trim()) return '「名稱」不可空白'
    if (!s('organization').trim()) return '「組織」不可空白'
    if (!['Environmental', 'Social', 'Governance'].includes(s('esgType')))
      return '「ESG 類型」須為 Environmental / Social / Governance'
    if (!DATE.test(s('periodFrom'))) return '「開始日期」格式須為 YYYY-MM-DD（例：2025-07-01）'
    if (s('periodTo') && !DATE.test(s('periodTo'))) return '「結束日期」格式須為 YYYY-MM-DD，或留空'
  } else if (current.value === 'literature') {
    if (!s('title').trim()) return '「標題」不可空白'
    if (s('ageWritten') && (isNaN(Number(s('ageWritten'))) || Number(s('ageWritten')) < 1))
      return '「撰寫年齡」須為正整數'
  } else if (current.value === 'papers') {
    if (!s('topic').trim()) return '「研究主題」不可空白'
    if (!s('name').trim()) return '「論文名稱」不可空白'
    if (!s('journal').trim()) return '「期刊」不可空白'
    if (!s('authors').trim()) return '「作者」不可空白'
    if (!YEAR.test(s('year'))) return '「年份」須為 4 位數字（例：2025）'
  } else if (current.value === 'holdings') {
    if (!s('symbol').trim()) return '「股票代碼」不可空白'
    if (!s('name').trim()) return '「名稱」不可空白'
    if (!['TWD', 'USD'].includes(s('currency'))) return '「幣別」須為 TWD 或 USD'
    if (!s('broker').trim()) return '「券商」不可空白'
    if (!Number.isFinite(Number(s('shares'))) || Number(s('shares')) <= 0) return '「股數」須為正數'
    if (!Number.isFinite(Number(s('avgPrice'))) || Number(s('avgPrice')) <= 0) return '「均價」須為正數'
    if (!Number.isFinite(Number(s('marketPrice'))) || Number(s('marketPrice')) <= 0) return '「市價」須為正數'
  } else if (current.value === 'academic') {
    if (!s('school').trim()) return '「學校」不可空白'
    if (!s('major').trim()) return '「科系」不可空白'
    const YEAR_MONTH = /^\d{4}(\/\d{2})?$/
    if (!YEAR_MONTH.test(s('periodFrom').trim())) return '「入學年月」格式須為 YYYY 或 YYYY/MM（例：2021/09）'
    if (s('periodTo').trim() && !YEAR_MONTH.test(s('periodTo').trim()) && s('periodTo').trim() !== '至今')
      return '「畢業年月」格式須為 YYYY、YYYY/MM，或填「至今」，或留空'
  } else if (current.value === 'futureplans') {
    if (!['short', 'mid-short', 'mid'].includes(s('phase')))
      return '「階段」須為 short / mid-short / mid'
    if (!s('title').trim()) return '「標題」不可空白'
    if (!s('subtitle').trim()) return '「副標題」不可空白'
  } else if (current.value === 'langcerts') {
    if (!['en', 'jp'].includes(s('lang'))) return '「語言」須為 en 或 jp'
    if (!s('name').trim()) return '「名稱」不可空白'
    if (!s('score').trim()) return '「成績」不可空白'
    const pct = Number(s('pct'))
    if (isNaN(pct) || pct < 0 || pct > 100) return '「進度百分比」須為 0 到 100 之間的數字'
  } else if (current.value === 'certgroups') {
    if (!['財會', '資訊'].includes(s('domain'))) return '「領域」須為 財會 或 資訊'
    if (!['國內', '國外'].includes(s('category'))) return '「類別」須為 國內 或 國外'
    if (!s('name').trim()) return '「證照名稱」不可空白'
  } else if (current.value === 'travel') {
    if (!s('country').trim()) return '「國家」不可空白'
    if (!s('city').trim()) return '「城市」不可空白'
    if (!['Asia', 'Europe', 'Americas', 'Africa', 'Australia'].includes(s('continent')))
      return '「洲別」須為 Asia / Europe / Americas / Africa / Australia'
    if (!DATE.test(s('visitedAt'))) return '「造訪日期」格式須為 YYYY-MM-DD（例：2025-07-01）'
  }
  return ''
}

// ── saveModal ──
async function saveModal(
  fd: Record<string, string>,
  pendingMultiFiles: (File | null)[],
  pendingSingleFile: File | null,
) {
  const validationError = validateForm(fd)
  if (validationError) { saveError.value = validationError; return }

  saving.value = true
  saveError.value = ''
  const s = (k: string): string => fd[k] ?? ''
  const isEdit = modalMode.value === 'edit'
  const buildPeriod = (from: string, to: string) => `${from.trim()} – ${to.trim() || '至今'}`

  try {
    if (current.value === 'internships') {
      const body = {
        company: s('company'), dept: s('dept'), role: s('role'),
        period: buildPeriod(s('periodFrom'), s('periodTo')),
        contribution: s('contribution'),
      }
      if (isEdit) {
        replaceInList(interns.value, await updateInternship(editId.value!, body))
      } else {
        let created = await createInternship(body)
        if (pendingSingleFile) created = await uploadInternshipPhoto(created.id, pendingSingleFile)
        interns.value.push(created)
      }

    } else if (current.value === 'projects') {
      const star = (['S', 'T', 'A', 'R'] as const)
        .map((l) => ({ label: l, text: s(`star${l}`) }))
        .filter((item) => item.text.trim())
      const body = {
        name: s('name'), type: s('type'),
        techLabel: s('techLabel') || '使用技術', tech: s('tech'),
        responsibility: s('responsibility'),
        members: Number(s('members')) || 1,
        period: buildPeriod(s('periodFrom'), s('periodTo')),
        core: s('core'),
        githubUrl: s('githubUrl') || undefined, youtubeUrl: s('youtubeUrl') || undefined,
        otherUrl: s('otherUrl') || undefined,
        star, createdAt: s('createdAt'),
      }
      if (isEdit) {
        replaceInList(projects.value, await updateProject(editId.value!, body))
      } else {
        projects.value.push(await createProject(body))
      }

    } else if (current.value === 'activities') {
      const body = {
        type: s('type') as 'leadership' | 'club',
        title: s('title'), organization: s('organization'),
        period: buildPeriod(s('periodFrom'), s('periodTo')),
        contribution: s('contribution'),
        photos: [] as string[],
      }
      if (isEdit) {
        replaceInList(experiences.value, await updateExperience(editId.value!, body))
      } else {
        let created = await createExperience(body)
        for (const file of pendingMultiFiles) {
          if (file) created = await uploadExperiencePhoto(created.id, file)
        }
        experiences.value.push(created)
      }

    } else if (current.value === 'social') {
      const sdgNumbers = s('sdgNumbers')
        .split(',').map((n) => parseInt(n.trim()))
        .filter((n): n is SdgNumber => !isNaN(n) && n >= 1 && n <= 17)
      const body = {
        name: s('name'), organization: s('organization'),
        esgType: s('esgType') as SocialActivity['esgType'],
        sdgNumbers,
        periodFrom: s('periodFrom'), periodTo: s('periodTo') || undefined,
        contribution: s('contribution'), reflection: s('reflection'),
      }
      if (isEdit) {
        replaceInList(socialActivities.value, await updateSocialActivity(editId.value!, body))
      } else {
        let created = await createSocialActivity(body)
        if (pendingSingleFile) created = await uploadSocialPhoto(created.id, pendingSingleFile)
        socialActivities.value.push(created)
      }

    } else if (current.value === 'literature') {
      const body = {
        title: s('title'),
        ageWritten: s('ageWritten') ? Number(s('ageWritten')) : undefined,
        period: s('period') || undefined,
        awards: s('awards'), summary: s('summary'),
        fullText: s('fullText') || undefined,
      }
      if (isEdit) {
        replaceInList(literatureWorks.value, await updateLiteratureWork(editId.value!, body))
      } else {
        literatureWorks.value.push(await createLiteratureWork(body))
      }

    } else if (current.value === 'papers') {
      const body = {
        topic: s('topic'), name: s('name'), journal: s('journal'),
        authors: s('authors'), year: Number(s('year')) || new Date().getFullYear(),
        purpose: s('purpose'), contribution: s('contribution'),
        notionUrl: s('notionUrl') || undefined,
      }
      if (isEdit) {
        replaceInList(papers.value, await updateThesisPaper(editId.value!, body))
      } else {
        papers.value.push(await createThesisPaper(body))
      }

    } else if (current.value === 'holdings') {
      const body = {
        symbol: s('symbol'), name: s('name'),
        currency: s('currency') as Holding['currency'],
        broker: s('broker'),
        shares: Number(s('shares')), avgPrice: Number(s('avgPrice')),
        marketPrice: Number(s('marketPrice')), dividend: Number(s('dividend')) || 0,
      }
      if (isEdit) {
        replaceInList(holdings.value, await updateHolding(editId.value!, body))
      } else {
        holdings.value.push(await createHolding(body))
      }

    } else if (current.value === 'academic') {
      const body = {
        school: s('school'), major: s('major'),
        period: buildPeriod(s('periodFrom'), s('periodTo')),
        gpa: s('gpa'), rank: s('rank'),
        facts: s('facts').split('\n').map((f) => f.trim()).filter(Boolean),
        sortOrder: isEdit ? (Number(fd['_sortOrder']) || 0) : academics.value.length + 1,
      }
      if (isEdit) {
        replaceInList(academics.value, await updateAcademicMilestone(editId.value!, body))
      } else {
        academics.value.push(await createAcademicMilestone(body))
      }

    } else if (current.value === 'futureplans') {
      const body = {
        phase: s('phase') as FuturePlan['phase'],
        title: s('title'), subtitle: s('subtitle'),
        items: s('items').split('\n').map((f) => f.trim()).filter(Boolean),
        sortOrder: isEdit ? (Number(fd['_sortOrder']) || 0) : futurePlans.value.length + 1,
      }
      if (isEdit) {
        replaceInList(futurePlans.value, await updateFuturePlan(editId.value!, body))
      } else {
        futurePlans.value.push(await createFuturePlan(body))
      }

    } else if (current.value === 'langcerts') {
      const body = {
        lang: s('lang') as LangCertAdmin['lang'],
        name: s('name'), score: s('score'), pct: Number(s('pct')) || 0,
      }
      if (isEdit) {
        replaceInList(langCerts.value, await updateLangCert(editId.value!, body))
      } else {
        langCerts.value.push(await createLangCert(body))
      }

    } else if (current.value === 'certgroups') {
      const body = {
        domain: s('domain') as CertGroupAdmin['domain'],
        category: s('category'),
        items: [s('name').trim()],
        sortOrder: isEdit ? (Number(fd['_sortOrder']) || 0) : certGroups.value.length + 1,
      }
      if (isEdit) {
        replaceInList(certGroups.value, await updateCertGroup(editId.value!, body))
      } else {
        certGroups.value.push(await createCertGroup(body))
      }

    } else if (current.value === 'travel') {
      const body = {
        country: s('country'), city: s('city'), continent: s('continent'),
        visitedAt: s('visitedAt'),
        companions: s('companions') || undefined,
        activities: s('activities') || undefined,
        purchases: s('purchases') || undefined,
        journal: s('journal') || undefined,
        photos: [] as string[],
      }
      if (isEdit) {
        replaceInList(travelEntries.value, await updateTravelEntry(editId.value!, body))
      } else {
        let created = await createTravelEntry(body)
        for (const file of pendingMultiFiles) {
          if (file) created = await uploadTravelPhoto(created.id, file)
        }
        travelEntries.value.push(created)
      }
    }

    modalOpen.value = false
  } catch (err) {
    saveError.value = err instanceof Error ? err.message : '儲存失敗，請再試一次'
  } finally {
    saving.value = false
  }
}

// ── handleModalSave (receives data emitted from AdminModal) ──
async function handleModalSave(data: {
  formData: Record<string, string>
  pendingMultiFiles: (File | null)[]
  pendingSingleFile: File | null
}) {
  await saveModal(data.formData, data.pendingMultiFiles, data.pendingSingleFile)
}

// ── Edit-mode photo management ──
async function uploadAdminPhoto(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file || editId.value === null) return
  ;(e.target as HTMLInputElement).value = ''
  photoUploading.value = true
  saveError.value = ''
  try {
    if (current.value === 'activities') {
      const updated = await uploadExperiencePhoto(editId.value, file)
      editingPhotos.value = updated.photos ?? []
      replaceInList(experiences.value, updated)
    } else if (current.value === 'travel') {
      const updated = await uploadTravelPhoto(editId.value, file)
      editingPhotos.value = updated.photos ?? []
      replaceInList(travelEntries.value, updated)
    }
  } catch (err) {
    saveError.value = err instanceof Error ? err.message : '上傳失敗'
  } finally {
    photoUploading.value = false
  }
}

async function deleteAdminPhoto(url: string) {
  if (editId.value === null) return
  photoUploading.value = true
  saveError.value = ''
  try {
    if (current.value === 'activities') {
      const updated = await deleteExperiencePhoto(editId.value, url)
      editingPhotos.value = updated.photos ?? []
      replaceInList(experiences.value, updated)
    } else if (current.value === 'travel') {
      const updated = await deleteTravelPhoto(editId.value, url)
      editingPhotos.value = updated.photos ?? []
      replaceInList(travelEntries.value, updated)
    }
  } catch (err) {
    saveError.value = err instanceof Error ? err.message : '刪除失敗'
  } finally {
    photoUploading.value = false
  }
}

function handleUploadSingleEdit(e: Event) {
  if (current.value === 'social') uploadAdminSocialPhoto(e)
  else if (current.value === 'internships') uploadAdminInternPhoto(e)
}

function handleDeleteSingleEdit() {
  if (current.value === 'social') deleteAdminSocialPhoto()
  else if (current.value === 'internships') deleteAdminInternPhoto()
}

async function uploadAdminSocialPhoto(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file || editId.value === null) return
  ;(e.target as HTMLInputElement).value = ''
  photoUploading.value = true
  saveError.value = ''
  try {
    const updated = await uploadSocialPhoto(editId.value, file)
    editingPhotoUrl.value = updated.photoUrl ?? ''
    replaceInList(socialActivities.value, updated)
  } catch (err) {
    saveError.value = err instanceof Error ? err.message : '上傳失敗'
  } finally {
    photoUploading.value = false
  }
}

async function deleteAdminSocialPhoto() {
  if (editId.value === null) return
  photoUploading.value = true
  saveError.value = ''
  try {
    const updated = await deleteSocialPhoto(editId.value)
    editingPhotoUrl.value = ''
    replaceInList(socialActivities.value, updated)
  } catch (err) {
    saveError.value = err instanceof Error ? err.message : '刪除失敗'
  } finally {
    photoUploading.value = false
  }
}

async function uploadAdminInternPhoto(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file || editId.value === null) return
  ;(e.target as HTMLInputElement).value = ''
  photoUploading.value = true
  saveError.value = ''
  try {
    const updated = await uploadInternshipPhoto(editId.value, file)
    editingPhotoUrl.value = updated.photoUrl ?? ''
    replaceInList(interns.value, updated)
  } catch (err) {
    saveError.value = err instanceof Error ? err.message : '上傳失敗'
  } finally {
    photoUploading.value = false
  }
}

async function deleteAdminInternPhoto() {
  if (editId.value === null) return
  photoUploading.value = true
  saveError.value = ''
  try {
    const updated = await deleteInternshipPhoto(editId.value)
    editingPhotoUrl.value = ''
    replaceInList(interns.value, updated)
  } catch (err) {
    saveError.value = err instanceof Error ? err.message : '刪除失敗'
  } finally {
    photoUploading.value = false
  }
}

// ── handleReorder (drag-and-drop sort) ──
async function handleReorder(fromIndex: number, toIndex: number) {
  if (fromIndex === toIndex) return

  function move<T>(arr: T[]): T[] {
    const copy = [...arr]
    copy.splice(toIndex, 0, ...copy.splice(fromIndex, 1))
    return copy
  }

  try {
    if (current.value === 'academic') {
      const reordered = move(academics.value)
      academics.value = reordered
      await reorderAcademic(reordered.map((a, i) => ({ id: a.id, sortOrder: i + 1 })))
      reordered.forEach((a, i) => { a.sortOrder = i + 1 })
    } else if (current.value === 'futureplans') {
      const reordered = move(futurePlans.value)
      futurePlans.value = reordered
      await reorderFuturePlans(reordered.map((p, i) => ({ id: p.id, sortOrder: i + 1 })))
      reordered.forEach((p, i) => { p.sortOrder = i + 1 })
    } else if (current.value === 'certgroups') {
      const reordered = move(certGroups.value)
      certGroups.value = reordered
      await reorderCertGroups(reordered.map((g, i) => ({ id: g.id, sortOrder: i + 1 })))
      reordered.forEach((g, i) => { g.sortOrder = i + 1 })
    }
  } catch {
    alert('排序更新失敗，請重試')
  }
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

.admin__main {
  flex: 1;
  padding: var(--space-7) var(--space-6);
  background: #f7f7f5;
  overflow-y: auto;
}

.notion-sync-bar {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}

.notion-sync-btn {
  padding: var(--space-2) var(--space-4);
  background: var(--color-ink-1);
  color: #fff;
  border: none;
  border-radius: var(--radius-sm);
  font-family: var(--font-cjk);
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}
.notion-sync-btn:hover:not(:disabled) { opacity: 0.82; }
.notion-sync-btn:disabled { opacity: 0.6; cursor: not-allowed; }

.notion-sync-msg {
  font-family: var(--font-cjk);
  font-size: 13px;
  color: var(--color-ink-2);
}
</style>
