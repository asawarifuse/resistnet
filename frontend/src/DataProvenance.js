import React, { useState } from 'react';

function DataProvenance() {
  const [show, setShow] = useState(false);

  return (
    <div className="provenance-panel">
      <button className="provenance-btn" onClick={() => setShow(!show)}>
        📊 Data & Methodology
      </button>

      {show && (
        <div className="provenance-content">
          <h3>Data Provenance</h3>
          
          <div className="provenance-section">
            <h4>🧬 AMR Resistance Data</h4>
            <ul>
              <li>Records: 54,720</li>
              <li>Districts: 114</li>
              <li>Pathogens: 5</li>
              <li>Antibiotics: 14</li>
              <li>Period: 2021-2023 (quarterly)</li>
            </ul>
            <p className="data-note">⚠️ Synthetic prototype dataset modeled on AMR surveillance characteristics. Not validated clinical data.</p>
          </div>

          <div className="provenance-section">
            <h4>💊 Antibiotic Consumption Data</h4>
            <ul>
              <li>Records: 229,824</li>
              <li>Channels: Retail, Hospital, Online, Government</li>
              <li>Period: 2021-2023 (monthly)</li>
            </ul>
            <p className="data-note">⚠️ Synthetic prototype dataset for demonstration. Not real pharmaceutical sales data.</p>
          </div>

          <div className="provenance-section">
            <h4>🔬 Pipeline</h4>
            <div className="pipeline-flow">
              DATA → FEATURES → MODEL → PREDICTION → RESPONSE
            </div>
          </div>

          <div className="provenance-section">
            <h4>🧠 Models</h4>
            <p>Prophet, Random Forest, XGBoost, LSTM, Ensemble</p>
            <p>Explainability: SHAP</p>
          </div>

          <p className="provenance-disclaimer">
            This is a prototype for demonstration. Not for clinical use without validation.
          </p>
        </div>
      )}
    </div>
  );
}

export default DataProvenance;