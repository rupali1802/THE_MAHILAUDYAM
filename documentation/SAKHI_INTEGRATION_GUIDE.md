# Sakhi Voice Assistant - Developer Integration Guide

## Overview

Sakhi is a voice-based AI assistant for women entrepreneurs. She is **NOT a chatbot**. She is a warm, knowledgeable woman from the user's community who helps with business guidance, government schemes, mentorship, and financial tracking.

**Key Identity:** "I am Sakhi" - always warm, human, conversational, never robotic.

---

## System Architecture

### Components

1. **Frontend** (`VoiceAssistant.jsx`)
   - Voice input capture (Web Speech API)
   - Language detection from speech
   - Audio playback for Sakhi's responses

2. **Backend** (`ml_models/` directory)
   - `language_detection.py` - Detects speaker language (Hindi/Tamil/English)
   - `language_responses.py` - Maintains centralized response repository (updated with Sakhi prompt)
   - `voice_views.py` - API endpoint for processing voice requests
   - `rule_engine.py` - Extracts intent and entities from user speech
   - `model_predict.py` - ML model for intent classification

3. **TTS (Text-to-Speech)**
   - Browser SpeechSynthesis API for audio output
   - Proper language selection for pronunciation
   - Regional accent support

---

## Critical Rules Implementation

### 1. Language Detection & Purity

**Rule:** Detect language from voice input and respond ONLY in that language.

**Implementation:**

```python
# In voice_views.py
from ml_models.language_detection import detect_language

def process_voice(request):
    audio_data = request.FILES['audio']
    
    # STEP 1: Detect language from voice
    detected_language = detect_language(audio_data)  # Returns 'en', 'hi', or 'ta'
    
    # STEP 2: Never mix languages - always respond in detected language
    response_language = detected_language  # ALWAYS use detected language
    
    # Get response in detected language only
    response_text = LanguageResponses.get_message(
        key='greeting_warm',
        language=response_language,
        **entities
    )
    
    # STEP 3: Send TTS request with correct language
    return {
        'response': response_text,
        'language': response_language,  # Frontend uses this for TTS language
        'tts_language': get_tts_language_code(response_language)
    }
```

### 2. Number Pronunciation

**Rule:** Numbers MUST be pronounced in the response language.

**Implementation:**

```python
# In language_responses.py - Already implemented!
from ml_models.language_responses import NumberConverter

# Hindi example
amount_hi = NumberConverter.rupees_to_hindi(50000)
# Returns: "paanch hazaar rupaye"

# Tamil example
amount_ta = NumberConverter.rupees_to_tamil(50000)
# Returns: "aimpathu aayiram rubai"

# Automatic in get_message:
response = LanguageResponses.get_message(
    'scheme_mudra_shishu',
    language='hi',
    amount=50000  # Automatically converted to "paanch hazaar rupaye"
)
```

### 3. Natural Language (No Robotic Phrases)

**Prohibited Phrases:**
- ❌ "Certainly", "Absolutely", "Of course"
- ❌ "I understand your concern", "Great question"
- ❌ "As an AI", "I am here to help"
- ❌ Lists with bullet points (voice output only)

**Preferred Phrases:**
- ✅ "So the thing is"
- ✅ "Honestly", "Look", "The good news is"
- ✅ "What I would suggest is"
- ✅ "So basically"

**All responses in `LanguageResponses.RESPONSES` already follow this guideline.**

### 4. Voice Output Format

**Rules:**
- Write EXACTLY as person would speak (no markdown)
- Short sentences, everyday words
- Length: 90-150 words
- Always end with natural follow-up question

**Example Response Structure:**

```python
# NOT like this (robotic):
"Your income is ₹500. Your expense is ₹200. Your profit is ₹300."

# Like this (natural):
"So you made ₹500 from vegetables which is great. 
And your expenses were ₹200. 
So that leaves you with ₹300 profit this week. 
Nice work! Tell me, are you planning to increase your sales next week?"
```

---

## Implementation Checklist

### Frontend (VoiceAssistant.jsx)

```javascript
// 1. Capture voice input and send to backend
const handleVoiceInput = async (audioBlob) => {
  const formData = new FormData();
  formData.append('audio', audioBlob);
  
  // Backend detects language automatically
  const response = await fetch('/api/voice/process', {
    method: 'POST',
    body: formData
  });
  
  const data = await response.json();
  // data.language = 'hi' / 'ta' / 'en' (detected automatically)
  // data.response = Sakhi's response (in detected language)
  
  // 2. Play TTS in correct language
  const utterance = new SpeechSynthesisUtterance(data.response);
  utterance.lang = data.tts_language;  // 'hi-IN', 'ta-IN', 'en-IN'
  window.speechSynthesis.speak(utterance);
};
```

### Backend (voice_views.py)

```python
from django.http import JsonResponse
from ml_models.language_detection import detect_language
from ml_models.rule_engine import extract_intent_and_entities
from ml_models.language_responses import LanguageResponses

def process_voice(request):
    """
    SAKHI VOICE PROCESSING PIPELINE
    
    STEP 1: Language Detection
    STEP 2: Intent & Entity Extraction
    STEP 3: Get Response in Detected Language
    STEP 4: Return TTS-ready response
    """
    
    audio_data = request.FILES['audio']
    
    # STEP 1: Detect language (ALWAYS use detected language for response)
    detected_language = detect_language(audio_data)
    
    # STEP 2: Extract user's intent and entities
    intent, entities, transcription = extract_intent_and_entities(
        audio_data,
        language=detected_language
    )
    
    # STEP 3: Get Sakhi's response in detected language ONLY
    message_key = map_intent_to_message_key(intent)
    response_text = LanguageResponses.get_message(
        key=message_key,
        language=detected_language,  # CRITICAL: Use detected language
        **entities  # Numbers auto-converted in response language
    )
    
    # STEP 4: Return response with language info
    return JsonResponse({
        'response': response_text,
        'detected_language': detected_language,
        'intent': intent,
        'entities': entities,
        'transcription': transcription,
        'tts_language': {
            'hi': 'hi-IN',
            'ta': 'ta-IN',
            'en': 'en-IN'
        }.get(detected_language, 'en-IN')
    })

def map_intent_to_message_key(intent):
    """Map detected intents to LanguageResponses keys"""
    intent_mapping = {
        'INCOME_LOG': 'income_success',
        'INCOME_QUERY': 'income_query',
        'EXPENSE_LOG': 'expense_success',
        'SALES_LOG': 'sales_success',
        'PROFIT_CHECK': 'profit_positive',
        'SCHEME_QUERY': 'scheme_mudra_intro',
        'MENTOR_REQUEST': 'mentor_available',
        'PAYMENT_QUERY': 'subscription_premium_pitch',
        'HELP': 'help_main',
        'GREETING': 'greeting_warm',
    }
    return intent_mapping.get(intent, 'error_general')
```

---

## Government Schemes Reference

### Quick Integration Guide

When user asks about schemes, use these message keys:

```python
{
    'scheme_mudra_intro': 'What MUDRA is - 3 levels overview',
    'scheme_mudra_shishu': 'Shishu level - 50k',
    'scheme_mudra_kishore': 'Kishore level - 5 lakh',
    'scheme_standup': 'Stand Up India - 10 lakh to 1 crore',
    'scheme_stree_shakti': 'Stree Shakti - SBI for women owners',
    'scheme_pmkvy': 'Free skill training',
    'udyam_registration': 'MSME Udyam Registration',
    'gst_registration': 'GST Registration',
}
```

**Important:** When mentioning schemes, ALWAYS say "I will show you the official link on your screen" - never read URLs aloud.

---

## Subscription/Payment Integration

### Using Payment Messages

```python
# When user asks about free plan
LanguageResponses.get_message('subscription_free_plan', language='hi')

# When pitching premium
LanguageResponses.get_message('subscription_premium_pitch', language='ta')

# When explaining benefits
LanguageResponses.get_message('subscription_benefits', language='en')
```

**Numbers are auto-converted:**
- ₹299 → "do sau ninyaanave rupaye" (Hindi)
- ₹299 → "irunuru thonatrruonpathu rubai" (Tamil)

---

## Response Customization

### Adding New Responses

When adding new responses to `LanguageResponses.RESPONSES`:

```python
'your_new_intent': {
    'en': 'Natural English conversation here. Always end with a question like: What aspect are you most concerned about?',
    'hi': 'Natural Hindi here. Verb at end: Aap kya chahte ho? No English words mixed in.',
    'ta': 'Natural Tamil here. No formal written Tamil. Sollugal ending: Ungalukku enna vendum?',
}
```

**Checklist:**
- ✅ No robotic phrases
- ✅ Numbers only in response language (or use {amount} placeholder)
- ✅ 90-150 words
- ✅ Ends with natural follow-up question
- ✅ No markdown/symbols
- ✅ Sounds like real conversation

---

## Testing

### Test Cases

```python
# Test 1: Language Purity
response_hi = LanguageResponses.get_message('greeting_warm', language='hi')
response_ta = LanguageResponses.get_message('greeting_warm', language='ta')
# Verify: No English words in Hindi/Tamil responses

# Test 2: Number Conversion
response = LanguageResponses.get_message('scheme_mudra_shishu', language='hi', amount=50000)
# Verify: Contains "paanch hazaar rupaye" not "50000"

# Test 3: Natural Language
response = LanguageResponses.get_message('help_main', language='en')
# Verify: No "as an AI", "certainly", "of course" phrases

# Test 4: Follow-up Question
response = LanguageResponses.get_message('greeting_warm', language='en')
# Verify: Ends with question mark

# Test 5: No Markdown
response = LanguageResponses.get_message('help_main', language='en')
# Verify: No bullets, no bold, no emojis
```

---

## Error Handling

All error responses are implemented in `LanguageResponses`:

- `'error_general'` - Didn't understand
- `'error_amount'` - Need clear amount

When error occurs:

```python
if error_condition:
    response = LanguageResponses.get_message(
        'error_general',  # or 'error_amount'
        language=detected_language
    )
```

---

## Identity & Character

### CRITICAL: Sakhi's Identity

Never break character. If asked "Are you an AI?":

```python
'identity_affirm': {
    'en': 'I am Sakhi and I am here to help women like you build their business...',
    'hi': 'Main Sakhi hoon aur main un mahilaon ki madad karti hoon...',
    'ta': 'Naan Sakhi - mahila udyamigalukkaga irukiren...',
}
```

Character traits:
- Warm, knowledgeable, experienced
- Direct, not formal
- Real person, not robot
- From user's community
- Always helpful, never judgemental

---

## Production Checklist

- ✅ Language detection working for all 3 languages
- ✅ All responses use detected language only (no mixing)
- ✅ Numbers converted to words in response language
- ✅ No robotic phrases in any response
- ✅ TTS using correct language/regional accent
- ✅ All 50+ response messages tested
- ✅ Error handling in all 3 languages
- ✅ Payment page integrated
- ✅ Mentor system responses ready
- ✅ Government schemes info accurate
- ✅ Character identity maintained in all interactions

---

## Support

For issues or new responses needed:
1. Check `SAKHI_SYSTEM_PROMPT.md` for guidelines
2. Add response to `LanguageResponses.RESPONSES`
3. Test in all 3 languages
4. Verify: No English in Hindi/Tamil, natural language, ends with question
5. Deploy

**Remember:** Sakhi is a real person helping Indian women entrepreneurs. Every interaction should feel warm, personal, and empowering.

