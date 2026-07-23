import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import MapView from './MapView';

function App() {
  const [stats, setStats] = useState(null);
  const [highRisk, setHighRisk] = useState([]);
  const [selectedDistrict, setSelectedDistrict] = useState(null);
  const [districtData, setDistrictData] = useState(null);

  const API = 'http://127.0.0.1:8000';

  useEffect(() => {
    fetchStats();
    fetchHighRisk();
  }, []);

  const fetchStats = async () => {
    try {
      const res = await axios.get(`${API}/api/stats`);
      setStats(res.data);
    } catch (err) {
      console.log("API not running. Start FastAPI first.");
    }
  };

  const fetchHighRisk = async () => {
    try {
      const res = await axios.get(`${API}/api/predict/high-risk?limit=10`);
      setHighRisk(res.data.high_risk_districts);
    } catch (err) {
      console.log("Could not fetch high-risk districts.");
    }
  };

  const fetchDistrict = async (district) => {
    try {
      const res = await axios.get(`${API}/api/predict/district?district=${district}`);
      setSelectedDistrict(district);
      setDistrictData(res.data);
    } catch (err) {
      console.log("Could not fetch district data.");
    }
  };

  return (
    <div className="App">
      {/* Header */}
      <header className="header">
        <h1>🦠 ResistNet</h1>
        <p>AMR Early Warning System — India</p>
      </header>

      {/* Stats Row */}
      {stats && (
        <div className="stats-row">
          <div className="stat-card">
            <h3>{stats.total_districts}</h3>
            <p>Districts</p>
          </div>
          <div className="stat-card">
            <h3>{stats.average_resistance}%</h3>
            <p>Avg Resistance</p>
          </div>
          <div className="stat-card red">
            <h3>{stats.red_alerts}</h3>
            <p>🔴 RED Alerts</p>
          </div>
          <div className="stat-card orange">
            <h3>{stats.orange_alerts}</h3>
            <p>🟠 ORANGE Alerts</p>
          </div>
        </div>
      )}

      {/* High Risk Districts */}
      <div className="section">
        <h2>⚠️ Top High-Risk Districts</h2>
        <div className="district-grid">
          {highRisk.map((d, i) => (
            <div 
              key={i} 
              className="district-card"
              onClick={() => fetchDistrict(d.district_name)}
            >
              <span className="rank">#{i + 1}</span>
              <div>
                <strong>{d.district_name}</strong>
                <small>{d.state_name}</small>
              </div>
              <span className="rate">{d.avg_resistance.toFixed(1)}%</span>
            </div>
          ))}
        </div>
      </div>

      {/* District Detail */}
      {districtData && (
        <div className="section">
          <h2>📍 {selectedDistrict} — Predictions</h2>
          <p>🔴 {districtData.red_alerts} RED | 🟠 {districtData.orange_alerts} ORANGE</p>
          <div className="predictions-table">
            <table>
              <thead>
                <tr>
                  <th>Pathogen</th>
                  <th>Antibiotic</th>
                  <th>Current</th>
                  <th>Predicted</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {districtData.predictions.slice(0, 5).map((p, i) => (
                  <tr key={i} className={p.severity === 'RED' ? 'row-red' : 'row-orange'}>
                    <td>{p.pathogen}</td>
                    <td>{p.antibiotic}</td>
                    <td>{p.current_resistance}%</td>
                    <td>{p.predicted_resistance}%</td>
                    <td>{p.severity === 'RED' ? '🔴' : '🟠'}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

            {/* Map Section */}
      <div className="section">
        <h2>🗺️ India District Risk Map</h2>
        <MapView 
          highRiskData={highRisk} 
          onDistrictClick={fetchDistrict} 
        />
      </div>

      <footer className="footer">
        <p>ResistNet v1.0 | Built for India's fight against superbugs</p>
      </footer>
    </div>
  );
}

export default App;