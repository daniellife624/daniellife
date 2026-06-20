export interface TimelineEvent {
  id: number
  gradeLabel: string
  awardTitle: string
  result: string
  date: string
  workId?: number
}

export interface LiteratureWork {
  id: number
  title: string
  ageWritten?: number
  period?: string
  awards: string
  summary: string
  fullText?: string
}
