import { CloudSun, Droplets, FlaskConical, Info, Leaf, Sprout, ThermometerSun, TriangleAlert } from 'lucide-react'
import MockBadge from './MockBadge'

const riskColor = { low: 'risk-low', medium: 'risk-medium', high: 'risk-high' }

export default function Results({ data }) {
  if (!data) {
    return (
      <section className="empty-state" aria-live="polite">
        <div className="empty-orbit"><Sprout size={29} /></div>
        <p className="eyebrow">Ready to model</p>
        <h2>Your rotation story starts here.</h2>
        <p>Enter the field details, then run the demo to see how the frontend and API work together.</p>
        <div className="request-preview">
          <span>POST</span><code>/api/farm/analyze</code>
          <span>POST</span><code>/api/rotation/suggest</code>
        </div>
      </section>
    )
  }

  const { analysis, rotation } = data
  return (
    <section className="results" aria-live="polite">
      <div className="results-heading">
        <div>
          <p className="eyebrow">Analysis complete</p>
          <h2>A practical path for your next three seasons.</h2>
        </div>
        <MockBadge />
      </div>

      <div className="insight-grid">
        <article className="insight-card climate-card">
          <div className="card-label"><CloudSun size={17} /> Climate snapshot</div>
          <strong>{analysis.climate.average_temperature_c}°C</strong>
          <span>average temperature</span>
          <div className="mini-stats">
            <p><Droplets size={15} /><b>{analysis.climate.annual_rainfall_mm} mm</b> rainfall</p>
            <p><ThermometerSun size={15} /><b>{analysis.climate.growing_season}</b> season</p>
          </div>
          <small>{analysis.climate.source}</small>
        </article>

        <article className="insight-card soil-card">
          <div className="card-label"><FlaskConical size={17} /> Soil snapshot</div>
          <strong>{analysis.soil.texture}</strong>
          <span>sample soil texture</span>
          <div className="soil-line">
            <div><b>{analysis.soil.ph}</b><span>pH</span></div>
            <div><b>{analysis.soil.organic_matter_percent}%</b><span>organic matter</span></div>
          </div>
          <small>{analysis.soil.source}</small>
        </article>

        <article className="insight-card risk-card">
          <div className="card-label"><TriangleAlert size={17} /> Risk signals</div>
          <div className="risk-list">
            {analysis.risks.map((risk) => (
              <div key={risk.type} title={risk.note}>
                <span className={`risk-dot ${riskColor[risk.level]}`} />
                <p><b>{risk.type}</b><small>{risk.level} risk</small></p>
              </div>
            ))}
          </div>
        </article>
      </div>

      <div className="section-title">
        <div><p className="eyebrow">Crop fit</p><h3>Suggested for this field</h3></div>
        <span>Rule-based score / 100</span>
      </div>
      <div className="crop-list">
        {analysis.suggested_crops.map((crop, index) => (
          <article className="crop-row" key={crop.crop}>
            <div className="crop-rank">0{index + 1}</div>
            <div className="crop-icon"><Leaf size={19} /></div>
            <div className="crop-copy">
              <div><h4>{crop.crop}</h4><span>{crop.water_need_m3_per_dunam} m³/dunam</span></div>
              <p>{crop.reason}</p>
            </div>
            <div className="score" style={{ '--score': `${crop.score}%` }}>
              <b>{crop.score}</b><span>fit</span>
            </div>
          </article>
        ))}
      </div>

      <div className="section-title rotation-title">
        <div><p className="eyebrow">Rotation plan</p><h3>{rotation.plan_name}</h3></div>
        <MockBadge compact />
      </div>
      <div className="timeline">
        {rotation.seasons.map((season) => (
          <article className="season" key={season.season}>
            <div className="season-number">{season.season}</div>
            <div className="season-copy">
              <span>{season.period}</span>
              <h4>{season.crop}</h4>
              <p>{season.explanation}</p>
            </div>
          </article>
        ))}
      </div>

      <div className="disclaimer"><Info size={16} /><p>{analysis.disclaimer}</p></div>
    </section>
  )
}

