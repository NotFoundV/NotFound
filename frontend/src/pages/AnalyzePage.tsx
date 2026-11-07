import { useCallback, useEffect, useState } from 'react'
import { analyzeIdea, fetchHistory, fetchHistoryDetail } from '../api/client'
import ComparisonTable from '../components/ComparisonTable'
import HistoryList from '../components/HistoryList'
import IdeaForm from '../components/IdeaForm'
import InsightBox from '../components/InsightBox'
import ProgressSteps from '../components/ProgressSteps'
import ServiceCards from '../components/ServiceCards'
import type { AnalysisRecord, HistoryItem } from '../types/analysis'

export default function AnalyzePage() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<AnalysisRecord | null>(null)
  const [history, setHistory] = useState<HistoryItem[]>([])

  const loadHistory = useCallback(() => {
    fetchHistory().then(setHistory).catch(() => setHistory([]))
  }, [])

  useEffect(loadHistory, [loadHistory])

  const handleAnalyze = async (idea: string) => {
    setLoading(true)
    setError(null)
    setResult(null)
    try {
      setResult(await analyzeIdea(idea))
      loadHistory()
    } catch (e) {
      setError(e instanceof Error ? e.message : '알 수 없는 오류가 발생했어요.')
    } finally {
      setLoading(false)
    }
  }

  const handleSelect = async (id: number) => {
    setError(null)
    try {
      setResult(await fetchHistoryDetail(id))
      window.scrollTo({ top: 0, behavior: 'smooth' })
    } catch (e) {
      setError(e instanceof Error ? e.message : '기록을 불러오지 못했어요.')
    }
  }

  return (
    <div className="page">
      <header className="topbar">
        <a href="/" className="logo">
          <span className="logo-mark">404</span> Found
        </a>
      </header>

      <main className="layout">
        <section className="main-col">
          <h1>
            내 아이디어, <em>이미 누가</em> 하고 있을까?
          </h1>
          <p className="lead">아이디어를 적으면 유사 서비스를 찾아 비즈니스 모델·핵심 기능·수익 구조·차별점을 비교해 드려요.</p>

          <IdeaForm disabled={loading} onSubmit={handleAnalyze} />
          {loading && <ProgressSteps />}
          {error && <p className="error">{error}</p>}

          {result && (
            <div className="result">
              <p className="result-idea">“{result.idea}”</p>
              <h2>유사 서비스 {result.services.length}곳</h2>
              <ServiceCards services={result.services} />
              <h2>항목별 비교</h2>
              <ComparisonTable services={result.services} />
              <InsightBox insight={result.insight} />
            </div>
          )}
        </section>

        <aside className="side-col">
          <h2>최근 분석</h2>
          <HistoryList items={history} activeId={result?.id ?? null} onSelect={handleSelect} />
        </aside>
      </main>
    </div>
  )
}
