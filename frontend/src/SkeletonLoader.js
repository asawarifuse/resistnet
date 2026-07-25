import React from 'react';

function SkeletonLoader({ count = 4 }) {
  return (
    <div className="skeleton-grid">
      {[...Array(count)].map((_, i) => (
        <div key={i} className="skeleton-card">
          <div className="skeleton-line skeleton-title"></div>
          <div className="skeleton-line skeleton-text"></div>
          <div className="skeleton-line skeleton-text short"></div>
        </div>
      ))}
    </div>
  );
}

export default SkeletonLoader;