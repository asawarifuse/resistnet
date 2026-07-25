import React, { useState } from 'react';
import axios from 'axios';

const API = 'http://localhost:8000';

const POPULAR_DISTRICTS = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata', 'Hyderabad'];

function CompareDistricts() {
  const [district1, setDistrict1] = useState('');
  const [district2, setDistrict2] = useState('');
  const [data1, setData1] = useState(null);
  const [data2, setData2] = useState(null);

  const fetchCompare = async () => {
    try {
      const [res1, res2] = await Promise.all([
        axios.get(`${API}/api/predict/district?district=${district1}`),
        axios.get(`${API}/api/predict/district?district=${district2}`)
      ]);
      setData1(res1.data);
      setData2(res2.data);
    } catch (err) {
      console.log("Could not fetch comparison");
    }
  };

  return (
    <div className="section">
      <h2>🔄 Compare Districts</h2>
      <p style={{ color: '#94a3b8', marginBottom: '15px' }}>
        Select two districts to compare AMR predictions side by side.
      </p>

      <div className="compare-selects">
        <select value={district1} onChange={(e) => setDistrict1(e.target.value)}>
          <option value="">Select District 1</option>
          {POPULAR_DISTRICTS.map(d => <option key={d} value={d}>{d}</option>)}
        </select>
        
        <span className="vs">VS</span>
        
        <select value={district2} onChange={(e) => setDistrict2(e.target.value)}>
          <option value="">Select District 2</option>
          {POPULAR_DISTRICTS.map(d => <option key={d} value={d}>{d}</option>)}
        </select>
        
        <button 
          className="compare-btn"
          onClick={fetchCompare}
          disabled={!district1 || !district2}
        >
          Compare
        </button>
      </div>

      {data1 && data2 && (
        <div className="compare-results">
          <div className="compare-card">
            <h3>📍 {district1}</h3>
            <div className="compare-stat">🔴 {data1.red_alerts} RED</div>
            <div className="compare-stat">🟠 {data1.orange_alerts} ORANGE</div>
            <div className="compare-stat">📊 {data1.total_predictions} Predictions</div>
            {data1.predictions && data1.predictions[0] && (
              <div className="top-threat">
                <small>Top Threat</small>
                <strong>{data1.predictions[0].pathogen}</strong>
                <span className="threat-rate">{data1.predictions[0].predicted_resistance}%</span>
              </div>
            )}
          </div>
          
          <div className="compare-vs">VS</div>
          
          <div className="compare-card">
            <h3>📍 {district2}</h3>
            <div className="compare-stat">🔴 {data2.red_alerts} RED</div>
            <div className="compare-stat">🟠 {data2.orange_alerts} ORANGE</div>
            <div className="compare-stat">📊 {data2.total_predictions} Predictions</div>
            {data2.predictions && data2.predictions[0] && (
              <div className="top-threat">
                <small>Top Threat</small>
                <strong>{data2.predictions[0].pathogen}</strong>
                <span className="threat-rate">{data2.predictions[0].predicted_resistance}%</span>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default CompareDistricts;