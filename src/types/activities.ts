export type ExperienceType = 'leadership' | 'club'

export interface Experience {
  id: number
  type: ExperienceType
  title: string
  organization: string
  period: string
  contribution: string
  photos: string[]
}

export interface TravelEntry {
  id: number
  country: string
  city: string
  continent: string
  visitedAt: string
  journal?: string
  companions?: string
  activities?: string
  purchases?: string
  photos?: string[]
}

export interface Continent {
  key: string
  label: string
  entries: TravelEntry[]
}
