import type { Experience, TravelEntry, Continent } from '@/types/activities'
import { apiFetch, getToken } from './client'

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

export async function uploadExperiencePhoto(id: number, file: File): Promise<Experience> {
  const form = new FormData()
  form.append('file', file)
  const token = getToken()
  const res = await fetch(`${BASE_URL}/api/activities/experiences/${id}/photo`, {
    method: 'POST',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    body: form,
  })
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`)
  return res.json()
}

export async function deleteExperiencePhoto(id: number, url: string): Promise<Experience> {
  return apiFetch<Experience>(`/api/activities/experiences/${id}/photo?url=${encodeURIComponent(url)}`, { method: 'DELETE' })
}

export async function deleteTravelPhoto(id: number, url: string): Promise<TravelEntry> {
  return apiFetch<TravelEntry>(`/api/activities/travel/${id}/photo?url=${encodeURIComponent(url)}`, { method: 'DELETE' })
}

export async function uploadTravelPhoto(id: number, file: File): Promise<TravelEntry> {
  const form = new FormData()
  form.append('file', file)
  const token = getToken()
  const res = await fetch(`${BASE_URL}/api/activities/travel/${id}/photo`, {
    method: 'POST',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    body: form,
  })
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`)
  return res.json()
}

export async function getExperiences(): Promise<Experience[]> {
  return apiFetch<Experience[]>('/api/activities/experiences')
}
export async function createExperience(body: Omit<Experience, 'id'>): Promise<Experience> {
  return apiFetch<Experience>('/api/activities/experiences', {
    method: 'POST', body: JSON.stringify(body),
  })
}
export async function updateExperience(id: number, body: Omit<Experience, 'id'>): Promise<Experience> {
  return apiFetch<Experience>(`/api/activities/experiences/${id}`, {
    method: 'PUT', body: JSON.stringify(body),
  })
}
export async function deleteExperience(id: number): Promise<void> {
  await apiFetch(`/api/activities/experiences/${id}`, { method: 'DELETE' })
}

export async function getTravelEntries(): Promise<TravelEntry[]> {
  return apiFetch<TravelEntry[]>('/api/activities/travel')
}
export async function createTravelEntry(body: Omit<TravelEntry, 'id'>): Promise<TravelEntry> {
  return apiFetch<TravelEntry>('/api/activities/travel', { method: 'POST', body: JSON.stringify(body) })
}
export async function updateTravelEntry(id: number, body: Omit<TravelEntry, 'id'>): Promise<TravelEntry> {
  return apiFetch<TravelEntry>(`/api/activities/travel/${id}`, { method: 'PUT', body: JSON.stringify(body) })
}
export async function deleteTravelEntry(id: number): Promise<void> {
  await apiFetch(`/api/activities/travel/${id}`, { method: 'DELETE' })
}

export function groupByContinent(entries: TravelEntry[]): Continent[] {
  const continents: Continent[] = [
    { key: 'Europe',    label: 'Europe',                          entries: [] },
    { key: 'Asia',      label: 'Asia',                            entries: [] },
    { key: 'Africa',    label: 'Africa',                          entries: [] },
    { key: 'Australia', label: 'Australia',                       entries: [] },
    { key: 'Americas',  label: 'North America and South America', entries: [] },
  ]
  for (const entry of entries) {
    const c = continents.find((c) => c.key === entry.continent)
    if (c) c.entries.push(entry)
  }
  return continents
}
