import React, { useState } from 'react';

function LiveDemo() {
  const [running, setRunning] = useState(false);
  const [step, setStep] = useState(0);

  const demoSteps = [
    "🦠 New AMR signal detected in Nagpur",
    "🧠 Sanket analyzing resistance patterns...",
    "📈 Risk increasing — 82% predicted",
    "🔴 District becomes CRITICAL",
    "🧩 SHAP explanation generated",
    "🔗 Propagation risk calculated for neighbors",
    "📢 Sahay creating incident response plan",
    "🎛️ Policy simulator testing interventions",
    "✅ Demo complete — Nagpur responded"
  ];

  const runDemo = () => {
    setRunning(true);
    setStep(0);
    
    let i = 0;
    const interval = setInterval(() => {
      i++;
      if (i >= demoSteps.length) {
        clearInterval(interval);
        setRunning(false);
      } else {
        setStep(i);
      }
    }, 1200);
  };

  return (
    <div className="live-demo-panel">
      <div className="demo-header">
        <h3>🎬 Live Demo</h3>
        <button className="demo-run-btn" onClick={runDemo} disabled={running}>
          {running ? '⏳ Running...' : '▶ Run Demo'}
        </button>
      </div>

      {step > 0 && (
        <div className="demo-timeline">
          {demoSteps.slice(0, step + 1).map((s, i) => (
            <div key={i} className="demo-step">
              <span className="demo-dot">{i < step ? '✅' : '⏳'}</span>
              <span>{s}</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default LiveDemo;