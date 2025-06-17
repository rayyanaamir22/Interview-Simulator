import React, { useEffect, useState, useRef } from 'react';

// Add type definitions for Web Speech API
declare global {
  interface Window {
    webkitSpeechRecognition: any;
  }
}

interface ClosedCaptionsProps {
  isEnabled: boolean;
  audioStream: MediaStream | null;
  onTranscript?: (text: string) => void;
}

const ClosedCaptions: React.FC<ClosedCaptionsProps> = ({ isEnabled, audioStream, onTranscript }) => {
  const [transcript, setTranscript] = useState<string>('');
  const [isTranscribing, setIsTranscribing] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const recognitionRef = useRef<any>(null);

  useEffect(() => {
    if (!isEnabled || !audioStream) {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
        recognitionRef.current = null;
      }
      setTranscript('');
      setError(null);
      return;
    }

    // Check if browser supports speech recognition
    if (!('webkitSpeechRecognition' in window)) {
      setError('Speech recognition not supported in this browser');
      return;
    }

    try {
      const SpeechRecognition = window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      const recognition = recognitionRef.current;

      recognition.continuous = true;
      recognition.interimResults = true;
      recognition.lang = 'en-US';

      recognition.onstart = () => {
        setIsTranscribing(true);
        setError(null);
      };

      recognition.onresult = (event: any) => {
        const current = event.resultIndex;
        const transcript = event.results[current][0].transcript;
        
        if (event.results[current].isFinal) {
          setTranscript(prev => {
            // Keep only the last 3 sentences for readability
            const sentences = (prev + ' ' + transcript).split(/[.!?]+/).filter(Boolean);
            return sentences.slice(-3).join('. ') + '.';
          });
        }

        // Call onTranscript with the final transcript
        if (event.results[current].isFinal && onTranscript) {
          onTranscript(transcript);
        }
      };

      recognition.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        if (event.error !== 'aborted') {
          setError(`Speech recognition error: ${event.error}`);
        }
        setIsTranscribing(false);
      };

      recognition.onend = () => {
        setIsTranscribing(false);
        // Restart recognition if it was enabled
        if (isEnabled && recognitionRef.current) {
          setTimeout(() => {
            if (isEnabled && recognitionRef.current) {
              recognitionRef.current.start();
            }
          }, 1000);
        }
      };

      recognition.start();
    } catch (e) {
      console.error('Error initializing speech recognition:', e);
      setError('Failed to initialize speech recognition');
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
        recognitionRef.current = null;
      }
    };
  }, [isEnabled, audioStream, onTranscript]);

  if (!isEnabled) return null;

  return (
    <div className="fixed bottom-24 left-0 right-0 flex justify-center">
      <div className="bg-black bg-opacity-75 text-white px-6 py-3 rounded-lg max-w-2xl text-center">
        {error ? (
          <span className="text-red-400">{error}</span>
        ) : (
          transcript || (isTranscribing ? 'Listening...' : '')
        )}
      </div>
    </div>
  );
};

export default ClosedCaptions; 