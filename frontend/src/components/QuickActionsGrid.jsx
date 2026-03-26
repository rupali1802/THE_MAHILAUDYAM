import React, { useState } from 'react';
import { Plus, Target, TrendingUp, BarChart3 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../hooks/useLanguage';

export default function QuickActions() {
  const navigate = useNavigate();
  const { t } = useLanguage();
  const [ripples, setRipples] = useState({});

  const actions = [
    { icon: Plus, label: t('income.addIncome'), path: '/income', gradient: 'linear-gradient(135deg, #22C55E 0%, #16A34A 100%)' },
    { icon: Plus, label: t('expense.addExpense'), path: '/expense', gradient: 'linear-gradient(135deg, #EF4444 0%, #DC2626 100%)' },
    { icon: Plus, label: t('dashboard.addSale'), path: '/sales', gradient: 'linear-gradient(135deg, #F59E0B 0%, #D97706 100%)' },
    { icon: Target, label: t('dashboard.viewProfit'), path: '/profit', gradient: 'linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%)' },
  ];

  const handleClick = (path, e) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    setRipples(prev => ({
      ...prev,
      [path]: { x, y }
    }));

    setTimeout(() => {
      setRipples(prev => ({
        ...prev,
        [path]: null
      }));
    }, 600);

    navigate(path);
  };

  return (
    <div style={{ marginBottom: '40px' }}>
      <h2 style={{
        margin: '0 0 20px 0',
        fontSize: '20px',
        fontWeight: 800,
        color: '#1F2937',
        fontFamily: 'Poppins, sans-serif'
      }}>
        {t('dashboard.quickActions')}
      </h2>
      
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
        gap: '16px'
      }}>
        {actions.map((action, idx) => {
          const Icon = action.icon;
          return (
            <button
              key={idx}
              onClick={(e) => handleClick(action.path, e)}
              style={{
                background: action.gradient,
                border: 'none',
                borderRadius: '16px',
                padding: '32px 24px',
                cursor: 'pointer',
                color: 'white',
                boxShadow: '0 12px 32px rgba(99, 102, 241, 0.2)',
                transition: 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)',
                animation: `slideUp 0.5s ease-out ${idx * 0.1}s both`,
                position: 'relative',
                overflow: 'hidden',
                fontFamily: 'Poppins, sans-serif'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-8px) scale(1.05)';
                e.currentTarget.style.boxShadow = '0 20px 48px rgba(99, 102, 241, 0.4)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0) scale(1)';
                e.currentTarget.style.boxShadow = '0 12px 32px rgba(99, 102, 241, 0.2)';
              }}>
              
              {/* Ripple Effect */}
              {ripples[action.path] && (
                <div
                  style={{
                    position: 'absolute',
                    left: ripples[action.path].x,
                    top: ripples[action.path].y,
                    width: '20px',
                    height: '20px',
                    borderRadius: '50%',
                    backgroundColor: 'rgba(255, 255, 255, 0.5)',
                    transform: 'translate(-50%, -50%)',
                    pointerEvents: 'none',
                    animation: 'ripple 0.6s ease-out'
                  }}
                />
              )}

              <div style={{ textAlign: 'center', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '12px' }}>
                <Icon size={32} />
                <span style={{ fontSize: '15px', fontWeight: 700 }}>
                  {action.label}
                </span>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
