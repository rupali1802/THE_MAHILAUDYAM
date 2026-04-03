import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../hooks/useLanguage';
import { getDeviceId } from '../utils/device';
import { getMentors, getMentorChats, sendMentorMessage } from '../services/api';
import { Users, MessageCircle, Send, ArrowLeft, Star, Briefcase, Loader2, MapPin, Mic, MicOff, Volume2, VolumeX } from 'lucide-react';
import '../styles/Mentor.css';

const SAMPLE_MENTORS = [
  { id: 1, name: 'Priya Subramaniam', specializationKey: 'organic', expertiseKey: 'handicraft', experience_years: 12, rating: 4.8, availability: 'available', languages_spoken: 'Tamil, English', bioKey: 'priya' },
  { id: 2, name: 'Meena Krishnan', specializationKey: 'dairy', expertiseKey: 'dairy', experience_years: 8, rating: 4.5, availability: 'available', languages_spoken: 'Tamil, Hindi', bioKey: 'meena' },
  { id: 3, name: 'Savita Patel', specializationKey: 'food', expertiseKey: 'foodProcessing', experience_years: 15, rating: 4.9, availability: 'available', languages_spoken: 'Hindi, English', bioKey: 'savita' },
  { id: 4, name: 'Lakshmi Rajan', specializationKey: 'digital', expertiseKey: 'digitalMarketing', experience_years: 6, rating: 4.6, availability: 'busy', languages_spoken: 'Tamil, English', bioKey: 'lakshmi' },
];

// Voice recognition setup
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const speech = window.speechSynthesis;

export default function Mentor() {
  const { t, language } = useLanguage();
  const [mentors, setMentors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);
  const [useAIMentor, setUseAIMentor] = useState(false);
  const [chats, setChats] = useState([]);
  const [aiChats, setAiChats] = useState([]);
  const [message, setMessage] = useState('');
  const [aiMessage, setAiMessage] = useState('');
  const [sending, setSending] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isAiListening, setIsAiListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const recognitionRef = useRef(null);
  const aiRecognitionRef = useRef(null);
  const messagesEndRef = useRef(null);
  const aiMessagesEndRef = useRef(null);

  useEffect(() => {
    getMentors(language)
      .then(r => setMentors(r.data.results?.length ? r.data.results : SAMPLE_MENTORS))
      .catch(() => setMentors(SAMPLE_MENTORS))
      .finally(() => setLoading(false));
  }, [language]);

  // Auto-scroll to latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chats]);

  const openChat = (mentor) => {
    setSelected(mentor);
    setChats([]);
    getMentorChats(mentor.id, language, getDeviceId())
      .then(r => setChats(r.data.results || []))
      .catch(() => setChats([]));
    
    // Auto-speak greeting in user's preferred language
    setTimeout(() => {
      const greeting = t('mentor.greeting') || t('mentor.greeting');
      speakText(greeting);
    }, 500);
  };

  const handleSend = async () => {
    if (!message.trim() || !selected || sending) return;
    
    const userMessage = message;
    setMessage('');
    setSending(true);
    
    // Ensure listening is stopped
    if (isListening) {
      stopListening();
    }

    try {
      // Send to backend which will get AI response
      const response = await sendMentorMessage({
        device_id: getDeviceId(),
        mentor_id: selected.id,
        message: userMessage,
        message_type: 'query',
        language: language,
      });

      // Add both user message and mentor response
      if (response.data.user_message) {
        setChats(prev => [...prev, response.data.user_message]);
      }
      if (response.data.mentor_response) {
        setChats(prev => [...prev, response.data.mentor_response]);
        
        // Auto-speak mentor response after a short delay
        if (response.data.mentor_response.message) {
          setTimeout(() => {
            speakText(response.data.mentor_response.message);
          }, 300);
        }
      }
    } catch (error) {
      console.error('Error sending message:', error);
      // Add user message anyway for feedback
      const userMsg = {
        id: Date.now(),
        message: userMessage,
        message_type: 'query',
        timestamp: new Date().toISOString()
      };
      setChats(prev => [...prev, userMsg]);
      
      // Add error response
      const errorMsg = {
        id: Date.now() + 1,
        message: t('mentor.errorResponse') || 'Sorry, I could not process your message. Please try again.',
        message_type: 'response',
        timestamp: new Date().toISOString()
      };
      setChats(prev => [...prev, errorMsg]);
    } finally {
      setSending(false);
    }
  };

  const startListening = () => {
    if (!SpeechRecognition) {
      alert('Speech Recognition not supported in your browser');
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognitionRef.current = recognition;
      recognition.lang = language === 'hi' ? 'hi-IN' : language === 'ta' ? 'ta-IN' : 'en-US';
      recognition.interimResults = true;
      recognition.continuous = false;

      recognition.onstart = () => {
        console.log('🎤 Voice recognition started');
        setIsListening(true);
      };

      recognition.onend = () => {
        console.log('🎤 Voice recognition ended');
        setIsListening(false);
      };

      recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }
        if (event.isFinal) {
          console.log('✅ Final transcript:', transcript);
          const finalText = transcript.trim();
          setMessage(finalText);
          setIsListening(false);
          // Voice capture complete - user can review and send
          console.log('🎤 Voice input captured, ready to send');
        } else {
          // Show interim results while speaking
          setMessage(transcript);
        }
      };

      recognition.onerror = (event) => {
        console.error('❌ Speech recognition error:', event.error);
        setIsListening(false);
      };

      recognition.start();
    } catch (error) {
      console.error('Error starting speech recognition:', error);
      setIsListening(false);
    }
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.abort();
        setIsListening(false);
      } catch (error) {
        console.error('Error stopping speech recognition:', error);
        setIsListening(false);
      }
    }
  };

  const speakText = (text) => {
    if (!speech) return;

    // Cancel any ongoing speech
    speech.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = language === 'hi' ? 'hi-IN' : language === 'ta' ? 'ta-IN' : 'en-US';
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 1;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = (event) => {
      console.error('Speech synthesis error:', event.error);
      setIsSpeaking(false);
    };

    speech.speak(utterance);
  };

  const stopSpeaking = () => {
    speech.cancel();
    setIsSpeaking(false);
  };

  // AI Mentor Functions
  const startAiListening = () => {
    if (!SpeechRecognition) {
      alert('Speech Recognition not supported in your browser');
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      aiRecognitionRef.current = recognition;
      recognition.lang = language === 'hi' ? 'hi-IN' : language === 'ta' ? 'ta-IN' : 'en-US';
      recognition.interimResults = true;
      recognition.continuous = false;

      recognition.onstart = () => {
        console.log('🎤 AI Mentor voice recognition started');
        setIsAiListening(true);
      };

      recognition.onend = () => {
        console.log('🎤 AI Mentor voice recognition ended');
        setIsAiListening(false);
      };

      recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }
        if (event.isFinal) {
          console.log('✅ Final transcript:', transcript);
          const finalText = transcript.trim();
          setAiMessage(finalText);
          setIsAiListening(false);
        } else {
          setAiMessage(transcript);
        }
      };

      recognition.onerror = (event) => {
        console.error('❌ Speech recognition error:', event.error);
        setIsAiListening(false);
      };

      recognition.start();
    } catch (error) {
      console.error('Error starting speech recognition:', error);
      setIsAiListening(false);
    }
  };

  const stopAiListening = () => {
    if (aiRecognitionRef.current) {
      try {
        aiRecognitionRef.current.abort();
        setIsAiListening(false);
      } catch (error) {
        console.error('Error stopping speech recognition:', error);
        setIsAiListening(false);
      }
    }
  };

  const handleAiSend = async () => {
    if (!aiMessage.trim() || sending) return;
    
    const userMessage = aiMessage;
    setAiMessage('');
    setSending(true);
    
    if (isAiListening) {
      stopAiListening();
    }

    try {
      // Send to backend for Mentor AI response
      const response = await fetch(`${process.env.REACT_APP_API_URL || 'http://localhost:8000/api'}/mentor-ai/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: userMessage,
          language: language,
          device_id: getDeviceId()
        })
      });

      if (!response.ok) {
        throw new Error('Failed to get mentor AI response');
      }

      const data = await response.json();

      // Add user message
      const userMsg = {
        id: Date.now(),
        message: userMessage,
        message_type: 'query',
        timestamp: new Date().toISOString()
      };
      setAiChats(prev => [...prev, userMsg]);

      // Add AI response
      const aiResponse = {
        id: Date.now() + 1,
        message: data.response || data.message || 'I am not sure about this information.',
        message_type: 'response',
        timestamp: new Date().toISOString()
      };
      setAiChats(prev => [...prev, aiResponse]);

      // Auto-speak mentor response
      if (data.response || data.message) {
        setTimeout(() => {
          speakText(data.response || data.message);
        }, 300);
      }
    } catch (error) {
      console.error('Error sending message to Mentor AI:', error);
      
      // Add user message
      const userMsg = {
        id: Date.now(),
        message: userMessage,
        message_type: 'query',
        timestamp: new Date().toISOString()
      };
      setAiChats(prev => [...prev, userMsg]);

      // Add error response
      const errorMsg = {
        id: Date.now() + 1,
        message: 'Sorry, I could not process your message. Please try again.',
        message_type: 'response',
        timestamp: new Date().toISOString()
      };
      setAiChats(prev => [...prev, errorMsg]);
    } finally {
      setSending(false);
    }
  };

  // Auto-scroll AI messages
  useEffect(() => {
    aiMessagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [aiChats]);

  if (useAIMentor) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', background: 'var(--bg-light)' }}>
        {/* AI Mentor Chat Header */}
        <div style={{ background: 'linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%)', color: 'white', padding: '16px', display: 'flex', alignItems: 'center', gap: '12px', boxShadow: 'var(--shadow-md)' }}>
          <button
            onClick={() => setUseAIMentor(false)}
            className="btn btn-text"
            style={{ color: 'white', padding: '8px', minHeight: 'auto' }}
          >
            <ArrowLeft size={24} />
          </button>
          <div style={{ background: 'rgba(255,255,255,0.2)', padding: '10px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Briefcase size={20} />
          </div>
          <div style={{ flex: 1 }}>
            <h3 style={{ margin: '0', fontSize: 'var(--font-lg)', fontWeight: 700 }}>🤖 Mentor AI</h3>
            <p style={{ margin: '4px 0 0', fontSize: 'var(--font-sm)', opacity: 0.9 }}>Business Mentor & Guidance Assistant</p>
          </div>
        </div>

        {/* AI Messages */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {aiChats.length === 0 ? (
            <div style={{ background: 'white', padding: '20px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--gray-200)', maxWidth: '85%', alignSelf: 'flex-start' }}>
              <p style={{ margin: '0', fontSize: 'var(--font-base)', color: 'var(--gray-900)', lineHeight: '1.6', fontWeight: 500 }}>
                👋 Hello! I'm your personal business mentor. 
              </p>
              <p style={{ margin: '12px 0 0', fontSize: 'var(--font-sm)', color: 'var(--gray-700)', lineHeight: '1.5' }}>
                I can help you with:
                <br/>✅ Business ideas and planning
                <br/>✅ Marketing strategies
                <br/>✅ Financial management
                <br/>✅ Government schemes and loans
                <br/>✅ Pricing and growth strategies
                <br/><br/>Ask me anything about your business!
              </p>
            </div>
          ) : (
            aiChats.map(c => (
              <div 
                key={c.id}
                style={{ 
                  alignSelf: c.message_type === 'query' ? 'flex-end' : 'flex-start',
                  maxWidth: '85%',
                  animation: 'fadeIn 0.3s ease'
                }}
              >
                <div style={{ 
                  background: c.message_type === 'query' ? '#8b5cf6' : 'white',
                  color: c.message_type === 'query' ? 'white' : 'var(--gray-900)',
                  padding: '12px 16px',
                  borderRadius: 'var(--radius-lg)',
                  border: c.message_type === 'query' ? 'none' : '1px solid var(--gray-200)',
                  boxShadow: c.message_type === 'query' ? 'var(--shadow-sm)' : 'none'
                }}>
                  <p style={{ margin: '0', fontSize: 'var(--font-base)', lineHeight: '1.5', whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>{c.message}</p>
                  {c.message_type === 'response' && (
                    <button
                      onClick={() => speakText(c.message)}
                      style={{
                        background: 'rgba(139, 92, 246, 0.1)',
                        border: '1px solid rgba(139, 92, 246, 0.3)',
                        color: '#8b5cf6',
                        padding: '4px 8px',
                        borderRadius: 'var(--radius-sm)',
                        fontSize: 'var(--font-xs)',
                        cursor: 'pointer',
                        marginTop: '8px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px'
                      }}
                      title="Listen to response"
                    >
                      <Volume2 size={14} /> 🔊 Listen
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
          {sending && (
            <div style={{ alignSelf: 'flex-start', maxWidth: '85%' }}>
              <div style={{ background: '#f3f4f6', padding: '12px 16px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--gray-200)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Loader2 size={16} className="animate-spin" style={{ color: '#8b5cf6' }} />
                <span style={{ color: 'var(--gray-600)', fontSize: 'var(--font-sm)' }}>Mentor thinking...</span>
              </div>
            </div>
          )}
          <div ref={aiMessagesEndRef} />
        </div>

        {/* AI Message Input - Fixed at Bottom */}
        <div style={{ background: 'white', padding: '16px', borderTop: '2px solid #8b5cf6', display: 'flex', gap: '10px', alignItems: 'flex-end', flexWrap: 'wrap', boxShadow: '0 -4px 12px rgba(0,0,0,0.1)' }}>
          {isAiListening && (
            <div style={{ width: '100%', padding: '12px', background: '#fef3c7', border: '2px solid #fbbf24', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Mic size={18} style={{ color: '#d97706', animation: 'pulse 1.5s infinite' }} />
                <span style={{ color: '#92400e', fontWeight: '600' }}>Listening...</span>
              </div>
            </div>
          )}
          
          <input
            className="form-input"
            placeholder={isAiListening ? 'Listening...' : 'Ask your business question...'}
            value={aiMessage}
            onChange={e => setAiMessage(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && !sending && !isAiListening && handleAiSend()}
            style={{ 
              flex: 1, 
              minHeight: '48px', 
              minWidth: '250px',
              padding: '12px 16px',
              fontSize: '16px',
              border: isAiListening ? '2px solid #fbbf24' : '2px solid #e5e7eb',
              borderRadius: '8px',
              fontFamily: 'inherit',
              background: isAiListening ? '#fffbeb' : 'white'
            }}
            disabled={sending || isAiListening}
          />
          
          {/* Mic Button - Voice Input for AI Mentor */}
          <button
            onClick={isAiListening ? stopAiListening : startAiListening}
            className="btn"
            style={{
              background: isAiListening ? '#ef4444' : '#8b5cf6',
              color: 'white',
              minHeight: '48px',
              minWidth: '48px',
              padding: '12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px',
              borderRadius: '8px',
              border: 'none',
              cursor: 'pointer',
              fontWeight: '600',
              transition: 'all 0.3s ease',
              boxShadow: isAiListening ? '0 0 12px rgba(239, 68, 68, 0.5)' : 'none'
            }}
            title={isAiListening ? 'Stop listening' : 'Voice input'}
          >
            {isAiListening ? <MicOff size={22} /> : <Mic size={22} />}
          </button>

          {/* Send Button for AI Mentor */}
          <button 
            onClick={handleAiSend}
            disabled={sending || !aiMessage.trim() || isAiListening}
            className="btn btn-secondary"
            style={{ 
              minHeight: '48px', 
              minWidth: '48px',
              padding: '12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              background: (!sending && aiMessage.trim() && !isAiListening) ? '#8b5cf6' : '#d1d5db',
              color: 'white',
              borderRadius: '8px',
              border: 'none',
              cursor: (!sending && aiMessage.trim() && !isAiListening) ? 'pointer' : 'not-allowed',
              transition: 'all 0.3s ease'
            }}
            title="Send message"
          >
            {sending ? <Loader2 size={22} className="animate-spin" /> : <Send size={22} />}
          </button>

          {/* Voice Output Control - Stop Speaking */}
          {isSpeaking && (
            <button
              onClick={stopSpeaking}
              style={{
                background: '#f97316',
                color: 'white',
                minHeight: '48px',
                padding: '12px 16px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '6px',
                borderRadius: '8px',
                border: 'none',
                cursor: 'pointer',
                fontWeight: '600',
                transition: 'all 0.3s ease'
              }}
              title="Stop speaking"
            >
              <VolumeX size={22} /> Cancel
            </button>
          )}
        </div>
      </div>
    );
  }

  if (selected) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', background: 'var(--bg-light)' }}>
        {/* Chat Header */}
        <div style={{ background: 'linear-gradient(135deg, var(--secondary) 0%, #0891b2 100%)', color: 'white', padding: '16px', display: 'flex', alignItems: 'center', gap: '12px', boxShadow: 'var(--shadow-md)' }}>
          <button
            onClick={() => setSelected(null)}
            className="btn btn-text"
            style={{ color: 'white', padding: '8px', minHeight: 'auto' }}
          >
            <ArrowLeft size={24} />
          </button>
          <div style={{ background: 'rgba(255,255,255,0.2)', padding: '10px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Users size={20} />
          </div>
          <div style={{ flex: 1 }}>
            <h3 style={{ margin: '0', fontSize: 'var(--font-lg)', fontWeight: 700 }}>{selected.name}</h3>
            <p style={{ margin: '4px 0 0', fontSize: 'var(--font-sm)', opacity: 0.9 }}>🤖 {t('mentor.connect_desc')}</p>
          </div>
        </div>

        {/* Messages */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          {chats.length === 0 ? (
            <div style={{ background: 'white', padding: '16px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--gray-200)', maxWidth: '80%', alignSelf: 'flex-start' }}>
              <p style={{ margin: '0', fontSize: 'var(--font-base)', color: 'var(--gray-900)', lineHeight: '1.6' }}>
                👋 {t('mentor.greeting')}
              </p>
            </div>
          ) : (
            chats.map(c => (
              <div 
                key={c.id}
                style={{ 
                  alignSelf: c.message_type === 'query' ? 'flex-end' : 'flex-start',
                  maxWidth: '80%',
                  animation: 'fadeIn 0.3s ease'
                }}
              >
                <div style={{ 
                  background: c.message_type === 'query' ? 'var(--secondary)' : 'white',
                  color: c.message_type === 'query' ? 'white' : 'var(--gray-900)',
                  padding: '12px 16px',
                  borderRadius: 'var(--radius-lg)',
                  border: c.message_type === 'query' ? 'none' : '1px solid var(--gray-200)',
                  boxShadow: c.message_type === 'query' ? 'var(--shadow-sm)' : 'none'
                }}>
                  <p style={{ margin: '0', fontSize: 'var(--font-base)', lineHeight: '1.5' }}>{c.message}</p>
                  {c.message_type === 'response' && (
                    <button
                      onClick={() => speakText(c.message)}
                      style={{
                        background: 'rgba(6, 182, 212, 0.1)',
                        border: '1px solid rgba(6, 182, 212, 0.3)',
                        color: '#06b6d4',
                        padding: '4px 8px',
                        borderRadius: 'var(--radius-sm)',
                        fontSize: 'var(--font-xs)',
                        cursor: 'pointer',
                        marginTop: '8px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px'
                      }}
                      title={t('dashboard.tapToSpeak')}
                    >
                      <Volume2 size={14} /> {t('voice.speaking')}
                    </button>
                  )}
                </div>
              </div>
            ))
          )}
          {sending && (
            <div style={{ alignSelf: 'flex-start', maxWidth: '80%' }}>
              <div style={{ background: '#f3f4f6', padding: '12px 16px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--gray-200)', display: 'flex', alignItems: 'center', gap: '8px' }}>
                <Loader2 size={16} className="animate-spin" style={{ color: '#06b6d4' }} />
                <span style={{ color: 'var(--gray-600)', fontSize: 'var(--font-sm)' }}>Mentor is thinking...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Message Input - Fixed at Bottom */}
        <div style={{ background: 'white', padding: '16px', borderTop: '2px solid #06b6d4', display: 'flex', gap: '10px', alignItems: 'flex-end', flexWrap: 'wrap', boxShadow: '0 -4px 12px rgba(0,0,0,0.1)' }}>
          {isListening && (
            <div style={{ width: '100%', padding: '12px', background: '#fef3c7', border: '2px solid #fbbf24', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '10px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Mic size={18} style={{ color: '#d97706', animation: 'pulse 1.5s infinite' }} />
                <span style={{ color: '#92400e', fontWeight: '600' }}>{t('voice.listening')}</span>
              </div>
            </div>
          )}
          
          <input
            className="form-input"
            placeholder={isListening ? t('voice.listening') + '...' : t('mentor.messagePlaceholder')}
            value={message}
            onChange={e => setMessage(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && !sending && !isListening && handleSend()}
            style={{ 
              flex: 1, 
              minHeight: '48px', 
              minWidth: '250px',
              padding: '12px 16px',
              fontSize: '16px',
              border: isListening ? '2px solid #fbbf24' : '2px solid #e5e7eb',
              borderRadius: '8px',
              fontFamily: 'inherit',
              background: isListening ? '#fffbeb' : 'white'
            }}
            disabled={sending || isListening}
          />
          
          {/* Mic Button - Voice Input */}
          <button
            onClick={isListening ? stopListening : startListening}
            className="btn"
            style={{
              background: isListening ? '#ef4444' : '#06b6d4',
              color: 'white',
              minHeight: '48px',
              minWidth: '48px',
              padding: '12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px',
              borderRadius: '8px',
              border: 'none',
              cursor: 'pointer',
              fontWeight: '600',
              transition: 'all 0.3s ease',
              boxShadow: isListening ? '0 0 12px rgba(239, 68, 68, 0.5)' : 'none'
            }}
            title={isListening ? t('voice.listening') : t('mentor.sendMessage')}
          >
            {isListening ? <MicOff size={22} /> : <Mic size={22} />}
          </button>

          {/* Send Button */}
          <button 
            onClick={handleSend}
            disabled={sending || !message.trim() || isListening}
            className="btn btn-secondary"
            style={{ 
              minHeight: '48px', 
              minWidth: '48px',
              padding: '12px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              background: (!sending && message.trim() && !isListening) ? '#06b6d4' : '#d1d5db',
              color: 'white',
              borderRadius: '8px',
              border: 'none',
              cursor: (!sending && message.trim() && !isListening) ? 'pointer' : 'not-allowed',
              transition: 'all 0.3s ease'
            }}
            title={t('mentor.send')}
          >
            {sending ? <Loader2 size={22} className="animate-spin" /> : <Send size={22} />}
          </button>

          {/* Voice Output Control - Stop Speaking */}
          {isSpeaking && (
            <button
              onClick={stopSpeaking}
              style={{
                background: '#f97316',
                color: 'white',
                minHeight: '48px',
                padding: '12px 16px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '6px',
                borderRadius: '8px',
                border: 'none',
                cursor: 'pointer',
                fontWeight: '600',
                transition: 'all 0.3s ease'
              }}
              title={t('common.cancel')}
            >
              <VolumeX size={22} /> {t('common.cancel')}
            </button>
          )}
        </div>
      </div>
    );
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(180deg, var(--bg-light) 0%, var(--white) 100%)', 
      padding: '20px',
      paddingBottom: '100px'
    }}>
      {/* Header */}
      <div style={{ 
        background: 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)',
        borderRadius: 'var(--radius-lg)', 
        padding: '24px', 
        marginBottom: '24px', 
        color: 'white', 
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.15)',
        backdropFilter: 'blur(10px)',
        border: '1px solid rgba(255, 255, 255, 0.2)'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ width: '60px', height: '60px', background: 'rgba(255,255,255,0.2)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', backdropFilter: 'blur(10px)', border: '1px solid rgba(255,255,255,0.3)' }}>
              <Briefcase size={28} />
            </div>
            <div>
              <h1 style={{ fontSize: 'var(--font-2xl)', fontWeight: 'var(--font-bold)', margin: '0', lineHeight: '1.2' }}>{t('mentor.title')}</h1>
              <p style={{ fontSize: 'var(--font-base)', opacity: '0.9', margin: '4px 0 0 0' }}>
                🤖 AI-Powered Personal Business Mentors
              </p>
            </div>
          </div>
        </div>
        
        {/* Total Card */}
        <div style={{ background: 'rgba(255,255,255,0.1)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '14px', padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <span style={{ fontSize: 'var(--font-xs)', opacity: '0.9', textTransform: 'uppercase', letterSpacing: '0.5px' }}>{t('mentor.connect_desc')}</span>
            <div style={{ fontSize: '24px', fontWeight: 'var(--font-bold)', marginTop: '4px' }}>{mentors.filter(m => m.availability === 'available').length} {t('mentor.available')}</div>
          </div>
        </div>
      </div>

      {/* List */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '48px 16px' }}>
          <Loader2 size={32} className="animate-spin" style={{ margin: '0 auto', color: '#06b6d4' }} />
          <p style={{ marginTop: '16px', color: 'var(--gray-600)', fontSize: 'var(--font-base)' }}>{t('common.loading')}</p>
        </div>
      ) : (
        <div>
          {/* AI Mentor Card */}
          <div
            onClick={() => {
              setUseAIMentor(true);
              setAiChats([]);
            }}
            style={{
              background: 'linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%)',
              borderRadius: 'var(--radius-lg)',
              padding: '20px',
              marginBottom: '24px',
              color: 'white',
              cursor: 'pointer',
              boxShadow: '0 8px 32px rgba(139, 92, 246, 0.3)',
              border: '2px solid rgba(139, 92, 246, 0.5)',
              transition: 'all 0.3s ease',
              transform: 'translateY(0)'
            }}
            onMouseOver={e => {
              e.currentTarget.style.transform = 'translateY(-4px)';
              e.currentTarget.style.boxShadow = '0 12px 40px rgba(139, 92, 246, 0.4)';
            }}
            onMouseOut={e => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 8px 32px rgba(139, 92, 246, 0.3)';
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '16px' }}>
              <div style={{ fontSize: '32px' }}>🤖</div>
              <div>
                <h3 style={{ margin: '0', fontSize: 'var(--font-lg)', fontWeight: 700 }}>Mentor AI</h3>
                <p style={{ margin: '4px 0 0', fontSize: 'var(--font-sm)', opacity: 0.9 }}>24/7 Business Guidance</p>
              </div>
            </div>
            <p style={{ margin: '0 0 12px', fontSize: 'var(--font-sm)', lineHeight: '1.6', opacity: 0.95 }}>
              Get instant business advice • Marketing strategies • Financial guidance • Scheme information • Problem solving
            </p>
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              <span style={{ background: 'rgba(255,255,255,0.2)', padding: '4px 12px', borderRadius: '12px', fontSize: 'var(--font-xs)', fontWeight: 600 }}>Always Available</span>
              <span style={{ background: 'rgba(255,255,255,0.2)', padding: '4px 12px', borderRadius: '12px', fontSize: 'var(--font-xs)', fontWeight: 600 }}>All Languages</span>
              <span style={{ background: 'rgba(255,255,255,0.2)', padding: '4px 12px', borderRadius: '12px', fontSize: 'var(--font-xs)', fontWeight: 600 }}>Voice & Text</span>
            </div>
          </div>

          {/* Human Mentors */}
          <div>
            <h2 style={{ margin: '0 0 20px', fontSize: 'var(--font-xl)', fontWeight: 700, color: 'var(--gray-900)' }}>👥 Expert Human Mentors</h2>
            {mentors.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '48px 16px', background: 'white', borderRadius: 'var(--radius-lg)', border: '2px dashed var(--gray-300)' }}>
                <Users size={48} style={{ margin: '0 auto', color: '#06b6d4', opacity: 0.3, marginBottom: '12px' }} />
                <p style={{ fontSize: 'var(--font-lg)', color: 'var(--gray-600)', margin: '0' }}>{t('mentor.noMentors')}</p>
              </div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '16px' }}>
                {mentors.map((m, idx) => {
            const availColor = { available: '#10b981', busy: '#f59e0b', offline: '#9ca3af' };
            const availBg = { available: '#ecfdf5', busy: '#fffbeb', offline: '#f3f4f6' };
            return (
              <div 
                key={m.id} 
                style={{
                  background: 'rgba(255,255,255,0.7)',
                  backdropFilter: 'blur(20px)',
                  border: '1px solid rgba(255,255,255,0.5)',
                  borderRadius: 'var(--radius-lg)',
                  padding: '20px',
                  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.08)',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  animation: `slideUp ${0.3 + idx * 0.05}s ease`,
                  transition: 'all 0.3s ease',
                  cursor: 'pointer'
                }}
                onMouseOver={e => {
                  e.currentTarget.style.transform = 'translateY(-4px)';
                  e.currentTarget.style.boxShadow = '0 12px 40px rgba(0, 0, 0, 0.12)';
                }}
                onMouseOut={e => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.08)';
                }}
              >
                {/* Header with Avatar and Status */}
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '12px', marginBottom: '12px' }}>
                  <div style={{ background: 'linear-gradient(135deg, #cffafe 0%, #a5f3fc 100%)', padding: '12px', borderRadius: 'var(--radius-md)', display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0 }}>
                    <Users size={20} style={{ color: '#06b6d4' }} />
                  </div>
                  <div style={{ flex: 1 }}>
                    <h3 style={{ margin: '0', fontSize: 'var(--font-lg)', fontWeight: 700, color: 'var(--gray-900)' }}>{m.name}</h3>
                    <p style={{ margin: '4px 0 0', fontSize: 'var(--font-sm)', color: '#06b6d4', fontWeight: 600 }}>
                      {t(`mentor.specializations.${m.specializationKey}`)}
                    </p>
                  </div>
                  <div 
                    style={{ 
                      background: availBg[m.availability], 
                      color: availColor[m.availability],
                      padding: '4px 12px',
                      borderRadius: 'var(--radius-full)',
                      fontSize: 'var(--font-xs)',
                      fontWeight: 600,
                      whiteSpace: 'nowrap'
                    }}
                  >
                    {t(`mentor.${m.availability}`) || m.availability}
                  </div>
                </div>

                {/* Expertise */}
                <p style={{ margin: '0 0 12px', fontSize: 'var(--font-sm)', color: 'var(--gray-700)', lineHeight: '1.5' }}>
                  {t(`mentor.expertiseAreas.${m.expertiseKey}`)}
                </p>

                {/* Metadata */}
                <div style={{ display: 'flex', gap: '8px', marginBottom: '12px', flexWrap: 'wrap' }}>
                  <div style={{ background: 'rgba(249, 115, 22, 0.1)', paddingColor: '#f97316', padding: '6px 12px', borderRadius: 'var(--radius-md)', display: 'flex', alignItems: 'center', gap: '4px', fontSize: 'var(--font-xs)', color: '#d97706' }}>
                    <Star size={14} style={{ color: '#f97316' }} /> {(typeof m.rating === 'string' ? parseFloat(m.rating) : m.rating)?.toFixed(1) || t('common.notAvailable')}
                  </div>
                  <div style={{ background: 'rgba(59, 130, 246, 0.1)', padding: '6px 12px', borderRadius: 'var(--radius-md)', display: 'flex', alignItems: 'center', gap: '4px', fontSize: 'var(--font-xs)', color: '#1e40af' }}>
                    <Briefcase size={14} /> {m.experience_years}{t('mentor.years')}
                  </div>
                  <div style={{ background: 'rgba(107, 114, 128, 0.1)', padding: '6px 12px', borderRadius: 'var(--radius-md)', fontSize: 'var(--font-xs)', color: '#374151' }}>
                    {m.languages_spoken}
                  </div>
                </div>

                {/* Bio */}
                {m.bioKey && (
                  <p style={{ margin: '0 0 12px', fontSize: 'var(--font-sm)', color: 'var(--gray-600)', lineHeight: '1.6', fontStyle: 'italic' }}>
                    "{t(`mentor.mentorBios.${m.bioKey}`)}"
                  </p>
                )}

                {/* Contact Button */}
                <button
                  onClick={() => openChat(m)}
                  disabled={m.availability === 'offline'}
                  style={{ 
                    background: m.availability === 'offline' ? '#d1d5db' : 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)',
                    color: 'white',
                    border: 'none',
                    borderRadius: 'var(--radius-md)',
                    padding: '10px 16px',
                    minHeight: '40px',
                    cursor: m.availability === 'offline' ? 'not-allowed' : 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    gap: '8px',
                    fontSize: 'var(--font-base)',
                    fontWeight: 600,
                    transition: 'all 0.3s ease',
                    backdropFilter: 'blur(10px)'
                  }}
                  onMouseOver={e => {
                    if (m.availability !== 'offline') {
                      e.currentTarget.style.transform = 'scale(1.02)';
                      e.currentTarget.style.boxShadow = '0 8px 16px rgba(6, 182, 212, 0.3)';
                    }
                  }}
                  onMouseOut={e => {
                    e.currentTarget.style.transform = 'scale(1)';
                    e.currentTarget.style.boxShadow = 'none';
                  }}
                >
                  <MessageCircle size={18} />
                  {t('mentor.sendMessage') || 'Send Message'}
                </button>
              </div>
            );
          })}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
