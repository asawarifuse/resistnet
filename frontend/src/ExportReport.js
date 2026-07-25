import React, { useState } from 'react';

function ExportReport({ districtData, selectedDistrict }) {
  const [exporting, setExporting] = useState(false);

  const exportCSV = () => {
    if (!districtData || !districtData.predictions) return;
    setExporting(true);
    
    let csv = 'Pathogen,Antibiotic,Current Resistance,Predicted Resistance,Severity\n';
    districtData.predictions.forEach(p => {
      csv += `"${p.pathogen}","${p.antibiotic}",${p.current_resistance},${p.predicted_resistance},${p.severity}\n`;
    });
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `resistnet_${selectedDistrict}_report.csv`;
    a.click();
    setExporting(false);
  };

  const exportJSON = () => {
    if (!districtData) return;
    const json = JSON.stringify(districtData, null, 2);
    const blob = new Blob([json], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `resistnet_${selectedDistrict}_data.json`;
    a.click();
  };

  if (!districtData) return null;

  return (
    <div className="export-section">
      <h3>📥 Export Report — {selectedDistrict}</h3>
      <div className="export-buttons">
        <button className="export-btn csv" onClick={exportCSV} disabled={exporting}>
          📄 Export CSV
        </button>
        <button className="export-btn json" onClick={exportJSON}>
          📋 Export JSON
        </button>
      </div>
    </div>
  );
}

export default ExportReport;