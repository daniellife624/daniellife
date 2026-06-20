import type { Experience, TravelEntry, Continent } from '@/types/activities'
import { apiFetch } from './client'

export async function getExperiences(): Promise<Experience[]> {
  return apiFetch<Experience[]>('/api/activities/experiences')
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
