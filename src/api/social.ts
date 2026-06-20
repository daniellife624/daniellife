import type { SocialActivity } from '@/types/social'
import { apiFetch } from './client'

export async function getSocialActivities(): Promise<SocialActivity[]> {
  return apiFetch<SocialActivity[]>('/api/social')
}
