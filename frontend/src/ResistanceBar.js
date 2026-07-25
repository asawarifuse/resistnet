import React from 'react';

function ResistanceBar({ value, max = 100 }) {
  const percent = (value / max) * 100;
  let color = '#22c55e';
  if (value > 70) color = '#ef4444';
  else if (value > 50) color = '#f97316';
  else if (value > 30) color = '#eab308';

  return (
    <div className="resistance-bar-container">
      <div className="resistance-bar-fill" style={{ width: `${percent}%`, background: color }}>
        <span className="resistance-bar-label">{value}%</span>
      </div>
    </div>
  );
}

export default ResistanceBar;