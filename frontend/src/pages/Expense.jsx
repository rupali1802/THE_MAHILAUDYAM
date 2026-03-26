import React, { useState, useEffect, useCallback } from 'react';
import { useLanguage } from '../hooks/useLanguage';
import { getExpense, addExpense, deleteExpense } from '../services/api';
import { formatCurrencyForLanguage, formatDateForLanguage, getTodayString } from '../utils/device';
import { TrendingDown, Plus, X, Loader2, Trash2 } from 'lucide-react';
import '../styles/DataPage.css';
import '../styles/Expense.css';

export default function Expense() {
  const { t, lang } = useLanguage();
  const [records, setRecords] = useState([]);
  const [total, setTotal] = useState('0');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [filterPeriod, setFilterPeriod] = useState('monthly');
  const [notification, setNotification] = useState(null);
  const [form, setForm] = useState({
    amount: '',
    category: 'other',
    payment_method: 'cash',
    date: getTodayString(),
    description: '',
  });

// Expense categories - must match backend Expense model choices
  const EXPENSE_CATEGORY_KEYS = ['raw_material', 'transport', 'rent', 'electricity', 'labor', 'marketing', 'equipment', 'other'];
  
  function getExpenseCategoryTranslations(t) {
    return EXPENSE_CATEGORY_KEYS.map(key => ({
      key,
      label: t(`common.categories.${key}`)
    }));
  }

  function getPaymentMethodTranslations(t) {
    return [
      { value: 'cash', label: t('expense.paymentMethods.cash') },
      { value: 'upi', label: t('expense.paymentMethods.upi') },
      { value: 'bank_transfer', label: t('expense.paymentMethods.bank_transfer') },
      { value: 'credit', label: t('expense.paymentMethods.credit') }
    ];
  }

  const expenseCategoryOptions = getExpenseCategoryTranslations(t);
  const paymentMethodOptions = getPaymentMethodTranslations(t);

  const fetchRecords = useCallback(() => {
    setLoading(true);
    getExpense({ period: filterPeriod })
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
    if (!form.amount) {
      showNotification(t('expense.required_field'), 'error');
      return;
    }
    setSaving(true);
    try {
      await addExpense(form);
      setForm({ amount: '', category: 'other', payment_method: 'cash', date: getTodayString(), description: '' });
      setShowForm(false);
      await fetchRecords();
      showNotification(t('common.success'));
    } catch (e) {
      showNotification(e.message || t('errors.serverError'), 'error');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm(t('common.confirmDelete'))) return;
    try {
      await deleteExpense(id);
      await fetchRecords();
      showNotification(t('common.deleted'));
    } catch (e) {
      showNotification(e.message || t('errors.serverError'), 'error');
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(180deg, var(--bg-light) 0%, var(--white) 100%)', padding: '20px' }}>
      {/* Header */}
      <div style={{ background: 'linear-gradient(135deg, var(--danger) 0%, #dc2626 100%)', borderRadius: 'var(--radius-lg)', padding: '24px', marginBottom: '24px', color: 'white', boxShadow: 'var(--shadow-lg)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', flexWrap: 'wrap', gap: '12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
            <div style={{ width: '60px', height: '60px', background: 'rgba(255,255,255,0.2)', borderRadius: '12px', display: 'flex', alignItems: 'center', justifyContent: 'center', backdropFilter: 'blur(10px)' }}>
              <TrendingDown size={28} />
            </div>
            <div>
              <h1 style={{ fontSize: 'var(--font-2xl)', fontWeight: 'var(--font-bold)', margin: '0', lineHeight: '1.2' }}>{t('expense.title')}</h1>
              <p style={{ fontSize: 'var(--font-sm)', opacity: '0.9', margin: '4px 0 0 0' }}>{t('expense.track')}</p>
            </div>
          </div>
          <button className="btn btn-primary" onClick={() => setShowForm(!showForm)} style={{ background: 'rgba(255,255,255,0.2)', border: '1px solid rgba(255,255,255,0.3)', color: 'white' }}>
            {showForm ? <X size={18} /> : <Plus size={18} />}
            {showForm ? t('common.cancel') : t('expense.addExpense')}
          </button>
        </div>
        
        {/* Total Card */}
        <div style={{ background: 'rgba(255,255,255,0.1)', backdropFilter: 'blur(20px)', border: '1px solid rgba(255,255,255,0.2)', borderRadius: '14px', padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <span style={{ fontSize: 'var(--font-xs)', opacity: '0.9', textTransform: 'uppercase', letterSpacing: '0.5px' }}>{t('expense.totalExpense')}</span>
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
          <h3 className="card-header">{t('expense.addExpense')}</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '20px' }}>
            <div className="form-group">
              <label className="form-label form-label-required">{t('expense.amount')}</label>
              <input type="number" className="form-input" placeholder={t('common.amount')} min="0" step="0.01" value={form.amount} onChange={(e) => setForm({...form, amount: e.target.value})} />
            </div>
            <div className="form-group">
              <label className="form-label">{t('expense.category')}</label>
              <select className="form-select" value={form.category} onChange={(e) => setForm({...form, category: e.target.value})}>
                {expenseCategoryOptions.map(cat => <option key={cat.key} value={cat.key}>{cat.label}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">{t('expense.paymentMethod')}</label>
              <select className="form-select" value={form.payment_method} onChange={(e) => setForm({...form, payment_method: e.target.value})}>
                {paymentMethodOptions.map(method => <option key={method.value} value={method.value}>{method.label}</option>)}
              </select>
            </div>
            <div className="form-group">
              <label className="form-label">{t('expense.date')}</label>
              <input type="date" className="form-input" value={form.date} onChange={(e) => setForm({...form, date: e.target.value})} />
            </div>
            <div className="form-group" style={{ gridColumn: '1 / -1' }}>
              <label className="form-label">{t('expense.description')}</label>
              <textarea className="form-textarea" placeholder={t('expense.descriptionPlaceholder')} value={form.description} onChange={(e) => setForm({...form, description: e.target.value})} />
            </div>
          </div>
          <button className="btn btn-primary btn-full" onClick={handleSubmit} disabled={saving || !form.amount} style={{ background: 'linear-gradient(135deg, var(--danger) 0%, #dc2626 100%)' }}>
            {saving ? <><Loader2 size={16} className="animate-spin" /> {t('expense.savingMsg')}</> : t('expense.recordBtn')}
          </button>
        </div>
      )}

      {/* Controls */}
      <div style={{ display: 'flex', gap: '12px', marginBottom: '20px', flexWrap: 'wrap' }}>
        <select className="form-select" value={filterPeriod} onChange={(e) => setFilterPeriod(e.target.value)} style={{ maxWidth: '200px' }}>
          <option value="today">{t('expense.today')}</option>
          <option value="weekly">{t('expense.weekly')}</option>
          <option value="monthly">{t('expense.monthly')}</option>
          <option value="yearly">{t('expense.yearly')}</option>
        </select>
      </div>

      {/* Records */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '60px 20px' }}>
          <Loader2 size={40} className="animate-spin" style={{ color: 'var(--danger)' }} />
          <p style={{ marginTop: '16px', color: 'var(--text-medium)' }}>{t('expense.loadingMsg')}</p>
        </div>
      ) : records.length === 0 ? (
        <div className="card" style={{ textAlign: 'center', padding: '60px 20px' }}>
          <TrendingDown size={48} style={{ color: 'var(--text-light)', marginBottom: '16px' }} />
          <h3 style={{ color: 'var(--text-dark)' }}>{t('expense.noRecords')}</h3>
          <p style={{ color: 'var(--text-light)', marginTop: '8px' }}>{t('expense.emptyMsg')}</p>
        </div>
      ) : (
        <div style={{ display: 'grid', gap: '12px' }}>
          {records.map((r, idx) => (
            <div key={r.id} className="card" style={{ padding: '16px', cursor: 'pointer', transition: 'all var(--transition-base)', animation: `slideUp ${0.2 + idx * 0.05}s ease` }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div style={{ flex: 1 }}>
                  <div style={{ fontWeight: 'var(--font-semibold)', fontSize: 'var(--font-base)', color: 'var(--text-dark)' }}>
                    {expenseCategoryOptions.find(cat => cat.key === r.category)?.label || r.category}
                  </div>
                  <div style={{ fontSize: 'var(--font-xs)', color: 'var(--text-light)', marginTop: '4px' }}>
                    {paymentMethodOptions.find(m => m.value === r.payment_method)?.label || r.payment_method} • {formatDateForLanguage(r.date, lang)}
                  </div>
                  {r.description && <div style={{ fontSize: 'var(--font-xs)', color: 'var(--text-medium)', marginTop: '6px', fontStyle: 'italic' }}>{r.description}</div>}
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontSize: 'var(--font-lg)', fontWeight: 'var(--font-bold)', color: 'var(--danger)' }}>-{formatCurrencyForLanguage(r.amount, lang)}</span>
                  <button onClick={() => handleDelete(r.id)} style={{ background: 'none', border: 'none', cursor: 'pointer', color: 'var(--danger)', padding: '4px', display: 'flex', alignItems: 'center' }}>
                    <Trash2 size={16} />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
