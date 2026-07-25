import React from 'react';

function Changelog({ show, onClose }) {
  if (!show) return null;

  const updates = [
    { version: 'v1.0', date: '25 Jul 2026', changes: ['Initial release', '114 districts monitored', '3 ML models ensemble', 'Interactive India risk map'] },
    { version: 'v0.9', date: '24 Jul 2026', changes: ['Dark/Light theme', 'Voice search', 'Export reports'] },
    { version: 'v0.8', date: '23 Jul 2026', changes: ['District comparison', 'Alert history', 'Keyboard shortcuts'] },
    { version: 'v0.5', date: '20 Jul 2026', changes: ['React dashboard', 'Leaflet.js map', 'Recharts analytics'] },
  ];

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content changelog-modal" onClick={e => e.stopPropagation()}>
        <h3>📝 What's New</h3>
        {updates.map((u, i) => (
          <div key={i} className="changelog-item">
            <div className="changelog-header">
              <strong>{u.version}</strong>
              <span>{u.date}</span>
            </div>
            <ul>
              {u.changes.map((c, j) => <li key={j}>{c}</li>)}
            </ul>
          </div>
        ))}
        <button className="modal-close" onClick={onClose}>✕</button>
      </div>
    </div>
  );
}

export default Changelog;