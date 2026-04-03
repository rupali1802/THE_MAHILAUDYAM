import React, { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../hooks/useLanguage';
import MicButton from '../components/MicButton';
import { predictIntent } from '../services/api';
import { speak, stop as stopSpeech } from '../utils/voiceOutput';
import { Loader2 } from 'lucide-react';

/**
 * Language-specific quick commands for voice interaction
 */
const QUICK_COMMANDS = {
  en: [
    'Record income 500 rupees',
    'Add expense 200 transport',
    'I sold 5 kg vegetables',
    'Show my profit',
    'Market price of tomato',
    'Government schemes for women',
  ],
  hi: [
    '500 rupaye ki aay record karo',
    'Kharcha 200 transport',
    'Aaj 5 kg tamatar becha',
    'Mera laabh dikhao',
    'Tamatar ka bhav batao',
    'Mahila yojanayen',
  ],
  ta: [
    '500 roopaay varumanam padhivu',
    'Selavu 200 payanam',
    '5 kg kaaikari vittren',
    'Laabham kaattu',
    'Thaakkali vilai kattu',
    'Penmani thittagal',
  ],
};

export default function VoiceAssistant() {
  const { t, lang } = useLanguage();
  const navigate = useNavigate();
  
  // State management
  const [transcript, setTranscript] = useState('');
  const [textInput, setTextInput] = useState('');
  const [response, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [history, setHistory] = useState([]);
  const [speaking, setSpeaking] = useState(false);
  
  // Refs
  const historyEndRef = useRef(null);
  const timeoutRef = useRef(null);

  // Auto-scroll to latest history item
  useEffect(() => {
    historyEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [history]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (timeoutRef.current) clearTimeout(timeoutRef.current);
      stopSpeech();
    };
  }, []);

  /**
   * Handle text input submission
   */
  const handleTextSubmit = (e) => {
    e.preventDefault();
    if (textInput.trim()) {
      processText(textInput);
      setTextInput('');
    }
  };

  /**
   * Process voice input and send to backend
   */
  const processText = async (text) => {
    if (!text.trim()) {
      setError(t('voice.emptyInput') || 'Please say something');
      return;
    }

    setTranscript(text);
    setLoading(true);
    setError('');
    setResponse('');

    try {
      console.log('🎯 Starting API call...');
      console.log('📝 Text:', text);
      console.log('🔤 Language:', lang);
      
      // Send to backend API with language
      const result = await predictIntent(text, lang);
      
      console.log('✅ API Response received:', result);
      
      if (!result?.data) {
        throw new Error('Invalid response from server');
      }

      const {
        response: responseText,
        intent,
        action,
        detected_language,
        language_name,
        language_confidence,
      } = result.data;
      
      console.log('✅ Response text:', responseText);
      console.log('✅ Intent:', intent);
      console.log('✅ Action:', action);

      // Update UI with response
      setResponse(responseText);

      // Add to history
      const historyItem = {
        id: Date.now(),
        user: text,
        ai: responseText,
        intent: intent || 'unknown',
        detected_language: detected_language || lang,
        language_name: language_name || lang,
        language_confidence: language_confidence || 0,
        timestamp: new Date().toLocaleTimeString(),
      };
      setHistory((prev) => [...prev, historyItem]);

      // Speak response in detected language
      setSpeaking(true);
      try {
        const outputLang = detected_language || lang;
        await speak(responseText, outputLang);
      } catch (speakError) {
        console.warn('Speech synthesis error:', speakError);
      } finally {
        setSpeaking(false);
      }

      // Navigate to relevant page based on intent
      if (action) {
        const actionRoutes = {
          income: '/income',
          record_income: '/income',
          expense: '/expense',
          record_expense: '/expense',
          sales: '/sales',
          record_sale: '/sales',
          profit: '/profit',
          show_profit: '/profit',
          market: '/market',
          show_market_prices: '/market',
          schemes: '/schemes',
          show_schemes: '/schemes',
          mentor: '/mentor',
          show_mentors: '/mentor',
          payment: '/payment',
          show_payment: '/payment',
        };

        const route = actionRoutes[action];
        if (route) {
          timeoutRef.current = setTimeout(() => {
            navigate(route);
          }, 2000);
        }
      }
    } catch (err) {
      console.error('❌ Error processing text:', err);
      console.error('❌ Error details:', {
        message: err.message,
        response: err.response,
        status: err.response?.status,
        data: err.response?.data,
      });
      
      let errMsg = t('errors.networkError') || 'Network Error';
      
      // Better error message extraction
      if (err.response?.data?.error) {
        errMsg = err.response.data.error;
      } else if (err.response?.data?.details) {
        errMsg = `Error: ${err.response.data.details}`;
      } else if (err.message) {
        errMsg = err.message;
      }
      
      console.error('🚨 Final error message:', errMsg);
      setError(errMsg);
      setResponse(errMsg);
    } finally {
      setLoading(false);
    }
  };

  /**
   * Handle MicButton result
   */
  const handleMicResult = (result) => {
    if (typeof result === 'string') {
      processText(result);
    } else if (result?.text) {
      processText(result.text);
    }
  };

  /**
   * Handle MicButton error
   */
  const handleMicError = (errorMsg) => {
    setError(errorMsg);
    console.error('Microphone error:', errorMsg);
  };

  /**
   * Clear current interaction
   */
  const clearCurrent = () => {
    setTranscript('');
    setResponse('');
    setError('');
  };

  return (
    <div style={{ padding: '16px', maxWidth: '1200px', margin: '0 auto', background: 'var(--bg-light)', paddingBottom: 100 }}>
      {/* Professional Header - SAKHI AI */}
      <div style={{ background: 'linear-gradient(135deg, #ff6b35 0%, #ff8c42 100%)', borderRadius: '24px', padding: '16px 24px', marginBottom: '24px', color: 'white', boxShadow: 'var(--shadow-lg)', textAlign: 'center' }}>
        <h1 style={{ margin: '0', fontSize: '24px', fontWeight: 700, letterSpacing: '0.5px' }}>{t('voice.assistant')}</h1>
      </div>

      {/* Subtitle */}
      <div style={{ textAlign: 'center', marginBottom: '24px', color: 'var(--gray-700)' }}>
        <p style={{ fontSize: 'var(--font-base)', margin: '0', fontWeight: 500 }}>{t('voice.speakingSubtitle')}</p>
      </div>

      {/* Text Input Option */}
      <div className="card card-interactive" style={{ animation: 'slideUp 0.25s ease', marginBottom: '24px' }}>
        <div className="card-body">
          <form onSubmit={handleTextSubmit}>
            <div style={{ display: 'flex', gap: '8px', alignItems: 'flex-start' }}>
              <div style={{ flex: 1 }}>
                <label style={{
                  display: 'block',
                  fontSize: 'var(--font-sm)',
                  fontWeight: 600,
                  marginBottom: '8px',
                  color: 'var(--gray-900)'
                }}>
                  📝 {t('voice.tapToSpeak') || 'Type or Say'}
                </label>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <input
                    type="text"
                    value={textInput}
                    onChange={(e) => setTextInput(e.target.value)}
                    placeholder={
                      {
                        en: "Type your command... e.g., 'Record income 500'",
                        hi: "अपनी आज्ञा दें... उदा. '500 की आय रिकॉर्ड करो'",
                        ta: "உங்கள் கட்டளை வகை செய்யவும்... எ.கா., '500 வருமானம் பதிவு செய்'",
                      }[lang] || "Type your command..."
                    }
                    style={{
                      flex: 1,
                      padding: '12px 14px',
                      borderRadius: 'var(--radius-md)',
                      border: '2px solid var(--primary-200)',
                      fontSize: 'var(--font-base)',
                      fontFamily: 'inherit',
                      transition: 'all 0.2s ease',
                      outline: 'none',
                    }}
                    onFocus={(e) => {
                      e.target.style.borderColor = 'var(--primary)';
                      e.target.style.boxShadow = '0 0 0 3px rgba(147, 51, 234, 0.1)';
                    }}
                    onBlur={(e) => {
                      e.target.style.borderColor = 'var(--primary-200)';
                      e.target.style.boxShadow = 'none';
                    }}
                    disabled={loading || speaking}
                  />
                  <button
                    type="submit"
                    disabled={loading || speaking || !textInput.trim()}
                    style={{
                      padding: '12px 20px',
                      background: 'linear-gradient(135deg, var(--primary), var(--primary-dark))',
                      color: 'white',
                      border: 'none',
                      borderRadius: 'var(--radius-md)',
                      fontWeight: 700,
                      cursor: loading || speaking ? 'not-allowed' : 'pointer',
                      opacity: loading || speaking || !textInput.trim() ? 0.5 : 1,
                      transition: 'all 0.2s ease',
                      fontSize: 'var(--font-sm)',
                      whiteSpace: 'nowrap',
                    }}
                    onMouseEnter={(e) => {
                      if (!loading && !speaking && textInput.trim()) {
                        e.target.style.transform = 'translateY(-2px)';
                        e.target.style.boxShadow = '0 8px 16px rgba(147, 51, 234, 0.3)';
                      }
                    }}
                    onMouseLeave={(e) => {
                      e.target.style.transform = 'translateY(0)';
                      e.target.style.boxShadow = 'none';
                    }}
                  >
                    {loading ? '⏳' : '✓ Send'}
                  </button>
                </div>
              </div>
            </div>
          </form>
        </div>
      </div>

      {/* Main Voice Card with Microphone */}
      <div className="card card-interactive" style={{ animation: 'slideUp 0.3s ease', marginBottom: '24px' }}>
        <div style={{
          background: 'linear-gradient(135deg, rgba(147, 51, 234, 0.1) 0%, rgba(124, 58, 237, 0.1) 100%)',
          padding: '32px',
          borderRadius: 'var(--radius-lg)',
          textAlign: 'center',
          border: '2px solid rgba(147, 51, 234, 0.1)',
        }}>
          <MicButton
            onResult={handleMicResult}
            onError={handleMicError}
            disabled={loading || speaking}
            lang={lang}
          />
          <p style={{ fontSize: 'var(--font-base)', opacity: 0.85, margin: '12px 0 0', color: 'var(--gray-700)', fontWeight: 600 }}>
            {loading
              ? t('voice.processing')
              : speaking
              ? t('voice.speaking')
              : t('voice.tapToSpeak')}
          </p>
        </div>
      </div>

      {/* Current Interaction */}
      {(error || transcript || response) && (
        <div className="card card-interactive" style={{ animation: 'slideUp 0.35s ease', marginBottom: '24px' }}>
          <div className="card-body">
            {error && (
              <div style={{
                background: '#fef2f2',
                border: '1px solid #fecaca',
                borderRadius: 'var(--radius-md)',
                padding: '12px',
                marginBottom: '12px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}>
                <span style={{ color: 'var(--danger)', fontSize: 'var(--font-sm)' }}>⚠️ {error}</span>
                <button
                  onClick={() => setError('')}
                  style={{
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    fontSize: '16px',
                    color: 'var(--danger)',
                  }}
                >
                  ✕
                </button>
              </div>
            )}

            {transcript && (
              <div style={{ marginBottom: '12px' }}>
                <p style={{ margin: '0 0 6px', fontSize: 'var(--font-sm)', fontWeight: 600, color: 'var(--gray-900)', textTransform: 'uppercase' }}>
                  {t('voice.youSaid')}
                </p>
                <p style={{
                  background: 'var(--primary-50)',
                  borderRadius: 'var(--radius-md)',
                  padding: '10px 14px',
                  fontSize: 'var(--font-base)',
                  color: 'var(--primary)',
                  fontStyle: 'italic',
                  border: '1px solid var(--primary-100)',
                  margin: 0
                }}>
                  "{transcript}"
                </p>
              </div>
            )}

            {loading && (
              <div style={{ display: 'flex', gap: 8, alignItems: 'center', color: 'var(--primary)', fontSize: 'var(--font-base)', margin: '12px 0' }}>
                <Loader2 size={18} className="animate-spin" />
                {t('voice.processing')}
              </div>
            )}

            {response && !loading && (
              <div>
                <p style={{ margin: '0 0 6px', fontSize: 'var(--font-sm)', fontWeight: 600, color: 'var(--gray-900)', textTransform: 'uppercase' }}>
                  {t('voice.aiResponse')}
                </p>
                <p style={{ margin: '0', fontSize: 'var(--font-base)', color: 'var(--gray-900)', lineHeight: '1.6' }}>
                  {response}
                </p>
              </div>
            )}

            {transcript && response && (
              <button
                onClick={clearCurrent}
                className="btn btn-text"
                style={{ marginTop: '12px', fontSize: 'var(--font-sm)' }}
              >
                {t('action.clear')} ✕
              </button>
            )}
          </div>
        </div>
      )}

      {/* Quick Commands */}
      <div className="card card-interactive" style={{ animation: 'slideUp 0.4s ease', marginBottom: '24px' }}>
        <div className="card-header">
          <span style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--primary)' }}>
            <h2 style={{ margin: '0', fontSize: 'var(--font-base)', fontWeight: 700 }}>{t('voice.quickCommands')}</h2>
          </span>
        </div>
        <div className="card-body">
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '10px' }}>
            {(QUICK_COMMANDS[lang] || QUICK_COMMANDS.en).map((cmd, i) => (
              <button
                key={i}
                onClick={() => processText(cmd)}
                disabled={loading}
                className="btn btn-secondary"
                style={{
                  fontSize: 'var(--font-sm)',
                  padding: '10px 16px',
                  minHeight: '40px',
                  opacity: loading ? 0.5 : 1,
                  cursor: loading ? 'not-allowed' : 'pointer',
                  transition: 'all 0.3s ease',
                }}
                onMouseEnter={(e) => !loading && (e.target.style.transform = 'translateY(-2px)', e.target.style.boxShadow = 'var(--shadow-md)')}
                onMouseLeave={(e) => (e.target.style.transform = 'translateY(0)', e.target.style.boxShadow = 'var(--shadow-sm)')}
              >
                {cmd}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Conversation History */}
      {history.length > 0 && (
        <div className="card card-interactive" style={{ animation: 'slideUp 0.45s ease' }}>
          <div className="card-header">
            <span style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--primary)' }}>
              <h2 style={{ margin: '0', fontSize: 'var(--font-base)', fontWeight: 700 }}>{t('voice.history')}</h2>
            </span>
          </div>
          <div className="card-body">
            <div style={{ display: 'grid', gap: '12px' }}>
              {history
                .slice(-10)
                .reverse()
                .map((h, idx) => (
                  <div 
                    key={h.id}
                    style={{
                      background: 'var(--bg-ultra-light)',
                      borderRadius: 'var(--radius-md)',
                      padding: '12px',
                      borderLeft: '3px solid var(--primary)',
                      animation: `slideUp ${0.3 + idx * 0.05}s ease`
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                      <span style={{
                        fontSize: 'var(--font-xs)',
                        background: 'var(--primary-50)',
                        color: 'var(--primary)',
                        padding: '2px 8px',
                        borderRadius: 'var(--radius-full)',
                        fontWeight: 600,
                        textTransform: 'uppercase',
                      }}>
                        {h.intent}
                      </span>
                      <span style={{ fontSize: 'var(--font-xs)', color: 'var(--gray-500)' }}>{h.timestamp}</span>
                    </div>
                    <div style={{ fontSize: 'var(--font-sm)', color: 'var(--gray-600)', fontStyle: 'italic', marginBottom: '4px' }}>
                      {t('voice.youSaid')}: "{h.user}"
                    </div>
                    <div style={{ fontSize: 'var(--font-sm)', color: 'var(--gray-900)' }}>
                      <strong>{t('voice.aiResponse')}:</strong> {h.ai}
                    </div>
                  </div>
                ))}
            </div>
          </div>
        </div>
      )}

      {/* Empty State */}
      {history.length === 0 && !transcript && (
        <div
          style={{
            textAlign: 'center',
            padding: '60px 20px',
            color: 'var(--gray-500)',
          }}
        >
          <div style={{ fontSize: '48px', marginBottom: 12 }}>🎤</div>
          <p style={{ fontSize: 'var(--font-base)', margin: '0' }}>{t('voice.noHistory')}</p>
        </div>
      )}

      <div ref={historyEndRef} />
    </div>
  );
}
