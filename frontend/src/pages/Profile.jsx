import React, { useState, useEffect } from 'react';
import { useLanguage } from '../hooks/useLanguage';
import { getUserProfile, updateUserProfile } from '../services/api';
import { getDeviceId } from '../utils/device';
import {
  User,
  Phone,
  Mail,
  MapPin,
  Store,
  Wallet,
  Copy,
  Check,
  Loader2,
} from 'lucide-react';

const BUSINESS_TYPES = [
  'agriculture',
  'handicraft',
  'food',
  'textile',
  'retail',
  'service',
  'dairy',
  'other',
];

export default function Profile() {
  const { t, lang, setLanguage } = useLanguage();
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const [copied, setCopied] = useState(false);
  const [form, setForm] = useState({
    name: '',
    phone: '',
    email: '',
    village: '',
    district: '',
    state: 'Tamil Nadu',
    business_name: '',
    business_type: 'other',
    upi_id: '',
  });

  const [selectedLanguage, setSelectedLanguage] = useState(lang);

  useEffect(() => {
    getUserProfile()
      .then((r) => setForm((prev) => ({ ...prev, ...r.data })))
      .catch(() => {});
  }, []);

  const handleLanguageChange = (code) => {
    setSelectedLanguage(code);
    setLanguage(code);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const copyDeviceId = () => {
    navigator.clipboard.writeText(getDeviceId());
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await updateUserProfile(form);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (error) {
      console.error('Failed to save profile:', error);
    } finally {
      setSaving(false);
    }
  };

  const getBusinessTypeLabel = (type) => {
    const labels = {
      agriculture: t('profile.businessTypes.agriculture'),
      handicraft: t('profile.businessTypes.handicraft'),
      food: t('profile.businessTypes.food'),
      textile: t('profile.businessTypes.textile'),
      retail: t('profile.businessTypes.retail'),
      service: t('profile.businessTypes.service'),
      dairy: t('profile.businessTypes.dairy'),
      other: t('profile.businessTypes.other'),
    };
    return labels[type] || type;
  };

  return (
    <div style={{ padding: '16px', maxWidth: '1200px', margin: '0 auto', background: 'var(--bg-light)', paddingBottom: 100 }}>
      {/* Header */}
      <div style={{ background: 'linear-gradient(135deg, var(--primary) 0%, #7c3aed 100%)', borderRadius: 'var(--radius-lg)', padding: '24px', marginBottom: '24px', color: 'white', boxShadow: 'var(--shadow-lg)', display: 'flex', alignItems: 'center', gap: '16px' }}>
        <div style={{ background: 'rgba(255,255,255,0.2)', padding: '12px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <User size={32} />
        </div>
        <h1 style={{ margin: '0', fontSize: 'var(--font-2xl)', fontWeight: 700 }}>{t('profile.title')}</h1>
      </div>

      <div style={{ display: 'grid', gap: '16px' }}>
        {/* Language Selector */}
        <div className="card card-interactive" style={{ animation: 'slideUp 0.3s ease' }}>
          <div className="card-header">
            <span style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--primary)' }}>
              <MapPin size={18} />
              <h2 style={{ margin: '0', fontSize: 'var(--font-base)', fontWeight: 700 }}>{t('profile.chooseLanguage')}</h2>
            </span>
          </div>
          <div className="card-body">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(100px, 1fr))', gap: '12px' }}>
              {['en', 'hi', 'ta'].map((code) => (
                <button
                  key={code}
                  className={selectedLanguage === code ? 'btn btn-primary' : 'btn btn-secondary'}
                  onClick={() => handleLanguageChange(code)}
                  style={{ width: '100%' }}
                >
                  {t(`profile.selectLanguage.${code === 'en' ? 'english' : code === 'hi' ? 'hindi' : 'tamil'}`)}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Personal Information */}
        <div className="card card-interactive" style={{ animation: 'slideUp 0.35s ease' }}>
          <div className="card-header">
            <span style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--primary)' }}>
              <User size={18} />
              <h2 style={{ margin: '0', fontSize: 'var(--font-base)', fontWeight: 700 }}>{t('profile.personalInfo')}</h2>
            </span>
          </div>
          <div className="card-body">
            <div style={{ display: 'grid', gap: '12px' }}>
              <div>
                <label className="form-label">{t('profile.name')}</label>
                <input
                  type="text"
                  name="name"
                  value={form.name}
                  onChange={handleInputChange}
                  placeholder={t('profile.namePlaceholder')}
                  className="form-input"
                />
              </div>

              <div>
                <label className="form-label">{t('profile.phone')}</label>
                <input
                  type="tel"
                  name="phone"
                  value={form.phone}
                  onChange={handleInputChange}
                  placeholder={t('profile.namePlaceholder')}
                  className="form-input"
                />
              </div>

              <div>
                <label className="form-label">{t('profile.email')}</label>
                <input
                  type="email"
                  name="email"
                  value={form.email}
                  onChange={handleInputChange}
                  placeholder={t('profile.emailPlaceholder')}
                  className="form-input"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Location */}
        <div className="card card-interactive" style={{ animation: 'slideUp 0.4s ease' }}>
          <div className="card-header">
            <span style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--primary)' }}>
              <MapPin size={18} />
              <h2 style={{ margin: '0', fontSize: 'var(--font-base)', fontWeight: 700 }}>{t('profile.location')}</h2>
            </span>
          </div>
          <div className="card-body">
            <div style={{ display: 'grid', gap: '12px' }}>
              <div>
                <label className="form-label">{t('profile.village')}</label>
                <input
                  type="text"
                  name="village"
                  value={form.village}
                  onChange={handleInputChange}
                  placeholder={t('profile.villagePlaceholder')}
                  className="form-input"
                />
              </div>

              <div>
                <label className="form-label">{t('profile.district')}</label>
                <input
                  type="text"
                  name="district"
                  value={form.district}
                  onChange={handleInputChange}
                  placeholder={t('profile.districtPlaceholder')}
                  className="form-input"
                />
              </div>

              <div>
                <label className="form-label">{t('profile.state')}</label>
                <input
                  type="text"
                  name="state"
                  value={form.state}
                  onChange={handleInputChange}
                  placeholder={t('profile.statePlaceholder')}
                  className="form-input"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Business Information */}
        <div className="card card-interactive" style={{ animation: 'slideUp 0.45s ease' }}>
          <div className="card-header">
            <span style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--primary)' }}>
              <Store size={18} />
              <h2 style={{ margin: '0', fontSize: 'var(--font-base)', fontWeight: 700 }}>{t('profile.businessInfo')}</h2>
            </span>
          </div>
          <div className="card-body">
            <div style={{ display: 'grid', gap: '12px' }}>
              <div>
                <label className="form-label">{t('profile.businessName')}</label>
                <input
                  type="text"
                  name="business_name"
                  value={form.business_name}
                  onChange={handleInputChange}
                  placeholder={t('profile.businessNamePlaceholder')}
                  className="form-input"
                />
              </div>

              <div>
                <label className="form-label">{t('profile.businessType')}</label>
                <select
                  name="business_type"
                  value={form.business_type}
                  onChange={handleInputChange}
                  className="form-input"
                >
                  {BUSINESS_TYPES.map((type) => (
                    <option key={type} value={type}>
                      {getBusinessTypeLabel(type)}
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label className="form-label">{t('profile.upiId')}</label>
                <input
                  type="text"
                  name="upi_id"
                  value={form.upi_id}
                  onChange={handleInputChange}
                  placeholder={t('profile.upiPlaceholder')}
                  className="form-input"
                />
              </div>
            </div>
          </div>
        </div>

        {/* Device ID */}
        <div className="card card-interactive" style={{ animation: 'slideUp 0.5s ease' }}>
          <div className="card-header">
            <span style={{ display: 'flex', alignItems: 'center', gap: '8px', color: 'var(--primary)' }}>
              <Wallet size={18} />
              <h2 style={{ margin: '0', fontSize: 'var(--font-base)', fontWeight: 700 }}>{t('profile.deviceId')}</h2>
            </span>
          </div>
          <div className="card-body">
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', background: 'var(--bg-ultra-light)', borderRadius: 'var(--radius-md)', padding: '12px 16px', fontFamily: 'monospace', fontSize: 'var(--font-sm)', wordBreak: 'break-all' }}>
              <code style={{ flex: 1, color: 'var(--gray-700)' }}>{getDeviceId()}</code>
              <button
                className="btn btn-secondary"
                onClick={copyDeviceId}
                title={t('profile.copyDeviceId')}
                style={{ minWidth: 'auto', padding: '8px 12px' }}
              >
                {copied ? <Check size={18} /> : <Copy size={18} />}
              </button>
            </div>
          </div>
        </div>

        {/* Save Button */}
        <button
          className="btn btn-primary"
          onClick={handleSave}
          disabled={saving}
          style={{ width: '100%', marginTop: '8px' }}
        >
          {saving ? (
            <>
              <Loader2 size={20} className="animate-spin" style={{ marginRight: '8px' }} />
              {t('common.loading')}
            </>
          ) : saved ? (
            <>
              <Check size={20} style={{ marginRight: '8px' }} />
              {t('profile.saved')}
            </>
          ) : (
            t('profile.save')
          )}
        </button>
      </div>
    </div>
  );
}

