# Gemini API Integration Guide

## Overview

The Mahila Udyam SAKHI Voice Assistant now supports optional integration with Google's Gemini AI to provide **enhanced, personalized responses** to women entrepreneurs. This feature is completely **optional** and the application works perfectly fine without it.

## Benefits of Gemini API Integration

### 🎯 Enhanced Responses
- **More Natural**: AI-generated responses feel conversational and human-like
- **Context-Aware**: Gemini understands business context and provides specific advice
- **Personalized**: Responses tailored to user's business type and situation

### 💼 Business Intelligence
- **Mentor Advice**: Get AI-generated business growth strategies
- **Market Insights**: Analyze current prices and predict market trends
- **Scheme Recommendations**: Automatic government scheme suggestions based on profile
- **Decision Support**: Help with financial decisions (what to buy/sell, when to invest)

### 🌍 Multi-Language Support
- Fully functional in **English, Hindi, and Tamil**
- Responses automatically generated in the user's selected language

### 📊 Use Cases
1. **Voice Recording Enhancement**
   - User says: "I sold 10kg tomatoes at ₹50 per kg"
   - Response (without Gemini): "Sale of ₹500 recorded"
   - Response (with Gemini): "Great! You sold tomatoes at ₹50/kg. Market rate is ₹45-55, so you got a good price. Consider increasing volumes..."

2. **Mentor Chat**
   - User asks: "How can I increase my income?"
   - Gemini provides personalized strategies based on their business type

3. **Market Analysis**
   - User checks: "What is the price of vegetables today?"
   - Gemini provides insights on when to buy/sell

## Setup Instructions

### Option 1: Using Gemini API (Recommended)

#### Step 1: Get a Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click "Create API Key" → "Create API key in new project"
3. Copy your API key

#### Step 2: Add API Key to Project
1. Open `backend/.env` in your editor
2. Replace the empty value:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
3. Save the file

#### Step 3: Reinstall Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Step 4: Restart Backend
```bash
python manage.py runserver
```

You should see:
```
✅ Gemini API initialized successfully
```

### Option 2: Without Gemini API (Still Works!)

If you don't have/want to use Gemini:
1. Leave `GEMINI_API_KEY` empty in `.env`
2. Application runs normally with rule-based responses
3. No features are lost, just less AI enhancement

## How It Works

### Architecture

```
Voice Input (Hindi)
    ↓
Language Detection (auto)
    ↓
Intent Prediction (income/expense/mentor/etc)
    ↓
Rule Engine Processing (extract amounts, dates)
    ↓
Database Save (Income/Expense/Sales record)
    ↓
[NEW] Gemini Enhancement (if enabled & API available)
    ↓
Response to User (in Hindi)
```

### Error Handling

The implementation is **bulletproof**:
- ✅ Works without API key installed
- ✅ Graceful fallback if API key missing
- ✅ Falls back to rule-based if API fails
- ✅ No crashes if rate limited
- ✅ Logs all errors for debugging

### Code Integration Points

**In `backend/ml_models/voice_views.py`:**
```python
# Step 4: Optional Gemini AI enhancement
if GeminiHelper.is_available():
    enhanced = GeminiHelper.enhance_response(
        text=text,
        language=language,
        context=context
    )
    if enhanced:
        response = enhanced  # Use AI response
    # else: fall back to rule-based response

# If Gemini fails for any reason:
# - Missing API key → skipped
# - API error → logged, falls back
# - Rate limit → logged, falls back
```

## Available Gemini Features

### 1. Response Enhancement
**Used in**: Voice Assistant (all intents)
**What it does**: Makes responses more natural and contextual
```python
GeminiHelper.enhance_response(text, language, context)
```

### 2. Mentor Advice
**Used in**: Mentor page (future enhancement)
**What it does**: Generate personalized business growth strategies
```python
GeminiHelper.generate_mentor_advice(user_data, language)
```

### 3. Market Insights
**Used in**: Market Price page (future enhancement)
**What it does**: Analyze products and recommend buy/sell timing
```python
GeminiHelper.analyze_market_insight(product, price, language)
```

### 4. Scheme Recommendations
**Used in**: Government Schemes page (future enhancement)
**What it does**: Recommend relevant government schemes for user
```python
GeminiHelper.recommend_schemes(user_profile, language)
```

## Testing the Integration

### Test Without Gemini (Default)
```bash
# Backend logs show:
# ℹ️  Gemini API key not found. Set GEMINI_API_KEY in .env
# ℹ️  Response generated using rule-based engine
```

### Test With Gemini (After Adding Key)
```bash
# Backend logs show:
# ✅ Gemini API initialized successfully
# 🤖 Attempting to enhance response with Gemini AI...
# ✅ Response enhanced with Gemini AI
```

### Example Test Command
In VoiceAssistant page or via text input:
```
Hindi: "आज मैंने 5 किग्रा टमाटर 60 रुपये किलो में बेचे"
English: "Today I sold 5kg tomatoes at 60 rupees per kg"
Tamil: "இன்று நான் 60 ரூபாய்க்கு 5 கிலோ தக்காளி விற்றேன்"
```

**Without Gemini:**
- "Sale of ₹300 recorded"

**With Gemini:**
- "Great! You've recorded a sale of ₹300 for 5kg tomatoes at ₹60/kg. Current market prices are ₹55-65/kg in Tamil Nadu, so you got a competitive rate. Tomatoes are in high demand during monsoon season. Consider connecting with local vendors for bulk orders..."

## Troubleshooting

### Problem: "Gemini not available" message
**Solution**: Check if API key is set
```bash
cd backend
grep GEMINI_API_KEY .env
# Should show: GEMINI_API_KEY=sk-xxxxx (not empty)
```

### Problem: "Failed to initialize Gemini API"
**Possible reasons:**
1. API key is invalid → Get a new one from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. API key has no credits → Gemini API is free but requires a billing account
3. Network issue → Check internet connection

### Problem: Response takes too long
**Why**: Gemini API calls take 1-3 seconds
**Solution**: This is normal for AI responses. Frontend timeout is set to 30 seconds.

### Problem: Want to disable Gemini temporarily
**Solution**: Set `GEMINI_API_KEY=` (empty) in `.env` and restart

## Security Notes

✅ **Safe Implementation:**
- API key stored in `.env` (never in code)
- API key never logged or sent to database
- Only device sends requests to Google Gemini
- Backend doesn't expose API key to frontend

⚠️ **Keep Your API Key Secret:**
- Never commit `.env` file to git
- `.gitignore` already excludes `.env`
- If key is leaked, regenerate from Google AI Studio

## Performance Impact

| Scenario | Time | Impact |
|----------|------|--------|
| Response without Gemini | ~200ms | Instant |
| Response with Gemini | ~1-3 seconds | Noticeable but acceptable |
| Voice processing (incl. Gemini) | ~2-4 seconds | User barely notices |

**Note**: Response caching coming soon for repeated queries

## Future Enhancements

📋 **Planned Features:**
- [ ] Response caching to reduce API calls
- [ ] Gemini streaming for real-time response generation
- [ ] Multi-turn conversation history
- [ ] Cost analysis (what to produce vs sell)
- [ ] Video tutorial generation
- [ ] Compliance checking (regulations, schemes eligibility)

## Feedback & Support

If you have issues or suggestions:
1. Check error logs: `python manage.py logs`
2. Review this guide
3. Contact: support@mahilaudyam.app

---

**Last Updated**: 2024
**Gemini Model**: gemini-pro
**Status**: Production Ready ✅
