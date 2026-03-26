import React, { useState, useEffect } from 'react';
import { useLanguage } from '../hooks/useLanguage';
import { getProfit } from '../services/api';
import { formatCurrencyForLanguage } from '../utils/device';
import { BarChart3, TrendingUp, TrendingDown, Percent, Loader2, PieChart } from 'lucide-react';
import '../styles/Profit.css';

export default function Profit() {
  const { t, lang } = useLanguage();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [period, setPeriod] = useState('monthly');

  useEffect(() => {
    setLoading(true);
    getProfit(period)
      .then((r) => setData(r.data))
      .catch(() => setData(null))
      .finally(() => setLoading(false));
  }, [period]);

  const fmt = (v) => formatCurrencyForLanguage(v || 0, lang);
  const isProfit = data && parseFloat(data.net_profit) >= 0;

  const PERIODS = [
    { key: 'today', label: t('common.today') },
    { key: 'weekly', label: t('common.thisWeek') },
    { key: 'monthly', label: t('common.thisMonth') },
    { key: 'yearly', label: t('common.thisYear') },
  ];

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(180deg, var(--bg-light) 0%, var(--white) 100%)', 
      padding: '20px',
      paddingBottom: '100px'
    }}>
      {/* Header */}
      <div style={{ 
        background: isProfit ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)' : 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
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
              <PieChart size={28} />
            </div>
            <div>
              <h1 style={{ fontSize: 'var(--font-2xl)', fontWeight: 'var(--font-bold)', margin: '0', lineHeight: '1.2' }}>{t('profit.title')}</h1>
              {data && (
                <p style={{ fontSize: 'var(--font-base)', opacity: '0.9', margin: '4px 0 0 0' }}>
                  {isProfit ? '📈 ' : '💪 '} {fmt(Math.abs(parseFloat(data.net_profit)))}
                </p>
              )}
            </div>
          </div>
        </div>
        
        {/* Total Card */}
        <div style={{ background: 'rgba(255,255,255,0.1)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '14px', padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <span style={{ fontSize: 'var(--font-xs)', opacity: '0.9', textTransform: 'uppercase', letterSpacing: '0.5px' }}>{isProfit ? t('profit.netProfit') : t('profit.netLoss')}</span>
            <div style={{ fontSize: '28px', fontWeight: 'var(--font-bold)', marginTop: '4px' }}>{fmt(Math.abs(parseFloat(data?.net_profit || 0)))}</div>
          </div>
        </div>
      </div>

      {/* Period Selector */}
      <div style={{ display: 'flex', gap: '8px', marginBottom: '24px', flexWrap: 'wrap' }}>
        {PERIODS.map((p, idx) => (
          <button
            key={p.key}
            onClick={() => setPeriod(p.key)}
            style={{
              padding: '10px 16px',
              borderRadius: 'var(--radius-full)',
              border: period === p.key ? 'none' : '2px solid var(--gray-300)',
              background: period === p.key ? (isProfit ? '#10b981' : '#ef4444') : 'white',
              color: period === p.key ? 'white' : 'var(--gray-900)',
              fontWeight: 600,
              cursor: 'pointer',
              fontSize: 'var(--font-base)',
              minHeight: '40px',
              whiteSpace: 'nowrap',
              transition: 'all 0.3s ease',
              backdropFilter: period === p.key ? 'blur(10px)' : 'none',
              boxShadow: period === p.key ? '0 4px 16px rgba(0, 0, 0, 0.1)' : 'none',
              animation: `slideUp ${0.3 + idx * 0.05}s ease`
            }}
          >
            {p.label}
          </button>
        ))}
      </div>

      {/* Content */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '48px 16px' }}>
          <Loader2 size={32} className="animate-spin" style={{ margin: '0 auto', color: 'var(--primary)' }} />
          <p style={{ marginTop: '16px', color: 'var(--gray-600)', fontSize: 'var(--font-base)' }}>{t('common.loading')}</p>
        </div>
      ) : !data ? (
        <div style={{ textAlign: 'center', padding: '48px 16px', background: 'white', borderRadius: 'var(--radius-lg)', border: '2px dashed var(--gray-300)' }}>
          <BarChart3 size={48} style={{ margin: '0 auto', color: 'var(--primary)', opacity: 0.3, marginBottom: '12px' }} />
          <p style={{ fontSize: 'var(--font-lg)', color: 'var(--gray-600)', margin: '0' }}>{t('errors.noData')}</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '16px' }}>
          {/* Stats Cards */}
          {[
            { label: t('dashboard.monthlyIncome'), value: fmt(data.total_income), icon: TrendingUp, color: '#10b981', bgColor: '#ecfdf5' },
            { label: t('dashboard.monthlyExpense'), value: fmt(data.total_expense), icon: TrendingDown, color: '#ef4444', bgColor: '#fef2f2' },
            { label: t('profit.profitMargin'), value: `${data.profit_margin || 0}%`, icon: Percent, color: '#3b82f6', bgColor: '#eff6ff' },
            { label: t('profit.dailyAverage'), value: fmt(data.daily_average_profit), icon: BarChart3, color: '#f59e0b', bgColor: '#fffbeb' },
          ].map((s, i) => {
            const Icon = s.icon;
            return (
              <div 
                key={i} 
                style={{
                  background: 'rgba(255,255,255,0.7)',
                  backdropFilter: 'blur(20px)',
                  border: '1px solid rgba(255,255,255,0.5)',
                  borderRadius: 'var(--radius-lg)',
                  padding: '20px',
                  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.08)',
                  animation: `slideUp ${0.3 + i * 0.1}s ease`,
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
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '12px' }}>
                  <div style={{ background: s.bgColor, padding: '10px 12px', borderRadius: 'var(--radius-md)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                    <Icon size={20} style={{ color: s.color }} />
                  </div>
                  <span style={{ fontSize: 'var(--font-sm)', color: 'var(--gray-700)', fontWeight: 600 }}>{s.label}</span>
                </div>
                <p style={{ margin: '0', fontSize: 'var(--font-2xl)', fontWeight: 700, color: s.color }}>
                  {s.value}
                </p>
              </div>
            );
          })}

          {/* Summary Card - Full Width */}
          <div 
            style={{ 
              gridColumn: '1 / -1',
              background: 'rgba(255,255,255,0.7)',
              backdropFilter: 'blur(20px)',
              border: '1px solid rgba(255,255,255,0.5)',
              borderRadius: 'var(--radius-lg)',
              overflow: 'hidden',
              boxShadow: '0 8px 32px rgba(0, 0, 0, 0.08)',
              animation: 'slideUp 0.6s ease'
            }}
          >
            <div style={{ background: isProfit ? '#ecfdf5' : '#fef2f2', borderBottom: '1px solid rgba(0, 0, 0, 0.1)', padding: '20px' }}>
              <h3 style={{ 
                margin: '0', 
                color: isProfit ? '#10b981' : '#ef4444',
                fontSize: 'var(--font-lg)', 
                fontWeight: 700 
              }}>
                {isProfit ? t('profit.profitSummary') : t('profit.lossSummary')}
              </h3>
            </div>
            <div style={{ padding: '20px' }}>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '16px', marginBottom: '20px' }}>
                <div>
                  <p style={{ margin: '0 0 8px', fontSize: 'var(--font-sm)', color: 'var(--gray-600)', fontWeight: 600 }}>
                    {t('dashboard.monthlyIncome')}
                  </p>
                  <p style={{ margin: '0', fontSize: 'var(--font-2xl)', fontWeight: 700, color: '#10b981' }}>
                    {fmt(data.total_income)}
                  </p>
                </div>
                <div>
                  <p style={{ margin: '0 0 8px', fontSize: 'var(--font-sm)', color: 'var(--gray-600)', fontWeight: 600 }}>
                    {t('dashboard.monthlyExpense')}
                  </p>
                  <p style={{ margin: '0', fontSize: 'var(--font-2xl)', fontWeight: 700, color: '#ef4444' }}>
                    {fmt(data.total_expense)}
                  </p>
                </div>
                <div>
                  <p style={{ margin: '0 0 8px', fontSize: 'var(--font-sm)', color: 'var(--gray-600)', fontWeight: 600 }}>
                    {isProfit ? t('profit.netProfit') : t('profit.netLoss')}
                  </p>
                  <p style={{ margin: '0', fontSize: 'var(--font-2xl)', fontWeight: 700, color: isProfit ? '#10b981' : '#ef4444' }}>
                    {fmt(Math.abs(parseFloat(data.net_profit)))}
                  </p>
                </div>
              </div>

              {/* Progress Bar */}
              <div style={{ borderTop: '1px solid var(--gray-200)', paddingTop: '16px' }}>
                <p style={{ margin: '0 0 12px', fontSize: 'var(--font-sm)', fontWeight: 600, color: 'var(--gray-900)' }}>
                  {t('profit.incomeVsExpense')}
                </p>
                {[
                  { label: t('dashboard.monthlyIncome'), val: parseFloat(data.total_income), color: '#10b981' },
                  { label: t('dashboard.monthlyExpense'), val: parseFloat(data.total_expense), color: '#ef4444' },
                ].map((bar, i) => {
                  const max = Math.max(parseFloat(data.total_income), parseFloat(data.total_expense), 1);
                  const pct = Math.min((bar.val / max) * 100, 100);
                  return (
                    <div key={i} style={{ marginBottom: i === 0 ? '12px' : 0 }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                        <span style={{ fontSize: 'var(--font-sm)', color: 'var(--gray-700)' }}>{bar.label}</span>
                        <span style={{ fontSize: 'var(--font-sm)', fontWeight: 700, color: bar.color }}>{fmt(bar.val)}</span>
                      </div>
                      <div style={{ height: 8, background: 'var(--gray-200)', borderRadius: 'var(--radius-full)', overflow: 'hidden' }}>
                        <div style={{ width: `${pct}%`, height: '100%', background: bar.color, borderRadius: 'var(--radius-full)', transition: 'width 0.8s ease' }} />
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
