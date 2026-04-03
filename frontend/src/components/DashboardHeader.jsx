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

      {/* Right Section - Removed: Notifications & Profile */}
    </div>
  );
}
