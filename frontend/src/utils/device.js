/**
 * Mahila Udyam - Device Utilities
 * Device UUID, language, formatting, TTS functions
 */

// ==================== DEVICE ID ====================
export function getDeviceId() {
  let deviceId = localStorage.getItem('mu_device_id');
  if (!deviceId) {
    deviceId = 'MU-' + generateUUID();
    localStorage.setItem('mu_device_id', deviceId);
  }
  return deviceId;
}

function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0;
    const v = c === 'x' ? r : (r & 0x3) | 0x8;
    return v.toString(16);
  });
}

// ==================== LANGUAGE ====================
export function getLanguage() {
  return localStorage.getItem('mu_language') || 'en';
}

export function setLanguage(lang) {
  localStorage.setItem('mu_language', lang);
  document.documentElement.lang = lang;
  window.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang } }));
}

// ==================== CURRENCY FORMATTING ====================
export function formatCurrencyForLanguage(amount, lang) {
  const num = parseFloat(amount) || 0;

  // Indian number formatting
  const formatted = new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    minimumFractionDigits: 0,
    maximumFractionDigits: 2,
  }).format(num);

  // Add language-specific suffix
  if (lang === 'hi') return formatted + ' रुपये';
  if (lang === 'ta') return formatted + ' ரூபாய்';
  return formatted;
}

export function formatNumber(amount, lang) {
  const num = parseFloat(amount) || 0;
  return new Intl.NumberFormat('en-IN').format(num);
}

// ==================== DATE FORMATTING ====================
const MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
const MONTHS_HI = ['जनवरी', 'फरवरी', 'मार्च', 'अप्रैल', 'मई', 'जून', 'जुलाई', 'अगस्त', 'सितंबर', 'अक्टूबर', 'नवंबर', 'दिसंबर'];
const MONTHS_TA = ['ஜனவரி', 'பிப்ரவரி', 'மார்ச்', 'ஏப்ரல்', 'மே', 'ஜून்', 'ஜுலை', 'ஆகஸ்ட்', 'செப்டம்பர்', 'அக்டோபர்', 'நவம்பர்', 'டிசம்பர்'];

const MONTHS = {
  en: MONTHS_EN,
  hi: MONTHS_HI,
  ta: MONTHS_TA,
};

export function formatDateForLanguage(dateStr, lang) {
  if (!dateStr) return '';
  const date = new Date(dateStr);
  if (isNaN(date)) return dateStr;
  const day = date.getDate();
  const monthArray = MONTHS[lang] || MONTHS_EN;
  const month = monthArray[date.getMonth()];
  const year = date.getFullYear();
  return `${day} ${month} ${year}`;
}

export function getTodayString() {
  return new Date().toISOString().split('T')[0];
}

// ==================== NUMBER TO WORDS ====================
export function numberToWords(num, lang) {
  const n = Math.floor(parseFloat(num) || 0);

  const onesEn = ['', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
    'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen',
    'seventeen', 'eighteen', 'nineteen'];
  const tensEn = ['', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'];

  const onesHi = ['', 'ek', 'do', 'teen', 'chaar', 'paanch', 'chhah', 'saat', 'aath', 'nau',
    'das', 'gyarah', 'barah', 'terah', 'chaudah', 'pandrah', 'solah', 'satrah', 'atharah', 'unnees'];

  const onesTa = ['', 'ondru', 'irandu', 'moondru', 'naangu', 'ainthu', 'aaru', 'ezhu', 'ettu', 'onpathu',
    'pathu', 'pathinondu', 'pannindu', 'pathinmoondru', 'pathinnaangu', 'pathinainthu',
    'pathinaaru', 'pathinezhu', 'pathinettu', 'patthonpathu'];

  function convertEn(n) {
    if (n === 0) return 'zero';
    if (n < 20) return onesEn[n];
    if (n < 100) return tensEn[Math.floor(n / 10)] + (n % 10 ? ' ' + onesEn[n % 10] : '');
    if (n < 1000) return onesEn[Math.floor(n / 100)] + ' hundred' + (n % 100 ? ' ' + convertEn(n % 100) : '');
    if (n < 100000) return convertEn(Math.floor(n / 1000)) + ' thousand' + (n % 1000 ? ' ' + convertEn(n % 1000) : '');
    if (n < 10000000) return convertEn(Math.floor(n / 100000)) + ' lakh' + (n % 100000 ? ' ' + convertEn(n % 100000) : '');
    return convertEn(Math.floor(n / 10000000)) + ' crore' + (n % 10000000 ? ' ' + convertEn(n % 10000000) : '');
  }

  function convertHi(n) {
    if (n === 0) return 'shoonya';
    if (n < 20) return onesHi[n] || String(n);
    if (n < 1000) return convertHi(Math.floor(n / 100)) + ' sau ' + convertHi(n % 100);
    if (n < 100000) return convertHi(Math.floor(n / 1000)) + ' hazaar ' + (n % 1000 ? convertHi(n % 1000) : '');
    if (n < 10000000) return convertHi(Math.floor(n / 100000)) + ' laakh ' + (n % 100000 ? convertHi(n % 100000) : '');
    return convertHi(Math.floor(n / 10000000)) + ' karod ' + (n % 10000000 ? convertHi(n % 10000000) : '');
  }

  function convertTa(n) {
    if (n === 0) return 'poojiyam';
    if (n < 20) return onesTa[n] || String(n);
    if (n < 1000) return convertTa(Math.floor(n / 100)) + ' noooru ' + convertTa(n % 100);
    if (n < 100000) return convertTa(Math.floor(n / 1000)) + ' aayiram ' + (n % 1000 ? convertTa(n % 1000) : '');
    if (n < 10000000) return convertTa(Math.floor(n / 100000)) + ' latcham ' + (n % 100000 ? convertTa(n % 100000) : '');
    return convertTa(Math.floor(n / 10000000)) + ' kodi ' + (n % 10000000 ? convertTa(n % 10000000) : '');
  }

  if (lang === 'hi') return convertHi(n);
  if (lang === 'ta') return convertTa(n);
  return convertEn(n);
}

// ==================== TEXT TO SPEECH ====================
export function speakInLanguage(text, lang) {
  if (!window.speechSynthesis) return;

  window.speechSynthesis.cancel();

  const utterance = new SpeechSynthesisUtterance(text);

  const langMap = { en: 'en-IN', hi: 'hi-IN', ta: 'ta-IN' };
  utterance.lang = langMap[lang] || 'en-IN';
  utterance.rate = 0.9;
  utterance.pitch = 1;
  utterance.volume = 1;

  // Try to pick an appropriate voice
  const voices = window.speechSynthesis.getVoices();
  const targetLang = langMap[lang] || 'en-IN';
  const voice = voices.find(v => v.lang === targetLang) ||
    voices.find(v => v.lang.startsWith(lang)) ||
    voices.find(v => v.lang.startsWith('en'));

  if (voice) utterance.voice = voice;

  window.speechSynthesis.speak(utterance);
}

export function stopSpeaking() {
  if (window.speechSynthesis) {
    window.speechSynthesis.cancel();
  }
}
