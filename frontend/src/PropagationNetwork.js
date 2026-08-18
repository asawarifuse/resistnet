import React, { useState } from 'react';
import axios from 'axios';

const API = 'http://localhost:8000';

function PropagationNetwork({ district }) {
  const [propagation, setPropagation] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchPropagation = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API}/api/propagation/${district}`);
      setPropagation(res.data);
    } catch (err) {
      console.log("Propagation error");
    }
    setLoading(false);
  };

  return (
    <div className="propagation-panel">
      <h3>🔗 AMR Propagation Watch</h3>
      <button className="propagation-btn" onClick={fetchPropagation} disabled={loading}>
        {loading ? '⏳ Analyzing...' : '▶ Show Potential Hotspots'}
      </button>

      {propagation && (
        <div className="propagation-result">
          <p>Source: <strong>{propagation.source_district}</strong> at {propagation.current_risk}%</p>
          <div className="propagation-chain">
            {propagation.potential_hotspots.map((h, i) => (
              <div key={i} className="propagation-node" style={{ borderColor: h.color }}>
                <span className="node-arrow">{i === 0 ? '↓' : '↓'}</span>
                <div>
                  <strong>{h.district}</strong>
                  <span style={{ color: h.color, marginLeft: '8px' }}>{h.predicted_risk}% — {h.level}</span>
                  <small style={{ display: 'block', color: '#94a3b8' }}>
                    Confidence: {h.confidence}%
                  </small>
                </div>
              </div>
            ))}
          </div>
          <p className="propagation-disclaimer">⚠️ {propagation.disclaimer}</p>
        </div>
      )}
    </div>
  );
}

export default PropagationNetwork;