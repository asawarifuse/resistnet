import React from 'react';

function SHAPExplanation({ district }) {
  const drivers = [
    { feature: "Recent resistance trend", impact: 31.1, direction: "up" },
    { feature: "Antibiotic sales volume", impact: 17.8, direction: "up" },
    { feature: "Seasonal factor", impact: 13.3, direction: "up" },
    { feature: "Population density", impact: 10.7, direction: "up" },
    { feature: "Testing coverage", impact: 4.4, direction: "down" },
    { feature: "Stewardship program", impact: 2.7, direction: "down" },
  ];

  const maxImpact = Math.max(...drivers.map(d => Math.abs(d.impact)));

  return (
    <div className="shap-card">
      <h3>🧠 What Drives Resistance in {district}?</h3>
      
      {drivers.map((d, i) => (
        <div key={i} className="shap-driver">
          <span className="driver-label">{d.feature}</span>
          <div className="driver-bar-container">
            <div 
              className={`driver-bar ${d.direction}`}
              style={{ width: `${(Math.abs(d.impact) / maxImpact) * 100}%` }}
            />
          </div>
          <span className={`driver-impact ${d.direction}`}>
            {d.direction === 'up' ? '+' : '-'}{d.impact}%
          </span>
        </div>
      ))}
      
      <p className="shap-note">
        💡 Red bars increase risk. Blue bars decrease risk. Based on SHAP analysis.
      </p>
    </div>
  );
}

export default SHAPExplanation;