import React, { useState } from 'react';

function VoiceSearch({ onResult }) {
  const [listening, setListening] = useState(false);

  const startListening = () => {
    if (!('webkitSpeechRecognition' in window)) {
      alert('Voice search not supported in your browser. Use Chrome.');
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = 'en-IN';
    recognition.continuous = false;

    recognition.onstart = () => setListening(true);
    recognition.onend = () => setListening(false);
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      onResult(transcript);
    };

    recognition.start();
  };

  return (
    <button 
      className={`voice-btn ${listening ? 'listening' : ''}`}
      onClick={startListening}
      title="Voice Search"
    >
      {listening ? '🎙️ Listening...' : '🎤'}
    </button>
  );
}

export default VoiceSearch;