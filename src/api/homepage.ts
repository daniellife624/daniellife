import { apiFetch } from './client'
import type {
  Internship,
  Project,
  CertData,
  AcademicMilestone,
  FuturePlan,
} from '@/types/homepage'

export async function getInternships(): Promise<Internship[]> {
  try {
    return await apiFetch<Internship[]>('/api/homepage/internships')
  } catch {
    return []
  }
}

export async function getProjects(): Promise<Project[]> {
  try {
    return await apiFetch<Project[]>('/api/homepage/projects')
  } catch {
    return []
  }
}

export async function getCertData(): Promise<CertData> {
  try {
    return await apiFetch<CertData>('/api/homepage/certs')
  } catch {
    return { language: { en: [], jp: [] }, finance: [], it: [] }
  }
}

export async function getAcademicMilestones(): Promise<AcademicMilestone[]> {
  try {
    return await apiFetch<AcademicMilestone[]>('/api/homepage/academic')
  } catch {
    return []
  }
}

export async function getFuturePlans(): Promise<FuturePlan[]> {
  try {
    return await apiFetch<FuturePlan[]>('/api/homepage/future-plans')
  } catch {
    return []
  }
}
