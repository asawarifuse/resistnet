import React, { useState, useEffect } from 'react';

function ThemeToggle() {
  const [dark, setDark] = useState(true);

  useEffect(() => {
    document.body.className = dark ? 'dark-theme' : 'light-theme';
  }, [dark]);

  return (
    <button className="theme-toggle" onClick={() => setDark(!dark)}>
      {dark ? '☀️ Light' : '🌙 Dark'}
    </button>
  );
}

export default ThemeToggle;