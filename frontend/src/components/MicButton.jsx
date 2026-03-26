import React, { useState, useRef, useEffect } from 'react';
import { useLanguage } from '../hooks/useLanguage';

/**
 * MicButton Component
 * Speech recognition button with multi-language support
 * Handles browser compatibility, language switching, and error states
 */
export default function MicButton({ onResult, onError, disabled, lang = 'en' }) {
  const { t, lang: contextLang } = useLanguage();
  
  // State management
  const [listening, setListening] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [interim, setInterim] = useState('');
  const [browserSupport, setBrowserSupport] = useState(true);
  
  // Refs for recognition and recognition state
  const recognitionRef = useRef(null);
  const isSuspendedRef = useRef(false);
  
  // Determine active language
  const currentLang = lang || contextLang || 'en';

  // Language to Web Speech API locale mapping
  const LANG_MAP = {
    en: 'en-IN',
    hi: 'hi-IN',
    ta: 'ta-IN',
  };

  /**
   * Get SpeechRecognition API with browser compatibility fallback
   */
  const getSpeechRecognition = () => {
    return (
      (typeof window !== 'undefined' && window.SpeechRecognition) ||
      (typeof window !== 'undefined' && window.webkitSpeechRecognition)
    );
  };

  /**
   * Initialize speech recognition with proper configuration
   */
  const initializeRecognition = () => {
    try {
      const SpeechRecognition = getSpeechRecognition();
      
      if (!SpeechRecognition) {
        setBrowserSupport(false);
        onError?.(t('voice.notSupported'));
        return null;
      }

      const recognition = new SpeechRecognition();
      
      // Configure recognition
      recognition.lang = LANG_MAP[currentLang] || 'en-IN';
      recognition.interimResults = true;
      recognition.maxAlternatives = 1;
      recognition.continuous = false;

      // Event handlers
      recognition.onstart = () => {
        setListening(true);
        setInterim('');
        console.log(`Speech recognition started for ${recognition.lang}`);
      };

      recognition.onend = () => {
        setListening(false);
        setInterim('');
        setProcessing(false);
        console.log('Speech recognition ended');
      };

      recognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        // Process results
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;

          if (event.results[i].isFinal) {
            finalTranscript += transcript + ' ';
          } else {
            interimTranscript += transcript;
          }
        }

        // Update interim state for live feedback
        setInterim(interimTranscript);

        // Callback on final result
        if (finalTranscript.trim()) {
          setProcessing(true);
          onResult?.({
            text: finalTranscript.trim(),
            language: currentLang,
            confidence: event.results[event.results.length - 1][0].confidence,
            timestamp: new Date().toISOString(),
          });
        }
      };

      recognition.onerror = (event) => {
        setListening(false);
        setInterim('');
        setProcessing(false);

        // Translate error to user message
        const errorMessage = getErrorMessage(event.error, t);
        console.error(`Speech recognition error: ${event.error}`, errorMessage);
        onError?.(errorMessage);
      };

      return recognition;
    } catch (error) {
      console.error('Error initializing recognition:', error);
      setBrowserSupport(false);
      onError?.(t('voice.unknownError'));
      return null;
    }
  };

  /**
   * Map Web Speech API errors to translation keys
   */
  const getErrorMessage = (errorType, translator) => {
    const errorMap = {
      'not-allowed': 'voice.permissionDenied',
      'no-speech': 'voice.noSpeech',
      'network': 'errors.networkError',
      'audio-capture': 'voice.microphoneError',
      'bad-grammar': 'voice.error',
      'service-not-allowed': 'voice.serviceNotAllowed',
    };

    const key = errorMap[errorType] || 'voice.unknownError';
    return translator(key);
  };

  /**
   * Start speech recognition
   */
  const startListening = () => {
    if (!browserSupport || disabled) return;

    try {
      // Stop any existing recognition
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }

      // Reinitialize for language change
      const recognition = initializeRecognition();
      if (recognition) {
        recognitionRef.current = recognition;
        isSuspendedRef.current = false;
        recognition.start();
      }
    } catch (error) {
      console.error('Error starting listening:', error);
      onError?.(t('voice.error'));
    }
  };

  /**
   * Stop speech recognition
   */
  const stopListening = () => {
    if (recognitionRef.current) {
      try {
        isSuspendedRef.current = true;
        recognitionRef.current.stop();
      } catch (error) {
        console.warn('Error stopping recognition:', error);
      }
    }
    setListening(false);
    setInterim('');
  };

  /**
   * Abort recognition (hard stop)
   */
  const abortListening = () => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.abort();
      } catch (error) {
        console.warn('Error aborting recognition:', error);
      }
    }
    setListening(false);
    setInterim('');
    setProcessing(false);
  };

  // Re-initialize when language changes
  useEffect(() => {
    if (listening) {
      stopListening();
      // Small delay before reinitializing with new language
      const timer = setTimeout(() => {
        initializeRecognition();
      }, 200);
      return () => clearTimeout(timer);
    }
  }, [currentLang]);

  // Cleanup on component unmount
  useEffect(() => {
    return () => {
      abortListening();
    };
  }, []);

  // Check browser support on mount
  useEffect(() => {
    if (!getSpeechRecognition()) {
      setBrowserSupport(false);
    }
  }, []);

  // Render nothing if not supported
  if (!browserSupport) {
    return (
      <div
        title={t('voice.notSupported')}
        style={{
          width: 80,
          height: 80,
          borderRadius: '50%',
          background: '#ccc',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'not-allowed',
          opacity: 0.5,
        }}
      >
        🎤
      </div>
    );
  }

  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      <button
        onClick={listening ? stopListening : startListening}
        disabled={disabled || processing}
        aria-label={
          listening
            ? t('voice.stopListening')
            : processing
            ? t('voice.processing')
            : t('voice.tapToSpeak')
        }
        title={
          listening
            ? t('voice.stopListening')
            : processing
            ? t('voice.processing')
            : t('voice.tapToSpeak')
        }
        style={{
          width: 80,
          height: 80,
          borderRadius: '50%',
          border: 'none',
          cursor: disabled || processing ? 'not-allowed' : 'pointer',
          background: listening
            ? 'linear-gradient(135deg, #ef4444, #dc2626)'
            : processing
            ? 'linear-gradient(135deg, #f97316, #ea580c)'
            : 'linear-gradient(135deg, #e63384, #be185d)',
          color: '#fff',
          fontSize: 32,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: listening
            ? '0 0 0 8px rgba(239,68,68,0.2), 0 8px 24px rgba(239,68,68,0.4)'
            : 'inset 0 1px 3px rgba(0,0,0,0.2), 0 4px 12px rgba(230,51,132,0.4)',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          animation: listening ? 'pulse 1s ease-in-out infinite' : 'none',
          opacity: disabled ? 0.5 : 1,
          transform: listening ? 'scale(1.05)' : processing ? 'scale(0.98)' : 'scale(1)',
        }}
      >
        {listening ? '⏹️' : processing ? '⏳' : '🎤'}
      </button>

      {/* Interim transcript indicator */}
      {interim && (
        <div
          style={{
            position: 'absolute',
            top: '100%',
            left: '50%',
            transform: 'translateX(-50%)',
            marginTop: 8,
            padding: '4px 12px',
            background: 'rgba(0,0,0,0.8)',
            color: '#fff',
            borderRadius: 4,
            fontSize: 12,
            maxWidth: 200,
            whiteSpace: 'nowrap',
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            animation: 'fadeIn 0.2s ease',
          }}
        >
          {interim}
        </div>
      )}

      <style>{`
        @keyframes pulse {
          0%, 100% {
            box-shadow: 0 0 0 8px rgba(239,68,68,0.2), 0 8px 24px rgba(239,68,68,0.4);
          }
          50% {
            box-shadow: 0 0 0 16px rgba(239,68,68,0.1), 0 8px 24px rgba(239,68,68,0.4);
          }
        }
        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: translateX(-50%) translateY(-4px);
          }
          to {
            opacity: 1;
            transform: translateX(-50%) translateY(0);
          }
        }
      `}</style>
    </div>
  );
}
