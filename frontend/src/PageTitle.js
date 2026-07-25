import { useEffect } from 'react';

function PageTitle({ redAlerts }) {
  useEffect(() => {
    if (redAlerts > 0) {
      document.title = `🔴 ${redAlerts} Alerts — ResistNet`;
    } else {
      document.title = '🦠 ResistNet — AMR Early Warning System';
    }
  }, [redAlerts]);

  return null;
}

export default PageTitle;