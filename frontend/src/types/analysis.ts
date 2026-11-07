export interface ServiceAnalysis {
  name: string
  url: string | null
  summary: string
  business_model: string
  core_features: string
  revenue_model: string
  differentiation: string
}

export interface AnalysisRecord {
  id: number
  idea: string
  created_at: string
  services: ServiceAnalysis[]
  insight: string
}

export interface HistoryItem {
  id: number
  idea: string
  created_at: string
  service_names: string[]
}
