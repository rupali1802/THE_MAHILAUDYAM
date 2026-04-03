# Mentor Chat System - Implementation Guide

## System Architecture

The Mahila Udyam Mentor Chat system is designed as a **4-Stage Interactive Flow** that guides women entrepreneurs through a smooth mentorship experience.

---

## Stage 1: Select Mentor
**Purpose**: User browsing and mentor selection

### Display Elements:
- **Mentor Grid Cards** showing:
  - Mentor name & avatar  
  - Experience years
  - Rating & reviews
  - Languages spoken
  - Availability status (✅ Available / 🔴 Busy)
  - "Start Chat" button

### Key Features:
- Responsive grid layout
- Hover animations (card lift effect)
- Language-aware mentor display
- Click card to proceed to Stage 2

---

## Stage 2: Select Language
**Purpose**: User chooses preferred communication language

### Language Options:
- 🇬🇧 **English** (en)
- 🇮🇳 **తెలుఫ్ */ Tamil** (ta)
- 🇮🇳 **हिंदी Hindu** (hi)

### Rules:
- ✅ User can change language before chat starts
- ✅ All mentor responses will be in selected language
- ✅ NO language mixing in responses
- ✅ Language auto-detected from voice input

### Backend Compliance:
- Sends language code (`language: 'ta'`) to `/api/mentor-chat/`
- Mentor AI responds ONLY in selected language
- Language detection enforces pure language output (Tamil/Hindi/English - NO mixing)

---

## Stage 3: Select Communication Mode
**Purpose**: User chooses how to interact (Text or Voice)

### Options:

#### ⌨️ Text Mode
- User types questions in text input
- Receives text responses
- Optional: Click "Listen" button to hear response as speech
- No forced voice output

#### 🎤 Voice Mode
- User taps microphone to speak question
- Speech recognition converts voice → text
- Mentor AI responds in text
- Response automatically read aloud via text-to-speech
- User hears mentor's voice response

### Strict Rules:
- **Text Mode**: User inputs text, receives text
- **Voice Mode**: User inputs voice, receives voice response (text read aloud)
- Do NOT convert text-to-speech in pure text mode
- Do NOT show text transcription as speech in voice mode
- Input format and output format MUST match

---

## Stage 4: Chat Interface
**Purpose**: Active mentorship conversation

### Features:

#### Message Display
- **User Messages**: Blue bubble, right-aligned
- **Mentor Messages**: White bubble, left-aligned
- Auto-scroll to latest message
- Timestamps on each message

#### Voice Interaction (if Voice Mode selected)
1. **Listening State**:
   - 🎤 Microphone button shows red "Stop Listening"
   - Yellow input box with "Listening..." indicator
   - Speech recognition active
   
2. **Recording**:
   - Browser records user speech
   - Shows interim transcription
   - Stops automatically when speech ends

3. **Mentor Response**:
   - Text response received from backend
   - Automatically converted to speech
   - Plays audio in selected language
   - User can tap "Stop" to cancel playback

#### Text Interaction (if Text Mode selected)
1. **Input**:
   - User types question
   - "Send" button enabled when text present
   
2. **Optional Voice Playback**:
   - "Listen" button appears on mentor response
   - User can choose to hear response
   - Not forced like in Voice Mode

#### Always Available:
- **Voice Output Controls**:
  - "Listen" button for any mentor response
  - "Stop" button while audio playing
  - User controls audio playback

---

## Backend Integration

### API Endpoint: `/api/mentor-chat/` (POST)

```json
{
  "device_id": "MU-xxxxx",
  "mentor_id": 1,
  "message": "How can I increase my sales?",
  "language": "ta",
  "message_type": "query",
  "input_type": "voice"  // or "text"
}
```

### Response:
```json
{
  "success": true,
  "user_message": {
    "id": 123,
    "message": "How can I increase my sales?",
    "message_type": "query",
    "timestamp": "2026-04-03T17:45:00Z"
  },
  "mentor_response": {
    "id": 124,
    "message": "Your mentor's response in CHOSEN LANGUAGE only",
    "message_type": "response",
    "timestamp": "2026-04-03T17:45:05Z"
  },
  "language": "ta",
  "income_focused": false,
  "expense_focused": true
}
```

---

## Mentor Response Behavior

### Income-Related Questions
When user asks about income/earnings/revenue/profit:

1. **Detection**: Backend detects income keywords
2. **Context**: Fetches user's current month income from database
3. **Response**: Provides personalized advice based on actual financial data
4. **Focus**: Practical tips to increase income

Example:
- User: "How can I increase my sales?"
- Mentor: "I see you've earned ₹X this month. Here are 3 ways to boost your sales: [practical advice in user's language]"

### Expense-Related Questions
When user asks about costs/spending/materials:

1. **Detection**: Backend detects expense keywords
2. **Context**: Fetches user's current month expenses
3. **Response**: Provides budgeting and expense reduction tips
4 **Focus**: Cost optimization strategies

### General Business Questions
For other business topics:
- Mentor provides expert guidance on:
  - Business planning & ideas
  - Marketing strategies
  - Pricing strategies
  - Customer management
  - Government schemes
  - Problem-solving

---

## Language Enforcement

### Strict Rules (NO Mixing):
✅ **CORRECT**: উত্তর শুধুমাত্র தமிழ் மொழியில্
✅ **CORRECT**: केवल हिंदी में उत्तर दें
✅ **CORRECT**: Answer only in English

❌ **WRONG**: "புதிய பணி என்பது new opportunity"
❌ **WRONG**: "आपको ₹500 earn करना है"

### Implementation:
- Language detection from user message
- Gemini API prompt enforcement: "Respond ONLY in [language]"
- Character encoding validation (Tamil chars, Devanagari, ASCII)
- If response > 60% English when Tamil/Hindi requested → reject and retry

---

## User Journey Example

### Scenario: Woman Entrepreneur Asking About Income

**Step 1**: User selects "Meena Krishnan" (Dairy Business Mentor)
**Step 2**: Chooses "தமிழ் Tamil" language
**Step 3**: Selects "🎤 Voice Mode"
**Step 4**: Taps microphone, says: "எப்படி எனது வருமானம் அதிகரிக்கலாம்?"
  - Audio recorded & transcribed
  - Backend detects income keywords
  - Fetches user's current income: ₹5000 this month

**Response**: 
"நல்லது! இந்த மாதம் உங்கள் வருமானம் ₹5000. உங்கள் விক்রয় அதிகரிக்க மூன்று வழிகள்:
1. நாள்தோறும் 2 கூடுதல் வாடிக்கையாளர் தொடர்பு கொள்ளவும்
2. உங்கள் பிரিய பொருளுக்கு 10% ছাড் கொடுக்கவும்
3. WhatsApp மூலம் தினசரி அழைப்பு பাঠுங்கள்"

**Audio**: Automatically played in Tamil voice

**Follow-up**: User asks another question, same language/mode maintained

---

## Technical Stack

### Frontend (React)
- Stage-based component architecture
- Speech Recognition API (user voice input)
- Web Speech API (mentor voice output)
- Real-time transcription display
- Responsive message list with auto-scroll

### Backend (Django)
- `MentorChatView` API endpoint
- Language detection (LanguageDetector)
- Income/Expense context fetching
- Gemini API integration with strict language prompts
- Fallback responses for API failures

### AI Models
- **Google Gemini API**: Primary AI mentor response generation
- **Language Detection**: Auto-detect user language
- **Voice Processing**:
  - Web Speech API (browser-based, no external API)
  - Language-specific recognition (en-US, ta-IN, hi-IN)
  - Text-to-speech (browser native)

---

## Testing Checklist

✅ **Language Selection**
- [ ] User can select all 3 languages
- [ ] Selection persists through chat
- [ ] Can change language before chat starts

✅ **Voice Mode**
- [ ] Microphone recording works
- [ ] Transcription displays
- [ ] Response plays automatically
- [ ] Can stop audio playback

✅ **Text Mode**
- [ ] Text input works
- [ ] Send button enabled/disabled correctly
- [ ] Can optionally listen to response

✅ **No Language Mixing**
- [ ] Tamil response contains no English
- [ ] Hindi response contains no English/Tamil
- [ ] English response is pure English

✅ **Income/Expense Context**
- [ ] Income question fetches user's income
- [ ] Expense question fetches user's expenses
- [ ] Response includes contextual data

---

## Notes

- All communication preserves user privacy (device_id based)
- No user authentication needed (device-based)
- Mentor responses are AI-generated (marked as AI-assisted)
- Full conversation history saved for follow-ups
- Supports offline fallback responses if API unavailable
