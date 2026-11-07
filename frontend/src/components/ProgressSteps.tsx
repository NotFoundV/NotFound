import { useEffect, useState } from 'react'

const STEPS = ['유사 서비스 탐색 중', '항목별 분석 중']
// 백엔드는 한 번의 요청으로 두 단계를 처리하므로, 웹 검색 단계에 보통 걸리는 시간 뒤에 표시를 넘긴다
const SEARCH_STEP_MS = 45_000

export default function ProgressSteps() {
  const [step, setStep] = useState(0)
  const [seconds, setSeconds] = useState(0)

  useEffect(() => {
    const started = Date.now()
    const timer = window.setInterval(() => {
      const elapsed = Date.now() - started
      setSeconds(Math.floor(elapsed / 1000))
      setStep(elapsed >= SEARCH_STEP_MS ? 1 : 0)
    }, 1000)
    return () => window.clearInterval(timer)
  }, [])

  return (
    <div className="progress" role="status" aria-live="polite">
      <ol>
        {STEPS.map((label, i) => (
          <li key={label} className={i < step ? 'done' : i === step ? 'active' : ''}>
            <span className="dot" />
            {label}
            {i === step && <span className="ellipsis" />}
          </li>
        ))}
      </ol>
      <p className="hint">{seconds}초 경과 · 웹 검색을 포함해 보통 1~3분 걸려요</p>
    </div>
  )
}
