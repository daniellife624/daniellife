export type IdeaStatus = 'pending' | 'rejected' | 'approved'

export interface ThesisNote {
  content: string
  updatedAt: string
}

export interface ThesisIdea {
  id: number
  title: string
  content: string
  status: IdeaStatus
  createdAt: string
}

export interface ThesisPaper {
  id: number
  topic: string
  name: string
  journal: string
  authors: string
  year: number
  purpose: string
  contribution: string
  notes?: string | null
  notionUrl?: string | null
}
