import React, { useState, useEffect } from 'react';

function PulseDot() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setVisible(true);
      setTimeout(() => setVisible(false), 3000);
    }, 15000);
    return () => clearInterval(interval);
  }, []);

  if (!visible) return null;

  return (
    <span className="pulse-dot" title="New alerts detected!">
      🔴 New
    </span>
  );
}

export default PulseDot;