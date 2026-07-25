import React from 'react';

function NotificationBadge({ redAlerts }) {
  if (!redAlerts || redAlerts === 0) return null;

  return (
    <span className="notif-badge" title={`${redAlerts} high risk alerts`}>
      🔴 {redAlerts}
    </span>
  );
}

export default NotificationBadge;