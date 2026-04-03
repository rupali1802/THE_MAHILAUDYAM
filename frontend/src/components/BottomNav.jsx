import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { useLanguage } from '../hooks/useLanguage';
import {
  LayoutDashboard,
  TrendingUp,
  TrendingDown,
  ShoppingCart,
  Mic,
  BarChart3,
  Store,
  ClipboardList,
  Users,
} from 'lucide-react';
import '../styles/BottomNav.css';

const BottomNav = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { t } = useLanguage();

  // Determine if we should hide bottom nav (e.g., on landing page)
  if (location.pathname === '/') {
    return null;
  }

  const navItems = [
    {
      path: '/dashboard',
      label: 'bottomNav.dashboard',
      icon: LayoutDashboard,
    },
    {
      path: '/income',
      label: 'bottomNav.income',
      icon: TrendingUp,
    },
    {
      path: '/expense',
      label: 'bottomNav.expense',
      icon: TrendingDown,
    },
    {
      path: '/sales',
      label: 'bottomNav.sales',
      icon: ShoppingCart,
    },
    {
      path: '/voice',
      label: 'bottomNav.voice',
      icon: Mic,
    },
    {
      path: '/profit',
      label: 'bottomNav.profit',
      icon: BarChart3,
    },
    {
      path: '/market',
      label: 'bottomNav.market',
      icon: Store,
    },
    {
      path: '/schemes',
      label: 'bottomNav.schemes',
      icon: ClipboardList,
    },
    {
      path: '/mentor',
      label: 'bottomNav.mentor',
      icon: Users,
    },
  ];

  const isActive = (itemPath) => {
    return location.pathname === itemPath || location.pathname.startsWith(itemPath + '/');
  };

  return (
    <nav className="bottom-nav">
      <div className="bottom-nav__container">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = isActive(item.path);

          return (
            <button
              key={item.path}
              className={`bottom-nav__item ${active ? 'bottom-nav__item--active' : ''}`}
              onClick={() => navigate(item.path)}
              title={t(item.label)}
            >
              <Icon size={20} className="bottom-nav__icon" />
              <span className="bottom-nav__label">{t(item.label)}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
};

export default BottomNav;
