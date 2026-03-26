import { useLanguage as useLanguageContext } from '../context/LanguageContext';

export function useLanguage() {
  return useLanguageContext();
}
