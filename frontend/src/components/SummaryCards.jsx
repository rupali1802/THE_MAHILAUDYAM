import React from 'react';
import { TrendingUp, TrendingDown, DollarSign, Target } from 'lucide-react';
import { formatCurrencyForLanguage } from '../utils/device';
import { useLanguage } from '../hooks/useLanguage';

export default function SummaryCards({ summary, lang }) {
  const { t } = useLanguage();
  const fmt = (val) => formatCurrencyForLanguage(val || 0, lang);

  const cards = [
    {
      title: t('dashboard.totalIncome'),
      value: summary?.monthly_income || 0,
      icon: TrendingUp,
      gradient: 'linear-gradient(135deg, #22C55E 0%, #16A34A 100%)',
      bgColor: 'rgba(34, 197, 94, 0.1)',
      trend: '+12.5%',
      color: '#22C55E'
    },
    {
      title: t('dashboard.totalExpense'),
      value: summary?.monthly_expense || 0,
      icon: TrendingDown,
      gradient: 'linear-gradient(135deg, #EF4444 0%, #DC2626 100%)',
      bgColor: 'rgba(239, 68, 68, 0.1)',
      trend: '-3.2%',
      color: '#EF4444'
    },
    {
      title: t('dashboard.totalSales'),
      value: summary?.monthly_income || 0,
      icon: DollarSign,
      gradient: 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)',
      bgColor: 'rgba(245, 158, 11, 0.1)',
      trend: '+8.7%',
      color: '#F59E0B'
    },
    {
      title: t('dashboard.netProfit'),
      value: (summary?.monthly_income || 0) - (summary?.monthly_expense || 0),
      icon: Target,
      gradient: 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)',
      bgColor: 'rgba(99, 102, 241, 0.1)',
      trend: '+15.3%',
      color: '#6366F1'
    }
  ];

  return (
    <div style={{
      display: 'grid',
      gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
      gap: '20px',
      marginBottom: '32px'
    }}>
      {cards.map((card, idx) => {
        const Icon = card.icon;
        return (
          <div
            key={idx}
            style={{
              background: 'rgba(255, 255, 255, 0.8)',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(255, 255, 255, 0.4)',
              borderRadius: '20px',
              padding: '24px',
              transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
              cursor: 'pointer',
              animation: `slideUp 0.5s ease-out ${idx * 0.1}s both`,
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.08)',
              position: 'relative',
              overflow: 'hidden'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-12px) scale(1.02)';
              e.currentTarget.style.boxShadow = `0 24px 48px rgba(99, 102, 241, 0.2)`;
              e.currentTarget.style.borderColor = card.color;
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0) scale(1)';
              e.currentTarget.style.boxShadow = '0 8px 32px rgba(0, 0, 0, 0.08)';
              e.currentTarget.style.borderColor = 'rgba(255, 255, 255, 0.4)';
            }}>
            
            {/* Gradient Background Blur */}
            <div style={{
              position: 'absolute',
              top: '-50%',
              right: '-50%',
              width: '200px',
              height: '200px',
              borderRadius: '50%',
              background: card.gradient,
              opacity: 0.1,
              filter: 'blur(40px)',
              animation: 'floating 6s ease-in-out infinite'
            }} />

            {/* Content */}
            <div style={{ position: 'relative', zIndex: 1 }}>
              {/* Icon & Trend */}
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'flex-start',
                marginBottom: '16px'
              }}>
                <div style={{
                  background: card.gradient,
                  padding: '12px',
                  borderRadius: '12px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: `0 4px 12px ${card.color}40`
                }}>
                  <Icon size={24} style={{ color: 'white' }} />
                </div>
                <div style={{
                  background: card.bgColor,
                  color: card.color,
                  padding: '4px 12px',
                  borderRadius: '8px',
                  fontSize: '12px',
                  fontWeight: 700,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '4px'
                }}>
                  <TrendingUp size={14} />
                  {card.trend}
                </div>
              </div>

              {/* Title */}
              <p style={{
                margin: '0 0 8px 0',
                fontSize: '12px',
                color: '#6B7280',
                fontWeight: 600,
                textTransform: 'uppercase',
                letterSpacing: '0.5px'
              }}>
                {card.title}
              </p>

              {/* Value */}
              <p style={{
                margin: 0,
                fontSize: '28px',
                fontWeight: 800,
                color: card.color,
                fontFamily: 'Montserrat, sans-serif'
              }}>
                {fmt(card.value)}
              </p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
