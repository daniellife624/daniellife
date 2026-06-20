import type { Experience, TravelEntry, Continent } from '@/types/activities'
import { apiFetch } from './client'

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
