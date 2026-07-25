import React, { useState } from 'react';

function Tooltip({ text, children }) {
  const [show, setShow] = useState(false);

  return (
    <div 
      className="tooltip-wrapper"
      onMouseEnter={() => setShow(true)}
      onMouseLeave={() => setShow(false)}
    >
      {children}
      {show && <div className="tooltip-box">{text}</div>}
    </div>
  );
}

export default Tooltip;