import type { SocialActivity } from '@/types/social'
import { apiFetch, getToken } from './client'

const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

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

export async function uploadSocialPhoto(id: number, file: File): Promise<SocialActivity> {
  const form = new FormData()
  form.append('file', file)
  const token = getToken()
  const res = await fetch(`${BASE_URL}/api/social/${id}/photo`, {
    method: 'POST',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
    body: form,
  })
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`)
  return res.json()
}

export async function deleteSocialPhoto(id: number): Promise<SocialActivity> {
  return apiFetch<SocialActivity>(`/api/social/${id}/photo`, { method: 'DELETE' })
}

export async function updateSocialPhotoPosition(id: number, position: string): Promise<SocialActivity> {
  return apiFetch<SocialActivity>(`/api/social/${id}/photo-position`, {
    method: 'PATCH', body: JSON.stringify({ position }),
  })
}
