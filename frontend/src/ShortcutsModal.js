import React from 'react';

function ShortcutsModal({ show, onClose }) {
  if (!show) return null;

  const shortcuts = [
    { key: 'Ctrl + K', action: 'Focus search bar' },
    { key: 'Esc', action: 'Close this modal' },
    { key: 'Click District', action: 'View predictions' },
    { key: '🔄 Refresh', action: 'Reload all data' },
  ];

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <h3>⌨️ Keyboard Shortcuts</h3>
        <div className="shortcuts-list">
          {shortcuts.map((s, i) => (
            <div key={i} className="shortcut-row">
              <kbd>{s.key}</kbd>
              <span>{s.action}</span>
            </div>
          ))}
        </div>
        <button className="modal-close" onClick={onClose}>✕</button>
        <p className="modal-hint">Press ? to open this anytime</p>
      </div>
    </div>
  );
}

export default ShortcutsModal;