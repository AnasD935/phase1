import { useRef, useState } from 'react'
import { Crosshair, Hand, MapPin } from 'lucide-react'

const clamp = (value, min, max) => Math.max(min, Math.min(max, value))

function formatCoordinate(value, positive, negative) {
  return `${Math.abs(Number(value || 0)).toFixed(2)}\u00B0${Number(value) >= 0 ? positive : negative}`
}

export default function LocationMap({ latitude, longitude, onLocationChange }) {
  const mapRef = useRef(null)
  const [dragging, setDragging] = useState(false)
  const top = clamp(((90 - Number(latitude || 0)) / 180) * 100, 4, 96)
  const left = clamp(((Number(longitude || 0) + 180) / 360) * 100, 4, 96)

  function selectPoint(clientX, clientY) {
    const rect = mapRef.current?.getBoundingClientRect()
    if (!rect) return

    const x = clamp((clientX - rect.left) / rect.width, 0, 1)
    const y = clamp((clientY - rect.top) / rect.height, 0, 1)
    onLocationChange({
      latitude: Number((90 - y * 180).toFixed(2)),
      longitude: Number((x * 360 - 180).toFixed(2)),
    })
  }

  function handlePointerDown(event) {
    event.currentTarget.setPointerCapture(event.pointerId)
    setDragging(true)
    selectPoint(event.clientX, event.clientY)
  }

  function handlePointerMove(event) {
    if (dragging) selectPoint(event.clientX, event.clientY)
  }

  function handleKeyDown(event) {
    const step = event.shiftKey ? 5 : 0.5
    const offsets = {
      ArrowUp: [step, 0],
      ArrowDown: [-step, 0],
      ArrowLeft: [0, -step],
      ArrowRight: [0, step],
    }
    if (!offsets[event.key]) return

    event.preventDefault()
    const [latitudeOffset, longitudeOffset] = offsets[event.key]
    onLocationChange({
      latitude: Number(clamp(Number(latitude) + latitudeOffset, -90, 90).toFixed(2)),
      longitude: Number(clamp(Number(longitude) + longitudeOffset, -180, 180).toFixed(2)),
    })
  }

  return (
    <div
      ref={mapRef}
      className={`map-panel interactive ${dragging ? 'is-dragging' : ''}`}
      role="application"
      tabIndex="0"
      aria-label="Interactive illustrative map. Click or drag to select coordinates. Use arrow keys for fine adjustments."
      onPointerDown={handlePointerDown}
      onPointerMove={handlePointerMove}
      onPointerUp={() => setDragging(false)}
      onPointerCancel={() => setDragging(false)}
      onKeyDown={handleKeyDown}
    >
      <div className="map-grid" />
      <div className="map-land land-one" />
      <div className="map-land land-two" />
      <div className="map-land land-three" />
      <div className="map-pin" style={{ top: `${top}%`, left: `${left}%` }}>
        <span><MapPin size={17} strokeWidth={2.6} /></span>
      </div>
      <div className="map-label">
        <Crosshair size={14} /> {formatCoordinate(latitude, 'N', 'S')}, {formatCoordinate(longitude, 'E', 'W')}
      </div>
      <div className="map-caption"><Hand size={12} /> Click or drag to select</div>
      <div className="map-disclaimer">Illustrative map / no external service</div>
    </div>
  )
}

