import type { ThesisNote, ThesisIdea, ThesisPaper } from '@/types/thesis'
import { apiFetch, getToken } from './client'

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

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

export async function updatePaperNotes(id: number, notes: string): Promise<ThesisPaper> {
  return apiFetch<ThesisPaper>(`/api/thesis/papers/${id}/notes`, {
    method: 'PATCH',
    body: JSON.stringify({ notes }),
  })
}

export async function uploadPaperNoteImage(id: number, file: File): Promise<{ url: string }> {
  const form = new FormData()
  form.append('file', file)
  const token = getToken()
  const res = await fetch(`${BASE_URL}/api/thesis/papers/${id}/notes/image`, {
    method: 'POST',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    body: form,
  })
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`)
  return res.json()
}
