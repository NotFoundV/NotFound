import { useState, type FormEvent } from 'react'

interface Props {
  disabled: boolean
  onSubmit: (idea: string) => void
}

const MIN_LENGTH = 5

export default function IdeaForm({ disabled, onSubmit }: Props) {
  const [idea, setIdea] = useState('')
  const trimmed = idea.trim()

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault()
    if (trimmed.length >= MIN_LENGTH) onSubmit(trimmed)
  }

  return (
    <form className="idea-form" onSubmit={handleSubmit}>
      <label htmlFor="idea" className="label">
        창업 아이디어
      </label>
      <textarea
        id="idea"
        value={idea}
        onChange={(e) => setIdea(e.target.value)}
        placeholder="예) 대학생끼리 남는 전공 서적을 사고팔고, 학과별로 필기 노트도 공유하는 중고 거래 앱"
        rows={4}
        maxLength={2000}
        disabled={disabled}
      />
      <div className="form-footer">
        <span className="hint">{trimmed.length < MIN_LENGTH ? `${MIN_LENGTH}자 이상 적어 주세요` : `${trimmed.length}자`}</span>
        <button type="submit" className="btn-primary" disabled={disabled || trimmed.length < MIN_LENGTH}>
          {disabled ? '분석 중…' : '분석하기'}
        </button>
      </div>
    </form>
  )
}
