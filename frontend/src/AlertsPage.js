import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const API = 'http://localhost:8000';

function AlertsPage() {
  const [alerts, setAlerts] = useState([]);
  const [filter, setFilter] = useState('ALL');

  const fetchAlerts = useCallback(async () => {
    try {
      const severity = filter === 'ALL' ? '' : filter;
      const res = await axios.get(`${API}/api/alerts`, {
        params: { limit: 50, ...(severity && { severity }) }
      });
      setAlerts(res.data.alerts || []);
    } catch (err) {
      setAlerts([]);
    }
  }, [filter]);

  useEffect(() => {
    fetchAlerts();
  }, [fetchAlerts]);

  return (
    <div className="section">
      <h2>📋 Alert History</h2>
      
      <div className="filter-row">
        {['ALL', 'RED', 'ORANGE', 'YELLOW', 'GREEN'].map(f => (
          <button 
            key={f}
            className={`filter-btn ${filter === f ? 'active' : ''}`}
            onClick={() => setFilter(f)}
          >
            {f === 'ALL' ? '📋 All' : f === 'RED' ? '🔴 RED' : f === 'ORANGE' ? '🟠 ORANGE' : f === 'YELLOW' ? '🟡 YELLOW' : '🟢 GREEN'}
          </button>
        ))}
      </div>

      <div className="alerts-table-container">
        <table className="alerts-table">
          <thead>
            <tr>
              <th>Date</th>
              <th>District</th>
              <th>State</th>
              <th>Severity</th>
              <th>Message</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {alerts.map((alert, i) => (
              <tr key={i} className={`alert-row-${alert.severity?.toLowerCase()}`}>
                <td>{alert.created_at}</td>
                <td><strong>{alert.district_name}</strong></td>
                <td>{alert.state_name}</td>
                <td>
                  <span className={`severity-badge ${alert.severity?.toLowerCase()}`}>
                    {alert.severity}
                  </span>
                </td>
                <td>{alert.alert_text?.substring(0, 60)}...</td>
                <td>{alert.status === 'acknowledged' ? '✅' : '📤'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default AlertsPage;