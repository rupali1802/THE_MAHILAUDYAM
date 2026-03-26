import React from 'react';
import { Bell, User } from 'lucide-react';
import { useLanguage } from '../hooks/useLanguage';

export default function DashboardHeader() {
  const { t } = useLanguage();

  return (
    <div style={{
      background: 'linear-gradient(135deg, rgba(251, 146, 60, 0.1) 0%, rgba(249, 115, 22, 0.1) 100%)',
      backdropFilter: 'blur(10px)',
      borderBottom: '1px solid rgba(251, 146, 60, 0.2)',
      padding: '24px 32px',
      position: 'sticky',
      top: 0,
      zIndex: 1000,
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      gap: '24px'
    }}>
      {/* Left Section - Title */}
      <div>
        <h1 style={{
          margin: '0 0 4px 0',
          fontSize: '28px',
          fontWeight: 800,
          color: '#EA580C',
          fontFamily: 'Poppins, sans-serif',
          background: 'linear-gradient(135deg, #EA580C, #F97316)',
          backgroundClip: 'text',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent'
        }}>
          {t('dashboard.welcome')}
        </h1>
        <p style={{
          margin: 0,
          fontSize: '13px',
          color: '#6B7280',
          fontWeight: 500
        }}>
          {new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
        </p>
      </div>

      {/* Right Section - Notifications & Profile */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: '16px',
        marginLeft: 'auto'
      }}>
        {/* Notification Bell */}
        <div style={{
          position: 'relative',
          cursor: 'pointer',
          padding: '8px',
          borderRadius: '12px',
          transition: 'all 0.3s ease',
          backgroundColor: 'rgba(251, 146, 60, 0.1)',
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.backgroundColor = 'rgba(251, 146, 60, 0.2)';
          e.currentTarget.style.transform = 'scale(1.05)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.backgroundColor = 'rgba(251, 146, 60, 0.1)';
          e.currentTarget.style.transform = 'scale(1)';
        }}>
          <Bell size={20} style={{ color: '#EA580C' }} />
          {/* Notification Badge */}
          <div style={{
            position: 'absolute',
            top: '-4px',
            right: '-4px',
            width: '20px',
            height: '20px',
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #EF4444, #DC2626)',
            color: 'white',
            fontSize: '12px',
            fontWeight: 700,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: '2px solid white',
            boxShadow: '0 2px 8px rgba(239, 68, 68, 0.3)'
          }}>
            3
          </div>
        </div>

        {/* Profile Avatar */}
        <div style={{
          width: '40px',
          height: '40px',
          borderRadius: '12px',
          background: 'linear-gradient(135deg, #EA580C, #F97316)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          cursor: 'pointer',
          transition: 'all 0.3s ease',
          boxShadow: '0 4px 12px rgba(251, 146, 60, 0.3)'
        }}
        onMouseEnter={(e) => {
          e.currentTarget.style.transform = 'scale(1.1) rotate(5deg)';
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.transform = 'scale(1) rotate(0deg)';
        }}>
          <User size={20} style={{ color: 'white' }} />
        </div>
      </div>
    </div>
  );
}
