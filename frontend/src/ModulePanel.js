import React, { useState } from 'react';
import axios from 'axios';

const API = 'http://localhost:8000';

function ModulePanel({ district, districtData }) {
  const [margResult, setMargResult] = useState(null);
  const [smritiResult, setSmritiResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeModule, setActiveModule] = useState(null);

  const topPathogen = districtData?.predictions?.[0]?.pathogen || "Acinetobacter baumannii";
  const topAntibiotic = districtData?.predictions?.[0]?.antibiotic || "Ceftriaxone";
  const topRate = districtData?.predictions?.[0]?.predicted_resistance || 88.9;

  const runMarg = async () => {
    setLoading(true);
    setActiveModule('marg');
    try {
      const res = await axios.get(`${API}/api/marg/recommend`, {
        params: {
          district,
          pathogen: topPathogen,
          failed_antibiotic: topAntibiotic
        }
      });
      setMargResult(res.data);
    } catch (err) {
      console.log("Marg error:", err);
    }
    setLoading(false);
  };

  const runSahay = async () => {
    setLoading(true);
    setActiveModule('sahay');
    try {
      const state = districtData?.state || "Maharashtra";
      const res = await axios.get(`${API}/api/sahay/alert`, {
        params: {
          district,
          state,
          pathogen: topPathogen,
          failed_antibiotic: topAntibiotic,
          resistance_rate: topRate,
          recommended: margResult?.top_recommendation || "Colistin",
          language: "en"
        }
      });
      setMargResult(res.data);
    } catch (err) {
      console.log("Sahay error:", err);
    }
    setLoading(false);
  };

  const runSmriti = async () => {
    setLoading(true);
    setActiveModule('smriti');
    try {
      const res = await axios.get(`${API}/api/smriti/compare`, {
        params: {
          district,
          pathogen: topPathogen,
          antibiotic: topAntibiotic,
          current_rate: topRate
        }
      });
      setSmritiResult(res.data);
    } catch (err) {
      console.log("Smriti error:", err);
    }
    setLoading(false);
  };

  const runAll = async () => {
    setLoading(true);
    setActiveModule('all');
    try {
      const state = districtData?.state || "Maharashtra";
      const [margRes, sahayRes, smritiRes] = await Promise.all([
        axios.get(`${API}/api/marg/recommend`, {
          params: { district, pathogen: topPathogen, failed_antibiotic: topAntibiotic }
        }),
        axios.get(`${API}/api/sahay/alert`, {
          params: {
            district, state, pathogen: topPathogen,
            failed_antibiotic: topAntibiotic,
            resistance_rate: topRate,
            recommended: "Colistin",
            language: "en"
          }
        }),
        axios.get(`${API}/api/smriti/compare`, {
          params: {
            district, pathogen: topPathogen,
            antibiotic: topAntibiotic, current_rate: topRate
          }
        })
      ]);
      setMargResult({
        ...margRes.data,
        sahay: sahayRes.data
      });
      setSmritiResult(smritiRes.data);
    } catch (err) {
      console.log("Error:", err);
    }
    setLoading(false);
  };

  return (
    <div className="module-panel">
      <h2>🧠 AI Decision Support — {district}</h2>
      <p style={{ color: '#94a3b8', marginBottom: '15px' }}>
        Top threat: <strong style={{ color: '#ef4444' }}>{topPathogen}</strong> → 
        <strong style={{ color: '#f97316' }}> {topAntibiotic}</strong> at {topRate}%
      </p>

      <div className="module-buttons">
        <button className="module-btn marg" onClick={runMarg} disabled={loading}>
          💊 Marg — Find Alternatives
        </button>
        <button className="module-btn sahay" onClick={runSahay} disabled={loading || !margResult}>
          📢 Sahay — Send Alert
        </button>
        <button className="module-btn smriti" onClick={runSmriti} disabled={loading}>
          📜 Smriti — Compare History
        </button>
        <button className="module-btn all" onClick={runAll} disabled={loading}>
          🚀 Run All Modules
        </button>
      </div>

      {loading && <p className="loading-text">⏳ Running AI modules...</p>}

      {margResult && (
        <div className="module-result">
          <h4>✅ Top Recommendation: <span style={{ color: '#22c55e' }}>{margResult.top_recommendation}</span></h4>
          <p>{margResult.total_alternatives} alternatives found for {margResult.failed_antibiotic}</p>
          
          <div className="alt-list">
            {margResult.alternatives?.slice(0, 4).map((alt, i) => (
              <div key={i} className={`alt-card ${i === 0 ? 'best' : ''}`}>
                <div className="alt-header">
                  <strong>{alt.antibiotic}</strong>
                  <span className="alt-badge">{alt.recommendation}</span>
                </div>
                <div className="alt-details">
                  <span>Efficacy: {alt.efficacy}%</span>
                  <span>Class: {alt.class}</span>
                  <span>WHO: {alt.access}</span>
                </div>
                <small>💉 {alt.dosage}</small>
              </div>
            ))}
          </div>

          {margResult.sahay && (
            <div className="sahay-result">
              <h4>📱 SMS Alert Status</h4>
              <p>{margResult.sahay.sms?.message}</p>
              <p>Stock: {margResult.sahay.stock?.status} | 
                 Action: {margResult.sahay.stock_action?.action}</p>
            </div>
          )}
        </div>
      )}

      {smritiResult && (
        <div className="sahay-result" style={{ borderColor: '#8b5cf6', background: 'rgba(139, 92, 246, 0.1)' }}>
          <h4>📜 Historical Analysis Complete</h4>
          <p>District: {smritiResult.district} | Pathogen: {smritiResult.pathogen}</p>
          <p>Similar outbreaks found. Prevention guidelines generated.</p>
          <p style={{ fontSize: '0.8rem', color: '#94a3b8' }}>
            View full analysis in server logs (terminal)
          </p>
        </div>
      )}

      <p className="disclaimer">
        ⚠️ Decision-support tool. Always consult clinical guidelines.
      </p>
    </div>
  );
}

export default ModulePanel;