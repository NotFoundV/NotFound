export default function InsightBox({ insight }: { insight: string }) {
  return (
    <aside className="insight">
      <span className="insight-label">우리 아이디어가 파고들 빈틈</span>
      <p>{insight}</p>
    </aside>
  )
}
