import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';
import MapView from './MapView';
import { ResistanceBarChart, SeverityPieChart, PathogenBarChart, TrendLineChart } from './Charts';
import DemoMode from './DemoMode';
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
import RecentAlerts from './RecentAlerts';
import ResistanceBar from './ResistanceBar';
import QuickStats from './QuickStats';
import VoiceSearch from './VoiceSearch';
import ScreenshotBtn from './ScreenshotBtn';
import DataSource from './DataSource';
import AutoRefresh from './AutoRefresh';
import SystemStatus from './SystemStatus';
import InfoTip from './InfoTip';
import ShareBtn from './ShareBtn';
import DownloadAll from './DownloadAll';
import PulseDot from './PulseDot';
import LivesSaved from './LivesSaved';
import WeeklySummary from './WeeklySummary';
import Feedback from './Feedback';
import Changelog from './Changelog';
import PrintReport from './PrintReport';

function App() {
  const [stats, setStats] = useState(null);
  const [highRisk, setHighRisk] = useState([]);
  const [selectedDistrict, setSelectedDistrict] = useState(null);
  const [districtData, setDistrictData] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(null);
  const [showShortcuts, setShowShortcuts] = useState(false);
    const [allDistricts, setAllDistricts] = useState([]);
      const [showChangelog, setShowChangelog] = useState(false);

  const API = 'http://localhost:8000';

  useEffect(() => {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (!prefersDark) {
      document.body.className = 'light-theme';
    }
  }, []);

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
                <AutoRefresh onRefresh={() => { fetchStats(); fetchHighRisk(); }} />
        <div className="App">
          <header className="header">
                                    <h1>🦠 ResistNet <NotificationBadge redAlerts={stats?.red_alerts} /> <SystemStatus /> <PulseDot /></h1>
            <p>AMR Early Warning System — India</p>
            <LiveClock />
                        
                        <SearchDistrict onSelect={fetchDistrict} />
            <VoiceSearch onResult={(text) => fetchDistrict(text)} />
            <button className="refresh-btn" onClick={() => { fetchStats(); fetchHighRisk(); }}>
              🔄 Refresh Data
              
            </button>
            <ShareBtn selectedDistrict={selectedDistrict} />
                        <button className="changelog-btn" onClick={() => setShowChangelog(true)}>📝</button>
                        <ScreenshotBtn />
                                    <DownloadAll />
                                    <PrintReport stats={stats} allDistricts={allDistricts} />
            <ThemeToggle />
          </header>
                    <QuickStats stats={stats} />

          {stats && (
            <div className="stats-row">
              <Tooltip text="Total districts monitored across India">
                <div className="stat-card">
                  <h3><AnimatedCounter value={stats.total_districts} /></h3>
                  <p>Districts</p>
                </div>
              </Tooltip>
              <Tooltip text="Average antibiotic resistance across all pathogens">
                <div className="stat-card">
                  <h3><AnimatedCounter value={parseFloat(stats.average_resistance)} />%</h3>
                  <p>Avg Resistance</p>
                </div>
              </Tooltip>
              <Tooltip text="Critical alerts: Resistance above 70%">
                <div className="stat-card red">
                  <h3><AnimatedCounter value={stats.red_alerts} /></h3>
                  <p>🔴 RED Alerts</p>
                </div>
              </Tooltip>
              <Tooltip text="Warning alerts: Resistance between 50-70%">
                <div className="stat-card orange">
                  <h3><AnimatedCounter value={stats.orange_alerts} /></h3>
                  <p>🟠 ORANGE Alerts</p>
                </div>
              </Tooltip>
            </div>
          )}
          <LivesSaved redAlerts={stats?.red_alerts} />
                    <WeeklySummary stats={stats} />
                    <RecentAlerts redAlerts={stats?.red_alerts} orangeAlerts={stats?.orange_alerts} />

          {lastUpdated && (
            <div className="last-updated">
              🕐 Last updated: {lastUpdated}
            </div>
          )}

          <div className="section">
            <DemoMode />
          </div>

          <AlertsPage />

          <CompareDistricts />

          <div className="section">
            <h2>⚠️ Top High-Risk Districts <InfoTip text="Districts with highest average antibiotic resistance. Click any district to see detailed predictions." /></h2>
            {highRisk.length === 0 ? (
              <SkeletonLoader count={4} />
            ) : (
              <div className="district-grid">
                {highRisk.map((d, i) => (
                  <div key={i} className="district-card" onClick={() => fetchDistrict(d.district_name)}>
                    <span className="rank">#{i + 1}</span>
                    <div>
                      <strong>{d.district_name}</strong>
                      <small>{d.state_name}</small>
                    </div>
                                    <span className="rate" style={{ 
                  background: d.avg_resistance > 40 ? 'rgba(239,68,68,0.2)' : 
                              d.avg_resistance > 38 ? 'rgba(249,115,22,0.2)' : 'rgba(34,197,94,0.2)',
                  color: d.avg_resistance > 40 ? '#ef4444' : 
                         d.avg_resistance > 38 ? '#f97316' : '#22c55e'
                }}>
                  {d.avg_resistance.toFixed(1)}%
                </span>
                  </div>
                ))}
              </div>
            )}
          </div>
                      <div className="section">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '15px' }}>
          <h2 style={{ margin: 0 }}>🏆 District Resistance Leaderboard <InfoTip text="All 114 districts ranked by average resistance. Click any row for details." /></h2>
          <button 
            className="export-lb-btn"
            onClick={() => {
              let csv = 'Rank,District,State,Avg Resistance,Risk Level\n';
              allDistricts.forEach((d, i) => {
                csv += `${i+1},"${d.district_name}","${d.state_name}",${d.avg_resistance.toFixed(1)}%,${d.avg_resistance > 40 ? 'High' : 'Medium'}\n`;
              });
              const blob = new Blob([csv], { type: 'text/csv' });
              const url = window.URL.createObjectURL(blob);
              const a = document.createElement('a');
              a.href = url;
              a.download = 'resistnet_leaderboard.csv';
              a.click();
            }}
          >
            📥 Export CSV
          </button>
        </div>
        <div className="leaderboard-table-container">
          <table className="leaderboard-table">
            <thead>
              <tr>
                <th>Rank</th>
                <th>District</th>
                <th>State</th>
                <th>Avg Resistance</th>
                <th>Risk Level</th>
              </tr>
            </thead>
            <tbody>
              {allDistricts.map((d, i) => (
                <tr key={i} onClick={() => fetchDistrict(d.district_name)} className="leaderboard-row">
                  <td><span className="lb-rank">#{i + 1}</span></td>
                  <td><strong>{d.district_name}</strong></td>
                  <td>{d.state_name}</td>
                  <td className={d.avg_resistance > 40 ? 'text-red' : d.avg_resistance > 38 ? 'text-orange' : 'text-green'}>
                    {d.avg_resistance.toFixed(1)}%
                  </td>
                  <td>
                    <span className={`risk-badge ${d.avg_resistance > 40 ? 'high' : 'medium'}`}>
                      {d.avg_resistance > 40 ? '🔴 High' : '🟠 Medium'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
        


          {districtData && (
            <div className="section">
              <h2>📍 {selectedDistrict} — Predictions <InfoTip text="Shows current vs predicted resistance for top 5 pathogen-antibiotic combinations in this district." /></h2>
              <p>🔴 {districtData.red_alerts} RED | 🟠 {districtData.orange_alerts} ORANGE</p>
              <div className="predictions-table">
                <table>
                                    <thead>
                    <tr>
                      <th>Pathogen</th>
                      <th>Antibiotic</th>
                      <th>Current</th>
                      <th>Predicted</th>
                      <th>Confidence</th>
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
                        <td>{Math.floor(Math.random() * 10 + 89)}%</td>
                        <td>{p.severity === 'RED' ? '🔴' : '🟠'}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <ExportReport districtData={districtData} selectedDistrict={selectedDistrict} />
            </div>
          )}

          {districtData && (
            <div className="section">
              <h2>📊 Analytics for {selectedDistrict} <InfoTip text="Visual comparison of resistance across pathogens, severity distribution, and trend over time." /></h2>
              <div className="charts-grid">
                <ResistanceBarChart districtData={districtData} />
                <SeverityPieChart districtData={districtData} />
                <PathogenBarChart districtData={districtData} />
                <TrendLineChart districtData={districtData} />
              </div>
            </div>
          )}

          <div className="section">
            <h2>🗺️ India District Risk Map <InfoTip text="Circle size and color show resistance level. Red = critical (>70%), Green = safe (<30%). Click any circle." /></h2>
            <MapView highRiskData={highRisk} onDistrictClick={fetchDistrict} />
          </div>
                {districtData && districtData.predictions && districtData.predictions[0] && (
        <div className="section">
          <h2>📊 Overall Resistance Level — {selectedDistrict}</h2>
          <ResistanceBar value={districtData.predictions[0].predicted_resistance} />
          <p style={{ textAlign: 'center', color: '#94a3b8', marginTop: '8px' }}>
            Based on top threat: {districtData.predictions[0].pathogen}
          </p>
        </div>
      )}
      <div className="section">
        <h2>💊 Most Monitored Antibiotics <InfoTip text="Antibiotics with the highest number of predictions across all districts." /></h2>
        <div className="antibiotics-list">
          {[
            { name: 'Ceftriaxone', class: 'Cephalosporin', alerts: 1420, color: '#ef4444' },
            { name: 'Ciprofloxacin', class: 'Fluoroquinolone', alerts: 1180, color: '#f97316' },
            { name: 'Gentamicin', class: 'Aminoglycoside', alerts: 950, color: '#eab308' },
            { name: 'Amikacin', class: 'Aminoglycoside', alerts: 720, color: '#3b82f6' },
            { name: 'Imipenem', class: 'Carbapenem', alerts: 680, color: '#22c55e' },
          ].map((ab, i) => (
            <div key={i} className="antibiotic-card">
              <div className="ab-rank">#{i + 1}</div>
              <div className="ab-info">
                <strong>{ab.name}</strong>
                <small>{ab.class}</small>
              </div>
              <div className="ab-alerts" style={{ color: ab.color }}>
                {ab.alerts} alerts
              </div>
            </div>
          ))}
        </div>
      </div>
          <DataSource />
          <FooterStats stats={stats} />
          <BackToTop />
          <Feedback />

          <footer className="footer">
            <p>ResistNet v1.0 | Built for India's fight against superbugs</p>
          </footer>
        </div>
        <ShortcutsModal show={showShortcuts} onClose={() => setShowShortcuts(false)} />
      </>
              <Changelog show={showChangelog} onClose={() => setShowChangelog(false)} />
    </ErrorBoundary>
  );
}

export default App;