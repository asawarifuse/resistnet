import React, { useState } from 'react';
import html2canvas from 'html2canvas';

function ScreenshotBtn() {
  const [capturing, setCapturing] = useState(false);

  const takeScreenshot = async () => {
    setCapturing(true);
    try {
      const canvas = await html2canvas(document.querySelector('.App'), {
        backgroundColor: '#0f172a',
        scale: 0.7
      });
      const link = document.createElement('a');
      link.download = 'resistnet_dashboard.png';
      link.href = canvas.toDataURL();
      link.click();
    } catch (err) {
      console.log('Screenshot failed');
    }
    setCapturing(false);
  };

  return (
    <button className="screenshot-btn" onClick={takeScreenshot} disabled={capturing}>
      {capturing ? '📸 Capturing...' : '📸 Save Dashboard'}
    </button>
  );
}

export default ScreenshotBtn;