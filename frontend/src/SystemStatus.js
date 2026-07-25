import React, { useState, useEffect } from 'react';
import axios from 'axios';

function SystemStatus() {
  const [status, setStatus] = useState('checking');
  const API = 'http://localhost:8000';

  useEffect(() => {
    const check = async () => {
      try {
        await axios.get(`${API}/health`);
        setStatus('online');
      } catch {
        setStatus('offline');
      }
    };
    check();
    const timer = setInterval(check, 30000);
    return () => clearInterval(timer);
  }, []);

  const colors = { online: '#22c55e', offline: '#ef4444', checking: '#eab308' };

  return (
    <span className="system-status" style={{ color: colors[status] }} title={`API ${status}`}>
      ● {status === 'online' ? 'Live' : status === 'offline' ? 'Offline' : 'Checking...'}
    </span>
  );
}

export default SystemStatus;