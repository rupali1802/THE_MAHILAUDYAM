import React, { useState } from 'react';
import { useLanguage } from '../hooks/useLanguage';
import { amountToSpeech } from '../utils/numberConverter';
import './SubscriptionPlans.css';

export default function SubscriptionPlans() {
  const { t, lang } = useLanguage();
  const [billingPeriod, setBillingPeriod] = useState('monthly');
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [showPayment, setShowPayment] = useState(false);
  const [paymentMethod, setPaymentMethod] = useState('upi');
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    phone: '',
    upiId: '',
    bank: '',
    cardNumber: '',
    cardExpiry: '',
    cardCVV: '',
  });
  const [loading, setLoading] = useState(false);
  const [confirmationData, setConfirmationData] = useState(null);

  // Plan pricing
  const plans = {
    free: {
      name: t('subscription.freePlan') || 'Free Plan',
      price: 0,
      features: [
        t('subscription.browseSchemes') || 'Browse government schemes',
        t('subscription.basicVoiceChat') || 'Basic voice chat with Sakhi',
        t('subscription.mentorSessions') || '2 mentor sessions per month (free)',
      ],
    },
    premium: {
      name: t('subscription.premiumPlan') || 'Premium Plan',
      monthlyPrice: 299,
      annualPrice: 2499,
      monthlyDescription: t('subscription.perMonth') || 'per month',
      annualDescription: t('subscription.perYear') || 'per year',
      annualSavings: 1099,
      savingsText: t('subscription.saves') || 'You save',
      features: [
        t('subscription.unlimitedMentors') || 'Unlimited mentor sessions',
        t('subscription.priorityMatching') || 'Priority mentor matching',
        t('subscription.schemeTracking') || 'Full scheme application tracking',
        t('subscription.businessAnalytics') || 'Detailed business analytics',
        t('subscription.secureStorage') || 'Secure document storage',
      ],
    },
  };

  const currentPrice = billingPeriod === 'monthly' ? 
    plans.premium.monthlyPrice : 
    plans.premium.annualPrice;

  const handleSelectPlan = (plan) => {
    setSelectedPlan(plan);
    setShowPayment(true);
  };

  const handlePayment = async () => {
    if (!formData.fullName || !formData.email || !formData.phone) {
      alert(t('subscription.fillRequired') || 'Please fill all required fields');
      return;
    }

    setLoading(true);

    // Simulate Razorpay payment
    setTimeout(() => {
      const transactionId = 'TXN' + Date.now();
      const today = new Date().toLocaleDateString(lang === 'hi' ? 'hi-IN' : lang === 'ta' ? 'ta-IN' : 'en-IN');
      
      setConfirmationData({
        plan: selectedPlan === 'premium' ? plans.premium.name : '',
        amount: currentPrice,
        transactionId,
        date: today,
        email: formData.email,
      });

      setLoading(false);
      setShowPayment(false);
    }, 2000);
  };

  if (confirmationData) {
    return (
      <div className="subscription-container">
        <div className="confirmation-screen">
          <div className="confirmation-icon">✓</div>
          <h2 className="confirmation-title">
            {t('subscription.paymentSuccess') || 'Payment Successful!'}
          </h2>
          
          <div className="confirmation-details">
            <div className="detail-row">
              <span className="detail-label">{t('subscription.planName') || 'Plan'}:</span>
              <span className="detail-value">{confirmationData.plan}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">{t('subscription.amount') || 'Amount'}:</span>
              <span className="detail-value">{amountToSpeech(confirmationData.amount, lang)}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">{t('subscription.transactionId') || 'Transaction ID'}:</span>
              <span className="detail-value">{confirmationData.transactionId}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">{t('subscription.date') || 'Date'}:</span>
              <span className="detail-value">{confirmationData.date}</span>
            </div>
          </div>

          <button 
            className="btn btn-primary"
            onClick={() => window.location.href = '/dashboard'}
          >
            {t('subscription.backToDashboard') || 'Back to Dashboard'}
          </button>
          
          <button 
            className="btn btn-secondary"
            onClick={() => alert(t('subscription.downloadPdf') || 'Downloading receipt...')}
          >
            {t('subscription.downloadReceipt') || 'Download Receipt'}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="subscription-container">
      <div className="subscription-header">
        <h1 className="subscription-title">
          {t('subscription.choosePlan') || 'Choose Your Plan'}
        </h1>
        <p className="subscription-subtitle">
          {t('subscription.selectPlanDesc') || 'Select the perfect plan for your business'}
        </p>
      </div>

      {/* Billing Toggle */}
      <div className="billing-toggle">
        <button 
          className={`toggle-btn ${billingPeriod === 'monthly' ? 'active' : ''}`}
          onClick={() => setBillingPeriod('monthly')}
        >
          {t('subscription.monthly') || 'Monthly'}
        </button>
        <button 
          className={`toggle-btn ${billingPeriod === 'annual' ? 'active' : ''}`}
          onClick={() => setBillingPeriod('annual')}
        >
          {t('subscription.annual') || 'Annual'}
        </button>
      </div>

      {/* Plan Cards */}
      <div className="plans-grid">
        {/* Free Plan */}
        <div className="plan-card free-plan">
          <div className="plan-name">{plans.free.name}</div>
          <div className="plan-price">Free</div>
          <div className="plan-features">
            {plans.free.features.map((feature, idx) => (
              <div key={idx} className="feature">
                <span className="feature-icon">✓</span>
                <span className="feature-text">{feature}</span>
              </div>
            ))}
          </div>
          <button className="btn btn-secondary" disabled>
            {t('subscription.currentPlan') || 'Current Plan'}
          </button>
        </div>

        {/* Premium Plan */}
        <div className="plan-card premium-plan recommended">
          <div className="recommended-badge">
            {t('subscription.recommended') || 'RECOMMENDED'}
          </div>
          <div className="plan-name">{plans.premium.name}</div>
          <div className="plan-price">
            ₹{currentPrice}
            <span className="plan-period">
              {billingPeriod === 'monthly' ? 
                ` ${t('subscription.perMonth') || '/month'}` : 
                ` ${t('subscription.perYear') || '/year'}`
              }
            </span>
          </div>
          {billingPeriod === 'annual' && (
            <div className="savings-badge">
              {plans.premium.savingsText} ₹{plans.premium.annualSavings}
            </div>
          )}
          <div className="plan-features">
            {plans.premium.features.map((feature, idx) => (
              <div key={idx} className="feature">
                <span className="feature-icon">✓</span>
                <span className="feature-text">{feature}</span>
              </div>
            ))}
          </div>
          <button 
            className="btn btn-primary"
            onClick={() => handleSelectPlan('premium')}
          >
            {t('subscription.upgradePremium') || 'Upgrade to Premium'}
          </button>
        </div>
      </div>

      {/* Trust Badges */}
      <div className="trust-badges">
        <div className="badge">🔒 {t('subscription.securedByRazorpay') || 'Secured by Razorpay'}</div>
        <div className="badge">✓ {t('subscription.moneyBackGuarantee') || '7-Day Money Back Guarantee'}</div>
      </div>

      {/* Payment Form Modal */}
      {showPayment && (
        <div className="payment-modal-overlay" onClick={() => setShowPayment(false)}>
          <div className="payment-modal" onClick={e => e.stopPropagation()}>
            <button className="close-btn" onClick={() => setShowPayment(false)}>✕</button>
            
            <h2 className="payment-title">
              {t('subscription.completePayment') || 'Complete Your Payment'}
            </h2>

            {/* Payment Form */}
            <div className="payment-form">
              <div className="form-group">
                <label>{t('subscription.fullName') || 'Full Name'} *</label>
                <input 
                  type="text"
                  value={formData.fullName}
                  onChange={(e) => setFormData({...formData, fullName: e.target.value})}
                  placeholder={t('subscription.enterName') || 'Your full name'}
                />
              </div>

              <div className="form-group">
                <label>{t('subscription.email') || 'Email'} *</label>
                <input 
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({...formData, email: e.target.value})}
                  placeholder={t('subscription.enterEmail') || 'your@email.com'}
                />
              </div>

              <div className="form-group">
                <label>{t('subscription.phone') || 'Phone Number'} *</label>
                <input 
                  type="tel"
                  value={formData.phone}
                  onChange={(e) => setFormData({...formData, phone: e.target.value})}
                  placeholder={t('subscription.enterPhone') || '+91 98765 43210'}
                />
              </div>

              {/* Payment Methods */}
              <div className="payment-methods">
                <label className="method-option">
                  <input 
                    type="radio"
                    value="upi"
                    checked={paymentMethod === 'upi'}
                    onChange={(e) => setPaymentMethod(e.target.value)}
                  />
                  <span>{t('subscription.upi') || 'UPI'}</span>
                </label>
                <label className="method-option">
                  <input 
                    type="radio"
                    value="card"
                    checked={paymentMethod === 'card'}
                    onChange={(e) => setPaymentMethod(e.target.value)}
                  />
                  <span>{t('subscription.creditCard') || 'Credit/Debit Card'}</span>
                </label>
                <label className="method-option">
                  <input 
                    type="radio"
                    value="netbanking"
                    checked={paymentMethod === 'netbanking'}
                    onChange={(e) => setPaymentMethod(e.target.value)}
                  />
                  <span>{t('subscription.netBanking') || 'Net Banking'}</span>
                </label>
              </div>

              {paymentMethod === 'upi' && (
                <div className="form-group">
                  <label>{t('subscription.upiId') || 'UPI ID'}</label>
                  <input 
                    type="text"
                    value={formData.upiId}
                    onChange={(e) => setFormData({...formData, upiId: e.target.value})}
                    placeholder="username@bankname"
                  />
                </div>
              )}

              {paymentMethod === 'card' && (
                <>
                  <div className="form-group">
                    <label>{t('subscription.cardNumber') || 'Card Number'}</label>
                    <input 
                      type="text"
                      value={formData.cardNumber}
                      onChange={(e) => setFormData({...formData, cardNumber: e.target.value})}
                      placeholder="1234 5678 9012 3456"
                      maxLength="19"
                    />
                  </div>
                  <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px'}}>
                    <div className="form-group">
                      <label>{t('subscription.expiry') || 'MM/YY'}</label>
                      <input 
                        type="text"
                        value={formData.cardExpiry}
                        onChange={(e) => setFormData({...formData, cardExpiry: e.target.value})}
                        placeholder="12/25"
                        maxLength="5"
                      />
                    </div>
                    <div className="form-group">
                      <label>{t('subscription.cvv') || 'CVV'}</label>
                      <input 
                        type="text"
                        value={formData.cardCVV}
                        onChange={(e) => setFormData({...formData, cardCVV: e.target.value})}
                        placeholder="123"
                        maxLength="3"
                      />
                    </div>
                  </div>
                </>
              )}

              {paymentMethod === 'netbanking' && (
                <div className="form-group">
                  <label>{t('subscription.selectBank') || 'Select Your Bank'}</label>
                  <select value={formData.bank} onChange={(e) => setFormData({...formData, bank: e.target.value})}>
                    <option value="">Choose a bank...</option>
                    <option value="HDFC">HDFC Bank</option>
                    <option value="ICICI">ICICI Bank</option>
                    <option value="SBI">State Bank of India</option>
                    <option value="AXIS">Axis Bank</option>
                    <option value="KOTAK">Kotak Bank</option>
                  </select>
                </div>
              )}

              <button 
                className="btn btn-primary btn-full"
                onClick={handlePayment}
                disabled={loading}
              >
                {loading ? '...' : `${t('subscription.payNow') || 'Pay Now'} ₹${currentPrice}`}
              </button>
            </div>

            {/* Support Info */}
            <div className="support-info">
              <p>{t('subscription.needHelp') || 'Need help?'}</p>
              <p>📧 {t('subscription.supportEmail') || 'support@mahilaudyam.com'}</p>
              <p>📞 {t('subscription.supportPhone') || '+91 9876 543 210'}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
