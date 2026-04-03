/**
 * Text-to-Speech (TTS) Service for Mahila Udyam
 * Provides voice output with multi-language support (English, Hindi, Tamil)
 * Uses Web Speech API's SpeechSynthesis for natural speech output
 */

// Language to voice mapping
const LANGUAGE_VOICE_MAP = {
  en: 'en-IN',      // English (India)
  hi: 'hi-IN',      // Hindi (India)
  ta: 'ta-IN',      // Tamil (India)
};

// Speech synthesis configuration
const SPEECH_CONFIG = {
  rate: 0.9,        // Speed (0.1 - 10, default 1)
  pitch: 1.0,       // Pitch (0 - 2, default 1)
  volume: 1.0,      // Volume (0 - 1, default 1)
};

// Current utterance being spoken
let currentUtterance = null;

/**
 * Initialize speech synthesis voices
 * Required for Chrome - waits for voices to load before speaking
 * @returns {Promise<void>}
 */
const initializeVoices = async () => {
  const synth = window.speechSynthesis;
  
  return new Promise((resolve) => {
    if (synth.getVoices().length > 0) {
      resolve();
      return;
    }

    const voiceschanged = () => {
      synth.removeEventListener('voiceschanged', voiceschanged);
      resolve();
    };

    synth.addEventListener('voiceschanged', voiceschanged);
    
    // Timeout fallback for browsers that don't support voiceschanged
    setTimeout(() => {
      synth.removeEventListener('voiceschanged', voiceschanged);
      resolve();
    }, 1000);
  });
};

/**
 * Get appropriate voice for language
 * @param {string} lang - Language code (en|hi|ta)
 * @returns {SpeechSynthesisVoice|null}
 */
const getVoiceForLanguage = (lang) => {
  const voiceLang = LANGUAGE_VOICE_MAP[lang] || LANGUAGE_VOICE_MAP.en;
  const synth = window.speechSynthesis;
  const voices = synth.getVoices();

  // Try to find exact match
  let voice = voices.find(v => v.lang === voiceLang);
  
  // Fallback to language prefix
  if (!voice) {
    const langPrefix = voiceLang.split('-')[0];
    voice = voices.find(v => v.lang.startsWith(langPrefix));
  }

  // Default to first available voice
  if (!voice && voices.length > 0) {
    voice = voices[0];
  }

  return voice || null;
};

/**
 * Speak text in specified language
 * @param {string} text - Text to speak
 * @param {string} lang - Language code (en|hi|ta)
 * @returns {Promise<void>}
 */
export const speak = async (text, lang = 'en') => {
  try {
    // Check if browser supports Web Speech API
    if (!('speechSynthesis' in window)) {
      console.warn('Speech Synthesis API not supported in this browser');
      return;
    }

    // Initialize voices (required for Chrome)
    await initializeVoices();

    // Cancel any current speech
    window.speechSynthesis.cancel();

    // Get appropriate voice
    const voice = getVoiceForLanguage(lang);
    if (!voice) {
      console.warn(`No voice found for language: ${lang}`);
      return;
    }

    // Create utterance
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.voice = voice;
    utterance.lang = LANGUAGE_VOICE_MAP[lang] || LANGUAGE_VOICE_MAP.en;
    utterance.rate = SPEECH_CONFIG.rate;
    utterance.pitch = SPEECH_CONFIG.pitch;
    utterance.volume = SPEECH_CONFIG.volume;

    // Store reference for cancellation
    currentUtterance = utterance;

    // Handle completion
    return new Promise((resolve, reject) => {
      utterance.onend = () => {
        currentUtterance = null;
        resolve();
      };

      utterance.onerror = (event) => {
        currentUtterance = null;
        console.error('Speech synthesis error:', event.error);
        reject(new Error(`Speech error: ${event.error}`));
      };

      // Speak
      window.speechSynthesis.speak(utterance);
    });
  } catch (error) {
    console.error('Error in voice output:', error);
    throw error;
  }
};

/**
 * Stop current speech output
 * @returns {void}
 */
export const stop = () => {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
    currentUtterance = null;
  }
};

/**
 * Check if currently speaking
 * @returns {boolean}
 */
export const isSpeaking = () => {
  return 'speechSynthesis' in window && window.speechSynthesis.speaking;
};

/**
 * Get available voices for language
 * @param {string} lang - Language code (en|hi|ta)
 * @returns {SpeechSynthesisVoice[]}
 */
export const getVoicesForLanguage = (lang) => {
  if (!('speechSynthesis' in window)) {
    return [];
  }

  const voiceLang = LANGUAGE_VOICE_MAP[lang] || LANGUAGE_VOICE_MAP.en;
  const voices = window.speechSynthesis.getVoices();
  
  return voices.filter(v => v.lang === voiceLang || v.lang.startsWith(voiceLang.split('-')[0]));
};

/**
 * Get all available voices
 * @returns {SpeechSynthesisVoice[]}
 */
export const getAllVoices = () => {
  if (!('speechSynthesis' in window)) {
    return [];
  }

  return window.speechSynthesis.getVoices();
};

/**
 * Pause speech output (if supported)
 * @returns {void}
 */
export const pause = () => {
  if ('speechSynthesis' in window && window.speechSynthesis.pause) {
    window.speechSynthesis.pause();
  }
};

/**
 * Resume speech output (if supported)
 * @returns {void}
 */
export const resume = () => {
  if ('speechSynthesis' in window && window.speechSynthesis.resume) {
    window.speechSynthesis.resume();
  }
};

export default {
  speak,
  stop,
  isSpeaking,
  getVoicesForLanguage,
  getAllVoices,
  pause,
  resume,
};
