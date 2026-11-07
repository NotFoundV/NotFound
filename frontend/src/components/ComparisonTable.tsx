import type { ServiceAnalysis } from '../types/analysis'

const COLUMNS: { key: keyof ServiceAnalysis; label: string; highlight?: boolean }[] = [
  { key: 'business_model', label: '비즈니스 모델' },
  { key: 'core_features', label: '핵심 기능' },
  { key: 'revenue_model', label: '수익 구조' },
  { key: 'differentiation', label: '차별점', highlight: true },
]

export default function ComparisonTable({ services }: { services: ServiceAnalysis[] }) {
  return (
    <div className="table-wrap">
      <table className="compare">
        <thead>
          <tr>
            <th>서비스</th>
            {COLUMNS.map((c) => (
              <th key={c.key} className={c.highlight ? 'highlight' : undefined}>
                {c.label}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {services.map((s) => (
            <tr key={s.name}>
              <th scope="row">{s.name}</th>
              {COLUMNS.map((c) => (
                <td key={c.key} className={c.highlight ? 'highlight' : undefined}>
                  {s[c.key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
