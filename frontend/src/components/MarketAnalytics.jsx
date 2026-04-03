import React, { useState, useEffect } from 'react';
import { getRealtimeMarketAnalysis, getPriceTrends, getPriceHistory } from '../services/api';
import { useLanguage } from '../hooks/useLanguage';
import { TrendingUp, TrendingDown, AlertCircle, BarChart3, Calendar } from 'lucide-react';
import '../styles/MarketAnalytics.css';

/**
 * Real-time Market Analytics Component
 * Displays daily price updates, trends, and advanced analysis
 */
export default function MarketAnalytics() {
  const { t, lang } = useLanguage();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedCommodity, setSelectedCommodity] = useState(null);
  const [trends, setTrends] = useState(null);
  const [priceHistory, setPriceHistory] = useState([]);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    loadRealtimeAnalysis();
    // Refresh every 30 minutes
    const interval = setInterval(loadRealtimeAnalysis, 30 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const loadRealtimeAnalysis = async () => {
    try {
      setLoading(true);
      const response = await getRealtimeMarketAnalysis();
      if (response.data) {
        setAnalysis(response.data);
      }
    } catch (error) {
      console.error('Error loading real-time analysis:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadTrends = async (commodity) => {
    try {
      const response = await getPriceTrends(commodity);
      if (response.data) {
        setTrends(response.data);
        setSelectedCommodity(commodity);
      }
    } catch (error) {
      console.error('Error loading trends:', error);
    }
  };

  const loadPriceHistory = async (commodity) => {
    try {
      const response = await getPriceHistory(commodity, 30);
      if (response.data) {
        setPriceHistory(response.data.results || []);
      }
    } catch (error) {
      console.error('Error loading price history:', error);
    }
  };

  const handleCommodityClick = (commodity) => {
    setSelectedCommodity(commodity);
    setActiveTab('details');
    loadTrends(commodity);
    loadPriceHistory(commodity);
  };

  const getRecommendationColor = (recommendation) => {
    switch (recommendation) {
      case 'buy':
        return { bg: '#ecfdf5', color: '#059669', text: '📈 Buy' };
      case 'sell':
        return { bg: '#fef2f2', color: '#dc2626', text: '📉 Sell' };
      case 'hold':
        return { bg: '#fffbeb', color: '#d97706', text: '⏸ Hold' };
      default:
        return { bg: '#f3f4f6', color: '#6b7280', text: '➖ Hold' };
    }
  };

  const getTrendIcon = (trend) => {
    if (trend === 'up') return <TrendingUp size={20} color="#10b981" />;
    if (trend === 'down') return <TrendingDown size={20} color="#ef4444" />;
    return <TrendingUp size={20} color="#f59e0b" />;
  };

  if (loading && !analysis) {
    return (
      <div style={{ 
        display: 'flex', 
        justifyContent: 'center', 
        alignItems: 'center', 
        minHeight: '300px',
        color: '#6b7280'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '24px', marginBottom: '12px' }}>📊</div>
          <p>{t('common.loading') || 'Loading market analysis...'}</p>
        </div>
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', background: '#f9fafb', borderRadius: '12px' }}>
      {/* Tab Navigation */}
      <div style={{ 
        display: 'flex', 
        gap: '12px', 
        marginBottom: '24px',
        borderBottom: '1px solid #e5e7eb',
        paddingBottom: '12px',
        overflowX: 'auto'
      }}>
        <button
          onClick={() => setActiveTab('overview')}
          style={{
            padding: '8px 16px',
            background: activeTab === 'overview' ? '#3b82f6' : 'transparent',
            color: activeTab === 'overview' ? 'white' : '#6b7280',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
            fontWeight: 500,
            whiteSpace: 'nowrap',
            transition: 'all 0.3s'
          }}
        >
          📊 {t('analytics.overview')}
        </button>
        <button
          onClick={() => setActiveTab('trends')}
          style={{
            padding: '8px 16px',
            background: activeTab === 'trends' ? '#3b82f6' : 'transparent',
            color: activeTab === 'trends' ? 'white' : '#6b7280',
            border: 'none',
            borderRadius: '6px',
            cursor: 'pointer',
            fontWeight: 500,
            whiteSpace: 'nowrap',
            transition: 'all 0.3s'
          }}
        >
          📈 {t('analytics.trends')}
        </button>
        {selectedCommodity && (
          <button
            onClick={() => setActiveTab('details')}
            style={{
              padding: '8px 16px',
              background: activeTab === 'details' ? '#3b82f6' : 'transparent',
              color: activeTab === 'details' ? 'white' : '#6b7280',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontWeight: 500,
              whiteSpace: 'nowrap',
              transition: 'all 0.3s'
            }}
          >
            🔍 {t('analytics.details')}
          </button>
        )}
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && analysis && (
        <div>
          {/* Summary Cards */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
            gap: '12px',
            marginBottom: '24px'
          }}>
            <div style={{
              background: 'white',
              padding: '16px',
              borderRadius: '10px',
              borderLeft: '4px solid #10b981',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
            }}>
              <div style={{ fontSize: '12px', color: '#6b7280', marginBottom: '8px' }}>📈 {t('analytics.trendingUp')}</div>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#10b981' }}>
                {analysis.summary?.trending_up || 0}
              </div>
            </div>

            <div style={{
              background: 'white',
              padding: '16px',
              borderRadius: '10px',
              borderLeft: '4px solid #ef4444',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
            }}>
              <div style={{ fontSize: '12px', color: '#6b7280', marginBottom: '8px' }}>📉 {t('analytics.trendingDown')}</div>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#ef4444' }}>
                {analysis.summary?.trending_down || 0}
              </div>
            </div>

            <div style={{
              background: 'white',
              padding: '16px',
              borderRadius: '10px',
              borderLeft: '4px solid #f59e0b',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
            }}>
              <div style={{ fontSize: '12px', color: '#6b7280', marginBottom: '8px' }}>➖ {t('analytics.stable')}</div>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#f59e0b' }}>
                {analysis.summary?.stable || 0}
              </div>
            </div>

            <div style={{
              background: 'white',
              padding: '16px',
              borderRadius: '10px',
              borderLeft: '4px solid #3b82f6',
              boxShadow: '0 1px 3px rgba(0,0,0,0.1)'
            }}>
              <div style={{ fontSize: '12px', color: '#6b7280', marginBottom: '8px' }}>📊 {t('analytics.totalCommodities')}</div>
              <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#3b82f6' }}>
                {analysis.total_commodities || 0}
              </div>
            </div>
          </div>

          {/* Opportunities */}
          {analysis.opportunities && analysis.opportunities.length > 0 && (
            <div style={{ marginBottom: '24px' }}>
              <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px', color: '#111827' }}>
                🎯 {t('analytics.marketOpportunities')}
              </h3>
              <div style={{
                display: 'grid',
                gap: '12px',
              }}>
                {analysis.opportunities.slice(0, 5).map((opp, idx) => {
                  const recommendation = getRecommendationColor(opp.recommendation);
                  return (
                    <div
                      key={idx}
                      onClick={() => handleCommodityClick(opp.commodity_name)}
                      style={{
                        background: 'white',
                        padding: '16px',
                        borderRadius: '10px',
                        cursor: 'pointer',
                        border: '1px solid #e5e7eb',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        transition: 'all 0.3s',
                        ':hover': { boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }
                      }}
                    >
                      <div>
                        <div style={{ fontWeight: '600', color: '#111827', marginBottom: '4px' }}>
                          {opp.commodity_name}
                        </div>
                        <div style={{ fontSize: '12px', color: '#6b7280' }}>
                          Current: ₹{opp.current_price} • Trend: {opp.trend_percentage.toFixed(2)}%
                        </div>
                      </div>
                      <div style={{
                        background: recommendation.bg,
                        color: recommendation.color,
                        padding: '8px 12px',
                        borderRadius: '6px',
                        fontWeight: '600',
                        fontSize: '12px'
                      }}>
                        {recommendation.text}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}

          {/* All Commodities */}
          <div>
            <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px', color: '#111827' }}>
              📋 {t('analytics.allCommodities')}
            </h3>
            <div style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fill, minmax(250px, 1fr))',
              gap: '12px'
            }}>
              {analysis.all_analysis && analysis.all_analysis.map((item, idx) => {
                const recommendation = getRecommendationColor(item.recommendation);
                return (
                  <div
                    key={idx}
                    onClick={() => handleCommodityClick(item.commodity_name)}
                    style={{
                      background: 'white',
                      padding: '16px',
                      borderRadius: '10px',
                      cursor: 'pointer',
                      border: '1px solid #e5e7eb',
                      transition: 'all 0.3s'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '12px' }}>
                      <div style={{ fontWeight: '600', color: '#111827' }}>
                        {item.commodity_name}
                      </div>
                      {getTrendIcon(item.trend)}
                    </div>
                    <div style={{ fontSize: '14px', fontWeight: '600', marginBottom: '8px' }}>
                      ₹{item.current_price}
                    </div>
                    <div style={{
                      fontSize: '12px',
                      color: '#6b7280',
                      marginBottom: '12px',
                      lineHeight: '1.5'
                    }}>
                      7d: {item.avg_price_7d.toFixed(2)} | 30d: {item.avg_price_30d.toFixed(2)}
                    </div>
                    <div style={{
                      background: recommendation.bg,
                      color: recommendation.color,
                      padding: '6px 12px',
                      borderRadius: '6px',
                      fontWeight: '600',
                      fontSize: '11px',
                      textAlign: 'center'
                    }}>
                      {recommendation.text}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* Trends Tab */}
      {activeTab === 'trends' && analysis && (
        <div>
          <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px', color: '#111827' }}>
            Daily Price Movements
          </h3>
          <div style={{
            display: 'grid',
            gap: '12px',
          }}>
            {analysis.all_analysis && analysis.all_analysis.map((item, idx) => (
              <div
                key={idx}
                style={{
                  background: 'white',
                  padding: '16px',
                  borderRadius: '10px',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  border: '1px solid #e5e7eb'
                }}
              >
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: '600', color: '#111827', marginBottom: '4px' }}>
                    {item.commodity_name}
                  </div>
                  <div style={{ fontSize: '12px', color: '#6b7280' }}>
                    Volatility: {item.volatility_score.toFixed(1)}% • Momentum: {item.momentum_score.toFixed(1)}
                  </div>
                </div>
                <div style={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'flex-end',
                  gap: '8px'
                }}>
                  <div style={{
                    fontSize: '14px',
                    fontWeight: '600',
                    color: item.trend_percentage > 0 ? '#10b981' : item.trend_percentage < 0 ? '#ef4444' : '#f59e0b'
                  }}>
                    {item.trend_percentage > 0 ? '+' : ''}{item.trend_percentage.toFixed(2)}%
                  </div>
                  {getTrendIcon(item.trend)}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Details Tab */}
      {activeTab === 'details' && selectedCommodity && trends && (
        <div>
          <h3 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px', color: '#111827' }}>
            {selectedCommodity} - Detailed Analysis
          </h3>

          {trends.analysis && (
            <div style={{
              background: 'white',
              padding: '16px',
              borderRadius: '10px',
              marginBottom: '16px',
              border: '1px solid #e5e7eb'
            }}>
              <div style={{ fontSize: '14px', lineHeight: '1.6', color: '#374151' }}>
                {trends.analysis.insights}
              </div>
            </div>
          )}

          {/* Price Statistics */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))',
            gap: '12px',
            marginBottom: '16px'
          }}>
            <div style={{
              background: 'white',
              padding: '12px',
              borderRadius: '8px',
              border: '1px solid #e5e7eb'
            }}>
              <div style={{ fontSize: '11px', color: '#6b7280', marginBottom: '6px' }}>Current Price</div>
              <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#111827' }}>
                ₹{trends.analysis?.current_price.toFixed(2)}
              </div>
            </div>

            <div style={{
              background: 'white',
              padding: '12px',
              borderRadius: '8px',
              border: '1px solid #e5e7eb'
            }}>
              <div style={{ fontSize: '11px', color: '#6b7280', marginBottom: '6px' }}>7-Day Avg</div>
              <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#111827' }}>
                ₹{trends.analysis?.avg_price_7d.toFixed(2)}
              </div>
            </div>

            <div style={{
              background: 'white',
              padding: '12px',
              borderRadius: '8px',
              border: '1px solid #e5e7eb'
            }}>
              <div style={{ fontSize: '11px', color: '#6b7280', marginBottom: '6px' }}>30-Day Avg</div>
              <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#111827' }}>
                ₹{trends.analysis?.avg_price_30d.toFixed(2)}
              </div>
            </div>
          </div>

          {/* Price History Chart (Simple) */}
          {priceHistory.length > 0 && (
            <div style={{
              background: 'white',
              padding: '16px',
              borderRadius: '10px',
              border: '1px solid #e5e7eb'
            }}>
              <h4 style={{ fontSize: '14px', fontWeight: '600', marginBottom: '12px', color: '#111827' }}>
                Price History (Last 30 Days)
              </h4>
              <div style={{
                display: 'flex',
                alignItems: 'flex-end',
                justifyContent: 'space-around',
                height: '150px',
                gap: '4px'
              }}>
                {priceHistory.map((item, idx) => {
                  const maxPrice = Math.max(...priceHistory.map(p => parseFloat(p.price)));
                  const minPrice = Math.min(...priceHistory.map(p => parseFloat(p.price)));
                  const range = maxPrice - minPrice || 1;
                  const height = ((parseFloat(item.price) - minPrice) / range) * 100;
                  return (
                    <div
                      key={idx}
                      style={{
                        height: `${Math.max(height, 5)}%`,
                        background: '#3b82f6',
                        borderRadius: '4px 4px 0 0',
                        flex: 1,
                        transition: 'all 0.3s'
                      }}
                      title={`₹${item.price} on ${item.market_date}`}
                    />
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
