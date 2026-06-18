export type Currency = 'TWD' | 'USD'

export interface Holding {
  id: number
  symbol: string
  name: string
  currency: Currency
  broker: string
  shares: number
  avgPrice: number
  marketPrice: number
  currentValue: number
  pnl: number
  returnRate: number
  dividend: number
}

export interface PortfolioSummary {
  twdValue: number
  twdCost: number
  twdPnl: number
  twdReturnRate: number
  twdDividend: number
  usdValue: number
  usdCost: number
  usdPnl: number
  usdReturnRate: number
  updatedAt: string
}
