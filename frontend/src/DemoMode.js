import React, { useState } from 'react';

const DEMO_ALERTS = [
  { district: "Mumbai", pathogen: "Acinetobacter baumannii", antibiotic: "Ceftriaxone", current: 88.6, predicted: 88.9, severity: "RED" },
  { district: "Kolkata", pathogen: "Klebsiella pneumoniae", antibiotic: "Ciprofloxacin", current: 82.1, predicted: 84.3, severity: "RED" },
  { district: "Chennai", pathogen: "Escherichia coli", antibiotic: "Gentamicin", current: 65.4, predicted: 68.2, severity: "ORANGE" },
  { district: "Delhi", pathogen: "Pseudomonas aeruginosa", antibiotic: "Imipenem", current: 45.2, predicted: 49.8, severity: "YELLOW" },
  { district: "Bangalore", pathogen: "Staphylococcus aureus", antibiotic: "Oxacillin", current: 28.7, predicted: 31.2, severity: "GREEN" },
];

function DemoMode() {
  const [showAlert, setShowAlert] = useState(false);
  const [currentAlert, setCurrentAlert] = useState(null);

  const generateAlert = () => {
    const alert = DEMO_ALERTS[Math.floor(Math.random() * DEMO_ALERTS.length)];
    setCurrentAlert(alert);
    setShowAlert(true);
  };

  return (
    <div className="demo-section">
      <h2>🎮 Demo Mode — Live Alert Simulation</h2>
      <p style={{ color: '#94a3b8', marginBottom: '15px' }}>
        Click the button to simulate a real-time AMR alert from any district.
      </p>
      
      <button className="demo-btn" onClick={generateAlert}>
        🚨 Generate Random Alert
      </button>

      {showAlert && currentAlert && (
        <div className={`demo-alert alert-${currentAlert.severity.toLowerCase()}`}>
          <div className="alert-header">
            <span className="alert-badge">{currentAlert.severity === 'RED' ? '🔴' : currentAlert.severity === 'ORANGE' ? '🟠' : currentAlert.severity === 'YELLOW' ? '🟡' : '🟢'}</span>
            <h3>{currentAlert.severity} ALERT — {currentAlert.district}</h3>
          </div>
          <div className="alert-body">
            <p><strong>{currentAlert.pathogen}</strong> resistance to <strong>{currentAlert.antibiotic}</strong></p>
            <div className="alert-stats">
              <div>
                <small>Current</small>
                <span className="stat-value">{currentAlert.current}%</span>
              </div>
              <div className="arrow">→</div>
              <div>
                <small>Predicted</small>
                <span className="stat-value" style={{color: currentAlert.severity === 'RED' ? '#ef4444' : '#f97316'}}>
                  {currentAlert.predicted}%
                </span>
              </div>
            </div>
            <p className="recommendation">
              {currentAlert.severity === 'RED' && '⚠️ Immediate action required. Switch to alternative antibiotic.'}
              {currentAlert.severity === 'ORANGE' && '⚠️ Monitor closely. Review prescription guidelines.'}
              {currentAlert.severity === 'YELLOW' && 'ℹ️ Routine monitoring. No immediate action needed.'}
              {currentAlert.severity === 'GREEN' && '✅ Safe to continue current treatment.'}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default DemoMode;