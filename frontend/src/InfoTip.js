import React, { useState } from 'react';

function InfoTip({ text }) {
  const [show, setShow] = useState(false);

  return (
    <span className="info-tip-wrapper">
      <span 
        className="info-tip-icon"
        onMouseEnter={() => setShow(true)}
        onMouseLeave={() => setShow(false)}
      >
        ℹ️
      </span>
      {show && <span className="info-tip-text">{text}</span>}
    </span>
  );
}

export default InfoTip;