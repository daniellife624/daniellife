import type { TimelineEvent, LiteratureWork } from '@/types/literature'
import { apiFetch } from './client'

export async function getTimelineEvents(): Promise<TimelineEvent[]> {
  return apiFetch<TimelineEvent[]>('/api/literature/timeline')
}

export async function getLiteratureWorks(): Promise<LiteratureWork[]> {
  return apiFetch<LiteratureWork[]>('/api/literature/works')
}
