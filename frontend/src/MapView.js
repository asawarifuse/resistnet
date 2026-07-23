import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, CircleMarker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix default marker icon
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// Approximate coordinates for major Indian district cities
const DISTRICT_COORDS = {
  "Mumbai": [19.0760, 72.8777],
  "Pune": [18.5204, 73.8567],
  "Nagpur": [21.1458, 79.0882],
  "Thane": [19.2183, 72.9781],
  "Nashik": [19.9975, 73.7898],
  "Aurangabad": [19.8762, 75.3433],
  "Solapur": [17.6599, 75.9064],
  "Kolhapur": [16.7050, 74.2433],
  "Chennai": [13.0827, 80.2707],
  "Coimbatore": [11.0168, 76.9558],
  "Madurai": [9.9252, 78.1198],
  "Bangalore": [12.9716, 77.5946],
  "Mysore": [12.2958, 76.6394],
  "Hubli": [15.3647, 75.1240],
  "Mangalore": [12.9141, 74.8560],
  "Kolkata": [22.5726, 88.3639],
  "Howrah": [22.5958, 88.2636],
  "Hyderabad": [17.3850, 78.4867],
  "Warangal": [17.9784, 79.5941],
  "Lucknow": [26.8467, 80.9462],
  "Kanpur": [26.4499, 80.3319],
  "Agra": [27.1767, 78.0081],
  "Varanasi": [25.3176, 82.9739],
  "Jaipur": [26.9124, 75.7873],
  "Jodhpur": [26.2389, 73.0243],
  "Udaipur": [24.5854, 73.7125],
  "Ahmedabad": [23.0225, 72.5714],
  "Surat": [21.1702, 72.8311],
  "Vadodara": [22.3072, 73.1812],
  "Delhi": [28.7041, 77.1025],
  "Gurugram": [28.4595, 77.0266],
  "Faridabad": [28.4089, 77.3178],
  "Bhopal": [23.2599, 77.4126],
  "Indore": [22.7196, 75.8577],
  "Patna": [25.5941, 85.1376],
  "Guwahati": [26.1445, 91.7362],
  "Bhubaneswar": [20.2961, 85.8245],
  "Dehradun": [30.3165, 78.0322],
  "Chandigarh": [30.7333, 76.7794],
  "Kochi": [9.9312, 76.2673],
  "Thiruvananthapuram": [8.5241, 76.9366],
};

function getColor(resistance) {
  if (resistance >= 70) return '#ef4444';  // RED
  if (resistance >= 50) return '#f97316';  // ORANGE
  if (resistance >= 30) return '#eab308';  // YELLOW
  return '#22c55e';                         // GREEN
}

function MapView({ highRiskData, onDistrictClick }) {
  const [markers, setMarkers] = useState([]);

  useEffect(() => {
    if (highRiskData && highRiskData.length > 0) {
      const mapped = highRiskData
        .filter(d => DISTRICT_COORDS[d.district_name])
        .map(d => ({
          ...d,
          position: DISTRICT_COORDS[d.district_name],
          color: getColor(d.avg_resistance)
        }));
      setMarkers(mapped);
    }
  }, [highRiskData]);

  return (
    <div className="map-container">
      <MapContainer 
        center={[22.5, 79]} 
        zoom={5} 
        style={{ height: '500px', width: '100%', borderRadius: '12px' }}
      >
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap contributors'
        />
        
        {markers.map((d, i) => (
          <CircleMarker
            key={i}
            center={d.position}
            radius={8 + d.avg_resistance / 10}
            fillColor={d.color}
            color="#fff"
            weight={1}
            fillOpacity={0.8}
            eventHandlers={{
              click: () => onDistrictClick(d.district_name)
            }}
          >
            <Popup>
              <div style={{ textAlign: 'center' }}>
                <strong>{d.district_name}</strong><br />
                <span style={{ color: d.color, fontWeight: 'bold' }}>
                  {d.avg_resistance.toFixed(1)}%
                </span><br />
                <small>{d.state_name}</small>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
      
      {/* Legend */}
      <div className="legend">
        <div><span style={{background:'#ef4444'}}></span> High (≥70%)</div>
        <div><span style={{background:'#f97316'}}></span> Medium (50-70%)</div>
        <div><span style={{background:'#eab308'}}></span> Low (30-50%)</div>
        <div><span style={{background:'#22c55e'}}></span> Safe (&lt;30%)</div>
      </div>
    </div>
  );
}

export default MapView;