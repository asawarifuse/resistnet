import React, { useState } from 'react';
import axios from 'axios';

const API = 'http://localhost:8000';

function PolicySimulator({ district, districtData }) {
  const [consumption, setConsumption] = useState(20);
  const [stewardship, setStewardship] = useState(10);
  const [testing, setTesting] = useState(10);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const topPathogen = districtData?.predictions?.[0]?.pathogen || "Acinetobacter baumannii";
  const topAntibiotic = districtData?.predictions?.[0]?.antibiotic || "Ceftriaxone";
  const topRate = districtData?.predictions?.[0]?.predicted_resistance || 82;

  const runSimulation = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API}/api/simulator/scenario`, {
        params: {
          district,
          pathogen: topPathogen,
          antibiotic: topAntibiotic,
          current_rate: topRate,
          consumption_reduction: consumption,
          stewardship_increase: stewardship,
          testing_increase: testing
        }
      });
      setResult(res.data);
    } catch (err) {
      console.log("Simulator error:", err);
    }
    setLoading(false);
  };

  return (
    <div className="simulator-panel">
      <h3>🎛️ AMR Policy Simulator</h3>
      <p style={{ color: '#94a3b8', fontSize: '0.85rem' }}>
        Test interventions for {district} — {topPathogen}/{topAntibiotic} at {topRate}%
      </p>

      <div className="slider-group">
        <label>Reduce high-risk antibiotic consumption: <strong>{consumption}%</strong></label>
        <input type="range" min="0" max="50" value={consumption} onChange={e => setConsumption(e.target.value)} />
      </div>

      <div className="slider-group">
        <label>Increase stewardship coverage: <strong>{stewardship}%</strong></label>
        <input type="range" min="0" max="50" value={stewardship} onChange={e => setStewardship(e.target.value)} />
      </div>

      <div className="slider-group">
        <label>Increase diagnostic testing: <strong>{testing}%</strong></label>
        <input type="range" min="0" max="50" value={testing} onChange={e => setTesting(e.target.value)} />
      </div>

      <button className="simulate-btn" onClick={runSimulation} disabled={loading}>
        {loading ? '⏳ Simulating...' : '▶ Run Simulation'}
      </button>

      {result && (
        <div className="simulation-result">
          <div className="sim-compare">
            <div className="sim-box" style={{ borderColor: result.baseline.color }}>
              <small>Current</small>
              <h2>{result.baseline.resistance}%</h2>
              <p style={{ color: result.baseline.color }}>{result.baseline.risk}</p>
            </div>
            <span className="arrow">→</span>
            <div className="sim-box" style={{ borderColor: result.projected.color }}>
              <small>Projected</small>
              <h2>{result.projected.resistance}%</h2>
              <p style={{ color: result.projected.color }}>{result.projected.risk}</p>
            </div>
          </div>
          <p className="sim-change" style={{ color: result.projected.change <= 0 ? '#22c55e' : '#ef4444' }}>
            {result.projected.change}% change | Confidence: {result.confidence}%
          </p>
          <p className="sim-disclaimer">⚠️ {result.disclaimer}</p>
        </div>
      )}
    </div>
  );
}

export default PolicySimulator;