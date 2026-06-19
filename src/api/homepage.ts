import type {
  Internship,
  Project,
  CertData,
  AcademicMilestone,
  FuturePlan,
} from '@/types/homepage'

// ── Internships ────────────────────────────────────────────
const _interns: Internship[] = [
  {
    id: 1,
    company: '國泰信',
    dept: '數位發展部',
    role: '實習生',
    period: '2023/07 – 2023/09',
    contribution:
      '協助數位產品開發與用戶體驗改善，完成多項數位轉型專案的前期需求分析與功能規劃，實際參與跨部門協作流程...',
  },
  {
    id: 2,
    company: 'KPMG',
    dept: '數位審計',
    role: '實習生',
    period: '2024/07 – 2024/09',
    contribution:
      '參與數位審計工具開發，協助自動化審計流程設計與資料分析，學習四大事務所的工作方法與產業知識...',
  },
  {
    id: 3,
    company: 'XXXX',
    dept: 'XXXX部',
    role: '實習生',
    period: '2025/07 – 2025/09',
    contribution: '待補充...',
  },
]

export async function getInternships(): Promise<Internship[]> {
  // TODO: return apiFetch<Internship[]>('/api/internships')
  return _interns
}

// ── Projects ───────────────────────────────────────────────
const _projects: Project[] = [
  {
    id: 1,
    name: 'Meetro 相遇地圖',
    type: 'code',
    techLabel: '使用技術',
    tech: 'Vue.js, Python',
    members: 5,
    period: '2026/06 – 2026/12',
    core: '串接地圖 API 實現即時位置分享與社交功能',
    githubUrl: '#',
    youtubeUrl: '#',
    createdAt: '2026-06-01',
    star: [
      { label: 'S', text: '團隊需要一個讓活動參與者可以即時找到彼此的地圖工具，市面上現有產品無法滿足特定社群需求...' },
      { label: 'T', text: '負責前端地圖模組開發，整合 Leaflet.js 與後端 WebSocket 推播，確保毫秒級位置更新...' },
      { label: 'A', text: '設計模組化地圖組件，封裝位置訂閱邏輯；撰寫 E2E 測試覆蓋核心場景，優化 Bundle 大小 30%...' },
      { label: 'R', text: '活動當天支撐 200+ 名用戶同時上線，平均延遲低於 200ms，獲得主辦方高度肯定...' },
    ],
  },
  {
    id: 2,
    name: 'Meetro 相遇地圖',
    type: 'uiux',
    techLabel: '使用軟體',
    tech: 'Figma',
    members: 6,
    period: '2026/06 – 2026/12',
    core: '設計直覺易用的地圖社交平台視覺體驗',
    githubUrl: '#',
    youtubeUrl: '#',
    createdAt: '2026-06-01',
    star: [
      { label: 'S', text: '初版介面缺乏引導設計，新用戶完成率僅 40%，需要完整重新設計用戶旅程...' },
      { label: 'T', text: '主導 UX 研究與 Figma 原型設計，與工程師協作確保設計可實現性...' },
      { label: 'A', text: '進行 5 輪可用性測試，採用 Material Design 設計語言，建立元件庫供團隊複用...' },
      { label: 'R', text: '重設計後新用戶完成率提升至 78%，NPS 分數從 32 提升至 67...' },
    ],
  },
  {
    id: 3,
    name: '存貨流程自動化',
    type: 'finance',
    techLabel: '使用技術',
    tech: '存貨帳前分析, Python',
    members: 11,
    period: '2026/06 – 2026/12',
    core: '以 Python 自動化存貨盤點與帳目核對流程',
    githubUrl: '#',
    createdAt: '2026-05-01',
    star: [
      { label: 'S', text: '中小企業每月花費 40+ 人時進行手動存貨核對，錯誤率高且效率低落...' },
      { label: 'T', text: '設計並實作 Python 自動化腳本，自動讀取 ERP 資料並生成差異報告...' },
      { label: 'A', text: '串接 SAP API 取得即時庫存資料，實作異常偵測演算法，建置視覺化報表介面...' },
      { label: 'R', text: '核對時間從 40 小時縮短至 2 小時，錯誤率降低 95%，已部署至 3 家企業...' },
    ],
  },
  {
    id: 4,
    name: 'Meetro 相遇地圖',
    type: 'code',
    techLabel: '使用技術',
    tech: 'Vue.js, Python',
    members: 5,
    period: '2026/06 – 2026/12',
    core: '以 FastAPI + PostgreSQL 建構高併發地圖後端',
    githubUrl: '#',
    youtubeUrl: '#',
    createdAt: '2026-04-01',
    star: [
      { label: 'S', text: '平台高峰期 API 回應延遲過高，影響用戶即時體驗...' },
      { label: 'T', text: '負責後端 API 設計與資料庫 Schema 規劃...' },
      { label: 'A', text: '採用 FastAPI + PostgreSQL + Redis 架構，實現 CQRS 讀寫分離...' },
      { label: 'R', text: 'API 回應時間 P99 < 100ms，支撐高峰流量無中斷...' },
    ],
  },
]

export async function getProjects(): Promise<Project[]> {
  // TODO: return apiFetch<Project[]>('/api/projects')
  return _projects
}

// ── Certifications ─────────────────────────────────────────
const _certData: CertData = {
  language: {
    en: [
      { name: 'TOEIC', score: '865', pct: 87.4 },
      { name: '劍橋英檢', score: 'B2+', pct: 78 },
    ],
    jp: [{ name: 'JLPT', score: 'N4', pct: 45 }],
  },
  finance: [
    { category: '國際證照', items: ['待補充'] },
    { category: '國內重要證照', items: ['待補充'] },
    { category: '國內其他證照', items: ['待補充'] },
    { category: 'ESG', items: ['待補充'] },
  ],
  it: [
    { category: '國際證照', items: ['待補充'] },
    { category: '國內重要證照', items: ['待補充'] },
    { category: '國內其他證照', items: ['待補充'] },
    { category: 'ESG', items: ['待補充'] },
  ],
}

export async function getCertData(): Promise<CertData> {
  // TODO: return apiFetch<CertData>('/api/certs')
  return _certData
}

// ── Academic ───────────────────────────────────────────────
const _academic: AcademicMilestone[] = [
  {
    id: 1,
    school: '專科 中科大',
    major: '資處系',
    period: '2018 – 2021',
    gpa: '4.26/4',
    rank: '4/XX',
    facts: ['GPA: 4.26/4', '系排: 4/XX', '市內獎', '國科會大一國文助教', '捧大第一名進中央金'],
  },
  {
    id: 2,
    school: '大學 中央',
    major: '財金系',
    period: '2021 – 2024',
    gpa: '4.26/4.30',
    rank: '3/71',
    facts: ['GPA: 4.26/4.30', '系排: 3/71', '大三上/大四下書卷獎', '院長獎', '大一會積分全院第7名'],
  },
  {
    id: 3,
    school: '碩士 臺大',
    major: '會計系',
    period: '2024 – 現在',
    gpa: '4.18/4.30',
    rank: '5/43',
    facts: ['GPA: 4.18/4.30', '系排: 5/43', '研究領域：AIS', '待補充', '待補充'],
  },
]

export async function getAcademicMilestones(): Promise<AcademicMilestone[]> {
  // TODO: return apiFetch<AcademicMilestone[]>('/api/academic')
  return _academic
}

// ── Future Plans ───────────────────────────────────────────
const _plans: FuturePlan[] = [
  {
    id: 1,
    phase: 'mid',
    title: '中期',
    subtitle: '畢業後 1–3 年',
    items: ['外商科技公司財務會計', '科技所用相關職位'],
  },
  {
    id: 2,
    phase: 'mid-short',
    title: '中短期',
    subtitle: '碩班畢業前',
    items: ['認真思考、撰寫論文主題', '上岸大外資財會相關職位實習（碩三一學年）'],
  },
  {
    id: 3,
    phase: 'short',
    title: '短期',
    subtitle: '近一年',
    items: ['考取 CMA', '參加學期實習（2天）', '拉高學業英文'],
  },
]

export async function getFuturePlans(): Promise<FuturePlan[]> {
  // TODO: return apiFetch<FuturePlan[]>('/api/plans')
  return _plans
}
