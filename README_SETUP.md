# 🚀 MahilaUdyam - Women Entrepreneur Platform

**MahilaUdyam** is a **voice-first AI platform for women entrepreneurs** with complete multilingual support, featuring smart financial tracking, AI mentor guidance, real-time market prices, government schemes, and voice-enabled assistance in Tamil, Hindi, and English.

### 🌟 Key Features

✅ **Voice-First AI Platform**: Speak in Tamil, Hindi, or English - no typing required  
✅ **Multilingual Support**: Complete support for Tamil, Hindi, English with strict language purity  
✅ **AI Mentor Chat**: Smart voice/text mentor with income-aware advice  
✅ **Market Price Tracking**: Real-time commodity prices (27+ items), voice-accessible  
✅ **Government Schemes**: 10+ women entrepreneurship schemes with eligibility info  
✅ **Income/Expense Tracking**: Daily financial management  
✅ **Accessible Design**: Low-literacy accessible through voice interface, responsive mobile-first UI  

---

## 📋 Tech Stack

### Backend
- **Framework**: Django 4.2.7
- **Database**: MySQL 8.0+
- **AI Integration**: Google Gemini API
- **Language**: Python 3.8+
- **ORM**: Django ORM

### Frontend
- **Framework**: React 18+
- **Language**: JavaScript
- **Styling**: CSS3 + Inline Styles
- **APIs**: Web Speech API (Voice Recognition & Synthesis)
- **Build Tool**: Create React App

---

## 🛠️ Prerequisites

Before setup, ensure you have:

- **Python 3.8+** - [Download](https://www.python.org/downloads/)
- **Node.js 14+** - [Download](https://nodejs.org/)
- **MySQL 8.0+** - [Download](https://www.mysql.com/downloads/)
- **Git** - [Download](https://git-scm.com/)
- **Google Gemini API Key** - [Get free key](https://makersuite.google.com/app/apikey)

**Verify installations:**
```bash
python --version
node --version
npm --version
mysql --version
git --version
```

---

## 📥 Installation

### 1. Clone Repository
```bash
git clone https://github.com/rupali1802/THE_MAHILAUDYAM.git
cd THE_MAHILAUDYAM/MahilaUdyam
```

### 2. Backend Setup

#### Step 1: Create Virtual Environment
```bash
cd backend
python -m venv venv_new

# On Windows (PowerShell):
.\venv_new\Scripts\activate

# On Windows (Command Prompt):
venv_new\Scripts\activate.bat

# On macOS/Linux:
source venv_new/bin/activate
```

#### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 3: Configure Environment Variables
Create `.env` file in `backend/` folder with your local configuration:

**`.env` file (create this in backend/ folder):**
```env
# Django Settings
DEBUG=True
SECRET_KEY=django-insecure-your-secret-key-here-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database Configuration - MySQL
DB_ENGINE=django.db.backends.mysql
DB_NAME=mahila_udyam
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_HOST=127.0.0.1
DB_PORT=3306

# Google Gemini API Key (get FREE from https://makersuite.google.com/app/apikey)
GEMINI_API_KEY=AIzaSy_your_gemini_api_key_here

# API Settings
API_TIMEOUT=30
```

#### Step 4: Create MySQL Database
```bash
mysql -u root -p
```

Then in MySQL prompt:
```sql
CREATE DATABASE mahila_udyam CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

#### Step 5: Run Database Migrations
```bash
# Make sure you're in backend/ folder and venv is activated
python manage.py migrate
```

#### Step 6: Populate Sample Data
```bash
python populate_data.py
```

This will add:
- 10 government schemes (Tamil/Hindi/English)
- 27 commodity market prices
- Sample mentors
- Sample user data

### 3. Frontend Setup

Open a **new terminal** window:

```bash
cd frontend
npm install
```

---

## 🚀 Running the Project

### Start Backend Server

**Terminal 1 - Backend:**
```bash
cd backend

# Activate virtual environment
# Windows PowerShell: .\venv_new\Scripts\activate
# Windows CMD: venv_new\Scripts\activate.bat
# macOS/Linux: source venv_new/bin/activate

python manage.py runserver 0.0.0.0:8000
```

**Expected output:**
```
✅ Using MySQL Database
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
Starting development server at http://0.0.0.0:8000/
Quit the server with CTRL-BREAK.
```

### Start Frontend Server

**Terminal 2 - Frontend (NEW TERMINAL):**
```bash
cd frontend
npm start
```

**Expected output:**
```
Compiled successfully!

You can now view mahila-udyam-frontend in the browser.

  Local:            http://localhost:3002
  On Your Network:  http://192.168.1.x:3002
```

### ✅ Application is Ready

Once both servers are running, open your browser:

- **Main App**: http://localhost:3002
- **Backend API**: http://localhost:8000/api
- **Django Admin**: http://localhost:8000/admin

---

## 🧪 Testing Workflow

### Test 1: Mentor Chat System (Main Feature)

1. **Open**: http://localhost:3002/mentor
2. **Select Mentor**: Click on **"Meena Krishnan"** (Dairy Business mentor)
3. **Select Language**: Choose **"தமிழ்"** (Tamil)
4. **Select Mode**: Choose **"🎤 Voice Chat"**

**Expected Display:**
- Mentor greeting in pure Tamil: "வணக்கம்! நான் Meena Krishnan..."
- 4 suggestion chips with Tamil questions:
  - "என் விற்பனை எப்படி அதிகரிக்க வேண்டும்?"
  - "சரியான விலை நிர்ধारணை எப்படி செய்ய வேண்டும்?"
  - "செலவுகளை எப்படி குறைக்க வேண்டும்?"
  - "எந்த அரசு திட்டத்திற்கு விண்ணப்பம் செய்ய வேண்டும்?"

**Test Voice Input:**
5. Click microphone 🎤 button (turns RED)
6. Speak in Tamil: "என் வருமானம் எப்படி அதிகரிக்க வேண்டும்?"
7. Wait 3-5 seconds for AI response

**Verify:**
- ✅ Mentor response appears in **pure Tamil** (no English words)
- ✅ Response reads aloud automatically
- ✅ Typing indicator shows bouncing dots while thinking
- ✅ Chat layout uses WhatsApp style (user blue right, mentor white left)

### Test 2: Market Price Page

1. **Open**: http://localhost:3002/market
2. **Verify**:
   - ✅ 27 commodities listed with Tamil names
   - ✅ Current prices shown in ₹ (Rupees)
   - ✅ Price trends (↑ up or ↓ down) visible
   - ✅ Market analysis available

### Test 3: Government Schemes Page

1. **Open**: http://localhost:3002/schemes
2. **Select Language**: Choose Tamil (தமிழ்)
3. **Verify**:
   - ✅ 10 government schemes displayed
   - ✅ All text in **pure Tamil** (no English names)
   - ✅ Scheme names, eligibility, benefits all in Tamil
   - ✅ Government agency names translated to Tamil

**Example Schemes:**
- Pradhan Mantri MUDRA Yojana (₹10 lakh loan)
- PM Swavapan Yojana (Interest Subsidy)
- PMFME Food Processing (₹25 lakh with 35% subsidy)
- Pradhan Mantri Suraksha Bima Yojana (₹2 lakh insurance)

### Test 4: Income/Expense Tracking

1. **Open**: http://localhost:3002/dashboard
2. **Add Income**:
   - Click "Add Income" button
   - Enter amount: 5000
   - Select date
   - Click "Save"
3. **Verify**:
   - ✅ Income appears in dashboard
   - ✅ Profit calculated correctly
   - ✅ Tamil UI labels visible

### Test 5: API Endpoints (Backend Verification)

**Test Schemes API with Tamil language:**
```bash
curl "http://localhost:8000/api/schemes/?language=ta"
```

**Expected Response:**
```json
{
  "results": [
    {
      "name": "பிரதான மন்திரி முட்ரா யோஜனா",
      "description": "Tamil description here...",
      "eligibility": "Tamil eligibility here...",
      "max_loan_amount": 1000000,
      "agency": "சிறு, நடு மற்றும் நடுநிலை தொழிலுறவு அமைச்சு"
    }
  ]
}
```

**Test Market Prices API:**
```bash
curl "http://localhost:8000/api/market-prices/"
```

**Expected Response:**
```json
{
  "results": [
    {
      "commodity": "தக்காளி",
      "current_price": 45.50,
      "trend": "up",
      "last_updated": "2026-04-03T10:30:00Z"
    }
  ]
}
```

**Test Mentor Chat API:**
```bash
curl -X POST "http://localhost:8000/api/mentor-chat/" \
  -H "Content-Type: application/json" \
  -d '{
    "device_id": "test-device-001",
    "mentor_id": 2,
    "message": "என் வருமானத்தை எப்படி அதிகரிக்க வேண்டும்?",
    "language": "ta"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "user_message": {
    "message": "என் வருமானத்தை எப்படி அதிகரிக்க வேண்டும்?",
    "message_type": "query"
  },
  "mentor_response": {
    "message": "[Pure Tamil response from Gemini AI]...",
    "message_type": "response"
  },
  "language": "ta",
  "income_focused": true
}
```

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"

**Cause:** Virtual environment not activated or dependencies not installed

**Solution:**
```bash
cd backend
.\venv_new\Scripts\activate  # Windows PowerShell
pip install -r requirements.txt
```

### Issue: "MySQL connection error" or "Can't connect to MySQL server"

**Cause:** MySQL not running or wrong credentials in `.env`

**Solution:**
1. **Check MySQL is running:**
   ```bash
   mysql -u root -p
   # Enter your password
   # If you see mysql> prompt, MySQL is running
   ```

2. **Verify `.env` credentials:**
   - Check your `.env` file has correct:
     - `DB_USER=root`
     - `DB_PASSWORD=your_actual_password`
     - `DB_HOST=127.0.0.1`

3. **Create database if not exists:**
   ```bash
   mysql -u root -p -e "CREATE DATABASE mahila_udyam CHARACTER SET utf8mb4;"
   ```

### Issue: "Gemini API key is invalid"

**Cause:** Missing or wrong API key in `.env`

**Solution:**
1. Get free API key: https://makersuite.google.com/app/apikey
2. Add to `.env`:
   ```env
   GEMINI_API_KEY=your_actual_key_here
   ```
3. Restart backend server

### Issue: "React app won't start - port 3002 already in use"

**Cause:** Another process using port 3002

**Solution (Windows PowerShell):**
```powershell
# Find process on port 3002
netstat -ano | findstr :3002

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Then restart
npm start
```

**Solution (macOS/Linux):**
```bash
# Kill process on port 3002
lsof -ti:3002 | xargs kill -9

# Restart
npm start
```

### Issue: "TypeError: Cannot read property 'results' of undefined" in Mentor Chat

**Cause:** Backend not running or API endpoint unreachable

**Solution:**
1. **Verify backend is running:**
   ```bash
   curl http://localhost:8000/api/mentors/
   ```

2. **Check browser console:** (F12 → Console)
   - Look for actual error messages
   - Check network tab for failed API calls

3. **Restart both servers:**
   - Kill backend (Ctrl+C)
   - Kill frontend (Ctrl+C)
   - Start fresh in new terminals

### Issue: "No module named 'mysql.connector'" during migration

**Cause:** MySQL Python driver not installed

**Solution:**
```bash
cd backend
.\venv_new\Scripts\activate
pip install mysqlclient
# OR
pip install mysql-connector-python
python manage.py migrate
```

### Issue: Database migration errors

**Cause:** Schema conflicts or outdated migrations

**Solution:**
1. **Backup your data (if production)**
2. **Check migration status:**
   ```bash
   python manage.py showmigrations
   ```
3. **Reset and remigrate (DEV ONLY):**
   ```bash
   python manage.py migrate api zero
   python manage.py migrate
   python populate_data.py
   ```

---

## 📁 Project Structure

```
MahilaUdyam/
│
├── backend/                           # Django Backend
│   ├── mahila_udyam_backend/
│   │   ├── settings.py               # Django configuration
│   │   ├── urls.py                   # Main URL routing
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── api/                          # Main Django App
│   │   ├── models.py                 # Database Models
│   │   ├── views.py                  # API ViewSets & Views
│   │   ├── serializers.py            # Data Serialization
│   │   ├── urls.py                   # API URL routing
│   │   ├── admin.py                  # Django Admin config
│   │   └── migrations/               # Database migrations
│   │
│   ├── ml_models/                    # AI & Language Processing
│   │   ├── gemini_helper.py          # Google Gemini API integration
│   │   ├── mentor_helper.py          # AI Mentor Logic
│   │   ├── language_detection.py     # Language auto-detection
│   │   ├── market_analyzer.py        # Market Price Analysis
│   │   └── rule_engine.py            # Business Logic
│   │
│   ├── manage.py
│   ├── requirements.txt               # Python Dependencies
│   ├── populate_data.py              # Sample Data Script
│   ├── .env (IGNORED)                # Local Environment Variables
│   ├── .env.example                  # Template for .env
│   └── venv_new/                     # Virtual Environment (not committed)
│
├── frontend/                          # React Frontend
│   ├── public/
│   │   └── index.html
│   │
│   ├── src/
│   │   ├── pages/
│   │   │   ├── MentorChat.jsx         # Main Mentor Chat Interface (4-stage flow)
│   │   │   ├── MarketPrice.jsx        # Market Price Tracking
│   │   │   ├── Schemes.jsx            # Government Schemes
│   │   │   ├── Dashboard.jsx          # Income/Expense Dashboard
│   │   │   └── VoiceAssistant.jsx
│   │   │
│   │   ├── components/
│   │   │   ├── BottomNav.jsx          # Navigation Bar
│   │   │   ├── DashboardHeader.jsx
│   │   │   └── ChartsSection.jsx
│   │   │
│   │   ├── services/
│   │   │   └── api.js                 # API Client (calls backend)
│   │   │
│   │   ├── hooks/
│   │   │   └── useLanguage.js         # Language Context Hook
│   │   │
│   │   ├── styles/
│   │   │   ├── Mentor.css
│   │   │   ├── MarketPrice.css
│   │   │   └── index.css
│   │   │
│   │   ├── utils/
│   │   │   ├── translations.js        # Language strings
│   │   │   └── device.js              # Device ID utility
│   │   │
│   │   ├── App.js                     # Main App Component
│   │   └── index.js
│   │
│   ├── package.json
│   ├── package-lock.json
│   └── node_modules/                 # Dependencies (not committed)
│
├── documentation/                     # Extended Documentation
│   ├── MENTOR_AI_SYSTEM_PROMPT.md
│   ├── GEMINI_INTEGRATION_GUIDE.md
│   ├── VOICE_ASSISTANT_SETUP_GUIDE.md
│   └── SAKHI_SYSTEM_PROMPT.md
│
├── README.md (THIS FILE)
├── README_SETUP.md
├── QUICKSTART.md                      # 5-minute setup guide
├── MENTOR_SYSTEM_GUIDE.md             # Mentor feature documentation
├── IMPLEMENTATION_SUMMARY.md
├── MARKET_PRICE_UPDATES_GUIDE.md
│
├── .gitignore                         # Excludes sensitive files
│   (Excludes: __pycache__, node_modules, .env, build/, venv/)
│
└── .github/
    └── copilot-instructions.md
```

---

## 🌍 Multilingual Support

The application fully supports all three languages equally:

| Language | Code | Status |
|----------|------|--------|
| தமிழ் (Tamil) | `ta` | ✅ Full Support |
| हिंदी (Hindi) | `hi` | ✅ Full Support |
| English | `en` | ✅ Full Support |

**Voice-First, Multilingual Approach:**
- All features accessible via voice in each language
- Backend auto-detects user's language
- AI responds in user's selected language only
- Strict language purity (no mixed "Hinglish" or "Tanglish")
- Accessible for low-literacy users through voice interface

---

## 📊 Database Schema

### Core Models

**User**
- `device_id` - Unique device identifier
- `created_at` - Account creation date

**Income**
- `device_id` - User identifier
- `amount` - Income amount in rupees
- `date` - Date of income
- `description` - Income source (Tamil/English)

**Expense**
- `device_id` - User identifier
- `amount` - Expense amount in rupees
- `date` - Date of expense
- `category` - Type of expense
- `description` - Expense details

**MarketPrice**
- `commodity` - Product name (Tamil)
- `current_price` - Current market price in ₹
- `trend` - Price trend (up/down/stable)
- `updated_at` - Last update timestamp

**Scheme**
- `name_en`, `name_ta`, `name_hi` - Translations
- `description_en`, `description_ta`, `description_hi`
- `eligibility_en`, `eligibility_ta`, `eligibility_hi`
- `max_loan_amount` - Maximum loan in rupees
- `subsidy_percentage` - Subsidy offered
- `agency` - Government ministry

**MentorChat**
- `device_id` - User identifier
- `mentor_id` - Selected mentor (1-4)
- `message` - Message content
- `message_type` - "query" or "response"
- `timestamp` - When sent

---

## 🔐 Security Notes

⚠️ **IMPORTANT for Production:**

1. **Never commit `.env`** (already in .gitignore)
2. **Change `SECRET_KEY`** in production
3. **Set `DEBUG=False`** in production Django settings
4. **Use strong MySQL password** (not "root")
5. **Enable HTTPS** in production
6. **Use environment variables** for all secrets
7. **Validate all user inputs** in production
8. **Set up CORS** properly for production domain

---

## 📚 Additional Documentation

- **[QUICKSTART.md](./QUICKSTART.md)** - Fast 5-minute setup
- **[MENTOR_SYSTEM_GUIDE.md](./MENTOR_SYSTEM_GUIDE.md)** - Complete mentor system details
- **[GEMINI_SETUP_SUMMARY.md](./GEMINI_SETUP_SUMMARY.md)** - Gemini API integration
- **[IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)** - Technical implementation details

---

## 🤝 Contributing

1. Fork: https://github.com/rupali1802/THE_MAHILAUDYAM/fork
2. Create branch: `git checkout -b feature/your-feature`
3. Commit: `git commit -m "Add your feature"`
4. Push: `git push origin feature/your-feature`
5. Create pull request

---

## 📞 Support & Issues

- **GitHub Issues**: https://github.com/rupali1802/THE_MAHILAUDYAM/issues
- **Create Detailed Issue:** Include:
  - OS & Python version
  - Error message (full traceback)
  - Steps to reproduce
  - Screenshots if applicable

---

## 🎯 Roadmap

- [ ] SMS notifications for scheme eligibility
- [ ] WhatsApp Business API integration
- [ ] Multi-device data sync
- [ ] Offline mode
- [ ] Government portal API direct integration
- [ ] Payment gateway (Razorpay/PhonePe)
- [ ] ML-based income prediction
- [ ] GPS-based local market comparison
- [ ] Community features (peer mentorship)

---

## 📄 License

Open source for community benefit

---

## ❤️ Acknowledgments

Built with care for women entrepreneurs by the technical community.

**Happy Entrepreneurship! 💪**
