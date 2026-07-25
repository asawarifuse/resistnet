import React, { useState } from 'react';
import axios from 'axios';

function DownloadAll() {
  const [loading, setLoading] = useState(false);
  const API = 'http://localhost:8000';

  const downloadAll = async () => {
    setLoading(true);
    try {
      const [stats, districts, highRisk] = await Promise.all([
        axios.get(`${API}/api/stats`),
        axios.get(`${API}/api/districts`),
        axios.get(`${API}/api/predict/high-risk?limit=50`)
      ]);

      const allData = {
        exported_at: new Date().toISOString(),
        statistics: stats.data,
        districts: districts.data,
        high_risk_districts: highRisk.data
      };

      const blob = new Blob([JSON.stringify(allData, null, 2)], { type: 'application/json' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `resistnet_full_export_${new Date().toISOString().slice(0,10)}.json`;
      a.click();
    } catch (err) {
      console.log('Download failed');
    }
    setLoading(false);
  };

  return (
    <button className="download-all-btn" onClick={downloadAll} disabled={loading}>
      {loading ? '⏳ Exporting...' : '📦 Export All Data'}
    </button>
  );
}

export default DownloadAll;