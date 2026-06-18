import type { TimelineEvent, LiteratureWork } from '@/types/literature'

const _timeline: TimelineEvent[] = [
  { id: 1, gradeLabel: '小學 / 五年級', awardTitle: '校內語文競賽作文', result: '第一名', date: '2010.05.10', workId: 1 },
  { id: 2, gradeLabel: '小學 / 六年級', awardTitle: '校內語文競賽作文', result: '第一名', date: '2011.05.10', workId: 2 },
  { id: 3, gradeLabel: '國中 / 二年級', awardTitle: '校內語文競賽作文', result: '第一名', date: '2014.05.10' },
  { id: 4, gradeLabel: '高中 / 一年級', awardTitle: '全國語文競賽', result: '優等', date: '2016.09.15' },
  { id: 5, gradeLabel: '大學 / 三年級', awardTitle: '校內語文競賽小說組', result: '首獎', date: '2023.05.20', workId: 3 },
]

export async function getTimelineEvents(): Promise<TimelineEvent[]> {
  // TODO: return apiFetch<TimelineEvent[]>('/api/literature/timeline')
  return _timeline
}

const _works: LiteratureWork[] = [
  {
    id: 1,
    title: '作品名稱',
    ageWritten: 18,
    period: '2023.06',
    awards: '校內語文競賽小說組首獎',
    summary: 'XXXXXXXXXXXXXXXXXXXX',
  },
  {
    id: 2,
    title: '作品名稱',
    ageWritten: 18,
    period: '2023.06',
    awards: '校內語文競賽小說組首獎',
    summary: 'XXXXXXXXXXXXXXXXXXXX',
  },
]

export async function getLiteratureWorks(): Promise<LiteratureWork[]> {
  // TODO: return apiFetch<LiteratureWork[]>('/api/literature')
  return _works
}
