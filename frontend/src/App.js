import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import MapView from './MapView';
import { ResistanceBarChart, SeverityPieChart, PathogenBarChart, TrendLineChart } from './Charts';
import AlertsPage from './AlertsPage';
import CompareDistricts from './CompareDistricts';
import ExportReport from './ExportReport';
import LiveClock from './LiveClock';
import ThemeToggle from './ThemeToggle';
import SearchDistrict from './SearchDistrict';
import SkeletonLoader from './SkeletonLoader';
import Tooltip from './Tooltip';
import FooterStats from './FooterStats';
import BackToTop from './BackToTop';
import NotificationBadge from './NotificationBadge';
import AnimatedCounter from './AnimatedCounter';
import PageTitle from './PageTitle';
import ErrorBoundary from './ErrorBoundary';
import ShortcutsModal from './ShortcutsModal';
import Changelog from './Changelog';
import QuickStats from './QuickStats';
import WeeklySummary from './WeeklySummary';
import VoiceSearch from './VoiceSearch';
import ScreenshotBtn from './ScreenshotBtn';
import DownloadAll from './DownloadAll';
import ShareBtn from './ShareBtn';
import PrintReport from './PrintReport';
import SystemStatus from './SystemStatus';
import ModulePanel from './ModulePanel';
import PolicySimulator from './PolicySimulator';
import ResponsePlaybook from './ResponsePlaybook';
import PropagationNetwork from './PropagationNetwork';
import EmergingHotspots from './EmergingHotspots';
import LiveDemo from './LiveDemo';
import ActionCards from './ActionCards';
import DataProvenance from './DataProvenance';
import DataSource from './DataSource';
import Feedback from './Feedback';

function App() {
  const [stats, setStats] = useState(null);
  const [highRisk, setHighRisk] = useState([]);
  const [allDistricts, setAllDistricts] = useState([]);
  const [selectedDistrict, setSelectedDistrict] = useState(null);
  const [districtData, setDistrictData] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [showShortcuts, setShowShortcuts] = useState(false);
  const [showChangelog, setShowChangelog] = useState(false);

  const API = 'http://localhost:8000';

  useEffect(() => {
    fetchStats();
    fetchHighRisk();
    fetchAllDistricts();
    // eslint-disable-next-line
  }, []);

  useEffect(() => {
    const handleKey = (e) => {
      if (e.key === '?' && !e.ctrlKey && !e.metaKey) {
        e.preventDefault();
        setShowShortcuts(true);
      }
      if (e.key === 'Escape') setShowShortcuts(false);
    };
    window.addEventListener('keydown', handleKey);
    return () => window.removeEventListener('keydown', handleKey);
  }, []);

  const fetchStats = async () => {
    try {
      const res = await axios.get(`${API}/api/stats`);
      setStats(res.data);
      setLastUpdated(new Date().toLocaleTimeString('en-IN'));
    } catch (err) {
      setStats({
        total_districts: 114, average_resistance: 37.5,
        red_alerts: 6456, orange_alerts: 12023, total_records: 54720
      });
      setLastUpdated(new Date().toLocaleTimeString('en-IN'));
    }
  };

  const fetchHighRisk = async () => {
    try {
      const res = await axios.get(`${API}/api/predict/high-risk?limit=10`);
      setHighRisk(res.data.high_risk_districts);
    } catch (err) {
      console.error("High risk error:", err.message);
    }
  };

  const fetchAllDistricts = async () => {
    try {
      const res = await axios.get(`${API}/api/predict/high-risk?limit=114`);
      setAllDistricts(res.data.high_risk_districts);
    } catch (err) {
      console.error("All districts error:", err.message);
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
    <ErrorBoundary>
      <>
        <PageTitle redAlerts={stats?.red_alerts} />
        <div className="App">

          <header className="header">
            <h1>🦠 ResistNet <NotificationBadge redAlerts={stats?.red_alerts} /> <SystemStatus /></h1>
            <p>AI-Powered AMR Early Warning & Response</p>
            <LiveClock />
            <SearchDistrict onSelect={fetchDistrict} />
            <div className="header-actions">
              <VoiceSearch onResult={(text) => fetchDistrict(text)} />
              <button className="refresh-btn" onClick={() => { fetchStats(); fetchHighRisk(); }}>🔄</button>
              <ScreenshotBtn />
              <DownloadAll />
              <ShareBtn selectedDistrict={selectedDistrict} />
              <PrintReport stats={stats} allDistricts={allDistricts} />
              <ThemeToggle />
              <button className="changelog-btn" onClick={() => setShowChangelog(true)}>📝</button>
            </div>
          </header>

          <QuickStats stats={stats} />

          <div className="command-center">
            <div className="cc-title">
              <h2>🖥️ Live AMR Command Center</h2>
              <span className="cc-live">● LIVE</span>
            </div>
            {lastUpdated && <div className="last-updated">🕐 Last updated: {lastUpdated}</div>}
            {stats && (
              <div className="stats-row">
                <Tooltip text="Total districts monitored"><div className="stat-card"><h3><AnimatedCounter value={stats.total_districts} /></h3><p>Districts</p></div></Tooltip>
                <Tooltip text="Average resistance"><div className="stat-card"><h3><AnimatedCounter value={parseFloat(stats.average_resistance)} />%</h3><p>Avg Resistance</p></div></Tooltip>
                <Tooltip text="Model-generated high-risk predictions"><div className="stat-card red"><h3><AnimatedCounter value={stats.red_alerts} /></h3><p>🔴 High-Risk Predictions</p></div></Tooltip>
                <Tooltip text="Model-generated elevated-risk predictions"><div className="stat-card orange"><h3><AnimatedCounter value={stats.orange_alerts} /></h3><p>🟠 Elevated-Risk Predictions</p></div></Tooltip>
              </div>
            )}
            <p style={{ fontSize: '0.7rem', color: '#64748b', textAlign: 'center', marginTop: '5px' }}>
              Model-generated signals — not confirmed outbreaks
            </p>
            <WeeklySummary stats={stats} />
          </div>

          <div className="section">
            <LiveDemo />
          </div>

          <div className="section">
            <ActionCards 
              onPredict={() => fetchDistrict("Mumbai")}
              onExplain={() => fetchDistrict("Bangalore")}
              onSimulate={() => fetchDistrict("Chennai")}
              onRespond={() => fetchDistrict("Kolkata")}
            />
          </div>

          <div className="map-rankings-row">
            <div className="map-block">
              <h2>🗺️ India District Risk Map</h2>
              <MapView highRiskData={highRisk} onDistrictClick={fetchDistrict} />
            </div>
            <div className="rankings-block">
              <h2>⚠️ Top High-Risk Districts</h2>
              {highRisk.length === 0 ? <SkeletonLoader count={4} /> : (
                <div className="district-grid">
                  {highRisk.map((d, i) => (
                    <div key={i} className="district-card" onClick={() => fetchDistrict(d.district_name)}>
                      <span className="rank">#{i + 1}</span>
                      <div><strong>{d.district_name}</strong><small>{d.state_name}</small></div>
                      <span className="rate" style={{ background: d.avg_resistance > 40 ? 'rgba(239,68,68,0.2)' : d.avg_resistance > 38 ? 'rgba(249,115,22,0.2)' : 'rgba(34,197,94,0.2)', color: d.avg_resistance > 40 ? '#ef4444' : d.avg_resistance > 38 ? '#f97316' : '#22c55e' }}>{d.avg_resistance.toFixed(1)}%</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {selectedDistrict && districtData && (
            <div className="drawer-section">
              <div className="section">
                <h2>📍 {selectedDistrict} — Predictions</h2>
                <p>🔴 {districtData.red_alerts} High-Risk | 🟠 {districtData.orange_alerts} Elevated-Risk</p>
                <div className="predictions-table">
                  <table>
                    <thead><tr><th>Pathogen</th><th>Antibiotic</th><th>Current</th><th>Predicted</th><th>Status</th></tr></thead>
                    <tbody>
                      {districtData.predictions.slice(0, 5).map((p, i) => (
                        <tr key={i} className={p.severity === 'RED' ? 'row-red' : 'row-orange'}>
                          <td>{p.pathogen}</td><td>{p.antibiotic}</td><td>{p.current_resistance}%</td><td>{p.predicted_resistance}%</td><td>{p.severity === 'RED' ? '🔴' : '🟠'}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
                <ExportReport districtData={districtData} selectedDistrict={selectedDistrict} />
              </div>
              <div className="section"><ModulePanel district={selectedDistrict} districtData={districtData} /></div>
              <div className="section"><PolicySimulator district={selectedDistrict} districtData={districtData} /></div>
              <div className="section"><ResponsePlaybook district={selectedDistrict} districtData={districtData} /></div>
              <div className="section"><PropagationNetwork district={selectedDistrict} /></div>
            </div>
          )}

          <div className="section"><EmergingHotspots /></div>

          <div className="section"><CompareDistricts /></div>

          {districtData && (
            <div className="section">
              <h2>📊 Analytics for {selectedDistrict}</h2>
              <div className="charts-grid">
                <ResistanceBarChart districtData={districtData} />
                <SeverityPieChart districtData={districtData} />
                <PathogenBarChart districtData={districtData} />
                <TrendLineChart districtData={districtData} />
              </div>
            </div>
          )}

          <AlertsPage />

          <div className="section">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
              <h2 style={{ margin: 0 }}>🏆 District Resistance Leaderboard</h2>
              <button className="export-lb-btn" onClick={() => {
                let csv = 'Rank,District,State,Avg Resistance,Risk Level\n';
                allDistricts.forEach((d, i) => { csv += `${i+1},"${d.district_name}","${d.state_name}",${d.avg_resistance.toFixed(1)}%,${d.avg_resistance > 40 ? 'High' : 'Medium'}\n`; });
                const blob = new Blob([csv], { type: 'text/csv' }); const url = window.URL.createObjectURL(blob); const a = document.createElement('a'); a.href = url; a.download = 'resistnet_leaderboard.csv'; a.click();
              }}>📥 Export CSV</button>
            </div>
            <div className="leaderboard-table-container">
              <table className="leaderboard-table">
                <thead><tr><th>Rank</th><th>District</th><th>State</th><th>Avg Resistance</th><th>Risk Level</th></tr></thead>
                <tbody>
                  {allDistricts.map((d, i) => (
                    <tr key={i} onClick={() => fetchDistrict(d.district_name)} className="leaderboard-row">
                      <td><span className="lb-rank">#{i + 1}</span></td>
                      <td><strong>{d.district_name}</strong></td>
                      <td>{d.state_name}</td>
                      <td className={d.avg_resistance > 40 ? 'text-red' : 'text-orange'}>{d.avg_resistance.toFixed(1)}%</td>
                      <td><span className={`risk-badge ${d.avg_resistance > 40 ? 'high' : 'medium'}`}>{d.avg_resistance > 40 ? '🔴 High' : '🟠 Medium'}</span></td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <DataSource />
          <DataProvenance />
          <FooterStats stats={stats} />
          <Feedback />

          <BackToTop />
          <ShortcutsModal show={showShortcuts} onClose={() => setShowShortcuts(false)} />
          <Changelog show={showChangelog} onClose={() => setShowChangelog(false)} />

          <footer className="footer">
            <p>ResistNet v2.0 | Prototype for demonstration | Not for clinical use</p>
          </footer>
        </div>
      </>
    </ErrorBoundary>
  );
}

export default App;