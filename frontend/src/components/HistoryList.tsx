import type { HistoryItem } from '../types/analysis'

interface Props {
  items: HistoryItem[]
  activeId: number | null
  onSelect: (id: number) => void
}

const formatDate = (iso: string) =>
  new Date(iso).toLocaleString('ko-KR', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })

export default function HistoryList({ items, activeId, onSelect }: Props) {
  if (items.length === 0) return <p className="hint">아직 분석 이력이 없어요.</p>
  return (
    <ul className="history">
      {items.map((item) => (
        <li key={item.id}>
          <button type="button" className={item.id === activeId ? 'active' : ''} onClick={() => onSelect(item.id)}>
            <span className="history-idea">{item.idea}</span>
            <span className="history-meta">
              {formatDate(item.created_at)} · {item.service_names.join(', ')}
            </span>
          </button>
        </li>
      ))}
    </ul>
  )
}
