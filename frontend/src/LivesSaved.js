import React, { useState, useEffect } from 'react';

function LivesSaved({ redAlerts }) {
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    if (!redAlerts) return;
    const target = Math.floor(redAlerts * 12.5);
    let current = 0;
    const step = Math.ceil(target / 60);
    const timer = setInterval(() => {
      current += step;
      if (current >= target) {
        setDisplay(target);
        clearInterval(timer);
      } else {
        setDisplay(current);
      }
    }, 40);
    return () => clearInterval(timer);
  }, [redAlerts]);

  return (
    <div className="lives-saved">
      <span className="lives-icon">🫀</span>
      <div>
        <h3>{display.toLocaleString()}+</h3>
        <p>Estimated Lives Impacted</p>
      </div>
    </div>
  );
}

export default LivesSaved;