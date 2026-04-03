import React, { useState, useEffect } from 'react';
import { useLanguage } from '../hooks/useLanguage';
import { getSchemes } from '../services/api';
import { ClipboardList, Loader2, ChevronDown, Tag, BookOpen, ExternalLink } from 'lucide-react';
import '../styles/Schemes.css';

const CATEGORY_KEYS = {
  loan: 'schemes.categories.loan',
  subsidy: 'schemes.categories.subsidy',
  training: 'schemes.categories.training',
  insurance: 'schemes.categories.insurance',
  market_linkage: 'schemes.categories.market_linkage',
  technology: 'schemes.categories.technology'
};

export default function Schemes() {
  const { t, language } = useLanguage();
  const [schemes, setSchemes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [expanded, setExpanded] = useState(null);

  // Agency name translation mapping
  const translateAgency = (agency) => {
    if (!agency) return 'N/A';
    
    const agencyMap = {
      'Ministry of Agriculture & Horticulture': {
        en: 'Ministry of Agriculture & Horticulture',
        hi: 'कृषि और बागवानी मंत्रालय',
        ta: 'விவசாயம் மற்றும் தோட்டக்கலை அமைப்பு'
      },
      'Ministry of Rural Development': {
        en: 'Ministry of Rural Development',
        hi: 'ग्रामीण विकास मंत्रालय',
        ta: 'கிராம வளர்ச்சி அமைப்பு'
      },
      'Ministry of Finance': {
        en: 'Ministry of Finance',
        hi: 'वित्त मंत्रालय',
        ta: 'நிதி அமைப்பு'
      },
      'Ministry of Labor & Employment': {
        en: 'Ministry of Labor & Employment',
        hi: 'श्रम और रोजगार मंत्रालय',
        ta: 'தொழிலாளர் மற்றும் வேலைவாய்ப்பு அமைப்பு'
      },
      'Ministry of MSME': {
        en: 'Ministry of MSME',
        hi: 'सूक्ष्म, लघु और मध्यम उद्यम मंत्रालय',
        ta: 'சிறு, நடு மற்றும் நடுநிலை தொழிலுறவு அமைப்பு'
      },
      'Ministry of Women & Child Development': {
        en: 'Ministry of Women & Child Development',
        hi: 'महिला और बाल विकास मंत्रालय',
        ta: 'பெண்கள் மற்றும் சிறுவர் வளர்ச்சி அமைப்பு'
      },
      'Ministry of Commerce & Industry': {
        en: 'Ministry of Commerce & Industry',
        hi: 'वाणिज्य और उद्योग मंत्रालय',
        ta: 'வணிகம் மற்றும் தொழிற்சாலை அமைப்பு'
      },
      'NABARD': {
        en: 'NABARD',
        hi: 'नाबार्ड',
        ta: 'நாபார்ட்'
      },
      'SBI': {
        en: 'State Bank of India',
        hi: 'भारतीय स्टेट बैंक',
        ta: 'இந்தியா மாநில வங்கி'
      }
    };

    const mapped = agencyMap[agency];
    if (mapped) {
      return mapped[language] || agency;
    }
    
    return agency;
  };

  useEffect(() => {
    setLoading(true);
    getSchemes('', language)
      .then((r) => setSchemes(r.data.results))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [language]);

  const filtered = filter === 'all' ? schemes : schemes.filter(s => s.category === filter);
  const categories = [...new Set(schemes.map(s => s.category))];

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(180deg, var(--bg-light) 0%, var(--white) 100%)', 
      padding: '20px',
      paddingBottom: '120px'
    }}>
      {/* Header */}
      <div style={{ 
        background: 'linear-gradient(135deg, #a855f7 0%, #9333ea 100%)',
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
              <ClipboardList size={28} />
            </div>
            <div>
              <h1 style={{ fontSize: 'var(--font-2xl)', fontWeight: 'var(--font-bold)', margin: '0', lineHeight: '1.2' }}>{t('schemes.title')}</h1>
              <p style={{ fontSize: 'var(--font-base)', opacity: '0.9', margin: '4px 0 0 0' }}>{t('schemes.subtitle')}</p>
            </div>
          </div>
        </div>
        
        {/* Total Card */}
        <div style={{ background: 'rgba(255,255,255,0.1)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '14px', padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <span style={{ fontSize: 'var(--font-xs)', opacity: '0.9', textTransform: 'uppercase', letterSpacing: '0.5px' }}>{t('schemes.forYou')}</span>
            <div style={{ fontSize: '24px', fontWeight: 'var(--font-bold)', marginTop: '4px' }}>{filter === 'all' ? schemes.length : schemes.filter(s => s.category === filter).length} {t('common.entries')}</div>
          </div>
        </div>
      </div>

      {/* Category Filter */}
      <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', marginBottom: '24px', paddingBottom: '8px', scrollBehavior: 'smooth' }}>
        <button
          onClick={() => setFilter('all')}
          style={{
            padding: '10px 16px',
            borderRadius: 'var(--radius-full)',
            border: filter === 'all' ? 'none' : '2px solid var(--gray-300)',
            background: filter === 'all' ? '#a855f7' : 'white',
            color: filter === 'all' ? 'white' : 'var(--gray-900)',
            fontWeight: 600,
            cursor: 'pointer',
            fontSize: 'var(--font-base)',
            minHeight: '40px',
            whiteSpace: 'nowrap',
            transition: 'all 0.3s ease',
            backdropFilter: filter === 'all' ? 'blur(10px)' : 'none',
            boxShadow: filter === 'all' ? '0 4px 16px rgba(0, 0, 0, 0.1)' : 'none'
          }}
        >
          {t('common.all')}
        </button>
        {categories.map((cat, idx) => (
          <button
            key={cat}
            onClick={() => setFilter(cat)}
            style={{
              padding: '10px 16px',
              borderRadius: 'var(--radius-full)',
              border: filter === cat ? 'none' : '2px solid var(--gray-300)',
              background: filter === cat ? '#a855f7' : 'white',
              color: filter === cat ? 'white' : 'var(--gray-900)',
              fontWeight: 600,
              cursor: 'pointer',
              fontSize: 'var(--font-base)',
              minHeight: '40px',
              whiteSpace: 'nowrap',
              transition: 'all 0.3s ease',
              backdropFilter: filter === cat ? 'blur(10px)' : 'none',
              boxShadow: filter === cat ? '0 4px 16px rgba(0, 0, 0, 0.1)' : 'none',
              animation: `slideUp ${0.3 + idx * 0.05}s ease`
            }}
          >
            {t(CATEGORY_KEYS[cat] || `schemes.categories.${cat}`)}
          </button>
        ))}
      </div>

      {/* Content */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '48px 16px' }}>
          <Loader2 size={32} className="animate-spin" style={{ margin: '0 auto', color: '#a855f7' }} />
          <p style={{ marginTop: '16px', color: 'var(--gray-600)', fontSize: 'var(--font-base)' }}>{t('common.loading')}</p>
        </div>
      ) : filtered.length === 0 ? (
        <div style={{ textAlign: 'center', padding: '48px 16px', background: 'white', borderRadius: 'var(--radius-lg)', border: '2px dashed var(--gray-300)' }}>
          <BookOpen size={48} style={{ margin: '0 auto', color: '#a855f7', opacity: 0.3, marginBottom: '12px' }} />
          <p style={{ fontSize: 'var(--font-lg)', color: 'var(--gray-600)', margin: '0' }}>{t('schemes.noRecords')}</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: '16px' }}>
          {filtered.map((scheme, idx) => (
            <div 
              key={scheme.id} 
              style={{
                background: 'rgba(255,255,255,0.7)',
                backdropFilter: 'blur(20px)',
                border: '1px solid rgba(255,255,255,0.5)',
                borderRadius: 'var(--radius-lg)',
                overflow: 'hidden',
                animation: `slideUp ${0.3 + idx * 0.05}s ease`,
                transition: 'all 0.3s ease',
                cursor: 'pointer',
                boxShadow: '0 8px 32px rgba(0, 0, 0, 0.08)'
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
              {/* Header - Always Visible */}
              <div
                onClick={() => setExpanded(expanded === scheme.id ? null : scheme.id)}
                style={{ 
                  background: 'linear-gradient(135deg, #ede9fe 0%, #f3e8ff 100%)',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  gap: '12px',
                  userSelect: 'none',
                  padding: '16px',
                  cursor: 'pointer'
                }}
              >
                <div style={{ flex: 1 }}>
                  <h3 style={{ margin: '0 0 4px', fontSize: 'var(--font-lg)', fontWeight: 700, color: '#a855f7' }}>
                    {scheme.name}
                  </h3>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <Tag size={14} style={{ color: '#7c3aed' }} />
                    <span style={{ fontSize: 'var(--font-sm)', color: 'var(--gray-600)' }}>{t(CATEGORY_KEYS[scheme.category] || `schemes.categories.${scheme.category}`)}</span>
                  </div>
                </div>
                <ChevronDown
                  size={20}
                  style={{
                    color: '#a855f7',
                    transition: 'transform 0.3s ease',
                    transform: expanded === scheme.id ? 'rotate(180deg)' : 'rotate(0deg)',
                    flexShrink: 0,
                  }}
                />
              </div>

              {/* Details - Collapsible */}
              {expanded === scheme.id && (
                <div style={{ borderTop: '1px solid rgba(0, 0, 0, 0.1)', padding: '16px' }}>
                  {scheme.description && (
                    <div style={{ marginBottom: '12px' }}>
                      <p style={{ margin: '0 0 6px', fontSize: 'var(--font-sm)', fontWeight: 600, color: 'var(--gray-900)', textTransform: 'uppercase' }}>
                        {t('common.description')}
                      </p>
                      <p style={{ margin: '0', fontSize: 'var(--font-base)', color: 'var(--gray-700)', lineHeight: '1.6' }}>
                        {scheme.description}
                      </p>
                    </div>
                  )}

                  {scheme.eligibility && (
                    <div style={{ marginBottom: '12px' }}>
                      <p style={{ margin: '0 0 6px', fontSize: 'var(--font-sm)', fontWeight: 600, color: 'var(--gray-900)', textTransform: 'uppercase' }}>
                        {t('schemes.eligibility')}
                      </p>
                      <p style={{ margin: '0', fontSize: 'var(--font-base)', color: 'var(--gray-700)', lineHeight: '1.6' }}>
                        {scheme.eligibility}
                      </p>
                    </div>
                  )}

                  {scheme.benefits && (
                    <div style={{ marginBottom: '12px' }}>
                      <p style={{ margin: '0 0 6px', fontSize: 'var(--font-sm)', fontWeight: 600, color: 'var(--gray-900)', textTransform: 'uppercase' }}>
                        {t('schemes.benefits')}
                      </p>
                      <p style={{ margin: '0', fontSize: 'var(--font-base)', color: 'var(--gray-700)', lineHeight: '1.6' }}>
                        {scheme.benefits}
                      </p>
                    </div>
                  )}

                  {scheme.max_amount && (
                    <div style={{ marginBottom: '12px' }}>
                      <p style={{ margin: '0 0 6px', fontSize: 'var(--font-sm)', fontWeight: 600, color: 'var(--gray-900)', textTransform: 'uppercase' }}>
                        {t('schemes.maxAmount')}
                      </p>
                      <p style={{ margin: '0', fontSize: 'var(--font-lg)', fontWeight: 700, color: '#a855f7' }}>
                        {scheme.max_amount}
                      </p>
                    </div>
                  )}

                  {scheme.agency && (
                    <div style={{ marginBottom: '16px' }}>
                      <p style={{ margin: '0 0 6px', fontSize: 'var(--font-sm)', fontWeight: 600, color: 'var(--gray-900)', textTransform: 'uppercase' }}>
                        {t('schemes.agency')}
                      </p>
                      <p style={{ margin: '0', fontSize: 'var(--font-base)', color: 'var(--gray-700)' }}>
                        {translateAgency(scheme.agency)}
                      </p>
                    </div>
                  )}

                  {/* Apply Button */}
                  {scheme.url && (
                    <a
                      href={scheme.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '8px',
                        padding: '12px 20px',
                        background: 'linear-gradient(135deg, #a855f7 0%, #9333ea 100%)',
                        color: 'white',
                        fontWeight: 600,
                        borderRadius: '8px',
                        border: 'none',
                        cursor: 'pointer',
                        fontSize: 'var(--font-base)',
                        transition: 'all 0.3s ease',
                        boxShadow: '0 4px 12px rgba(168, 85, 247, 0.3)',
                      }}
                      onMouseOver={e => {
                        e.currentTarget.style.transform = 'translateY(-2px)';
                        e.currentTarget.style.boxShadow = '0 6px 16px rgba(168, 85, 247, 0.4)';
                      }}
                      onMouseOut={e => {
                        e.currentTarget.style.transform = 'translateY(0)';
                        e.currentTarget.style.boxShadow = '0 4px 12px rgba(168, 85, 247, 0.3)';
                      }}
                    >
                      {t('schemes.applyNow')}
                      <ExternalLink size={16} />
                    </a>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
