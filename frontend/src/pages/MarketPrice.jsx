import React, { useState, useEffect } from 'react';
import { useLanguage } from '../hooks/useLanguage';
import { getMarketPrices } from '../services/api';
import { formatCurrencyForLanguage, formatDateForLanguage } from '../utils/device';
import { Store, TrendingUp, TrendingDown, Minus, Loader2, Search } from 'lucide-react';
import '../styles/MarketPrice.css';

export default function MarketPrice() {
  const { t, lang } = useLanguage();
  const [prices, setPrices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    getMarketPrices()
      .then((r) => setPrices(r.data.results || []))
      .catch(() => setPrices([]))
      .finally(() => setLoading(false));
  }, []);

  const filtered = prices.filter((p) =>
    p.commodity_name.toLowerCase().includes(search.toLowerCase())
  );

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'up':
        return <TrendingUp size={18} />;
      case 'down':
        return <TrendingDown size={18} />;
      default:
        return <Minus size={18} />;
    }
  };

  const getTrendLabel = (trend) => {
    switch (trend) {
      case 'up':
        return t('market.trendUp');
      case 'down':
        return t('market.trendDown');
      default:
        return t('market.trendStable');
    }
  };

  const getUnitLabel = (unit) => {
    if (!unit) return '';
    const unitMap = {
      'kg': t('market.units.kg'),
      'g': t('market.units.g'),
      'liter': t('market.units.liter'),
      'litre': t('market.units.liter'),
      'piece': t('market.units.piece'),
      'dozen': t('market.units.dozen'),
      'ton': 'ton',
      'quintal': 'quintal',
    };
    return unitMap[unit?.toLowerCase()] || unit;
  };

  const getCommodityName = (commodityName) => {
    if (!commodityName) return '';
    const comKey = commodityName.toLowerCase();
    const comMap = {
      'banana': 'banana',
      'chili': 'chili',
      'chili powder': 'chili',
      'coconut': 'coconut',
      'coriander': 'coriander',
      'coriander powder': 'coriander',
      'ghee': 'ghee',
      'mango': 'mango',
      'milk': 'milk',
      'onion': 'onion',
    };
    const key = comMap[comKey];
    if (key) return t(`market.commodities.${key}`);
    return commodityName;
  };

  const getMarketName = (marketLocation) => {
    if (!marketLocation) return '';
    const marKey = marketLocation.toLowerCase().replace(/\s+/g, '_');
    const marMap = {
      'chennai_fruit_market': 'chennai',
      'guntur_mandi': 'guntur',
      'kerala_mandi': 'kerala',
      'rajasthan_mandi': 'rajasthan',
      'tamil_nadu_dairy': 'tamil_dairy',
      'madurai_fruit_market': 'madurai',
      'delhi_dairy': 'delhi_dairy',
      'delhi_mandi': 'delhi_mandi',
    };
    const key = marMap[marKey];
    if (key) return t(`market.markets.${key}`);
    return marketLocation;
  };

  const trendColor = { up: '#10b981', down: '#ef4444', stable: '#f59e0b' };
  const trendBg = { up: '#ecfdf5', down: '#fef2f2', stable: '#fffbeb' };

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(180deg, var(--bg-light) 0%, var(--white) 100%)', 
      padding: '20px',
      paddingBottom: '120px'
    }}>
      {/* Header */}
      <div style={{ 
        background: 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)',
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
              <Store size={28} />
            </div>
            <div>
              <h1 style={{ fontSize: 'var(--font-2xl)', fontWeight: 'var(--font-bold)', margin: '0', lineHeight: '1.2' }}>{t('market.title')}</h1>
              <p style={{ fontSize: 'var(--font-base)', opacity: '0.9', margin: '4px 0 0 0' }}>
                {t('market.today')} • {formatDateForLanguage(new Date().toISOString().split('T')[0], lang)}
              </p>
            </div>
          </div>
        </div>
        
        {/* Total Card */}
        <div style={{ background: 'rgba(255,255,255,0.1)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '14px', padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <span style={{ fontSize: 'var(--font-xs)', opacity: '0.9', textTransform: 'uppercase', letterSpacing: '0.5px' }}>{t('market.noData')}</span>
            <div style={{ fontSize: '24px', fontWeight: 'var(--font-bold)', marginTop: '4px' }}>{filtered.length} {t('common.entries')}</div>
          </div>
        </div>
      </div>

      {/* Search Bar */}
      <div style={{ 
        marginBottom: '24px', 
        display: 'flex', 
        alignItems: 'center', 
        gap: '12px',
        background: 'rgba(255,255,255,0.7)',
        backdropFilter: 'blur(20px)',
        border: '1px solid rgba(255,255,255,0.5)',
        borderRadius: 'var(--radius-lg)',
        padding: '12px 16px',
        boxShadow: '0 4px 16px rgba(0, 0, 0, 0.08)'
      }}>
        <Search size={18} style={{ color: 'var(--accent)' }} />
        <input
          type="search"
          placeholder={t('market.searchPlaceholder')}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={{ 
            flex: 1, 
            minHeight: '40px',
            border: 'none',
            background: 'transparent',
            fontSize: 'var(--font-base)',
            color: 'var(--gray-900)',
            outline: 'none'
          }}
        />
      </div>

      {/* List */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '48px 16px' }}>
          <Loader2 size={32} className="animate-spin" style={{ margin: '0 auto', color: '#f59e0b' }} />
          <p style={{ marginTop: '16px', color: 'var(--gray-600)', fontSize: 'var(--font-base)' }}>{t('common.loading')}</p>
        </div>
      ) : filtered.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '48px 16px', background: 'white', borderRadius: 'var(--radius-lg)', border: '2px dashed var(--gray-300)' }}>
          <Store size={48} style={{ margin: '0 auto', color: '#f59e0b', opacity: 0.3, marginBottom: '12px' }} />
          <p style={{ fontSize: 'var(--font-lg)', color: 'var(--gray-600)', margin: '0' }}>{t('market.noRecords')}</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))', gap: '16px' }}>
          {filtered.map((p, idx) => {
            const trend = p.trend || 'stable';
            return (
              <div 
                key={p.id} 
                style={{
                  background: 'rgba(255,255,255,0.7)',
                  backdropFilter: 'blur(20px)',
                  border: '1px solid rgba(255,255,255,0.5)',
                  borderRadius: 'var(--radius-lg)',
                  padding: '20px',
                  boxShadow: '0 8px 32px rgba(0, 0, 0, 0.08)',
                  animation: `slideUp ${0.3 + idx * 0.05}s ease`,
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
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px', flex: 1 }}>
                    <div style={{ background: 'linear-gradient(135deg, #fef3c7 0%, #fed7aa 100%)', padding: '10px 12px', borderRadius: 'var(--radius-md)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                      <Store size={20} style={{ color: '#f59e0b' }} />
                    </div>
                    <div>
                      <h3 style={{ margin: '0', fontSize: 'var(--font-lg)', fontWeight: 700, color: 'var(--gray-900)' }}>
                        {getCommodityName(p.commodity_name)}
                      </h3>
                      <p style={{ margin: '4px 0 0', fontSize: 'var(--font-sm)', color: 'var(--gray-600)' }}>
                        {getMarketName(p.market_location)}
                      </p>
                    </div>
                  </div>
                  <div style={{
                    background: trendBg[trend],
                    color: trendColor[trend],
                    padding: '6px 12px',
                    borderRadius: 'var(--radius-md)',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '4px',
                    fontSize: 'var(--font-xs)',
                    fontWeight: 700,
                    whiteSpace: 'nowrap'
                  }}>
                    {getTrendIcon(trend)}
                    {getTrendLabel(trend)}
                  </div>
                </div>

                {/* Price and Unit */}
                <div style={{ borderTop: '1px solid rgba(0, 0, 0, 0.1)', paddingTop: '12px', marginTop: '12px' }}>
                  <p style={{ margin: '0 0 8px', fontSize: 'var(--font-sm)', color: 'var(--gray-600)', fontWeight: 600, textTransform: 'uppercase' }}>
                    {t('market.currentPrice')}
                  </p>
                  <div style={{ display: 'flex', alignItems: 'flex-end', gap: '8px' }}>
                    <p style={{ margin: '0', fontSize: 'var(--font-2xl)', fontWeight: 700, color: '#f59e0b' }}>
                      {formatCurrencyForLanguage(p.price, lang)}
                    </p>
                    <p style={{ margin: '0 0 4px', fontSize: 'var(--font-base)', color: 'var(--gray-600)', fontWeight: 600 }}>
                      /{getUnitLabel(p.unit)}
                    </p>
                  </div>
                </div>

                {/* Date */}
                <p style={{ margin: '12px 0 0', fontSize: 'var(--font-xs)', color: 'var(--gray-500)', fontStyle: 'italic' }}>
                  {t('market.updated')} {formatDateForLanguage(p.market_date, lang)}
                </p>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

