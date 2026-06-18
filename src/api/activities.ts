import type { Experience, TravelEntry, Continent } from '@/types/activities'

const _experiences: Experience[] = [
  {
    id: 1,
    type: 'leadership',
    title: '大一國文助教',
    organization: '國立臺中科技大學 通識教育中心',
    period: '2021/04 – 2023/06',
    contribution:
      '擔任大一國文課程助教，協助教授備課與批改作業；每週帶領學生討論文學作品，培養學生語文表達能力；期末協助規劃成果展...',
    photos: [],
  },
  {
    id: 2,
    type: 'club',
    title: 'GDSC 美術組核心幹部',
    organization: '國立中央大學',
    period: '2023/09 – 2024/01',
    contribution:
      '負責社群媒體視覺設計與活動文宣，統籌 Google Developer Student Club 美術組運作；協助舉辦技術工作坊海報設計，提升社員招募轉換率...',
    photos: [],
  },
]

export async function getExperiences(): Promise<Experience[]> {
  // TODO: return apiFetch<Experience[]>('/api/activities')
  return _experiences
}

const _travelEntries: TravelEntry[] = [
  { id: 1, country: '臺灣', city: '台北', continent: 'Asia', visitedAt: '2003-01-01' },
  { id: 2, country: '日本', city: '東京', continent: 'Asia', visitedAt: '2019-08-01' },
  { id: 3, country: '澳大利亞', city: '雪梨', continent: 'Australia', visitedAt: '2023-01-01' },
]

export async function getTravelEntries(): Promise<TravelEntry[]> {
  // TODO: return apiFetch<TravelEntry[]>('/api/travel')
  return _travelEntries
}

export function groupByContinent(entries: TravelEntry[]): Continent[] {
  const continents: Continent[] = [
    { key: 'Europe', label: 'Europe', entries: [] },
    { key: 'Asia', label: 'Asia', entries: [] },
    { key: 'Africa', label: 'Africa', entries: [] },
    { key: 'Australia', label: 'Australia', entries: [] },
    { key: 'Americas', label: 'North America and South America', entries: [] },
  ]
  for (const entry of entries) {
    const c = continents.find((c) => c.key === entry.continent)
    if (c) c.entries.push(entry)
  }
  return continents
}
