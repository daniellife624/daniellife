export type EsgType = 'Environmental' | 'Social' | 'Governance'
export type SdgNumber = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17

export interface SocialActivity {
  id: number
  name: string
  organization: string
  esgType: EsgType
  sdgNumbers: SdgNumber[]
  periodFrom: string
  periodTo: string
  contribution: string
  reflection: string
  photoUrl?: string
}
