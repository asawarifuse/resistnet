import React, { useState } from 'react';

function ShareBtn({ selectedDistrict }) {
  const [copied, setCopied] = useState(false);

  const share = () => {
    const url = selectedDistrict 
      ? `http://localhost:3000?district=${selectedDistrict}`
      : 'http://localhost:3000';
    
    navigator.clipboard.writeText(url).then(() => {
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    });
  };

  return (
    <button className="share-btn" onClick={share}>
      {copied ? '✅ Copied!' : '🔗 Share'}
    </button>
  );
}

export default ShareBtn;