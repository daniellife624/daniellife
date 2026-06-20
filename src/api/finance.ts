import type { Holding, PortfolioSummary } from '@/types/finance'
import { apiFetch } from './client'

export async function getHoldings(): Promise<Holding[]> {
  return apiFetch<Holding[]>('/api/finance/holdings')
}
export async function createHolding(body: Omit<Holding, 'id' | 'currentValue' | 'pnl' | 'returnRate'>): Promise<Holding> {
  return apiFetch<Holding>('/api/finance/holdings', {
    method: 'POST', body: JSON.stringify(body),
  })
}
export async function updateHolding(id: number, body: Omit<Holding, 'id' | 'currentValue' | 'pnl' | 'returnRate'>): Promise<Holding> {
  return apiFetch<Holding>(`/api/finance/holdings/${id}`, {
    method: 'PUT', body: JSON.stringify(body),
  })
}
export async function deleteHolding(id: number): Promise<void> {
  await apiFetch(`/api/finance/holdings/${id}`, { method: 'DELETE' })
}

export async function getPortfolioSummary(): Promise<PortfolioSummary> {
  return apiFetch<PortfolioSummary>('/api/finance/portfolio-summary')
}
