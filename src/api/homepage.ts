import { apiFetch, getToken } from './client'

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'
import type {
  Internship, Project, CertData, AcademicMilestone, FuturePlan,
  LangCertAdmin, CertGroupAdmin,
} from '@/types/homepage'

// ── Internships ──────────────────────────────────────────────────
export async function getInternships(): Promise<Internship[]> {
  try { return await apiFetch<Internship[]>('/api/homepage/internships') } catch { return [] }
}
export async function createInternship(body: Omit<Internship, 'id'>): Promise<Internship> {
  return apiFetch<Internship>('/api/homepage/internships', { method: 'POST', body: JSON.stringify(body) })
}
export async function updateInternship(id: number, body: Omit<Internship, 'id'>): Promise<Internship> {
  return apiFetch<Internship>(`/api/homepage/internships/${id}`, { method: 'PUT', body: JSON.stringify(body) })
}
export async function deleteInternship(id: number): Promise<void> {
  await apiFetch(`/api/homepage/internships/${id}`, { method: 'DELETE' })
}
export async function uploadInternshipPhoto(id: number, file: File): Promise<Internship> {
  const form = new FormData()
  form.append('file', file)
  const token = getToken()
  const res = await fetch(`${BASE_URL}/api/homepage/internships/${id}/photo`, {
    method: 'POST',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    body: form,
  })
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`)
  return res.json()
}
export async function deleteInternshipPhoto(id: number): Promise<Internship> {
  return apiFetch<Internship>(`/api/homepage/internships/${id}/photo`, { method: 'DELETE' })
}

// ── Projects ─────────────────────────────────────────────────────
export async function getProjects(): Promise<Project[]> {
  try { return await apiFetch<Project[]>('/api/homepage/projects') } catch { return [] }
}
export async function createProject(body: Omit<Project, 'id'>): Promise<Project> {
  return apiFetch<Project>('/api/homepage/projects', { method: 'POST', body: JSON.stringify(body) })
}
export async function updateProject(id: number, body: Omit<Project, 'id'>): Promise<Project> {
  return apiFetch<Project>(`/api/homepage/projects/${id}`, { method: 'PUT', body: JSON.stringify(body) })
}
export async function deleteProject(id: number): Promise<void> {
  await apiFetch(`/api/homepage/projects/${id}`, { method: 'DELETE' })
}

// ── CertData (public) ────────────────────────────────────────────
export async function getCertData(): Promise<CertData> {
  try { return await apiFetch<CertData>('/api/homepage/certs') }
  catch { return { language: { en: [], jp: [] }, finance: [], it: [] } }
}

// ── Lang Certs (admin) ───────────────────────────────────────────
export async function getLangCerts(): Promise<LangCertAdmin[]> {
  try { return await apiFetch<LangCertAdmin[]>('/api/homepage/lang-certs') } catch { return [] }
}
export async function createLangCert(body: Omit<LangCertAdmin, 'id'>): Promise<LangCertAdmin> {
  return apiFetch<LangCertAdmin>('/api/homepage/lang-certs', { method: 'POST', body: JSON.stringify(body) })
}
export async function updateLangCert(id: number, body: Omit<LangCertAdmin, 'id'>): Promise<LangCertAdmin> {
  return apiFetch<LangCertAdmin>(`/api/homepage/lang-certs/${id}`, { method: 'PUT', body: JSON.stringify(body) })
}
export async function deleteLangCert(id: number): Promise<void> {
  await apiFetch(`/api/homepage/lang-certs/${id}`, { method: 'DELETE' })
}

// ── Cert Groups (admin) ──────────────────────────────────────────
export async function getCertGroups(): Promise<CertGroupAdmin[]> {
  try { return await apiFetch<CertGroupAdmin[]>('/api/homepage/cert-groups') } catch { return [] }
}
export async function createCertGroup(body: Omit<CertGroupAdmin, 'id'>): Promise<CertGroupAdmin> {
  return apiFetch<CertGroupAdmin>('/api/homepage/cert-groups', { method: 'POST', body: JSON.stringify(body) })
}
export async function updateCertGroup(id: number, body: Omit<CertGroupAdmin, 'id'>): Promise<CertGroupAdmin> {
  return apiFetch<CertGroupAdmin>(`/api/homepage/cert-groups/${id}`, { method: 'PUT', body: JSON.stringify(body) })
}
export async function deleteCertGroup(id: number): Promise<void> {
  await apiFetch(`/api/homepage/cert-groups/${id}`, { method: 'DELETE' })
}

// ── Academic ─────────────────────────────────────────────────────
export async function getAcademicMilestones(): Promise<AcademicMilestone[]> {
  try { return await apiFetch<AcademicMilestone[]>('/api/homepage/academic') } catch { return [] }
}
export async function createAcademicMilestone(body: Omit<AcademicMilestone, 'id'>): Promise<AcademicMilestone> {
  return apiFetch<AcademicMilestone>('/api/homepage/academic', { method: 'POST', body: JSON.stringify(body) })
}
export async function updateAcademicMilestone(id: number, body: Omit<AcademicMilestone, 'id'>): Promise<AcademicMilestone> {
  return apiFetch<AcademicMilestone>(`/api/homepage/academic/${id}`, { method: 'PUT', body: JSON.stringify(body) })
}
export async function deleteAcademicMilestone(id: number): Promise<void> {
  await apiFetch(`/api/homepage/academic/${id}`, { method: 'DELETE' })
}

// ── FuturePlans ──────────────────────────────────────────────────
export async function getFuturePlans(): Promise<FuturePlan[]> {
  try { return await apiFetch<FuturePlan[]>('/api/homepage/future-plans') } catch { return [] }
}
export async function createFuturePlan(body: Omit<FuturePlan, 'id'>): Promise<FuturePlan> {
  return apiFetch<FuturePlan>('/api/homepage/future-plans', { method: 'POST', body: JSON.stringify(body) })
}
export async function updateFuturePlan(id: number, body: Omit<FuturePlan, 'id'>): Promise<FuturePlan> {
  return apiFetch<FuturePlan>(`/api/homepage/future-plans/${id}`, { method: 'PUT', body: JSON.stringify(body) })
}
export async function deleteFuturePlan(id: number): Promise<void> {
  await apiFetch(`/api/homepage/future-plans/${id}`, { method: 'DELETE' })
}
