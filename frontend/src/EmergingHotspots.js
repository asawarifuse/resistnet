import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API = 'http://localhost:8000';

function EmergingHotspots() {
  const [hotspots, setHotspots] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHotspots();
  }, []);

  const fetchHotspots = async () => {
    try {
      const res = await axios.get(`${API}/api/emerging/hotspots?limit=5`);
      setHotspots(res.data.hotspots);
    } catch (err) {
      console.log("Hotspots error");
    }
    setLoading(false);
  };

  return (
    <div className="emerging-panel">
            <h3>⚠️ Emerging Hotspots</h3>
      
      {loading ? (
        <p style={{ color: '#94a3b8' }}>Loading...</p>
      ) : hotspots.length === 0 ? (
        <p style={{ color: '#94a3b8' }}>No emerging hotspots detected.</p>
      ) : (
        <div className="hotspot-list">
          {hotspots.map((h, i) => (
            <div key={i} className="hotspot-card">
              <div className="hotspot-header">
                <strong>{h.district}</strong>
                <span className={`hotspot-badge ${h.risk_level.toLowerCase()}`}>
                  {h.risk_level}
                </span>
              </div>
              <div className="hotspot-metrics">
                <span>2021: {h.resistance_2021}%</span>
                <span>→</span>
                <span>2023: {h.resistance_2023}%</span>
                <span className="hotspot-change">(+{h.change}%)</span>
              </div>
              <small style={{ color: '#94a3b8' }}>
                {h.trend} | Consumption: +{h.consumption_change}%
              </small>
            </div>
          ))}
        </div>
      )}
      <p className="hotspot-disclaimer">Model-derived signals. Not confirmed outbreaks.</p>
    </div>
  );
}

export default EmergingHotspots;