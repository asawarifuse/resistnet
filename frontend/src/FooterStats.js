import React from 'react';

function FooterStats({ stats }) {
  if (!stats) return null;

  return (
    <div className="footer-stats">
      <div className="footer-stat">
        <span>🦠 Pathogens Tracked</span>
        <strong>5</strong>
      </div>
      <div className="footer-stat">
        <span>💊 Antibiotics Monitored</span>
        <strong>14</strong>
      </div>
      <div className="footer-stat">
        <span>📊 Total Records</span>
        <strong>{stats.total_records?.toLocaleString() || '54,720'}</strong>
      </div>
      <div className="footer-stat">
        <span>⚡ API Status</span>
        <strong className="status-online">● Live</strong>
      </div>
    </div>
  );
}

export default FooterStats;