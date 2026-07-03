import type { ThesisNote, ThesisIdea, ThesisPaper } from '@/types/thesis'
import { apiFetch } from './client'

export async function getThesisNote(): Promise<ThesisNote> {
  return apiFetch<ThesisNote>('/api/thesis/note')
}

export async function saveThesisNote(content: string): Promise<void> {
  await apiFetch('/api/thesis/note', {
    method: 'PUT',
    body: JSON.stringify({ content }),
  })
}

export async function getThesisIdeas(): Promise<ThesisIdea[]> {
  return apiFetch<ThesisIdea[]>('/api/thesis/ideas')
}

export async function addThesisIdea(idea: Omit<ThesisIdea, 'id'>): Promise<ThesisIdea> {
  return apiFetch<ThesisIdea>('/api/thesis/ideas', {
    method: 'POST',
    body: JSON.stringify(idea),
  })
}

export async function updateIdeaStatus(id: number, status: ThesisIdea['status']): Promise<void> {
  await apiFetch(`/api/thesis/ideas/${id}`, {
    method: 'PATCH',
    body: JSON.stringify({ status }),
  })
}

export async function updateThesisIdea(id: number, body: { title: string; content: string }): Promise<ThesisIdea> {
  return apiFetch<ThesisIdea>(`/api/thesis/ideas/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(body),
  })
}

export async function deleteThesisIdea(id: number): Promise<void> {
  await apiFetch(`/api/thesis/ideas/${id}`, { method: 'DELETE' })
}

export async function getThesisPapers(topic = '', journal = '', keyword = ''): Promise<ThesisPaper[]> {
  const params = new URLSearchParams()
  if (topic)   params.set('topic', topic)
  if (journal) params.set('journal', journal)
  if (keyword) params.set('keyword', keyword)
  const qs = params.toString() ? `?${params}` : ''
  return apiFetch<ThesisPaper[]>(`/api/thesis/papers${qs}`)
}
export async function createThesisPaper(body: Omit<ThesisPaper, 'id'>): Promise<ThesisPaper> {
  return apiFetch<ThesisPaper>('/api/thesis/papers', {
    method: 'POST', body: JSON.stringify(body),
  })
}
export async function updateThesisPaper(id: number, body: Omit<ThesisPaper, 'id'>): Promise<ThesisPaper> {
  return apiFetch<ThesisPaper>(`/api/thesis/papers/${id}`, {
    method: 'PUT', body: JSON.stringify(body),
  })
}
export async function deleteThesisPaper(id: number): Promise<void> {
  await apiFetch(`/api/thesis/papers/${id}`, { method: 'DELETE' })
}

export interface NotionSyncResult {
  synced: number[]
  failed: { id: number; name: string; error: string }[]
}

export async function syncNotionPapers(): Promise<NotionSyncResult> {
  return apiFetch<NotionSyncResult>('/api/thesis/papers/sync-notion', { method: 'POST' })
}
