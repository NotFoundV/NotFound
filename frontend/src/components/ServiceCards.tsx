import type { ServiceAnalysis } from '../types/analysis'

export default function ServiceCards({ services }: { services: ServiceAnalysis[] }) {
  return (
    <div className="cards">
      {services.map((s) => (
        <article key={s.name} className="card">
          <h3>{s.name}</h3>
          {s.url && (
            <a href={s.url} target="_blank" rel="noreferrer" className="card-link">
              {s.url.replace(/^https?:\/\//, '').replace(/\/$/, '')}
            </a>
          )}
          <p>{s.summary}</p>
        </article>
      ))}
    </div>
  )
}
