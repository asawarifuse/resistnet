import React, { useState } from 'react';

function Limitations() {
  const [show, setShow] = useState(false);

  const limitations = [
    "Prototype evaluated on synthetic/simulated data",
    "External validation not yet performed",
    "Predictions are not clinical diagnoses",
    "Intervention recommendations require expert validation",
    "Model performance may vary across districts",
    "Data availability and reporting quality can affect predictions",
    "False positive rate of 85.7% at current warning threshold",
    "Not for autonomous clinical decisions"
  ];

  return (
    <div className="limitations-panel">
      <button className="limitations-btn" onClick={() => setShow(!show)}>
        ⚠️ Current Limitations
      </button>
      {show && (
        <div className="limitations-content">
          <ul>
            {limitations.map((lim, i) => (
              <li key={i}>{lim}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default Limitations;