import { apiFetch } from './client'
import type {
  Internship,
  Project,
  CertData,
  AcademicMilestone,
  FuturePlan,
} from '@/types/homepage'

// ── Internships ─────────────────────────────────────────────
export async function getInternships(): Promise<Internship[]> {
  try { return await apiFetch<Internship[]>('/api/homepage/internships') } catch { return [] }
}
export async function createInternship(body: Omit<Internship, 'id'>): Promise<Internship> {
  return apiFetch<Internship>('/api/homepage/internships', {
    method: 'POST', body: JSON.stringify(body),
  })
}
export async function updateInternship(id: number, body: Omit<Internship, 'id'>): Promise<Internship> {
  return apiFetch<Internship>(`/api/homepage/internships/${id}`, {
    method: 'PUT', body: JSON.stringify(body),
  })
}
export async function deleteInternship(id: number): Promise<void> {
  await apiFetch(`/api/homepage/internships/${id}`, { method: 'DELETE' })
}

// ── Projects ─────────────────────────────────────────────────
export async function getProjects(): Promise<Project[]> {
  try { return await apiFetch<Project[]>('/api/homepage/projects') } catch { return [] }
}
export async function createProject(body: Omit<Project, 'id'>): Promise<Project> {
  return apiFetch<Project>('/api/homepage/projects', {
    method: 'POST', body: JSON.stringify(body),
  })
}
export async function updateProject(id: number, body: Omit<Project, 'id'>): Promise<Project> {
  return apiFetch<Project>(`/api/homepage/projects/${id}`, {
    method: 'PUT', body: JSON.stringify(body),
  })
}
export async function deleteProject(id: number): Promise<void> {
  await apiFetch(`/api/homepage/projects/${id}`, { method: 'DELETE' })
}

// ── CertData ─────────────────────────────────────────────────
export async function getCertData(): Promise<CertData> {
  try { return await apiFetch<CertData>('/api/homepage/certs') }
  catch { return { language: { en: [], jp: [] }, finance: [], it: [] } }
}

// ── Academic ─────────────────────────────────────────────────
export async function getAcademicMilestones(): Promise<AcademicMilestone[]> {
  try { return await apiFetch<AcademicMilestone[]>('/api/homepage/academic') } catch { return [] }
}

// ── FuturePlans ──────────────────────────────────────────────
export async function getFuturePlans(): Promise<FuturePlan[]> {
  try { return await apiFetch<FuturePlan[]>('/api/homepage/future-plans') } catch { return [] }
}
