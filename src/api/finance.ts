import type { Holding, PortfolioSummary } from '@/types/finance'
import { apiFetch } from './client'

export async function getHoldings(): Promise<Holding[]> {
  return apiFetch<Holding[]>('/api/finance/holdings')
}

export async function getPortfolioSummary(): Promise<PortfolioSummary> {
  return apiFetch<PortfolioSummary>('/api/finance/portfolio-summary')
}
