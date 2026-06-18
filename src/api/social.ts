import type { SocialActivity } from '@/types/social'

const _activities: SocialActivity[] = [
  {
    id: 1,
    name: '活動名稱 XXXXXX',
    organization: '外交部',
    esgType: 'Environmental',
    sdgNumbers: [13, 15],
    periodFrom: '2026/01/01',
    periodTo: '2026/04/02',
    contribution: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX...',
    reflection: '此活動讓我更了解環境永續的重要性...',
  },
  {
    id: 2,
    name: '活動名稱 XXXXXX',
    organization: '外交部',
    esgType: 'Social',
    sdgNumbers: [1, 3],
    periodFrom: '2026/01/01',
    periodTo: '2026/04/02',
    contribution: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX...',
    reflection: '透過社會參與深化對公民社會的理解...',
  },
  {
    id: 3,
    name: '活動名稱 XXXXXX',
    organization: '環保署',
    esgType: 'Environmental',
    sdgNumbers: [7, 13],
    periodFrom: '2025/06/01',
    periodTo: '2025/09/01',
    contribution: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX...',
    reflection: '參與環保活動增加對氣候議題的認識...',
  },
  {
    id: 4,
    name: '活動名稱 XXXXXX',
    organization: '金管會',
    esgType: 'Governance',
    sdgNumbers: [16, 17],
    periodFrom: '2025/03/01',
    periodTo: '2025/05/31',
    contribution: 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX...',
    reflection: '了解公司治理的重要性與實務操作...',
  },
]

export async function getSocialActivities(): Promise<SocialActivity[]> {
  // TODO: return apiFetch<SocialActivity[]>('/api/social')
  return _activities
}
