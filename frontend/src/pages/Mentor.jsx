import React, { useState, useEffect } from 'react';
import { useLanguage } from '../hooks/useLanguage';
import { getMentors, getMentorChats, sendMentorMessage } from '../services/api';
import { Users, MessageCircle, Send, ArrowLeft, Star, Briefcase, Loader2, MapPin } from 'lucide-react';
import '../styles/Mentor.css';

const SAMPLE_MENTORS = [
  { id: 1, name: 'Priya Subramaniam', specializationKey: 'organic', expertiseKey: 'handicraft', experience_years: 12, rating: 4.8, availability: 'available', languages_spoken: 'Tamil, English', bioKey: 'priya' },
  { id: 2, name: 'Meena Krishnan', specializationKey: 'dairy', expertiseKey: 'dairy', experience_years: 8, rating: 4.5, availability: 'available', languages_spoken: 'Tamil, Hindi', bioKey: 'meena' },
  { id: 3, name: 'Savita Patel', specializationKey: 'food', expertiseKey: 'foodProcessing', experience_years: 15, rating: 4.9, availability: 'available', languages_spoken: 'Hindi, English', bioKey: 'savita' },
  { id: 4, name: 'Lakshmi Rajan', specializationKey: 'digital', expertiseKey: 'digitalMarketing', experience_years: 6, rating: 4.6, availability: 'busy', languages_spoken: 'Tamil, English', bioKey: 'lakshmi' },
];

export default function Mentor() {
  const { t } = useLanguage();
  const [mentors, setMentors] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState(null);
  const [chats, setChats] = useState([]);
  const [message, setMessage] = useState('');
  const [sending, setSending] = useState(false);

  useEffect(() => {
    getMentors()
      .then(r => setMentors(r.data.results?.length ? r.data.results : SAMPLE_MENTORS))
      .catch(() => setMentors(SAMPLE_MENTORS))
      .finally(() => setLoading(false));
  }, []);

  const openChat = (mentor) => {
    setSelected(mentor);
    getMentorChats(mentor.id).then(r => setChats(r.data.results || [])).catch(() => setChats([]));
  };

  const handleSend = async () => {
    if (!message.trim() || !selected) return;
    setSending(true);
    try {
      await sendMentorMessage({ mentor: selected.id, message, message_type: 'query' });
      setChats(prev => [...prev, { id: Date.now(), message, message_type: 'query', timestamp: new Date().toISOString() }]);
      setMessage('');
    } catch {
      setChats(prev => [...prev, { id: Date.now(), message, message_type: 'query', timestamp: new Date().toISOString() }]);
      setMessage('');
    } finally { setSending(false); }
  };

  const availColor = { available: 'var(--success)', busy: 'var(--warning)', offline: 'var(--gray-400)' };
  const availBg = { available: '#ecfdf5', busy: '#fffbeb', offline: '#f3f4f6' };

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
            <p style={{ margin: '4px 0 0', fontSize: 'var(--font-sm)', opacity: 0.9 }}>{t(`mentor.specializations.${selected.specializationKey}`)}</p>
          </div>
        </div>

        {/* Messages */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '16px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <div style={{ background: 'white', padding: '12px 16px', borderRadius: 'var(--radius-lg)', border: '1px solid var(--gray-200)', maxWidth: '80%', alignSelf: 'flex-start' }}>
            <p style={{ margin: '0', fontSize: 'var(--font-base)', color: 'var(--gray-900)' }}>
              {t('mentor.greeting')}
            </p>
          </div>
          {chats.map(c => (
            <div 
              key={c.id}
              style={{ 
                alignSelf: c.message_type === 'query' ? 'flex-end' : 'flex-start',
                maxWidth: '80%'
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
                <p style={{ margin: '0', fontSize: 'var(--font-base)' }}>{c.message}</p>
              </div>
            </div>
          ))}
        </div>

        {/* Message Input */}
        <div style={{ background: 'white', padding: '16px', borderTop: '1px solid var(--gray-200)', display: 'flex', gap: '12px', alignItems: 'center' }}>
          <input
            className="form-input"
            placeholder={t('mentor.messagePlaceholder')}
            value={message}
            onChange={e => setMessage(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && handleSend()}
            style={{ flex: 1, minHeight: '40px' }}
          />
          <button 
            onClick={handleSend}
            disabled={sending || !message.trim()}
            className="btn btn-secondary"
            style={{ minHeight: '40px', padding: '10px 16px' }}
          >
            {sending ? <Loader2 size={18} className="animate-spin" /> : <Send size={18} />}
          </button>
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
                {mentors.length} {t('mentor.available')}
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
      ) : mentors.length === 0 ? (
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
  );
}
