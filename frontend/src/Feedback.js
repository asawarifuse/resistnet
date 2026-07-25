import React, { useState } from 'react';

function Feedback() {
  const [rated, setRated] = useState(null);
  const [done, setDone] = useState(false);

  const handleRate = (rating) => {
    setRated(rating);
    setTimeout(() => setDone(true), 800);
  };

  if (done) {
    return (
      <div className="feedback-widget">
        <span>✅ Thanks for your feedback!</span>
      </div>
    );
  }

  return (
    <div className="feedback-widget">
      <span>Was this helpful?</span>
      {[1, 2, 3, 4, 5].map(n => (
        <button 
          key={n} 
          className={`rate-btn ${rated === n ? 'rated' : ''}`}
          onClick={() => handleRate(n)}
        >
          {rated && rated >= n ? '⭐' : '☆'}
        </button>
      ))}
    </div>
  );
}

export default Feedback;