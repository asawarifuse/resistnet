import React from 'react';

function ActionCards({ onPredict, onExplain, onSimulate, onRespond }) {
  const cards = [
    { icon: '🔴', title: 'PREDICT', desc: 'Find emerging AMR hotspots', color: '#ef4444', action: onPredict },
    { icon: '🧠', title: 'EXPLAIN', desc: 'Understand why risk is increasing', color: '#8b5cf6', action: onExplain },
    { icon: '🎛️', title: 'SIMULATE', desc: 'Test intervention scenarios', color: '#3b82f6', action: onSimulate },
    { icon: '🚨', title: 'RESPOND', desc: 'Generate incident response plan', color: '#f97316', action: onRespond },
  ];

  return (
    <div className="action-cards">
      {cards.map((card, i) => (
        <div key={i} className="action-card" onClick={card.action} style={{ borderTop: `3px solid ${card.color}` }}>
          <span className="action-icon">{card.icon}</span>
          <h4>{card.title}</h4>
          <p>{card.desc}</p>
        </div>
      ))}
    </div>
  );
}

export default ActionCards;