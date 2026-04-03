import React, { useState, useEffect, useCallback } from 'react';
import { useLanguage } from '../hooks/useLanguage';
import { getIncome, addIncome } from '../services/api';
import { formatCurrencyForLanguage, formatDateForLanguage, getTodayString } from '../utils/device';
import { TrendingUp, Plus, X, Loader2, Trash2 } from 'lucide-react';
import '../styles/DataPage.css';
import '../styles/Income.css';

// Income categories - use their keys for translation (must match backend Income model choices)
const INCOME_CATEGORY_KEYS = ['sales', 'service', 'loan', 'grant', 'investment', 'other'];

function getIncomeCategoryTranslations(t) {
  return INCOME_CATEGORY_KEYS.map(key => ({
    key,
    label: t(`common.categories.${key}`)
  }));
}

export default function Income() {
  const { t, lang } = useLanguage();
  const incomeCategoryOptions = getIncomeCategoryTranslations(t);
  const [records, setRecords] = useState([]);
  const [total, setTotal] = useState('0');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [notification, setNotification] = useState(null);
  const [filterPeriod, setFilterPeriod] = useState('monthly');
  const [form, setForm] = useState({
    amount: '',
    source: '',
    category: 'sales',
    date: getTodayString(),
    description: '',
  });

  const fetchRecords = useCallback(() => {
    setLoading(true);
    getIncome({ period: filterPeriod })
      .then((r) => {
        setRecords(r.data.results || []);
        setTotal(r.data.total || '0');
      })
      .catch(() => showNotification(t('errors.serverError'), 'error'))
      .finally(() => setLoading(false));
  }, [filterPeriod]);

  useEffect(() => {
    fetchRecords();
  }, [fetchRecords]);

  const showNotification = (msg, type = 'success') => {
    setNotification({ msg, type });
    setTimeout(() => setNotification(null), 3000);
  };

  const handleSubmit = async () => {
    if (!form.amount || !form.source) {
      showNotification(t('income.required_field'), 'error');
      return;
    }
    setSaving(true);
    try {
      await addIncome(form);
      setForm({ amount: '', source: '', category: 'sales', date: getTodayString(), description: '' });
      setShowForm(false);
      await fetchRecords();
      showNotification(t('common.success'));
    } catch (e) {
      showNotification(e.message || t('errors.serverError'), 'error');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(180deg, var(--bg-light) 0%, var(--white) 100%)', padding: '20px' }}>
      {/* Header */}
      <div style={{ background: 'var(--gradient-primary)', borderRadius: 'var(--radius-lg)', padding: '24px', marginBottom: '24px', color: 'white', boxShadow: 'var(--shadow-lg)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ width: '60px', height: '60px', background: 'rgba(255,255,255,0.2)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', backdropFilter: 'blur(10px)' }}>
              <TrendingUp size={28} />
            </div>
            <div>
              <h1 style={{ fontSize: 'var(--font-2xl)', fontWeight: 'var(--font-bold)', margin: '0', lineHeight: '1.2' }}>{t('income.title')}</h1>
              <p style={{ fontSize: 'var(--font-sm)', opacity: '0.9', margin: '4px 0 0 0' }}>{t('income.track')}</p>
            </div>
          </div>
          <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
            {showForm ? <X size={18} /> : <Plus size={18} />}
            {showForm ? t('common.cancel') : t('income.addIncome')}
          </button>
        </div>
        
        {/* Total Card */}
        <div style={{ background: 'rgba(255,255,255,0.1)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '14px', padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <span style={{ fontSize: 'var(--font-xs)', opacity: '0.9', textTransform: 'uppercase', letterSpacing: '0.5px' }}>{t('income.totalIncome')}</span>
            <div style={{ fontSize: '28px', fontWeight: 'var(--font-bold)', marginTop: '4px' }}>{formatCurrencyForLanguage(total, lang)}</div>
          </div>
        </div>
      </div>

      {/* Notification */}
      {notification && (
        <div className={`alert alert-${notification.type}`} style={{ marginBottom: '16px', animation: 'slideUp var(--transition-base)' }}>
          <div>{notification.msg}</div>
        </div>
      )}

      {/* Form */}
      {showForm && (
        <div className="card" style={{ marginBottom: '24px', animation: 'slideUp var(--transition-base)' }}>
          <h3 className="card-header">{t('income.addIncome')}</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '20px' }}>
            <div className="form-group">
              <label className="form-label form-label-required">{t('income.source')}</label>
              <input type="text" className="form-input" placeholder={t('income.sourcePlaceholder')} value={form.source} onChange={(e) => setForm({...form, source: e.target.value})} />
            </div>
            <div className="form-group">
              <label className="form-label">{t('income.category')}</label>
              <select className="form-select" value={form.category} onChange={(e) => setForm({...form, category: e.target.value})}>
                {incomeCategoryOptions.map(cat => <option key={cat.key} value={cat.key}>{cat.label}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label form-label-required">{t('income.amount')}</label>
              <input type="number" className="form-input" placeholder={t('common.amount')} min="0" step="0.01" value={form.amount} onChange={(e) => setForm({...form, amount: e.target.value})} />
            </div>
            <div className="form-group">
              <label className="form-label">{t('income.date')}</label>
              <input type="date" className="form-input" value={form.date} onChange={(e) => setForm({...form, date: e.target.value})} />
            </div>
            <div className="form-group" style={{ gridColumn: '1 / -1' }}>
              <label className="form-label">{t('income.description')}</label>
              <textarea className="form-textarea" placeholder={t('income.descriptionPlaceholder')} value={form.description} onChange={(e) => setForm({...form, description: e.target.value})} />
            </div>
          </div>
          <button className="btn btn-primary btn-full" onClick={handleSubmit} disabled={saving || !form.amount}>
            {saving ? <><Loader2 size={16} className="animate-spin" /> {t('income.savingMsg')}</> : t('income.recordBtn')}
          </button>
        </div>
      )}

      {/* Controls */}
      <div style={{ display: 'flex', gap: '12px', marginBottom: '20px', flexWrap: 'wrap' }}>
        <select className="form-select" value={filterPeriod} onChange={(e) => setFilterPeriod(e.target.value)} style={{ maxWidth: '200px' }}>
          <option value="daily">{t('income.today')}</option>
          <option value="weekly">{t('income.weekly')}</option>
          <option value="monthly">{t('income.monthly')}</option>
          <option value="all">{t('income.all')}</option>
        </select>
      </div>

      {/* Records */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '60px 20px' }}>
          <Loader2 size={40} className="animate-spin" style={{ color: 'var(--primary)' }} />
          <p style={{ marginTop: '16px', color: 'var(--text-medium)' }}>{t('income.loadingMsg')}</p>
        </div>
      ) : records.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '60px 20px' }}>
          <TrendingUp size={48} style={{ color: 'var(--text-light)', marginBottom: '16px' }} />
          <h3 style={{ color: 'var(--text-dark)' }}>{t('income.noRecords')}</h3>
          <p style={{ color: 'var(--text-light)', marginTop: '8px' }}>{t('income.emptyMsg')}</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gap: '12px' }}>
          {records.map(r => (
            <div key={r.id} className="card" style={{ padding: '16px', cursor: 'pointer', transition: 'all var(--transition-base)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 'var(--font-semibold)', fontSize: 'var(--font-base)', color: 'var(--text-dark)' }}>{r.source}</div>
                  <div style={{ fontSize: 'var(--font-xs)', color: 'var(--text-light)', marginTop: '4px' }}>
                    {r.category} • {formatDateForLanguage(r.date, lang)}
                  </div>
                </div>
                <span style={{ fontSize: 'var(--font-lg)', fontWeight: 'var(--font-bold)', color: 'var(--success)' }}>+{formatCurrencyForLanguage(r.amount, lang)}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

