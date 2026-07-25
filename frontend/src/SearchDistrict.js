import React, { useState, useEffect } from 'react';

const ALL_DISTRICTS = [
  "Mumbai", "Pune", "Nagpur", "Thane", "Nashik", "Aurangabad", "Solapur", "Kolhapur",
  "Chennai", "Coimbatore", "Madurai", "Bangalore", "Mysore", "Hubli", "Mangalore",
  "Kolkata", "Howrah", "Hyderabad", "Warangal", "Lucknow", "Kanpur", "Agra", "Varanasi",
  "Jaipur", "Jodhpur", "Udaipur", "Ahmedabad", "Surat", "Vadodara", "Delhi", "Gurugram",
  "Faridabad", "Bhopal", "Indore", "Patna", "Guwahati", "Bhubaneswar", "Dehradun",
  "Chandigarh", "Kochi", "Thiruvananthapuram", "Erode", "Vellore", "Ujjain", "Ajmer",
  "Gulbarga", "Bellary", "Belgaum", "Jamshedpur", "Ranchi"
];

function SearchDistrict({ onSelect }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [show, setShow] = useState(false);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        document.querySelector('.search-input')?.focus();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleChange = (e) => {
    const val = e.target.value;
    setQuery(val);
    if (val.length > 0) {
      setResults(ALL_DISTRICTS.filter(d => d.toLowerCase().includes(val.toLowerCase())));
      setShow(true);
    } else {
      setShow(false);
    }
  };

  const handleSelect = (district) => {
    setQuery(district);
    setShow(false);
    onSelect(district);
  };

  return (
    <div className="search-container">
      <input
        type="text"
        placeholder="🔍 Search district... (Ctrl+K)"
        value={query}
        onChange={handleChange}
        className="search-input"
      />
      {show && results.length > 0 && (
        <div className="search-results">
          {results.slice(0, 8).map((d, i) => (
            <div key={i} className="search-item" onClick={() => handleSelect(d)}>
              📍 {d}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default SearchDistrict;