import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useLanguage } from '../hooks/useLanguage';

const NAV_ITEMS = [
  { path: '/', icon: '🏠', key: 'nav.dashboard' },
  { path: '/income', icon: '💰', key: 'nav.income' },
  { path: '/expense', icon: '💸', key: 'nav.expense' },
  { path: '/sales', icon: '🛍️', key: 'nav.sales' },
  { path: '/voice', icon: '🎤', key: 'nav.voice', highlight: true },
  { path: '/profit', icon: '📊', key: 'nav.profit' },
  { path: '/market', icon: '🌾', key: 'nav.market' },
  { path: '/schemes', icon: '📋', key: 'nav.schemes' },
];

export default function Navbar() {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <nav style={{
      position: 'fixed', bottom: 0, left: 0, right: 0,
      background: '#fff',
      borderTop: '1px solid #fce7f3',
      display: 'flex',
      zIndex: 100,
      boxShadow: '0 -4px 20px rgba(230,51,132,0.08)',
      overflowX: 'auto',
      height: 'var(--navbar-height)',
    }}>
      {NAV_ITEMS.map(item => {
        const active = location.pathname === item.path;
        return (
          <button
            key={item.path}
            onClick={() => navigate(item.path)}
            style={{
              flex: 1,
              minWidth: 52,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              gap: 2,
              padding: '6px 4px',
              background: item.highlight && active
                ? 'linear-gradient(135deg, #e63384, #be185d)'
                : item.highlight
                  ? 'linear-gradient(135deg, #f9a8d4, #fce7f3)'
                  : 'transparent',
              color: active ? '#e63384' : '#9ca3af',
              borderRadius: item.highlight ? 12 : 0,
              margin: item.highlight ? '4px 2px' : 0,
              transition: 'all 0.2s',
              fontFamily: 'inherit',
              cursor: 'pointer',
              border: 'none',
            }}
          >
            <span style={{ fontSize: 20 }}>{item.icon}</span>
            <span style={{
              fontSize: 10,
              fontWeight: active ? 600 : 400,
              color: item.highlight && active ? '#fff' : active ? '#e63384' : '#9ca3af',
              lineHeight: 1.2,
              textAlign: 'center',
            }}>
              {t(item.key)}
            </span>
          </button>
        );
      })}
    </nav>
  );
}
