import React, { useState, useEffect, useCallback } from 'react';
import { useLanguage } from '../hooks/useLanguage';
import { getPayments, addPayment, getUserProfile } from '../services/api';
import { formatCurrencyForLanguage, formatDateForLanguage, getTodayString } from '../utils/device';
import { Wallet, Plus, Trash2, Loader2, QrCode, Copy } from 'lucide-react';

export default function Payment() {
  const { t, lang } = useLanguage();
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [upiId, setUpiId] = useState('');
  const [notification, setNotification] = useState(null);
  const [form, setForm] = useState({
    amount: '',
    method: 'upi',
    payment_type: 'received',
    reference_number: '',
    party_name: '',
    date: getTodayString(),
    status: 'success',
    description: '',
  });

  const fetchRecords = useCallback(() => {
    setLoading(true);
    getPayments()
      .then((r) => setRecords(r.data.results || r.data))
      .catch(() => {})
      .finally(() => setLoading(false));
    getUserProfile()
      .then((r) => setUpiId(r.data.upi_id || ''))
      .catch(() => {});
  }, []);

  useEffect(() => {
    fetchRecords();
  }, [fetchRecords]);

  const showNotificationMsg = (msg, type = 'success') => {
    setNotification({ msg, type });
    setTimeout(() => setNotification(null), 3000);
  };

  const handleSubmit = async () => {
    if (!form.amount) return;
    setSaving(true);
    try {
      await addPayment(form);
      setForm({
        amount: '',
        method: 'upi',
        payment_type: 'received',
        reference_number: '',
        party_name: '',
        date: getTodayString(),
        status: 'success',
        description: '',
      });
      setShowForm(false);
      fetchRecords();
      showNotificationMsg(t('payment.saved'));
    } catch {
      showNotificationMsg(t('errors.serverError'), 'error');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm(t('common.confirmDelete'))) return;
    setRecords(records.filter(r => r.id !== id));
  };

  const methodLabel = (method) => {
    const labels = {
      upi: t('payment.paymentMethods.upi'),
      cash: t('payment.paymentMethods.cash'),
      bank_transfer: t('payment.paymentMethods.bank_transfer'),
      cheque: t('payment.paymentMethods.cheque')
    };
    return labels[method] || method;
  };

  return (
    <div style={{ padding: '16px', maxWidth: '1200px', margin: '0 auto', background: 'var(--bg-light)', paddingBottom: 100 }}>
      {/* Header */}
      <div style={{ background: 'linear-gradient(135deg, var(--primary) 0%, #7c3aed 100%)', borderRadius: 'var(--radius-lg)', padding: '24px', marginBottom: '24px', color: 'white', boxShadow: 'var(--shadow-lg)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
          <div style={{ background: 'rgba(255,255,255,0.2)', padding: '12px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Wallet size={32} />
          </div>
          <div>
            <h1 style={{ margin: '0', fontSize: 'var(--font-2xl)', fontWeight: 700 }}>{t('payment.title')}</h1>
            <p style={{ fontSize: 'var(--font-sm)', opacity: 0.9, margin: '4px 0 0' }}>{t('payment.managePayments')}</p>
          </div>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="btn btn-primary"
          style={{ gap: '8px' }}
        >
          {showForm ? '✕' : <Plus size={20} />}
          {!showForm && t('payment.addPayment')}
        </button>
      </div>

      <div style={{ display: 'grid', gap: '16px' }}>
        {/* QR Display Card */}
        <div className="card card-interactive" style={{ animation: 'slideUp 0.3s ease' }}>
          <div className="card-body" style={{ textAlign: 'center' }}>
            <div style={{ background: 'var(--primary-100)', padding: '16px', borderRadius: 'var(--radius-md)', display: 'inline-flex', alignItems: 'center', justifyContent: 'center', marginBottom: '12px' }}>
              <QrCode size={28} style={{ color: 'var(--primary)' }} />
            </div>
            <h3 style={{ margin: '0 0 12px', fontSize: 'var(--font-lg)', fontWeight: 700, color: 'var(--primary)' }}>{t('payment.yourQR')}</h3>
            {upiId ? (
              <div style={{ background: 'var(--bg-ultra-light)', borderRadius: 'var(--radius-md)', padding: '16px', border: '2px solid var(--primary-200)' }}>
                <p style={{ fontSize: 'var(--font-xs)', color: 'var(--primary)', margin: '0 0 8px', fontWeight: 700, textTransform: 'uppercase' }}>{t('payment.upiId')}</p>
                <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                  <code style={{ flex: 1, fontSize: 'var(--font-base)', fontWeight: 600, color: 'var(--gray-800)', wordBreak: 'break-all' }}>{upiId}</code>
                  <button className="btn btn-secondary" onClick={() => { navigator.clipboard.writeText(upiId); setUpiId(upiId); }} style={{ minWidth: 'auto', padding: '8px' }} title={t('payment.copyUpi')}>
                    <Copy size={16} />
                  </button>
                </div>
              </div>
            ) : (
              <p style={{ fontSize: 'var(--font-sm)', color: 'var(--gray-600)', margin: '0' }}>{t('payment.addUpiToProfile')}</p>
            )}
          </div>
        </div>

        {/* Form Section */}
        {showForm && (
          <div className="card card-interactive" style={{ animation: 'slideUp 0.35s ease' }}>
            <div className="card-body" style={{ display: 'grid', gap: '16px' }}>
              <h3 style={{ margin: '0 0 12px', fontSize: 'var(--font-lg)', fontWeight: 700, color: 'var(--primary)' }}>{t('payment.addPayment')}</h3>

              <div>
                <label className="form-label">{t('payment.amount')} *</label>
                <input
                  type="number"
                  min="0"
                  placeholder={t('common.amount')}
                  value={form.amount}
                  onChange={(e) => setForm({ ...form, amount: e.target.value })}
                  className="form-input"
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
                <div>
                  <label className="form-label">{t('payment.method')}</label>
                  <select
                    value={form.method}
                    onChange={(e) => setForm({ ...form, method: e.target.value })}
                    className="form-input"
                  >
                    <option value="upi">{t('payment.paymentMethods.upi')}</option>
                    <option value="cash">{t('payment.paymentMethods.cash')}</option>
                    <option value="bank_transfer">{t('payment.paymentMethods.bank_transfer')}</option>
                    <option value="cheque">{t('payment.paymentMethods.cheque')}</option>
                  </select>
                </div>

                <div>
                  <label className="form-label">{t('payment.type')}</label>
                  <select
                    value={form.payment_type}
                    onChange={(e) => setForm({ ...form, payment_type: e.target.value })}
                    className="form-input"
                  >
                    <option value="received">{t('payment.received')}</option>
                    <option value="sent">{t('payment.sent')}</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="form-label">{t('payment.partyName')}</label>
                <input
                  type="text"
                  placeholder={t('payment.partyName')}
                  value={form.party_name}
                  onChange={(e) => setForm({ ...form, party_name: e.target.value })}
                  className="form-input"
                />
              </div>

              <div>
                <label className="form-label">{t('payment.date')}</label>
                <input
                  type="date"
                  value={form.date}
                  onChange={(e) => setForm({ ...form, date: e.target.value })}
                  className="form-input"
                />
              </div>

              <div>
                <label className="form-label">{t('payment.description')}</label>
                <textarea
                  placeholder={t('common.descriptionPlaceholder')}
                  value={form.description}
                  onChange={(e) => setForm({ ...form, description: e.target.value })}
                  className="form-input"
                  rows="3"
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                <button
                  onClick={handleSubmit}
                  disabled={saving || !form.amount}
                  className="btn btn-primary"
                >
                  {saving ? (
                    <>
                      <Loader2 size={18} className="animate-spin" style={{ marginRight: '8px' }} />
                      {t('common.loading')}
                    </>
                  ) : (
                    <>
                      <Plus size={18} style={{ marginRight: '8px' }} />
                      {t('payment.save')}
                    </>
                  )}
                </button>
                <button
                  onClick={() => setShowForm(false)}
                  className="btn btn-secondary"
                >
                  {t('common.cancel')}
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Payment Records List */}
        {loading ? (
          <div style={{ textAlign: 'center', padding: '48px 16px' }}>
            <Loader2 size={32} className="animate-spin" style={{ margin: '0 auto', color: 'var(--primary)' }} />
          </div>
        ) : records.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '48px 16px', background: 'white', borderRadius: 'var(--radius-lg)', border: '2px dashed var(--gray-300)' }}>
            <Wallet size={48} style={{ color: 'var(--gray-400)', margin: '0 auto 12px' }} />
            <p style={{ fontSize: 'var(--font-lg)', color: 'var(--gray-600)', margin: '0' }}>{t('payment.noRecords')}</p>
          </div>
        ) : (
          <div className="card-grid">
            {records.map((record, idx) => (
              <div 
                key={record.id} 
                className="card card-interactive"
                style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  gap: '16px',
                  animation: `slideUp ${0.3 + idx * 0.05}s ease`
                }}
              >
                <div className="card-body" style={{ display: 'flex', alignItems: 'center', gap: '16px', width: '100%' }}>
                  {/* Icon */}
                  <div style={{ background: record.payment_type === 'received' ? 'var(--success-100)' : 'var(--danger-100)', padding: '12px', borderRadius: 'var(--radius-md)', display: 'flex', alignItems: 'center', justifyContent: 'center', minWidth: '48px', height: '48px' }}>
                    <Wallet size={20} style={{ color: record.payment_type === 'received' ? 'var(--success)' : 'var(--danger)' }} />
                  </div>

                  {/* Content */}
                  <div style={{ flex: 1 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '6px', flexWrap: 'wrap' }}>
                      <p style={{ margin: '0', fontWeight: 700, fontSize: 'var(--font-base)', color: 'var(--primary)' }}>
                        {methodLabel(record.method)}
                      </p>
                      <span style={{ fontSize: 'var(--font-xs)', fontWeight: 700, padding: '4px 10px', borderRadius: 'var(--radius-full)', background: record.status === 'success' ? 'var(--success-100)' : record.status === 'pending' ? 'var(--warning-100)' : 'var(--danger-100)', color: record.status === 'success' ? 'var(--success)' : record.status === 'pending' ? 'var(--warning)' : 'var(--danger)', textTransform: 'capitalize' }}>
                        {record.status}
                      </span>
                    </div>
                    <p style={{ fontSize: 'var(--font-sm)', color: 'var(--gray-600)', margin: '0' }}>
                      {record.party_name && `${record.party_name} • `}
                      {formatDateForLanguage(record.date, lang)}
                    </p>
                  </div>

                  {/* Amount */}
                  <div style={{ textAlign: 'right', marginRight: '12px' }}>
                    <p style={{ margin: '0', fontSize: 'var(--font-lg)', fontWeight: 700, color: record.payment_type === 'received' ? 'var(--success)' : 'var(--danger)' }}>
                      {record.payment_type === 'received' ? '+' : '-'}{formatCurrencyForLanguage(record.amount, lang)}
                    </p>
                  </div>

                  {/* Delete Button */}
                  <button
                    onClick={() => handleDelete(record.id)}
                    className="btn btn-danger"
                    style={{ minWidth: 'auto', padding: '8px 12px' }}
                    title={t('common.delete')}
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Notification */}
      {notification && (
        <div
          style={{
            position: 'fixed',
            bottom: '100px',
            left: '16px',
            right: '16px',
            maxWidth: '400px',
            marginLeft: 'auto',
            marginRight: 'auto',
            padding: '12px 16px',
            borderRadius: 'var(--radius-md)',
            fontWeight: 600,
            fontSize: 'var(--font-base)',
            color: 'white',
            boxShadow: 'var(--shadow-lg)',
            background: notification.type === 'error' ? 'var(--danger)' : 'linear-gradient(135deg, var(--primary), var(--secondary))',
          }}
        >
          {notification.msg}
        </div>
      )}
    </div>
  );
}
