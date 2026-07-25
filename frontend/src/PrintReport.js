import React from 'react';

function PrintReport({ stats, allDistricts }) {
  const handlePrint = () => {
    const printWindow = window.open('', '_blank');
    const top5 = allDistricts.slice(0, 5);
    
    printWindow.document.write(`
      <html>
        <head>
          <title>ResistNet Report</title>
          <style>
            body { font-family: Arial; padding: 30px; color: #1e293b; }
            h1 { color: #dc2626; border-bottom: 2px solid #dc2626; padding-bottom: 10px; }
            h2 { color: #334155; margin-top: 25px; }
            table { width: 100%; border-collapse: collapse; margin: 15px 0; }
            th { background: #f1f5f9; padding: 10px; text-align: left; }
            td { padding: 8px 10px; border-bottom: 1px solid #e2e8f0; }
            .stat-box { display: inline-block; padding: 15px; margin: 10px; background: #f8fafc; border-radius: 8px; text-align: center; }
            .stat-box h3 { margin: 0; color: #dc2626; font-size: 1.5rem; }
            .footer { margin-top: 30px; color: #94a3b8; font-size: 0.8rem; border-top: 1px solid #e2e8f0; padding-top: 15px; }
            @media print { body { padding: 0; } }
          </style>
        </head>
        <body>
          <h1>🦠 ResistNet — AMR Surveillance Report</h1>
          <p>Generated: ${new Date().toLocaleString('en-IN')}</p>
          
          <h2>Summary Statistics</h2>
          <div>
            <div class="stat-box"><h3>${stats?.total_districts || 114}</h3>Districts</div>
            <div class="stat-box"><h3>${stats?.average_resistance || 37.5}%</h3>Avg Resistance</div>
            <div class="stat-box"><h3>${stats?.red_alerts || 6456}</h3>🔴 RED Alerts</div>
            <div class="stat-box"><h3>${stats?.orange_alerts || 12023}</h3>🟠 ORANGE Alerts</div>
          </div>
          
          <h2>Top 5 High-Risk Districts</h2>
          <table>
            <tr><th>Rank</th><th>District</th><th>State</th><th>Resistance</th></tr>
            ${top5.map((d, i) => `<tr><td>#${i+1}</td><td>${d.district_name}</td><td>${d.state_name}</td><td><strong>${d.avg_resistance.toFixed(1)}%</strong></td></tr>`).join('')}
          </table>
          
          <div class="footer">
            ResistNet v1.0 | Built by Asawari Vasantrao Fuse | Data calibrated to ICMR AMR Surveillance Network
          </div>
        </body>
      </html>
    `);
    printWindow.document.close();
    printWindow.print();
  };

  return (
    <button className="print-report-btn" onClick={handlePrint}>
      🖨️ Print Report
    </button>
  );
}

export default PrintReport;