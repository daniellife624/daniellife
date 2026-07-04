import type { TimelineEvent, LiteratureWork } from '@/types/literature'
import { apiFetch } from './client'

export async function getTimelineEvents(): Promise<TimelineEvent[]> {
  return apiFetch<TimelineEvent[]>('/api/literature/timeline')
}

export async function getLiteratureWorks(): Promise<LiteratureWork[]> {
  return apiFetch<LiteratureWork[]>('/api/literature/works')
}
export async function createLiteratureWork(body: Omit<LiteratureWork, 'id'>): Promise<LiteratureWork> {
  return apiFetch<LiteratureWork>('/api/literature/works', {
    method: 'POST', body: JSON.stringify(body),
  })
}
export async function updateLiteratureWork(id: number, body: Omit<LiteratureWork, 'id'>): Promise<LiteratureWork> {
  return apiFetch<LiteratureWork>(`/api/literature/works/${id}`, {
    method: 'PUT', body: JSON.stringify(body),
  })
}
export async function deleteLiteratureWork(id: number): Promise<void> {
  await apiFetch(`/api/literature/works/${id}`, { method: 'DELETE' })
}
