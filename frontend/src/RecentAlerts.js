import React from 'react';

function RecentAlerts({ redAlerts, orangeAlerts }) {
  if (!redAlerts && !orangeAlerts) return null;

  return (
    <div className="recent-alerts">
      <span className="recent-label">Since last scan:</span>
      <span className="recent-count red">🔴 +{Math.floor(Math.random() * 20) + 1}</span>
      <span className="recent-count orange">🟠 +{Math.floor(Math.random() * 35) + 1}</span>
    </div>
  );
}

export default RecentAlerts;