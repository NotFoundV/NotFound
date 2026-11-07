import type { AnalysisRecord, HistoryItem } from '../types/analysis'

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let res: Response
  try {
    res = await fetch(`/api${path}`, {
      ...init,
      headers: { 'Content-Type': 'application/json', ...init?.headers },
    })
  } catch {
    throw new Error('서버에 연결하지 못했어요. 네트워크를 확인해 주세요.')
  }
  if (!res.ok) {
    const body = await res.json().catch(() => null)
    const detail = body?.detail
    const message = typeof detail === 'string' ? detail : `요청에 실패했어요 (${res.status}).`
    throw new Error(message)
  }
  return res.json() as Promise<T>
}

export function analyzeIdea(idea: string): Promise<AnalysisRecord> {
  return request('/analyze', { method: 'POST', body: JSON.stringify({ idea }) })
}

export function fetchHistory(): Promise<HistoryItem[]> {
  return request('/history')
}

export function fetchHistoryDetail(id: number): Promise<AnalysisRecord> {
  return request(`/history/${id}`)
}
