import type { Holding, PortfolioSummary } from '@/types/finance'

const _holdings: Holding[] = [
  { id: 1, symbol: '00713', name: '元大台灣高息低波', currency: 'TWD', broker: '國泰世華', shares: 264, avgPrice: 51.77, marketPrice: 59.80, currentValue: 15787, pnl: 2120, returnRate: 15.51, dividend: 313 },
  { id: 2, symbol: '00881', name: '國泰台灣科技領頭', currency: 'TWD', broker: '國泰世華', shares: 281, avgPrice: 34.98, marketPrice: 53.00, currentValue: 14893, pnl: 5064, returnRate: 51.52, dividend: 424 },
  { id: 3, symbol: '00922', name: '國泰台灣領袖50', currency: 'TWD', broker: '國泰世華', shares: 352, avgPrice: 27.96, marketPrice: 38.97, currentValue: 13717, pnl: 3876, returnRate: 39.38, dividend: 629 },
  { id: 4, symbol: '奈米投_Level1', name: '奈米投 Level 1', currency: 'USD', broker: '富邦', shares: 1, avgPrice: 50.11, marketPrice: 50.11, currentValue: 50.11, pnl: 0, returnRate: 0, dividend: 0 },
  { id: 5, symbol: '奈米投_Level2', name: '奈米投 Level 2', currency: 'USD', broker: '富邦', shares: 1, avgPrice: 101.40, marketPrice: 101.40, currentValue: 101.40, pnl: 0, returnRate: 0, dividend: 0 },
  { id: 6, symbol: '奈米投_Level3', name: '奈米投 Level 3', currency: 'USD', broker: '富邦', shares: 1, avgPrice: 300.00, marketPrice: 307.40, currentValue: 307.40, pnl: 7.40, returnRate: 2.47, dividend: 0 },
]

const _summary: PortfolioSummary = {
  twdValue: 44398,
  twdCost: 33339,
  twdPnl: 11059,
  twdReturnRate: 33.17,
  twdDividend: 1366,
  usdValue: 458.91,
  usdCost: 451.51,
  usdPnl: 7.40,
  usdReturnRate: 1.64,
  updatedAt: '2026/06/15',
}

export async function getHoldings(): Promise<Holding[]> {
  // TODO: return apiFetch<Holding[]>('/api/finance/holdings')
  return _holdings
}

export async function getPortfolioSummary(): Promise<PortfolioSummary> {
  // TODO: return apiFetch<PortfolioSummary>('/api/finance/summary')
  return _summary
}
