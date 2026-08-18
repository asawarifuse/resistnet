import React, { useState } from 'react';
import axios from 'axios';

const API = 'http://localhost:8000';

function ResponsePlaybook({ district, districtData }) {
  const [playbook, setPlaybook] = useState(null);
  const [loading, setLoading] = useState(false);

  const topPathogen = districtData?.predictions?.[0]?.pathogen || "Acinetobacter baumannii";
  const topAntibiotic = districtData?.predictions?.[0]?.antibiotic || "Ceftriaxone";
  const topRate = districtData?.predictions?.[0]?.predicted_resistance || 82;
  const severity = districtData?.predictions?.[0]?.severity || "CRITICAL";

  const generatePlan = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API}/api/response/playbook`, {
        params: {
          district,
          pathogen: topPathogen,
          antibiotic: topAntibiotic,
          resistance_rate: topRate,
          severity
        }
      });
      setPlaybook(res.data);
    } catch (err) {
      console.log("Playbook error");
    }
    setLoading(false);
  };

  return (
    <div className="playbook-panel">
      <h3>🚨 AMR Incident Response Playbook</h3>
      <button className="playbook-btn" onClick={generatePlan} disabled={loading}>
        {loading ? '⏳ Generating...' : '📋 Generate Response Plan'}
      </button>

      {playbook && (
        <div className="playbook-result">
          <div className="incident-header">
            <span className="incident-id">{playbook.incident_id}</span>
            <span className="incident-severity">{playbook.severity}</span>
          </div>
          
          <p>{playbook.pathogen} → {playbook.antibiotic} at <strong>{playbook.resistance_rate}%</strong></p>

          <div className="action-grid">
            {[
              { title: "🏥 Hospital", items: playbook.hospital_actions },
              { title: "💊 Pharmacy", items: playbook.pharmacy_actions },
              { title: "🏛️ Public Health", items: playbook.public_health_actions },
              { title: "👨‍⚕️ Clinician", items: playbook.clinician_actions }
            ].map((section, i) => (
              <div key={i} className="action-card">
                <h4>{section.title}</h4>
                <ul>
                  {section.items.slice(0, 4).map((item, j) => (
                    <li key={j}>{item}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          <p className="playbook-disclaimer">⚠️ {playbook.disclaimer}</p>
        </div>
      )}
    </div>
  );
}

export default ResponsePlaybook;