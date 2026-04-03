import React, { useState, useEffect, useRef } from 'react';
import { useLanguage } from '../hooks/useLanguage';
import { getMarketPrices } from '../services/api';
import { formatCurrencyForLanguage, formatDateForLanguage } from '../utils/device';
import { Store, TrendingUp, TrendingDown, Minus, Loader2, Search, Mic, MicOff, Sparkles, Send } from 'lucide-react';
import '../styles/MarketPrice.css';

// Voice recognition setup
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

// Helper function to detect language of text based on character scripts
const detectLanguageOfText = (text) => {
  if (!text) return 'en';
  
  // Count character ranges to determine language
  // Devanagari (Hindi): \u0900-\u097F
  // Tamil: \u0B80-\u0BFF
  const devanagariChars = (text.match(/[\u0900-\u097F]/g) || []).length;
  const tamilChars = (text.match(/[\u0B80-\u0BFF]/g) || []).length;
  const englishChars = (text.match(/[a-zA-Z]/g) || []).length;
  
  const totalChars = text.length;
  const englishRatio = englishChars / totalChars;
  const devanagariRatio = devanagariChars / totalChars;
  const tamilRatio = tamilChars / totalChars;
  
  console.log(`🔍 Character analysis: EN=${englishRatio.toFixed(2)} HI=${devanagariRatio.toFixed(2)} TA=${tamilRatio.toFixed(2)}`);
  
  if (devanagariRatio > 0.15) return 'hi';  // >15% Devanagari = Hindi
  if (tamilRatio > 0.15) return 'ta';      // >15% Tamil = Tamil
  return 'en';                               // Otherwise English
};

export default function MarketPrice() {
  const { t, lang, language } = useLanguage();
  const [prices, setPrices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [analysisQuery, setAnalysisQuery] = useState('');
  const [analysisResult, setAnalysisResult] = useState('');
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [selectedCommodity, setSelectedCommodity] = useState('');
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [languageForAnalysis, setLanguageForAnalysis] = useState(language || 'en');  // ✅ FALLBACK #1: Cache language selection
  const [retryCount, setRetryCount] = useState(0);  // ✅ FALLBACK #2: Track retry attempts
  const recognitionRef = useRef(null);
  const speechSynthesisRef = useRef(null);
  const languageRef = useRef(language || 'en');  // ✅ FALLBACK #3: Ref for immediate access

  useEffect(() => {
    getMarketPrices()
      .then((r) => {
        const pricesData = r.data.results || [];
        setPrices(pricesData);
      })
      .catch(() => setPrices([]))
      .finally(() => setLoading(false));
  }, []);

  // ✅ FALLBACK #4: Sync cached language with context whenever it changes
  useEffect(() => {
    const currentLang = language || 'en';
    console.log(`🌐 Language context changed: ${currentLang}`);
    setLanguageForAnalysis(currentLang);
    languageRef.current = currentLang;  // Update ref immediately for closures
    setRetryCount(0);  // Reset retry on language change
  }, [language]);

  const filtered = prices.filter((p) =>
    p.commodity_name.toLowerCase().includes(search.toLowerCase())
  );

  // Voice input for analysis
  const startListening = () => {
    if (!SpeechRecognition) {
      alert(t('errors.speechNotSupported') || 'Speech Recognition not supported');
      return;
    }

    try {
      // ✅ FALLBACK: Capture language at moment of listening
      const listeningLanguage = languageForAnalysis || language || 'en';
      console.log(`🎤 Starting voice input with language: ${listeningLanguage}`);
      
      const recognition = new SpeechRecognition();
      recognitionRef.current = recognition;
      recognition.lang = listeningLanguage === 'hi' ? 'hi-IN' : listeningLanguage === 'ta' ? 'ta-IN' : 'en-US';
      recognition.interimResults = false;
      recognition.continuous = false;

      recognition.onstart = () => {
        console.log('🎤 Listening started with lang:', recognition.lang);
        setIsListening(true);
      };

      recognition.onend = () => {
        console.log('🎤 Listening ended');
        setIsListening(false);
      };

      recognition.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            transcript += event.results[i][0].transcript + ' ';
          }
        }
        
        if (transcript.trim()) {
          console.log('✅ Transcript:', transcript.trim());
          setAnalysisQuery(prevQuery => prevQuery + transcript.trim());
        }
      };

      recognition.onerror = (event) => {
        console.error('❌ Speech recognition error:', event.error);
        setIsListening(false);
      };

      recognition.start();
    } catch (error) {
      console.error('Error starting speech recognition:', error);
      setIsListening(false);
    }
  };

  const stopListening = () => {
    if (recognitionRef.current) {
      try {
        recognitionRef.current.abort();
        setIsListening(false);
      } catch (error) {
        console.error('Error stopping speech recognition:', error);
        setIsListening(false);
      }
    }
  };

  // Text-to-speech for analysis
  const speakAnalysis = (text) => {
    if (!('speechSynthesis' in window)) {
      console.warn('Speech synthesis not supported');
      return;
    }

    // ✅ FALLBACK: Use multiple language sources for speech
    let speakLanguage = languageRef.current;  // Ref first
    if (!speakLanguage || speakLanguage === 'en') {
      speakLanguage = languageForAnalysis;  // Then state cache
    }
    if (!speakLanguage) {
      speakLanguage = language || 'en';  // Then context
    }

    console.log(`🔊 Speech synthesis language sources:`);
    console.log(`   Ref: ${languageRef.current}`);
    console.log(`   Cache: ${languageForAnalysis}`);
    console.log(`   Context: ${language}`);
    console.log(`   Using: ${speakLanguage}`);

    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = speakLanguage === 'hi' ? 'hi-IN' : speakLanguage === 'ta' ? 'ta-IN' : 'en-US';
    utterance.rate = 0.9;
    utterance.pitch = 1;
    utterance.volume = 1;

    utterance.onstart = () => {
      console.log(`🔊 Speaking started in: ${utterance.lang}`);
      setIsSpeaking(true);
    };

    utterance.onend = () => {
      console.log('🔊 Speaking ended');
      setIsSpeaking(false);
    };

    utterance.onerror = (error) => {
      console.error('❌ Speech synthesis error:', error);
      setIsSpeaking(false);
    };

    speechSynthesisRef.current = utterance;
    window.speechSynthesis.speak(utterance);
  };

  const stopSpeaking = () => {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
    }
  };

  // ✅ ENHANCED: Get market analysis with multiple fallback mechanisms
  const getMarketAnalysis = async (retryAttempt = 0) => {
    if (!analysisQuery.trim()) {
      alert(t('market.analysisPlaceholder') || 'Please enter a question');
      return;
    }

    setAnalysisLoading(true);
    setAnalysisResult('');
    
    try {
      const apiUrl = `${process.env.REACT_APP_API_URL || 'http://localhost:8000/api'}/market-analysis/`;
      
      // ✅ FALLBACK #5: Use multiple language sources in order of preference
      let finalLanguage = languageRef.current;  // Ref is immediate  
      if (!finalLanguage || finalLanguage === 'en') {
        finalLanguage = languageForAnalysis;  // State cache
      }
      if (!finalLanguage) {
        finalLanguage = language || 'en';  // Context
      }
      
      console.log(`\n${'='.repeat(60)}`);
      console.log(`🔄 ANALYSIS REQUEST #${retryAttempt + 1}`);
      console.log(`${'='.repeat(60)}`);
      console.log(`📡 API URL: ${apiUrl}`);
      console.log(`📝 Query: ${analysisQuery}`);
      console.log(`🌐 Language (ref): ${languageRef.current}`);
      console.log(`🔄 Language (state cache): ${languageForAnalysis}`);
      console.log(`🌐 Language (context): ${language}`);
      console.log(`✅ FINAL Language to send: ${finalLanguage}`);
      console.log(`🔄 Retry attempt: ${retryAttempt}`);
      
      const response = await fetch(apiUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: analysisQuery,
          language: finalLanguage,  // ✅ Use the guaranteed language
          commodity: selectedCommodity || '',
          retry_count: retryAttempt  // Send to backend for logging
        })
      });

      console.log(`📨 Response status: ${response.status}`);

      if (!response.ok) {
        const errorData = await response.json();
        console.error('❌ API Error:', errorData);
        throw new Error(errorData.error || `Server error: ${response.status}`);
      }

      const data = await response.json();
      console.log(`✅ Analysis received from backend`);
      console.log(`📊 Backend returned language: ${data.language || 'NOT SPECIFIED'}`);
      
      // Extract analysis text from response
      const analysisText = typeof data.analysis === 'string' 
        ? data.analysis 
        : (data.analysis && data.analysis.analysis) 
          ? data.analysis.analysis 
          : 'No analysis available';
      
      const cleanedAnalysis = analysisText.trim();
      console.log(`📄 Response text (first 150 chars): ${cleanedAnalysis.substring(0, 150)}`);
      
      // ✅ FALLBACK #6: Detect actual language of returned text
      const detectedLang = detectLanguageOfText(cleanedAnalysis);
      const responseLanguage = data.language || finalLanguage;
      
      console.log(`🔍 Character detection: ${detectedLang}`);
      console.log(`🔍 Expected language: ${finalLanguage}`);
      console.log(`🔍 Match: ${detectedLang === finalLanguage ? '✅ YES' : '❌ NO'}`);
      
      // ✅ FALLBACK #7: If language mismatch and haven't retried yet, retry with stronger enforcement
      if (detectedLang !== finalLanguage && finalLanguage !== 'en' && retryAttempt < 2) {
        console.warn(`⚠️ Language mismatch! Expected ${finalLanguage}, got ${detectedLang}`);
        console.log(`🔄 Retrying with explicit language enforcement...`);
        setRetryCount(retryAttempt + 1);
        
        // Wait 500ms then retry
        await new Promise(resolve => setTimeout(resolve, 500));
        return getMarketAnalysis(retryAttempt + 1);
      }
      
      // ✅ FALLBACK #8: Store result WITH language metadata for display
      const resultWithLanguage = {
        text: cleanedAnalysis,
        language: responseLanguage,
        detectedLanguage: detectedLang,
        sentLanguage: finalLanguage,
        timestamp: new Date().toISOString()
      };
      
      setAnalysisResult(cleanedAnalysis);
      // Store full metadata in a separate ref if needed for debugging
      window.lastAnalysisLanguageMetadata = resultWithLanguage;
      
      console.log(`✅ RESULT SET FOR DISPLAY`);
      console.log(`   Text language: ${resultWithLanguage.language}`);
      console.log(`   Display language: ${finalLanguage}`);
      console.log(`${'='.repeat(60)}\n`);
      
      // Speak the analysis with RESPONSE language (what backend returned)
      if (cleanedAnalysis && cleanedAnalysis !== 'No analysis available') {
        setTimeout(() => {
          console.log(`🔊 Speaking in language: ${responseLanguage}`);
          speakAnalysis(cleanedAnalysis);
        }, 500);
      }
      
      setRetryCount(0);  // Reset retries on success
    } catch (error) {
      console.error('❌ Error getting market analysis:', error);
      const errorMsg = `Error: ${error.message || 'Could not analyze. Please check connection.'}`;
      setAnalysisResult(errorMsg);
    } finally {
      setAnalysisLoading(false);
    }
  };

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
      // agriculture
      'rice': 'rice',
      'wheat': 'wheat',
      'onion': 'onion',
      'carrot': 'carrot',
      'tomato': 'tomato',
      'potato': 'potato',
      // fruits
      'banana': 'banana',
      'mango': 'mango',
      'apple': 'apple',
      'orange': 'orange',
      // dairy
      'milk': 'milk',
      'ghee': 'ghee',
      'yogurt': 'yogurt',
      'paneer': 'paneer',
      // spices
      'turmeric': 'turmeric',
      'chili': 'chili',
      'chili powder': 'chili',
      'coconut': 'coconut',
      'coriander': 'coriander',
      'coriander powder': 'coriander',
      'black pepper': 'black pepper',
      // oils
      'coconut oil': 'coconut oil',
      'sesame oil': 'sesame oil',
      // processed foods
      'pickle': 'pickle',
      'jams': 'jams',
      'dry snacks': 'dry snacks',
      // handicrafts
      'handmade cloth': 'handmade cloth',
      'embroidered saree': 'embroidered saree',
      'handmade jewelry': 'handmade jewelry',
      'wooden craft': 'wooden craft',
    };
    const key = comMap[comKey];
    if (key) return t(`market.commodities.${key}`) || commodityName;
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

      {/* AI Market Analysis Section */}
      <div style={{
        background: 'linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%)',
        borderRadius: 'var(--radius-lg)',
        padding: '24px',
        marginBottom: '24px',
        color: 'white',
        boxShadow: '0 8px 32px rgba(0, 0, 0, 0.15)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' }}>
          <Sparkles size={24} />
          <h2 style={{ margin: '0', fontSize: 'var(--font-xl)', fontWeight: 700 }}>
            {t('market.aiAnalysis') || 'Market Intelligence'}
          </h2>
        </div>

        {/* Analysis Input */}
        <div style={{ display: 'flex', gap: '12px', marginBottom: '16px', flexWrap: 'wrap' }}>
          <input
            type="text"
            placeholder={t('market.analysisPlaceholder') || "Ask about market trends, pricing, or products... (or use voice)"}
            value={analysisQuery}
            onChange={(e) => setAnalysisQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && !analysisLoading && getMarketAnalysis()}
            style={{
              flex: 1,
              minHeight: '40px',
              minWidth: '200px',
              padding: '10px 16px',
              border: '1px solid rgba(255,255,255,0.3)',
              borderRadius: 'var(--radius-md)',
              fontSize: 'var(--font-base)',
              background: 'rgba(255,255,255,0.15)',
              color: 'white',
              outline: 'none',
              backdropFilter: 'blur(10px)',
            }}
            disabled={analysisLoading || isListening}
          />

          <button
            onClick={isListening ? stopListening : startListening}
            style={{
              background: isListening ? '#ef4444' : 'rgba(255,255,255,0.3)',
              color: 'white',
              border: '1px solid rgba(255,255,255,0.3)',
              padding: '10px 16px',
              minHeight: '40px',
              borderRadius: 'var(--radius-md)',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              transition: 'all 0.3s ease',
              fontWeight: 600,
            }}
            title={isListening ? t('market.stop') : t('market.voice')}
          >
            {isListening ? <MicOff size={18} /> : <Mic size={18} />}
            {isListening ? t('market.stop') : t('market.voice')}
          </button>

          <button
            onClick={getMarketAnalysis}
            disabled={!analysisQuery.trim() || analysisLoading}
            style={{
              background: analysisQuery.trim() && !analysisLoading ? '#10b981' : '#9ca3af',
              color: 'white',
              border: 'none',
              padding: '10px 16px',
              minHeight: '40px',
              borderRadius: 'var(--radius-md)',
              cursor: analysisQuery.trim() && !analysisLoading ? 'pointer' : 'not-allowed',
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              transition: 'all 0.3s ease',
              fontWeight: 600,
            }}
          >
            {analysisLoading ? <Loader2 size={18} className="animate-spin" /> : <Send size={18} />}
            {analysisLoading ? t('market.analyzing') : t('market.analyze')}
          </button>
        </div>

        {/* Commodity Selector */}
        <div style={{ marginBottom: '16px' }}>
          <label style={{ fontSize: 'var(--font-sm)', opacity: 0.9, marginBottom: '8px', display: 'block' }}>
            {t('market.commodityLabel') || 'Select commodity for context:'}
          </label>
          <select
            value={selectedCommodity}
            onChange={(e) => setSelectedCommodity(e.target.value)}
            style={{
              width: '100%',
              marginTop: '8px',
              padding: '10px 12px',
              border: '1px solid rgba(255,255,255,0.3)',
              borderRadius: 'var(--radius-md)',
              background: 'rgba(255,255,255,0.2)',
              color: 'white',
              fontSize: 'var(--font-sm)',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
            }}
          >
            <option style={{background: '#333', color: 'white'}} value="">{t('market.generalAnalysis')}</option>
            {[...new Set(prices.map(p => p.commodity_name))].map(commodity => (
              <option key={commodity} style={{background: '#333', color: 'white'}} value={commodity}>
                {getCommodityName(commodity)}
              </option>
            ))}
          </select>
        </div>

        {/* Analysis Result Display */}
        {analysisResult && (
          <div style={{
            background: 'rgba(255,255,255,0.1)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255,255,255,0.2)',
            borderRadius: 'var(--radius-md)',
            padding: '20px',
            marginTop: '20px',
            fontSize: 'var(--font-sm)',
            lineHeight: '1.8',
            whiteSpace: 'pre-wrap',
            wordWrap: 'break-word',
            animation: 'fadeIn 0.3s ease-in'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '12px' }}>
              <h3 style={{ margin: '0', fontSize: 'var(--font-lg)', fontWeight: 600 }}>
                {t('market.analysis') || 'Analysis Result'}:
              </h3>
              {analysisResult && !analysisResult.startsWith('Error:') && (
                <button
                  onClick={isSpeaking ? stopSpeaking : () => speakAnalysis(analysisResult)}
                  style={{
                    background: isSpeaking ? '#ef4444' : '#3b82f6',
                    color: 'white',
                    border: 'none',
                    padding: '8px 12px',
                    borderRadius: 'var(--radius-sm)',
                    cursor: 'pointer',
                    fontSize: 'var(--font-xs)',
                    fontWeight: 600,
                    transition: 'all 0.2s ease',
                  }}
                  title={isSpeaking ? t('market.stopSpeaking') : t('market.speak')}
                >
                  🔊 {isSpeaking ? t('market.stop') : t('market.speak')}
                </button>
              )}
            </div>
            
            {/* Images removed - text only display */}
            
            <div style={{ color: 'rgba(255,255,255,0.95)', display: 'block' }}>
              {analysisResult}
            </div>
          </div>
        )}
      </div>

      {/* Market Prices List */}
      {loading ? (
        <div style={{ textAlign: 'center', padding: '48px 16px' }}>
          <Loader2 size={32} className="animate-spin" style={{ margin: '0 auto', color: '#f59e0b' }} />
          <p style={{ marginTop: '16px', color: 'var(--gray-600)', fontSize: 'var(--font-base)' }}>{t('common.loading')}</p>
        </div>
      ) : (
        filtered.length > 0 && (
          <div><h2 style={{ margin: '0 0 16px', fontWeight: 700, fontSize: 'var(--font-xl)', color: 'var(--gray-900)' }}>
            {t('market.allPrices') || 'All Market Prices'}
          </h2></div>
        )
      )}

      {/* All Market Prices Grid (when not showing analysis data) */}
      {!loading && filtered.length > 0 && (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '16px' }}>
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
                  overflow: 'hidden',
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
                {/* Card Content */}
                <div style={{ padding: '16px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                    <div style={{ flex: 1 }}>
                      <h3 style={{ margin: '0', fontSize: 'var(--font-lg)', fontWeight: 700, color: 'var(--gray-900)' }}>
                        {getCommodityName(p.commodity_name)}
                      </h3>
                      <p style={{ margin: '4px 0 0', fontSize: 'var(--font-sm)', color: 'var(--gray-600)' }}>
                        {getMarketName(p.market_location)}
                      </p>
                    </div>
                    <div style={{
                      background: trendBg[trend],
                      color: trendColor[trend],
                      padding: '6px 10px',
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

                  {/* Price */}
                  <div style={{ borderTop: '1px solid rgba(0, 0, 0, 0.1)', paddingTop: '12px', marginTop: '12px' }}>
                    <p style={{ margin: '0 0 8px', fontSize: 'var(--font-xs)', color: 'var(--gray-600)', fontWeight: 600, textTransform: 'uppercase' }}>
                      {t('market.currentPrice')}
                    </p>
                    <div style={{ display: 'flex', alignItems: 'flex-end', gap: '8px' }}>
                      <p style={{ margin: '0', fontSize: 'var(--font-xl)', fontWeight: 700, color: '#f59e0b' }}>
                        {formatCurrencyForLanguage(p.price, lang)}
                      </p>
                      <p style={{ margin: '0 0 4px', fontSize: 'var(--font-sm)', color: 'var(--gray-600)', fontWeight: 600 }}>
                        /{getUnitLabel(p.unit)}
                      </p>
                    </div>
                  </div>

                  {/* Date */}
                  <p style={{ margin: '12px 0 0', fontSize: 'var(--font-xs)', color: 'var(--gray-500)', fontStyle: 'italic' }}>
                    {t('market.updated')} {formatDateForLanguage(p.market_date, lang)}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {!loading && filtered.length === 0 && (
        <div style={{ textAlign: 'center', padding: '48px 16px', background: 'white', borderRadius: 'var(--radius-lg)', border: '2px dashed var(--gray-300)' }}>
          <Store size={48} style={{ margin: '0 auto', color: '#f59e0b', opacity: 0.3, marginBottom: '12px' }} />
          <p style={{ fontSize: 'var(--font-lg)', color: 'var(--gray-600)', margin: '0' }}>{t('market.noRecords')}</p>
        </div>
      )}
    </div>
  );
}

