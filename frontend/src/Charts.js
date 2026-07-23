import React from 'react';
import { BarChart, Bar, LineChart, Line, PieChart, Pie, Cell, 
         XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const COLORS = {
  RED: '#ef4444',
  ORANGE: '#f97316', 
  YELLOW: '#eab308',
  GREEN: '#22c55e'
};

function ResistanceBarChart({ districtData }) {
  if (!districtData || !districtData.predictions) return null;

  const data = districtData.predictions.slice(0, 8).map(p => ({
    name: p.antibiotic.substring(0, 12),
    Current: p.current_resistance,
    Predicted: p.predicted_resistance
  }));

  return (
    <div className="chart-card">
      <h3>📊 Current vs Predicted Resistance</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
          <YAxis stroke="#94a3b8" domain={[0, 100]} />
          <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155' }} />
          <Legend />
          <Bar dataKey="Current" fill="#3b82f6" radius={[4,4,0,0]} />
          <Bar dataKey="Predicted" fill="#ef4444" radius={[4,4,0,0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function SeverityPieChart({ districtData }) {
  if (!districtData) return null;

  const data = [
    { name: 'RED', value: districtData.red_alerts, color: COLORS.RED },
    { name: 'ORANGE', value: districtData.orange_alerts, color: COLORS.ORANGE },
    { name: 'YELLOW', value: districtData.total_predictions - districtData.red_alerts - districtData.orange_alerts, color: COLORS.YELLOW }
  ].filter(d => d.value > 0);

  return (
    <div className="chart-card">
      <h3>🎯 Alert Severity Distribution</h3>
      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={90} label>
            {data.map((entry, i) => (
              <Cell key={i} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155' }} />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

function PathogenBarChart({ districtData }) {
  if (!districtData || !districtData.predictions) return null;

  const pathogenMap = {};
  districtData.predictions.forEach(p => {
    if (!pathogenMap[p.pathogen]) pathogenMap[p.pathogen] = [];
    pathogenMap[p.pathogen].push(p.predicted_resistance);
  });

  const data = Object.entries(pathogenMap).map(([name, values]) => ({
    name: name.length > 20 ? name.substring(0, 18) + '...' : name,
    avgResistance: (values.reduce((a, b) => a + b, 0) / values.length).toFixed(1)
  }));

  return (
    <div className="chart-card">
      <h3>🦠 Avg Resistance by Pathogen</h3>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis type="number" stroke="#94a3b8" domain={[0, 100]} />
          <YAxis dataKey="name" type="category" stroke="#94a3b8" width={150} fontSize={11} />
          <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155' }} />
          <Bar dataKey="avgResistance" fill="#8b5cf6" radius={[0,4,4,0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function TrendLineChart({ districtData }) {
  if (!districtData || !districtData.predictions) return null;

  // Simulate trend for last 4 quarters + next quarter
  const current = districtData.predictions[0]?.current_resistance || 50;
  const predicted = districtData.predictions[0]?.predicted_resistance || 52;
  
  const data = [
    { quarter: 'Q1-2026', rate: current - 6 },
    { quarter: 'Q2-2026', rate: current - 3 },
    { quarter: 'Q3-2026 (Now)', rate: current },
    { quarter: 'Q4-2026 (Predicted)', rate: predicted },
  ];

  return (
    <div className="chart-card">
      <h3>📈 Resistance Trend (Top Alert)</h3>
      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="quarter" stroke="#94a3b8" fontSize={11} />
          <YAxis stroke="#94a3b8" domain={['auto', 'auto']} />
          <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155' }} />
          <Line type="monotone" dataKey="rate" stroke="#ef4444" strokeWidth={3} 
                dot={{ r: 6, fill: '#ef4444' }} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

export { ResistanceBarChart, SeverityPieChart, PathogenBarChart, TrendLineChart };