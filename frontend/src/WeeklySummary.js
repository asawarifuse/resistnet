import React from 'react';

function WeeklySummary({ stats }) {
  if (!stats) return null;

  const trend = stats.average_resistance > 37 ? 'increasing 📈' : 'stable 📊';
  const topDistrict = stats.top_risk_district?.name || 'Unknown';

  return (
    <div className="weekly-summary">
      <div className="weekly-item">
        <span>📈 Trend</span>
        <strong>{trend}</strong>
      </div>
      <div className="weekly-item">
        <span>🔴 Critical</span>
        <strong>{stats.red_alerts?.toLocaleString()} alerts</strong>
      </div>
      <div className="weekly-item">
        <span>📍 Highest Risk</span>
        <strong>{topDistrict} ({stats.top_risk_district?.avg_resistance}%)</strong>
      </div>
      <div className="weekly-item">
        <span>📅 Week</span>
        <strong>{new Date().toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })} - {new Date(Date.now() + 604800000).toLocaleDateString('en-IN', { month: 'short', day: 'numeric' })}</strong>
      </div>
    </div>
  );
}

export default WeeklySummary;