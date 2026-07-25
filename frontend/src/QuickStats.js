import React from 'react';

function QuickStats({ stats }) {
  if (!stats) return null;

  const quickItems = [
    { icon: '🏥', label: 'Top District', value: stats.top_risk_district?.name || 'N/A' },
    { icon: '🦠', label: 'Pathogens', value: '5' },
    { icon: '💊', label: 'Antibiotics', value: '14' },
    { icon: '📊', label: 'Records', value: (stats.total_records || 54720).toLocaleString() },
  ];

  return (
    <div className="quick-stats">
      {quickItems.map((item, i) => (
        <div key={i} className="quick-stat-item">
          <span className="quick-icon">{item.icon}</span>
          <div>
            <small>{item.label}</small>
            <strong>{item.value}</strong>
          </div>
        </div>
      ))}
    </div>
  );
}

export default QuickStats;