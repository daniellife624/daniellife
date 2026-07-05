export type ExperienceType = 'leadership' | 'club' | 'other'

export interface PhotoItem {
  url: string
  position: string
}

export interface Experience {
  id: number
  type: ExperienceType
  title: string
  organization: string
  period: string
  contribution: string
  photos: PhotoItem[]
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
  photos?: PhotoItem[]
}

export interface Continent {
  key: string
  label: string
  entries: TravelEntry[]
}
