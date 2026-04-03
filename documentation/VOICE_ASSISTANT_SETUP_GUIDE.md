# Voice Assistant Setup Guide

## Overview

Mahila Udyam uses the browser's built-in Web Speech API for voice recognition — no external API keys needed, works offline.

## How it Works

```
User speaks → Web Speech API → Text → ML Model → Intent + Response → TTS
```

## Supported Languages

| Language | Code | Speech Recognition | TTS |
|---|---|---|---|
| English | en | en-IN | en-IN |
| Hindi | hi | hi-IN | hi-IN |
| Tamil | ta | ta-IN | ta-IN |

## Browser Compatibility

| Browser | Voice Input | TTS Output |
|---|---|---|
| Chrome (recommended) | ✅ Full support | ✅ |
| Edge | ✅ Full support | ✅ |
| Firefox | ❌ No support | ✅ |
| Safari (iOS 14.5+) | ✅ | ✅ |

**Recommendation:** Use Google Chrome for best experience.

## Microphone Setup

1. Open Chrome
2. Visit your app URL
3. Click the microphone button
4. Chrome will ask for microphone permission
5. Click "Allow"

To fix microphone issues:
- Chrome → Settings → Privacy → Site Settings → Microphone
- Allow your app's URL

## Voice Command Examples

### Income Recording
- "I received 500 rupees today"
- "Income of two thousand from vegetable sale"
- "Got payment 1500 rupees from customer"

### Expense Recording
- "Expense 300 for raw material"
- "Paid 150 electricity bill"
- "Spent 500 on labor"

### Sales Recording
- "Sold 5 kg tomatoes at 40 rupees"
- "Sale of 3 sarees for 2400 rupees"
- "10 pieces sold at 50 each"

### Profit Check
- "Show my profit this month"
- "What is my profit today?"
- "Calculate profit for this week"

## ML Intent Classification

The system uses TF-IDF + Logistic Regression:

1. Text is preprocessed (lowercase, normalize)
2. TF-IDF vectorizer converts to 500 features
3. Logistic Regression predicts intent (9 classes)
4. Rule engine handles the intent and extracts entities
5. Response generated in user's language

**Confidence threshold**: Results with <50% confidence fall back to rule-based matching.

## Troubleshooting

**"Speech recognition not supported"**
→ Switch to Google Chrome

**"Microphone access denied"**
→ Allow microphone in browser settings

**"Network error"**
→ Ensure backend is running at localhost:8000

**Hindi/Tamil not recognized well**
→ Speak clearly, avoid mixing languages
→ Use romanized Hindi/Tamil if native script not recognized
