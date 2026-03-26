import React, { createContext, useContext, useState, useCallback, useEffect } from 'react';
import { translations } from '../utils/translations';

const LanguageContext = createContext(null);

export const LanguageProvider = ({ children }) => {
  const [language, setLanguageState] = useState(() => {
    const saved = localStorage.getItem('language');
    return saved || 'en';
  });

  const setLanguage = useCallback((code) => {
    if (!['en', 'hi', 'ta'].includes(code)) return;
    localStorage.setItem('language', code);
    localStorage.setItem('languageSelected', 'true');
    setLanguageState(code);
    document.documentElement.lang = code;
    window.dispatchEvent(
      new CustomEvent('languageChanged', { detail: { code } })
    );
  }, []);

  // Translate key - fallback to English then key itself
  const t = useCallback((key) => {
    if (!key) return '';
    const keys = key.split('.');
    const resolve = (obj) => keys.reduce((acc, k) => acc?.[k], obj);
    return (
      resolve(translations[language]) ||
      resolve(translations['en']) ||
      key
    );
  }, [language]);

  // Get BCP-47 voice language code
  const getVoiceLang = useCallback(() => {
    const map = { en: 'en-IN', hi: 'hi-IN', ta: 'ta-IN' };
    return map[language] || 'en-IN';
  }, [language]);

  useEffect(() => {
    document.documentElement.lang = language;
  }, [language]);

  return (
    <LanguageContext.Provider value={{ language, lang: language, setLanguage, t, getVoiceLang }}>
      {children}
    </LanguageContext.Provider>
  );
};

export const useLanguage = () => {
  const ctx = useContext(LanguageContext);
  if (!ctx) {
    throw new Error('useLanguage must be used inside LanguageProvider');
  }
  return ctx;
};

export { LanguageContext };

export default LanguageProvider;
