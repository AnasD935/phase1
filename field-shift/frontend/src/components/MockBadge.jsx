export default function MockBadge({ compact = false }) {
  return (
    <span className={`mock-badge ${compact ? 'compact' : ''}`}>
      <span className="mock-dot" aria-hidden="true" /> Demo / Mock Data
    </span>
  )
}

