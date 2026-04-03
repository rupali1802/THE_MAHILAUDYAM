import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../hooks/useLanguage';
import { getDeviceId } from '../utils/device';
import { getMentors, sendMentorMessage } from '../services/api';
import { Users, MessageCircle, Send, ArrowLeft, Star, Briefcase, Loader2, Mic, MicOff, Volume2, VolumeX, Languages } from 'lucide-react';
import '../styles/Mentor.css';

const SAMPLE_MENTORS = [
  { id: 1, name: 'Priya Subramaniam', specializationKey: 'organic', expertiseKey: 'handicraft', experience_years: 12, rating: 4.8, availability: 'available', languages_spoken: 'Tamil, English', bioKey: 'priya' },
  { id: 2, name: 'Meena Krishnan', specializationKey: 'dairy', expertiseKey: 'dairy', experience_years: 8, rating: 4.5, availability: 'available', languages_spoken: 'Tamil, Hindi', bioKey: 'meena' },
  { id: 3, name: 'Savita Patel', specializationKey: 'food', expertiseKey: 'foodProcessing', experience_years: 15, rating: 4.9, availability: 'available', languages_spoken: 'Hindi, English', bioKey: 'savita' },
  { id: 4, name: 'Lakshmi Rajan', specializationKey: 'digital', expertiseKey: 'digitalMarketing', experience_years: 6, rating: 4.6, availability: 'busy', languages_spoken: 'Tamil, English', bioKey: 'lakshmi' },
];

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const speechSynthesis = window.speechSynthesis;

export default function MentorChat() {
  const { t, language: appLanguage } = useLanguage();
  const [mentors, setMentors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stage, setStage] = useState('select'); // select -> language -> input -> chat
  const [selectedMentor, setSelectedMentor] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState('en');
  const [inputType, setInputType] = useState('text'); // text or voice
  const [chats, setChats] = useState([]);
  const [message, setMessage] = useState('');
  const [sending, setSending] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const recognitionRef = useRef(null);
  const messagesEndRef = useRef(null);

  // Debug logging
  useEffect(() => {
    console.log('💬 Mentor Chat State:', { stage, selectedMentor: selectedMentor?.name, selectedLanguage, inputType });
  }, [stage, selectedMentor, selectedLanguage, inputType]);

  // Language names
  const languageNames = {
    'en': '🇬🇧 English',
    'ta': '🇮🇳 தமிழ்',
    'hi': '🇮🇳 हिंदी'
  };

  // Suggestion chips with multilingual questions
  const suggestionChips = {
    'en': [
      'How can I increase my sales?',
      'What is good pricing for my products?',
      'How do I manage my expenses better?',
      'Which government scheme can I apply for?'
    ],
    'ta': [
      'என் விற்பனை எப்படி அதிகரிக்க வேண்டும்?',
      'சரியான விலை நির்ধारணை எப்படி செய்ய வேண்டும்?',
      'செலவுகளை எப்படி குறைக்க வேண்டும்?',
      'எந்த அரசு திட்டத்திற்கு விண்ணப்பம் செய்ய வேண்டும்?'
    ],
    'hi': [
      'मैं अपनी बिक्री कैसे बढ़ा सकता हूँ?',
      'सही मूल्य निर्धारण कैसे करें?',
      'खर्चों को कैसे कम करूँ?',
      'कौन सी सरकारी योजना के लिए आवेदन करूँ?'
    ]
  };

  // Multilingual greeting messages
  const greetingMessages = {
    'en': (name) => `👋 Hello! I'm ${name}. I'm here to help you with your business questions. Feel free to ask me anything!`,
    'ta': (name) => `வணக்கம்! நான் ${name}. உங்களின் வணிக கேள்விகளுக்கு உதவ இங்கே இருக்கிறேன். எதையும் கேட்கலாம்!`,
    'hi': (name) => `नमस्ते! मैं ${name} हूँ। मैं आपके व्यावसायिक सवालों में मदद करने के लिए यहाँ हूँ। कुछ भी पूछें!`
  };

  // Multilingual "thinking" messages
  const thinkingMessages = {
    'en': (name) => `${name} is thinking...`,
    'ta': (name) => `${name} சிந்தித்து கொண்டிருக்கிறார்...`,
    'hi': (name) => `${name} सोच रहे हैं...`
  };

  // Multilingual "Listen" button
  const listenLabel = {
    'en': 'Listen',
    'ta': 'கேளுங்கள்',
    'hi': 'सुनें'
  };

  useEffect(() => {
    getMentors(appLanguage)
      .then(r => setMentors(r.data.results?.length ? r.data.results : SAMPLE_MENTORS))
      .catch(() => setMentors(SAMPLE_MENTORS))
      .finally(() => setLoading(false));
  }, [appLanguage]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [chats]);

  const startListening = () => {
    if (!SpeechRecognition) {
      alert('Speech Recognition not supported');
      return;
    }

    try {
      const recognition = new SpeechRecognition();
      recognitionRef.current = recognition;
      recognition.lang = selectedLanguage === 'hi' ? 'hi-IN' : selectedLanguage === 'ta' ? 'ta-IN' : 'en-US';
      recognition.interimResults = true;
      recognition.continuous = false;

      recognition.onstart = () => {
        setIsListening(true);
      };

      recognition.onend = () => {
        setIsListening(false);
      };

      recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }
        if (event.isFinal) {
          setMessage(transcript.trim());
          setIsListening(false);
        } else {
          setMessage(transcript);
        }
      };

      recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
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
      recognitionRef.current.abort();
      setIsListening(false);
    }
  };

  const speakText = (text) => {
    if (!speechSynthesis) return;
    
    speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = selectedLanguage === 'hi' ? 'hi-IN' : selectedLanguage === 'ta' ? 'ta-IN' : 'en-US';
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 1;

    utterance.onstart = () => setIsSpeaking(true);
    utterance.onend = () => setIsSpeaking(false);
    utterance.onerror = () => setIsSpeaking(false);

    speechSynthesis.speak(utterance);
  };

  const stopSpeaking = () => {
    if (speechSynthesis) {
      speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  };

  const handleSend = async () => {
    if (!message.trim() || !selectedMentor || sending) return;

    const userMessage = message;
    setMessage('');
    setSending(true);

    if (isListening) {
      stopListening();
    }

    try {
      const response = await sendMentorMessage({
        device_id: getDeviceId(),
        mentor_id: selectedMentor.id,
        message: userMessage,
        message_type: 'query',
        language: selectedLanguage,
      });

      // Add user message
      if (response.data.user_message) {
        setChats(prev => [...prev, response.data.user_message]);
      }

      // Add mentor response
      if (response.data.mentor_response) {
        setChats(prev => [...prev, response.data.mentor_response]);

        // If voice output selected, speak the response
        if (inputType === 'voice' && response.data.mentor_response.message) {
          setTimeout(() => {
            speakText(response.data.mentor_response.message);
          }, 500);
        }
      }
    } catch (error) {
      console.error('Error:', error);
      const errorMsg = {
        id: Date.now(),
        message: 'Sorry, could not process your message. Please try again.',
        message_type: 'response',
        timestamp: new Date().toISOString()
      };
      setChats(prev => [...prev, errorMsg]);
    } finally {
      setSending(false);
    }
  };

  // Stage 1: Select Mentor
  if (stage === 'select') {
    return (
      <div style={{ minHeight: '100vh', background: 'linear-gradient(180deg, var(--bg-light) 0%, var(--white) 100%)', padding: '20px', paddingBottom: '120px' }}>
        {/* Header */}
        <div style={{ background: 'linear-gradient(135deg, #2563eb 0%, #0891b2 100%)', color: 'white', borderRadius: 'var(--radius-lg)', padding: '24px', marginBottom: '24px', boxShadow: 'var(--shadow-lg)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px', marginBottom: '16px' }}>
            <div style={{ width: '60px', height: '60px', background: 'rgba(255,255,255,0.2)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <Users size={32} />
            </div>
            <div>
              <h1 style={{ fontSize: '24px', fontWeight: 700, margin: '0' }}>Select Your Mentor</h1>
              <p style={{ fontSize: '14px', opacity: 0.9, margin: '4px 0 0' }}>Choose a business mentor to guide you</p>
            </div>
          </div>
        </div>

        {/* Mentors Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
          {loading ? (
            <div style={{ gridColumn: '1/-1', display: 'flex', justifyContent: 'center', padding: '40px' }}>
              <Loader2 size={32} className="animate-spin" style={{ color: '#2563eb' }} />
            </div>
          ) : (
            mentors.map(mentor => (
              <div
                key={mentor.id}
                onClick={() => {
                  console.log('🧠 Selected mentor:', mentor.name);
                  setSelectedMentor(mentor);
                  setStage('language');
                }}
                style={{
                  background: 'white',
                  borderRadius: 'var(--radius-lg)',
                  border: '2px solid var(--gray-200)',
                  padding: '20px',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  boxShadow: 'var(--shadow-sm)',
                  userSelect: 'none'
                }}
                onMouseEnter={e => {
                  e.currentTarget.style.transform = 'translateY(-4px)';
                  e.currentTarget.style.borderColor = '#2563eb';
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.borderColor = 'var(--gray-200)';
                }}
              >
                <div style={{ display: 'flex', alignItems: 'center', marginBottom: '16px' }}>
                  <div style={{ width: '50px', height: '50px', background: 'linear-gradient(135deg, #2563eb 0%, #0891b2 100%)', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontSize: '24px', marginRight: '12px' }}>
                    👩‍💼
                  </div>
                  <div>
                    <h3 style={{ margin: '0', fontSize: 'var(--font-lg)', fontWeight: 600 }}>{mentor.name}</h3>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginTop: '4px' }}>
                      <Star size={14} style={{ color: '#fbbf24', fill: '#fbbf24' }} />
                      <span style={{ fontSize: 'var(--font-sm)', color: 'var(--gray-600)' }}>{mentor.rating} ({mentor.total_reviews || 0})</span>
                    </div>
                  </div>
                </div>

                <div style={{ marginBottom: '12px' }}>
                  <p style={{ fontSize: 'var(--font-sm)', color: 'var(--gray-700)', margin: '0 0 8px', lineHeight: 1.5 }}>
                    <strong>Experience:</strong> {mentor.experience_years} years
                  </p>
                  <p style={{ fontSize: 'var(--font-sm)', color: 'var(--gray-700)', margin: '0 0 8px' }}>
                    <strong>Languages:</strong> {mentor.languages_spoken}
                  </p>
                  <p style={{ fontSize: 'var(--font-sm)', color: 'var(--gray-700)', margin: '0' }}>
                    <strong>Status:</strong> {mentor.availability === 'available' ? '✅ Available' : '🔴 Busy'}
                  </p>
                </div>

                <button style={{ width: '100%', background: '#2563eb', color: 'white', border: 'none', padding: '12px', borderRadius: '8px', fontWeight: 600, cursor: 'pointer', transition: 'all 0.3s ease' }} onMouseEnter={e => e.target.style.background = '#1d4ed8'} onMouseLeave={e => e.target.style.background = '#2563eb'}>
                  Start Chat →
                </button>
              </div>
            ))
          )}
        </div>
      </div>
    );
  }

  // Stage 2: Select Language
  if (stage === 'language') {
    return (
      <div style={{ minHeight: '100vh', background: 'linear-gradient(180deg, var(--bg-light) 0%, var(--white) 100%)', padding: '20px', paddingBottom: '120px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ maxWidth: '500px', width: '100%' }}>
          <button
            onClick={() => {
              setStage('select');
              setSelectedMentor(null);
            }}
            style={{ background: 'transparent', border: 'none', color: '#2563eb', cursor: 'pointer', fontSize: '16px', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '20px' }}
          >
            <ArrowLeft size={20} /> Go Back
          </button>

          <div style={{ background: 'white', borderRadius: 'var(--radius-lg)', padding: '32px', boxShadow: 'var(--shadow-lg)' }}>
            <div style={{ textAlign: 'center', marginBottom: '32px' }}>
              <Languages size={48} style={{ color: '#2563eb', margin: '0 auto 16px', display: 'block' }} />
              <h2 style={{ fontSize: '24px', fontWeight: 700, margin: '0 0 8px' }}>Choose Language</h2>
              <p style={{ fontSize: '14px', color: 'var(--gray-600)', margin: '0' }}>Select your preferred communication language</p>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              {Object.entries(languageNames).map(([code, name]) => (
                <button
                  key={code}
                  onClick={() => {
                    console.log('🌐 Selected language:', code);
                    setSelectedLanguage(code);
                    setTimeout(() => setStage('input'), 100);
                  }}
                  style={{
                    background: selectedLanguage === code ? '#2563eb' : 'var(--gray-100)',
                    color: selectedLanguage === code ? 'white' : 'var(--gray-900)',
                    border: selectedLanguage === code ? '2px solid #2563eb' : '2px solid var(--gray-300)',
                    padding: '16px 20px',
                    borderRadius: '12px',
                    fontSize: '16px',
                    fontWeight: 600,
                    cursor: 'pointer',
                    transition: 'all 0.3s ease'
                  }}
                  onMouseEnter={e => {
                    if (selectedLanguage !== code) {
                      e.target.style.borderColor = '#2563eb';
                      e.target.style.background = '#eff6ff';
                    }
                  }}
                  onMouseLeave={e => {
                    if (selectedLanguage !== code) {
                      e.target.style.background = 'var(--gray-100)';
                      e.target.style.borderColor = 'var(--gray-300)';
                    }
                  }}
                >
                  {name}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Stage 3: Select Input Type
  if (stage === 'input') {
    return (
      <div style={{ minHeight: '100vh', background: 'linear-gradient(180deg, var(--bg-light) 0%, var(--white) 100%)', padding: '20px', paddingBottom: '120px', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ maxWidth: '500px', width: '100%' }}>
          <button
            onClick={() => setStage('language')}
            style={{ background: 'transparent', border: 'none', color: '#2563eb', cursor: 'pointer', fontSize: '16px', fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '20px' }}
          >
            <ArrowLeft size={20} /> Go Back
          </button>

          <div style={{ background: 'white', borderRadius: 'var(--radius-lg)', padding: '32px', boxShadow: 'var(--shadow-lg)' }}>
            <div style={{ textAlign: 'center', marginBottom: '32px' }}>
              <MessageCircle size={48} style={{ color: '#2563eb', margin: '0 auto 16px', display: 'block' }} />
              <h2 style={{ fontSize: '24px', fontWeight: 700, margin: '0 0 8px' }}>Communication Style</h2>
              <p style={{ fontSize: '14px', color: 'var(--gray-600)', margin: '0' }}>Choose how you want to communicate with {selectedMentor.name}</p>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <button
                onClick={() => {
                  console.log('⌨️ Selected text input');
                  setInputType('text');
                  setTimeout(() => setStage('chat'), 100);
                }}
                style={{
                  background: inputType === 'text' ? '#2563eb' : 'var(--gray-100)',
                  color: inputType === 'text' ? 'white' : 'var(--gray-900)',
                  border: inputType === 'text' ? '2px solid #2563eb' : '2px solid var(--gray-300)',
                  padding: '20px',
                  borderRadius: '12px',
                  fontSize: '16px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '16px'
                }}
                onMouseEnter={e => {
                  if (inputType !== 'text') {
                    e.currentTarget.style.borderColor = '#2563eb';
                    e.currentTarget.style.background = '#eff6ff';
                  }
                }}
                onMouseLeave={e => {
                  if (inputType !== 'text') {
                    e.currentTarget.style.background = 'var(--gray-100)';
                    e.currentTarget.style.borderColor = 'var(--gray-300)';
                  }
                }}
              >
                <span style={{ fontSize: '32px' }}>⌨️</span>
                <div style={{ textAlign: 'left' }}>
                  <div style={{ fontWeight: 700, fontSize: '16px' }}>Text Chat</div>
                  <div style={{ fontSize: '13px', opacity: 0.8, marginTop: '4px' }}>Type your questions and receive text responses</div>
                </div>
              </button>

              <button
                onClick={() => {
                  console.log('🎤 Selected voice input');
                  setInputType('voice');
                  setTimeout(() => setStage('chat'), 100);
                }}
                style={{
                  background: inputType === 'voice' ? '#2563eb' : 'var(--gray-100)',
                  color: inputType === 'voice' ? 'white' : 'var(--gray-900)',
                  border: inputType === 'voice' ? '2px solid #2563eb' : '2px solid var(--gray-300)',
                  padding: '20px',
                  borderRadius: '12px',
                  fontSize: '16px',
                  fontWeight: 600,
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '16px'
                }}
                onMouseEnter={e => {
                  if (inputType !== 'voice') {
                    e.currentTarget.style.borderColor = '#2563eb';
                    e.currentTarget.style.background = '#eff6ff';
                  }
                }}
                onMouseLeave={e => {
                  if (inputType !== 'voice') {
                    e.currentTarget.style.background = 'var(--gray-100)';
                    e.currentTarget.style.borderColor = 'var(--gray-300)';
                  }
                }}
              >
                <span style={{ fontSize: '32px' }}>🎤</span>
                <div style={{ textAlign: 'left' }}>
                  <div style={{ fontWeight: 700, fontSize: '16px' }}>Voice Chat</div>
                  <div style={{ fontSize: '13px', opacity: 0.8, marginTop: '4px' }}>Speak your questions and hear voice responses</div>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // Stage 4: Chat Interface
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh', background: 'var(--bg-light)' }}>
      {/* Header */}
      <div style={{ background: 'linear-gradient(135deg, #2563eb 0%, #0891b2 100%)', color: 'white', padding: '16px', display: 'flex', alignItems: 'center', gap: '12px', boxShadow: 'var(--shadow-md)' }}>
        <button
          onClick={() => {
            setStage('select');
            setSelectedMentor(null);
            setChats([]);
          }}
          style={{ background: 'transparent', border: 'none', color: 'white', cursor: 'pointer', padding: '8px', display: 'flex', alignItems: 'center' }}
        >
          <ArrowLeft size={24} />
        </button>
        <div style={{ background: 'rgba(255,255,255,0.2)', padding: '10px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <Users size={20} />
        </div>
        <div style={{ flex: 1 }}>
          <h3 style={{ margin: '0', fontSize: 'var(--font-lg)', fontWeight: 700 }}>{selectedMentor.name}</h3>
          <p style={{ margin: '4px 0 0', fontSize: 'var(--font-sm)', opacity: 0.9 }}>
            {languageNames[selectedLanguage]} • {inputType === 'voice' ? '🎤 Voice' : '⌨️ Text'} Mode
          </p>
        </div>
      </div>

      {/* Messages */}
      <div style={{ flex: 1, overflowY: 'auto', padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {chats.length === 0 ? (
          <>
            <div style={{ background: 'white', padding: '16px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--gray-200)', maxWidth: '80%', alignSelf: 'flex-start' }}>
              <p style={{ margin: '0', fontSize: 'var(--font-base)', color: 'var(--gray-900)', lineHeight: '1.6' }}>
                {greetingMessages[selectedLanguage](selectedMentor.name)}
              </p>
            </div>
            
            {/* Suggestion Chips */}
            <div style={{ marginTop: '16px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
              <p style={{ margin: '8px 0 0 0', fontSize: 'var(--font-xs)', color: 'var(--gray-600)', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                {selectedLanguage === 'ta' ? 'பரிந்துரைக்கப்பட்ட கேள்விகள்:' : selectedLanguage === 'hi' ? 'सुझाए गए प्रश्न:' : 'Suggested Questions:'}
              </p>
              {suggestionChips[selectedLanguage].map((chip, idx) => (
                <button
                  key={idx}
                  onClick={() => {
                    setMessage(chip);
                    setTimeout(() => {
                      document.querySelector('input[placeholder*="கேள்வி"]')?.focus() || 
                      document.querySelector('input[placeholder*="सवाल"]')?.focus() || 
                      document.querySelector('input[placeholder*="question"]')?.focus();
                    }, 0);
                  }}
                  style={{
                    background: 'linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 100%)',
                    border: '1px solid #7dd3fc',
                    color: '#0369a1',
                    padding: '10px 14px',
                    borderRadius: '20px',
                    fontSize: 'var(--font-sm)',
                    fontWeight: 500,
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    textAlign: 'left',
                    maxWidth: '100%',
                    whiteSpace: 'normal'
                  }}
                  onMouseEnter={e => {
                    e.currentTarget.style.background = 'linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)';
                    e.currentTarget.style.color = 'white';
                    e.currentTarget.style.borderColor = '#06b6d4';
                  }}
                  onMouseLeave={e => {
                    e.currentTarget.style.background = 'linear-gradient(135deg, #e0f2fe 0%, #f0f9ff 100%)';
                    e.currentTarget.style.color = '#0369a1';
                    e.currentTarget.style.borderColor = '#7dd3fc';
                  }}
                >
                  {chip}
                </button>
              ))}
            </div>
          </>
        ) : (
          chats.map(c => (
            <div key={c.id} style={{ 
              display: 'flex',
              justifyContent: c.message_type === 'query' ? 'flex-end' : 'flex-start',
              marginBottom: '8px'
            }}>
              {c.message_type === 'response' && (
                <div style={{ width: '32px', height: '32px', background: '#2563eb', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontSize: '16px', marginRight: '8px', flexShrink: 0 }}>
                  👩‍💼
                </div>
              )}
              
              <div style={{ maxWidth: '75%' }}>
                <div style={{
                  background: c.message_type === 'query' ? '#2563eb' : '#ffffff',
                  color: c.message_type === 'query' ? 'white' : '#111827',
                  padding: '10px 14px',
                  borderRadius: c.message_type === 'query' ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
                  border: c.message_type === 'query' ? 'none' : '1px solid #e5e7eb',
                  boxShadow: c.message_type === 'query' ? '0 2px 4px rgba(37, 99, 235, 0.2)' : '0 1px 2px rgba(0,0,0,0.05)',
                  wordWrap: 'break-word',
                  lineHeight: '1.5'
                }}>
                  <p style={{ margin: '0', fontSize: 'var(--font-sm)', whiteSpace: 'pre-wrap' }}>{c.message}</p>
                  
                  {c.message_type === 'response' && inputType === 'text' && (
                    <button
                      onClick={() => speakText(c.message)}
                      style={{
                        background: 'rgba(37, 99, 235, 0.15)',
                        border: 'none',
                        color: '#2563eb',
                        padding: '4px 8px',
                        borderRadius: '6px',
                        fontSize: 'var(--font-xs)',
                        cursor: 'pointer',
                        marginTop: '6px',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px',
                        fontWeight: 500
                      }}
                      title={`Listen to response in ${languageNames[selectedLanguage]}`}
                    >
                      <Volume2 size={12} /> {listenLabel[selectedLanguage]}
                    </button>
                  )}
                </div>
                <p style={{ 
                  margin: '4px 0 0 0', 
                  fontSize: 'var(--font-xs)', 
                  color: '#9ca3af',
                  paddingLeft: c.message_type === 'response' ? '8px' : '0'
                }}>
                  {new Date(c.timestamp).toLocaleTimeString({}, {hour: '2-digit', minute:'2-digit'})}
                </p>
              </div>
            </div>
          ))
        )}
        {sending && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            <div style={{ width: '32px', height: '32px', background: '#2563eb', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontSize: '16px', flexShrink: 0 }}>
              👩‍💼
            </div>
            <div style={{ background: '#f3f4f6', padding: '10px 14px', borderRadius: '18px 18px 18px 4px', border: '1px solid #e5e7eb', display: 'flex', alignItems: 'center', gap: '6px' }}>
              <div style={{ width: '6px', height: '6px', background: '#9ca3af', borderRadius: '50%', animation: 'bounce 1.4s infinite' }} />
              <div style={{ width: '6px', height: '6px', background: '#9ca3af', borderRadius: '50%', animation: 'bounce 1.4s infinite 0.2s' }} />
              <div style={{ width: '6px', height: '6px', background: '#9ca3af', borderRadius: '50%', animation: 'bounce 1.4s infinite 0.4s' }} />
              <span style={{ color: '#6b7280', fontSize: 'var(--font-xs)', marginLeft: '4px' }}>{thinkingMessages[selectedLanguage](selectedMentor.name)}</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area - WhatsApp Style */}
      <div style={{ background: 'white', padding: '12px 16px', borderTop: '2px solid #e5e7eb', display: 'flex', gap: '8px', alignItems: 'flex-end', flexWrap: 'wrap' }}>
        {isListening && (
          <div style={{ width: '100%', padding: '10px 12px', background: '#fef3c7', border: '2px solid #fbbf24', borderRadius: '8px', display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
            <Mic size={16} style={{ color: '#d97706', animation: 'pulse 1.5s infinite' }} />
            <span style={{ color: '#92400e', fontWeight: '600', fontSize: 'var(--font-sm)' }}>
              {selectedLanguage === 'ta' ? 'கேளுகிறேன்...' : selectedLanguage === 'hi' ? 'सुन रहें हैं...' : 'Listening...'}
            </span>
          </div>
        )}

        {/* Voice/Mic Button */}
        {inputType === 'voice' && (
          <button
            onClick={isListening ? stopListening : startListening}
            style={{
              background: isListening ? '#ff4444' : '#2563eb',
              color: 'white',
              minHeight: '44px',
              minWidth: '44px',
              padding: '10px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              borderRadius: '50%',
              border: 'none',
              cursor: 'pointer',
              fontWeight: '600',
              transition: 'all 0.3s ease',
              boxShadow: isListening ? '0 0 16px rgba(255, 68, 68, 0.6)' : '0 2px 8px rgba(37, 99, 235, 0.3)',
              flexShrink: 0
            }}
            title={isListening ? (selectedLanguage === 'ta' ? 'கேட்க நிறுத்தவும்' : selectedLanguage === 'hi' ? 'सुनना बंद करें' : 'Stop listening') : (selectedLanguage === 'ta' ? 'குரல் உள்ளீடு' : selectedLanguage === 'hi' ? 'वॉइस इनपुट' : 'Voice input')}
          >
            {isListening ? <MicOff size={22} /> : <Mic size={22} />}
          </button>
        )}

        {/* Text Input */}
        <input
          className="form-input"
          placeholder={isListening ? (selectedLanguage === 'ta' ? 'கேளுகிறேன்...' : selectedLanguage === 'hi' ? 'सुन रहें हैं...' : 'Listening...') : (inputType === 'voice' ? (selectedLanguage === 'ta' ? 'பேச உங்கள் கேள்வி...' : selectedLanguage === 'hi' ? 'अपना सवाल बोलें...' : 'Speak your question...') : (selectedLanguage === 'ta' ? 'உங்கள் கேள்வி தட்ட்சர் சொல்லுங்கள்...' : selectedLanguage === 'hi' ? 'अपना प्रश्न टाइप करें...' : 'Type your question...'))}
          value={message}
          onChange={e => setMessage(e.target.value)}
          onKeyDown={e => e.key === 'Enter' && !sending && !isListening && handleSend()}
          style={{
            flex: 1,
            minHeight: '44px',
            minWidth: '200px',
            padding: '12px 14px',
            fontSize: '15px',
            border: isListening ? '2px solid #fbbf24' : '2px solid #e5e7eb',
            borderRadius: '24px',
            fontFamily: 'inherit',
            background: isListening ? '#fffbeb' : 'white',
            outline: 'none',
            transition: 'all 0.2s ease'
          }}
          disabled={sending || (inputType === 'voice' && isListening)}
          onFocus={e => e.target.style.borderColor = '#2563eb'}
          onBlur={e => e.target.style.borderColor = '#e5e7eb'}
        />

        {/* Send Button */}
        <button
          onClick={handleSend}
          disabled={sending || !message.trim() || (inputType === 'voice' && isListening)}
          style={{
            minHeight: '44px',
            minWidth: '44px',
            padding: '10px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            background: (!sending && message.trim() && !(inputType === 'voice' && isListening)) ? '#2563eb' : '#d1d5db',
            color: 'white',
            borderRadius: '50%',
            border: 'none',
            cursor: (!sending && message.trim() && !(inputType === 'voice' && isListening)) ? 'pointer' : 'not-allowed',
            transition: 'all 0.3s ease',
            boxShadow: (!sending && message.trim() && !(inputType === 'voice' && isListening)) ? '0 2px 8px rgba(37, 99, 235, 0.3)' : 'none',
            flexShrink: 0
          }}
          title={selectedLanguage === 'ta' ? 'செய்தி அனுப்பவும்' : selectedLanguage === 'hi' ? 'संदेश भेजें' : 'Send message'}
        >
          {sending ? <Loader2 size={22} className="animate-spin" /> : <Send size={22} />}
        </button>

        {/* Stop Speaking Button */}
        {isSpeaking && (
          <button
            onClick={stopSpeaking}
            style={{
              background: '#f97316',
              color: 'white',
              minHeight: '44px',
              padding: '10px 14px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px',
              borderRadius: '24px',
              border: 'none',
              cursor: 'pointer',
              fontWeight: '600',
              transition: 'all 0.3s ease',
              fontSize: 'var(--font-sm)'
            }}
            title={selectedLanguage === 'ta' ? 'பேசுவதை நிறுத்தவும்' : selectedLanguage === 'hi' ? 'बोलना बंद करें' : 'Stop speaking'}
          >
            <VolumeX size={18} /> {selectedLanguage === 'ta' ? 'நிறுத்து' : selectedLanguage === 'hi' ? 'रोकें' : 'Stop'}
          </button>
        )}
      </div>
    </div>
  );
}
