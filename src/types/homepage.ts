export interface Internship {
  id: number
  company: string
  dept: string
  role: string
  period: string
  contribution: string
  photoUrl?: string
}

export interface StarItem {
  label: 'S' | 'T' | 'A' | 'R'
  text: string
}

export type ProjectType = 'code' | 'uiux' | 'finance'

export interface Project {
  id: number
  name: string
  type: string // comma-separated ProjectType values, e.g. "code,finance"
  techLabel: string
  tech: string
  members: number
  period: string
  core: string
  githubUrl?: string
  youtubeUrl?: string
  otherUrl?: string
  star: StarItem[]
  createdAt: string
}

export interface LangCert {
  name: string
  score: string
  pct: number
}

export interface LangCertAdmin {
  id: number
  lang: 'en' | 'jp'
  name: string
  score: string
  pct: number
}

export interface CertGroup {
  category: string
  items: string[]
}

export interface CertGroupAdmin {
  id: number
  domain: '財會' | '資訊' | 'finance' | 'it'
  category: string
  items: string[]
  sortOrder: number
}

export interface CertData {
  language: { en: LangCert[]; jp: LangCert[] }
  finance: CertGroup[]
  it: CertGroup[]
}

export interface AcademicMilestone {
  id: number
  school: string
  major: string
  period: string
  gpa: string
  rank: string
  facts: string[]
  sortOrder?: number
}

export type PlanPhase = 'short' | 'mid-short' | 'mid'

export interface FuturePlan {
  id: number
  phase: PlanPhase
  title: string
  subtitle: string
  items: string[]
  sortOrder?: number
}
