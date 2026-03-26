import React, { useState, useEffect } from 'react';
import { useLanguage } from '../hooks/useLanguage';
import { getDashboard } from '../services/api';
import { Loader2, Activity } from 'lucide-react';
import DashboardHeader from '../components/DashboardHeader';
import SummaryCards from '../components/SummaryCards';
import QuickActionsGrid from '../components/QuickActionsGrid';
import ChartsSection from '../components/ChartsSection';
import FloatingVoiceButton from '../components/FloatingVoiceButton';
import FloatingBackground from '../components/FloatingBackground';
import '../styles/DashboardAnimations.css';

export default function Dashboard() {
  const { t, lang } = useLanguage();
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getDashboard()
      .then((r) => setSummary(r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div 
      className="bg-gradient-page"
      style={{
        minHeight: '100vh',
        paddingBottom: '120px',
        position: 'relative',
        animation: 'pageEnter 0.8s ease-out'
      }}>
      
      {/* Floating Background Elements */}
      <FloatingBackground />

      {/* Header */}
      <DashboardHeader />

      {/* Main Content */}
      <div style={{
        maxWidth: '1400px',
        margin: '0 auto',
        padding: '32px 24px',
        position: 'relative',
        zIndex: 1
      }}>
        {loading ? (
          <div style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            minHeight: '400px'
          }}>
            <div style={{ textAlign: 'center' }}>
              <Loader2 
                size={48} 
                className="animate-spin" 
                style={{
                  margin: '0 auto',
                  color: '#6366F1',
                  marginBottom: '16px'
                }} 
              />
              <p style={{ color: '#6B7280', fontWeight: 500 }}>
                {t('common.loading')}
              </p>
            </div>
          </div>
        ) : summary ? (
          <>
            {/* Summary Cards */}
            <SummaryCards summary={summary} lang={lang} />

            {/* Quick Actions */}
            <QuickActionsGrid />

            {/* Charts Section */}
            <ChartsSection summary={summary} />

            {/* Floating Stats Card */}
            <div 
              className="animate-slide-up"
              style={{
                background: 'rgba(255, 255, 255, 0.8)',
                backdropFilter: 'blur(20px)',
                border: '1px solid rgba(255, 255, 255, 0.4)',
                borderRadius: '20px',
                padding: '28px',
                boxShadow: '0 8px 32px rgba(0, 0, 0, 0.08)',
                marginTop: '32px'
              }}>
              <h3 style={{
                margin: '0 0 24px 0',
                fontSize: '18px',
                fontWeight: 700,
                color: '#1F2937',
                fontFamily: 'Poppins, sans-serif'
              }}>
                {t('dashboard.performanceSummary') || 'Performance Summary'}
              </h3>
              <div style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '16px'
              }}>
                <div style={{
                  background: 'rgba(34, 197, 94, 0.1)',
                  padding: '20px',
                  borderRadius: '12px',
                  borderLeft: '4px solid #22C55E'
                }}>
                  <p style={{ margin: '0 0 8px 0', fontSize: '12px', color: '#6B7280', fontWeight: 600 }}>
                    {t('dashboard.todaysGrowth') || "Today's Growth"}
                  </p>
                  <p style={{ margin: 0, fontSize: '20px', fontWeight: 800, color: '#22C55E' }}>
                    +12.5%
                  </p>
                </div>
                <div style={{
                  background: 'rgba(99, 102, 241, 0.1)',
                  padding: '20px',
                  borderRadius: '12px',
                  borderLeft: '4px solid #6366F1'
                }}>
                  <p style={{ margin: '0 0 8px 0', fontSize: '12px', color: '#6B7280', fontWeight: 600 }}>
                    {t('dashboard.monthTargetAchievement') || 'Month Target Achievement'}
                  </p>
                  <p style={{ margin: 0, fontSize: '20px', fontWeight: 800, color: '#6366F1' }}>
                    87%
                  </p>
                </div>
                <div style={{
                  background: 'rgba(245, 158, 11, 0.1)',
                  padding: '20px',
                  borderRadius: '12px',
                  borderLeft: '4px solid #F59E0B'
                }}>
                  <p style={{ margin: '0 0 8px 0', fontSize: '12px', color: '#6B7280', fontWeight: 600 }}>
                    {t('dashboard.efficiencyScore') || 'Efficiency Score'}
                  </p>
                  <p style={{ margin: 0, fontSize: '20px', fontWeight: 800, color: '#F59E0B' }}>
                    94/100
                  </p>
                </div>
              </div>
            </div>
          </>
        ) : (
          <div style={{
            textAlign: 'center',
            padding: '64px 24px',
            background: 'rgba(255, 255, 255, 0.8)',
            borderRadius: '20px',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(255, 255, 255, 0.4)'
          }}>
            <Activity 
              size={48} 
              style={{
                margin: '0 auto 16px',
                color: '#6366F1',
                opacity: 0.3
              }} 
            />
            <p style={{
              fontSize: '16px',
              color: '#6B7280',
              margin: '0',
              fontWeight: 500
            }}>
              {t('common.error')}
            </p>
          </div>
        )}
      </div>

      {/* Floating Voice Button */}
      <FloatingVoiceButton />
    </div>
  );
}
