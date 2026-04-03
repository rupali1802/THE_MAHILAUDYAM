import React from 'react';
import { Mic } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../hooks/useLanguage';

export default function FloatingVoiceButton() {
  const navigate = useNavigate();
  const { t } = useLanguage();

  const handleVoiceClick = () => {
    // Navigate to voice page
    navigate('/voice');
  };

  return (
    <>
      {/* Floating Voice Button - SAKHI - Center Bottom */}
      <div
        style={{
          position: 'fixed',
          bottom: '120px',
          left: '50%',
          transform: 'translateX(-50%)',
          zIndex: 999,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: '12px'
        }}
      >
        {/* SAKHI Label - Animated */}
        <div
          style={{
            background: 'linear-gradient(135deg, #EA580C, #F97316)',
            color: 'white',
            padding: '8px 24px',
            borderRadius: '20px',
            fontSize: '14px',
            fontWeight: 700,
            fontFamily: 'Poppins, sans-serif',
            boxShadow: '0 8px 24px rgba(234, 88, 12, 0.4)',
            animation: 'fadeIn 0.5s ease',
            textTransform: 'uppercase',
            letterSpacing: '1px'
          }}
        >
          {t('voice.assistant') || 'SAKHI AI'}
        </div>

        {/* Main Voice Button */}
        <button
          onClick={handleVoiceClick}
          style={{
            width: '90px',
            height: '90px',
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #EA580C 0%, #D97706 100%)',
            border: '3px solid rgba(255, 255, 255, 0.4)',
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 12px 40px rgba(234, 88, 12, 0.5)',
            transition: 'all 0.3s ease',
            animation: 'floatUp 3s ease-in-out infinite',
            position: 'relative',
            overflow: 'hidden'
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = 'scale(1.12)';
            e.currentTarget.style.boxShadow = '0 20px 60px rgba(234, 88, 12, 0.7)';
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = 'scale(1)';
            e.currentTarget.style.boxShadow = '0 12px 40px rgba(234, 88, 12, 0.5)';
          }}
        >
          {/* Button Content */}
          <div style={{ position: 'relative', zIndex: 2, textAlign: 'center' }}>
            <Mic size={40} style={{ color: 'white', marginBottom: '4px' }} />
            <div style={{
              fontSize: '11px',
              fontWeight: 800,
              color: 'white',
              fontFamily: 'Poppins, sans-serif',
              textTransform: 'uppercase',
              letterSpacing: '0.5px'
            }}>
              {t('voice.assistant')}
            </div>
          </div>
        </button>
      </div>

      {/* Inline Styles for Animations */}
      <style>{`
        @keyframes floatUp {
          0%, 100% {
            transform: translateY(0px);
          }
          50% {
            transform: translateY(-12px);
          }
        }

        @keyframes fadeIn {
          from {
            opacity: 0;
            transform: scale(0.9);
          }
          to {
            opacity: 1;
            transform: scale(1);
          }
        }
      `}</style>
    </>
  );
}
