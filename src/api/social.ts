import type { SocialActivity } from '@/types/social'
import { apiFetch } from './client'

export async function getSocialActivities(): Promise<SocialActivity[]> {
  return apiFetch<SocialActivity[]>('/api/social')
}
export async function createSocialActivity(body: Omit<SocialActivity, 'id'>): Promise<SocialActivity> {
  return apiFetch<SocialActivity>('/api/social', {
    method: 'POST', body: JSON.stringify(body),
  })
}
export async function updateSocialActivity(id: number, body: Omit<SocialActivity, 'id'>): Promise<SocialActivity> {
  return apiFetch<SocialActivity>(`/api/social/${id}`, {
    method: 'PUT', body: JSON.stringify(body),
  })
}
export async function deleteSocialActivity(id: number): Promise<void> {
  await apiFetch(`/api/social/${id}`, { method: 'DELETE' })
}
