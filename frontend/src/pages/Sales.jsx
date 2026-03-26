import React, { useState, useEffect, useCallback } from 'react';
import { useLanguage } from '../hooks/useLanguage';
import { getSales, addSale, deleteSale } from '../services/api';
import { formatCurrencyForLanguage, formatDateForLanguage, getTodayString, getDeviceId } from '../utils/device';
import { ShoppingCart, Plus, Trash2, Loader2, Edit2, X, TrendingUp, Calendar } from 'lucide-react';
import '../styles/DataPage.css';
import '../styles/Sales.css';

const PRODUCT_CATEGORIES = [
  'vegetables',
  'fruits',
  'dairy',
  'grains',
  'spices',
  'handicrafts',
  'other'
];

const UNIT_OPTIONS = [
  'kg',
  'g',
  'liter',
  'piece',
  'dozen'
];

const CATEGORY_KEYS = {
  vegetables: 'category.vegetables',
  fruits: 'category.fruits',
  dairy: 'category.dairy',
  grains: 'category.grains',
  spices: 'category.spices',
  handicrafts: 'category.handicrafts',
  other: 'category.other'
};

const UNIT_KEYS = {
  kg: 'unit.kg',
  g: 'unit.g',
  liter: 'unit.liter',
  piece: 'unit.piece',
  dozen: 'unit.dozen'
};

export default function Sales() {
  const { t, lang } = useLanguage();
  const [records, setRecords] = useState([]);
  const [total, setTotal] = useState('0');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [notification, setNotification] = useState(null);
  const [filterPeriod, setFilterPeriod] = useState('monthly');
  const [searchTerm, setSearchTerm] = useState('');
  const [form, setForm] = useState({
    product: '',
    category: PRODUCT_CATEGORIES[0],
    quantity: '1',
    unit: 'kg',
    amount: '',
    date: getTodayString(),
    notes: '',
  });

  const fetchRecords = useCallback(() => {
    setLoading(true);
    getSales({ period: filterPeriod })
      .then((r) => {
        setRecords(r.data.results || []);
        setTotal(r.data.total || '0');
      })
      .catch(() => {
        showNotification(t('action.error'), 'error');
      })
      .finally(() => setLoading(false));
  }, [filterPeriod]);

  useEffect(() => {
    fetchRecords();
  }, [fetchRecords]);

  const showNotification = (msg, type = 'success') => {
    setNotification({ msg, type });
    setTimeout(() => setNotification(null), 3000);
  };

  const resetForm = () => {
    setForm({
      product: '',
      category: PRODUCT_CATEGORIES[0],
      quantity: '1',
      unit: 'kg',
      amount: '',
      date: getTodayString(),
      notes: '',
    });
    setEditingId(null);
  };

  const handleSubmit = async () => {
    if (!form.amount || !form.product || !form.quantity) {
      showNotification(t('common.required'), 'error');
      return;
    }
    setSaving(true);
    try {
      const payload = {
        device_id: getDeviceId(),
        product_name: form.product,
        quantity: parseFloat(form.quantity),
        unit: form.unit,
        price_per_unit: parseFloat(form.amount),
        total_amount: parseFloat(form.quantity) * parseFloat(form.amount),
        sale_date: form.date,
        description: form.notes || '',
        category: form.category,
      };
      
      await addSale(payload);
      resetForm();
      setShowForm(false);
      await fetchRecords();
      showNotification(t('action.success'));
    } catch (err) {
      showNotification(err.message || t('action.error'), 'error');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm(t('action.confirmDelete'))) return;
    try {
      await deleteSale(id);
      await fetchRecords();
      showNotification(t('action.deleted'));
    } catch {
      showNotification(t('action.error'), 'error');
    }
  };

  const handleEdit = (record) => {
    setForm({
      product: record.product_name,
      category: PRODUCT_CATEGORIES[0],
      quantity: record.quantity.toString(),
      unit: record.unit || UNIT_OPTIONS[0],
      amount: record.price_per_unit.toString(),
      date: record.sale_date,
      notes: record.description || '',
    });
    setEditingId(record.id);
    setShowForm(true);
  };

  // Filter records based on search term
  const filteredRecords = records.filter(r =>
    r.product_name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Group records by unit (since backend doesn't have category)
  const groupedRecords = UNIT_OPTIONS.reduce((acc, unit) => {
    acc[unit] = filteredRecords.filter(r => r.unit === unit);
    return acc;
  }, {});

  return (
    <div className="sales-page">
      {/* Header */}
      <div className="sales-header">
        <div className="header-top">
          <div className="title-section">
            <div className="icon-badge">
              <ShoppingCart size={28} />
            </div>
            <div>
              <h1>{t('sales.title') || 'Sales'}</h1>
              <p className="subtitle">{t('sales.track')}</p>
            </div>
          </div>
          <button 
            className={`add-sales-btn ${showForm ? 'active' : ''}`}
            onClick={() => {
              if (showForm) {
                setShowForm(false);
                resetForm();
              } else {
                resetForm();
                setShowForm(true);
              }
            }}
          >
            {showForm ? <X size={20} /> : <Plus size={20} />}
            {showForm ? t('common.cancel') : t('sales.addSale')}
          </button>
        </div>

        {/* Total Card */}
        <div className="total-card">
          <div className="total-info">
            <span className="total-label">{t('sales.totalSales')}</span>
            <span className="total-amount">
              {formatCurrencyForLanguage(total, lang)}
            </span>
          </div>
          <div className="total-icon">
            <TrendingUp size={32} />
          </div>
        </div>
      </div>

      {/* Notifications */}
      {notification && (
        <div className={`notification-toast ${notification.type}`}>
          <div className="notification-content">
            {notification.msg}
          </div>
          <button 
            className="notification-close"
            onClick={() => setNotification(null)}
          >
            <X size={16} />
          </button>
        </div>
      )}

      {/* Add/Edit Form */}
      {showForm && (
        <div className="form-card">
          <h2>{editingId ? t('sales.editSale') : t('sales.addSale')}</h2>
          
          <div className="form-grid">
            <div className="form-group">
              <label>{t('sales.productName')} *</label>
              <input
                type="text"
                placeholder={t('sales.productPlaceholder')}
                value={form.product}
                onChange={(e) => setForm({ ...form, product: e.target.value })}
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label>{t('sales.category') || 'Category'}</label>
              <select
                value={form.category}
                onChange={(e) => setForm({ ...form, category: e.target.value })}
                className="form-input"
              >
                {PRODUCT_CATEGORIES.map(cat => (
                  <option key={cat} value={cat}>{t(CATEGORY_KEYS[cat])}</option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>{t('sales.quantity')} *</label>
              <div className="quantity-input">
                <input
                  type="number"
                  step="0.01"
                  min="0"
                  placeholder={t('common.amount')}
                  value={form.quantity}
                  onChange={(e) => setForm({ ...form, quantity: e.target.value })}
                  className="form-input"
                />
                <select
                  value={form.unit}
                  onChange={(e) => setForm({ ...form, unit: e.target.value })}
                  className="form-input unit-select"
                >
                  {UNIT_OPTIONS.map(unit => (
                    <option key={unit} value={unit}>{t(UNIT_KEYS[unit])}</option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-group">
              <label>{t('sales.pricePerUnit')} *</label>
              <input
                type="number"
                step="0.01"
                min="0"
                placeholder={t('common.amount')}
                value={form.amount}
                onChange={(e) => setForm({ ...form, amount: e.target.value })}
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label>{t('common.date')}</label>
              <input
                type="date"
                value={form.date}
                onChange={(e) => setForm({ ...form, date: e.target.value })}
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label>{t('sales.description')}</label>
              <textarea
                placeholder={t('common.description')}
                value={form.notes}
                onChange={(e) => setForm({ ...form, notes: e.target.value })}
                className="form-input"
                rows="2"
              />
            </div>
          </div>

          <button 
            className="submit-btn"
            onClick={handleSubmit}
            disabled={saving}
          >
            {saving ? (
              <>
                <Loader2 size={18} className="spin" />
                {t('common.saving')}
              </>
            ) : (
              editingId ? t('common.edit') : t('sales.addSale')
            )}
          </button>
        </div>
      )}

      {/* Search & Filter */}
      <div className="controls-bar">
        <input
          type="text"
          placeholder={t('common.search')}
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
        <select
          value={filterPeriod}
          onChange={(e) => setFilterPeriod(e.target.value)}
          className="filter-select"
        >
          <option value="daily">{t('profit.today')}</option>
          <option value="weekly">{t('profit.weekly')}</option>
          <option value="monthly">{t('profit.monthly')}</option>
          <option value="all">{t('common.all')}</option>
        </select>
      </div>

      {/* Records List */}
      {loading ? (
        <div className="loading-state">
          <Loader2 size={40} className="spin" />
          <p>{t('common.loading')}</p>
        </div>
      ) : filteredRecords.length === 0 ? (
        <div className="empty-state">
          <ShoppingCart size={48} />
          <h3>{t('sales.noRecords')}</h3>
          <p>{t('sales.emptyMsg')}</p>
        </div>
      ) : (
        <div className="records-container">
          {UNIT_OPTIONS.map(unit => {
            const unitRecords = groupedRecords[unit];
            if (unitRecords.length === 0) return null;

            return (
              <div key={unit} className="category-section">
                <h3 className="category-title">{t(UNIT_KEYS[unit])}</h3>
                <div className="records-grid">
                  {unitRecords.map((r) => (
                    <div key={r.id} className="record-card">
                      <div className="record-header">
                        <div className="product-info">
                          <h4>{r.product_name}</h4>
                          <p className="product-meta">
                            {r.quantity} {t(UNIT_KEYS[r.unit] || r.unit)} • {formatDateForLanguage(r.sale_date, lang)}
                          </p>
                        </div>
                        <div className="record-actions">
                          <button
                            className="action-btn edit"
                            onClick={() => handleEdit(r)}
                            title={t('common.edit')}
                          >
                            <Edit2 size={16} />
                          </button>
                          <button
                            className="action-btn delete"
                            onClick={() => handleDelete(r.id)}
                            title={t('common.delete')}
                          >
                            <Trash2 size={16} />
                          </button>
                        </div>
                      </div>
                      <div className="record-footer">
                        <span className="price">
                          {formatCurrencyForLanguage(r.total_amount, lang)}
                        </span>
                        {r.description && <span className="notes-badge">{t('sales.note')}</span>}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
