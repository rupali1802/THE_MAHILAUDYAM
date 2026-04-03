import { useContext } from 'react';
import { LanguageContext } from '../context/LanguageContext';

export function useLanguage() {
  const ctx = useContext(LanguageContext);
  if (!ctx) {
    // Provide default values when context is not available
    return {
      language: 'en',
      lang: 'en',
      setLanguage: () => {},
      t: (key) => key,
      getVoiceLang: () => 'en-IN'
    };
  }
  return ctx;
}
