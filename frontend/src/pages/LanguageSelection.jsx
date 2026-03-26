import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useLanguage } from '../hooks/useLanguage';
import './LanguageSelection.css';

const LANGUAGES = [
  {
    code: 'en',
    flag: '🇬🇧',
    native: 'English',
    english: 'English',
    phrase: "Welcome! Let's grow your business.",
    button: 'Continue in English',
    color: '#4f46e5',
  },
  {
    code: 'hi',
    flag: '🇮🇳',
    native: 'हिन्दी',
    english: 'Hindi',
    phrase: 'नमस्ते! अपना व्यापार बढ़ाएं।',
    button: 'हिन्दी में जारी रखें',
    color: '#7c3aed',
  },
  {
    code: 'ta',
    flag: '🇮🇳',
    native: 'தமிழ்',
    english: 'Tamil',
    phrase: 'வணக்கம்! உங்கள் தொழிலை வளர்க்கலாம்.',
    button: 'தமிழில் தொடரவும்',
    color: '#9333ea',
  },
];

export default function LanguageSelection() {
  const navigate = useNavigate();
  const { setLanguage } = useLanguage();
  const [selected, setSelected] = useState(
    localStorage.getItem('language') || null
  );
  const [animating, setAnimating] = useState(false);

  const handleSelect = (code) => {
    if (animating) return;
    setAnimating(true);
    setSelected(code);
    setLanguage(code);
    setTimeout(() => navigate('/dashboard'), 600);
  };

  return (
    <div className="lang-container">
      <div className="lang-bg" />
      <div className="lang-glow-1" />
      <div className="lang-glow-2" />

      <motion.div
        className="lang-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        <div className="lang-logo">🌸</div>
        <h1 className="lang-title">MAHILA UDYAM</h1>
        <p className="lang-subtitle">Choose your language</p>
        <p className="lang-subtitle-multi">
          अपनी भाषा चुनें &nbsp;•&nbsp; உங்கள் மொழியை தேர்ந்தெடுக்கவும்
        </p>
      </motion.div>

      <div className="lang-cards">
        {LANGUAGES.map((lang, i) => (
          <motion.div
            key={lang.code}
            className={`lang-card ${selected === lang.code ? 'lang-card-selected' : ''}`}
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.15, duration: 0.6 }}
            whileHover={{ scale: 1.03, y: -4 }}
            whileTap={{ scale: 0.97 }}
            onClick={() => handleSelect(lang.code)}
            style={{ '--card-color': lang.color }}
          >
            {selected === lang.code && (
              <div className="lang-check">✓</div>
            )}
            <div className="lang-flag">{lang.flag}</div>
            <div className="lang-native">{lang.native}</div>
            <div className="lang-english">{lang.english}</div>
            <div className="lang-phrase">{lang.phrase}</div>
            <button className="lang-btn">{lang.button}</button>
          </motion.div>
        ))}
      </div>
    </div>
  );
}
