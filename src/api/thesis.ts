import type { ThesisNote, ThesisIdea, ThesisPaper } from '@/types/thesis'

const _note: ThesisNote = {
  content: '碩論注意事項、教授建議',
  updatedAt: '2026/06/15',
}

export async function getThesisNote(): Promise<ThesisNote> {
  // TODO: return apiFetch<ThesisNote>('/api/thesis/notes')
  return { ..._note }
}

export async function saveThesisNote(content: string): Promise<void> {
  // TODO: apiFetch('/api/thesis/notes', { method: 'PUT', body: JSON.stringify({ content }) })
  _note.content = content
}

const _ideas: ThesisIdea[] = [
  { id: 1, title: '想法一', content: '關於 AIS 與 AI 整合的研究方向...', status: 'pending', createdAt: '2026-06-01' },
  { id: 2, title: '想法二', content: '研究生成式 AI 對財務報表分析的影響...', status: 'approved', createdAt: '2026-06-05' },
  { id: 3, title: '想法三', content: '某個方向無法執行的原因...', status: 'rejected', createdAt: '2026-06-10' },
]

export async function getThesisIdeas(): Promise<ThesisIdea[]> {
  // TODO: return apiFetch<ThesisIdea[]>('/api/thesis/ideas')
  return _ideas
}

export async function addThesisIdea(idea: Omit<ThesisIdea, 'id'>): Promise<ThesisIdea> {
  // TODO: return apiFetch<ThesisIdea>('/api/thesis/ideas', { method: 'POST', body: JSON.stringify(idea) })
  const newIdea: ThesisIdea = { ...idea, id: Date.now() }
  _ideas.push(newIdea)
  return newIdea
}

export async function updateIdeaStatus(id: number, status: ThesisIdea['status']): Promise<void> {
  // TODO: apiFetch(`/api/thesis/ideas/${id}`, { method: 'PUT', body: JSON.stringify({ status }) })
  const idea = _ideas.find((i) => i.id === id)
  if (idea) idea.status = status
}

export async function deleteThesisIdea(id: number): Promise<void> {
  // TODO: apiFetch(`/api/thesis/ideas/${id}`, { method: 'DELETE' })
  const idx = _ideas.findIndex((i) => i.id === id)
  if (idx !== -1) _ideas.splice(idx, 1)
}

const _papers: ThesisPaper[] = [
  {
    id: 1,
    topic: 'LLM',
    name: 'The impact of generative AI on information processing: Evidence from the ban of ChatGPT in Italy.',
    journal: 'Journal of Accounting and Economics',
    authors: 'Bertomeu, J., Lin, Y., Liu, Y., & Ni, Z.',
    year: 2025,
    purpose: '本論文的研究目的旨在探討「生成式人工智慧（如ChatGPT）的出現與應用，是否影響資本市場的資訊處理效率」...',
    contribution: '1. 縮減文字空間：首創利用「義大利禁用ChatGPT」的自然實驗，提供生成式AI影響資本市場資訊效率的因果證據...',
  },
]

export async function getThesisPapers(topic = '', journal = '', keyword = ''): Promise<ThesisPaper[]> {
  // TODO: return apiFetch<ThesisPaper[]>(`/api/thesis/papers?topic=${topic}&journal=${journal}&q=${keyword}`)
  return _papers.filter(
    (p) =>
      (!topic || p.topic === topic) &&
      (!journal || p.journal === journal) &&
      (!keyword || p.name.toLowerCase().includes(keyword.toLowerCase())),
  )
}
