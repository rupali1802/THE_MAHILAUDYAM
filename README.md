# 🚀 MahilaUdyam - Women Entrepreneurs Empowerment Platform

**MahilaUdyam** is a **Tamil-first mobile application** designed to empower women entrepreneurs with:

- 💬 **AI Mentor Chat** - Voice/text mentor with income-aware guidance
- 📊 **Financial Dashboard** - Income/expense tracking and profit analysis  
- 📈 **Market Price Tracker** - Real-time commodity prices (27+ items)
- 📋 **Government Schemes** - Eligibility checker for 10+ women entrepreneurship schemes
- 🎤 **Voice Assistant** - Speech recognition & synthesis in Tamil, Hindi, English
- 🌍 **Multilingual** - Pure Tamil (primary), Hindi, English with strict language purity

Built for **Villupuram Hackathon 2026** | **GitHub**: [rupali1802/THE_MAHILAUDYAM](https://github.com/rupali1802/THE_MAHILAUDYAM)

---

## ⚡ Quick Start (5 Minutes)

### For Impatient Users: Jump to [QUICKSTART.md](./QUICKSTART.md)

```bash
# 1. Clone & navigate
git clone https://github.com/rupali1802/THE_MAHILAUDYAM.git
cd THE_MAHILAUDYAM/MahilaUdyam

# 2. Backend (Terminal 1)
cd backend
python -m venv venv_new
.\venv_new\Scripts\activate     # Windows
source venv_new/bin/activate    # macOS/Linux
pip install -r requirements.txt
# Create .env (copy template, add MySQL password & Gemini API key)
python manage.py migrate
python manage.py runserver

# 3. Frontend (Terminal 2)
cd frontend
npm install
npm start
```

Open **http://localhost:3002** → Click "Mentor" → Select Tamil (தமிழ்) → Try voice chat 🎤

---

## 📚 Full Documentation

- **[README_SETUP.md](./README_SETUP.md)** ⭐ **START HERE** - Complete step-by-step guide with:
  - Prerequisites & installation instructions
  - Backend & Frontend setup with screenshots
  - Environment configuration (.env template)
  - How to run both servers
  - 5 comprehensive test workflows (API + UI tests)
  - Troubleshooting section for common issues
  - Database schema documentation
  - Security notes for production

- **[QUICKSTART.md](./QUICKSTART.md)** - 5-minute setup for experienced developers

- **[MENTOR_SYSTEM_GUIDE.md](./MENTOR_SYSTEM_GUIDE.md)** - Deep dive into mentor chat system architecture

- **[GEMINI_SETUP_SUMMARY.md](./GEMINI_SETUP_SUMMARY.md)** - Google Gemini API integration details

- **[IMPLEMENTATION_SUMMARY.md](./IMPLEMENTATION_SUMMARY.md)** - Technical implementation notes

- **[MARKET_PRICE_UPDATES_GUIDE.md](./MARKET_PRICE_UPDATES_GUIDE.md)** - Managing market price data

---

## 🎯 Key Features

### 1. **Mentor Chat System** (Main Feature)
- 4-stage flow: Select Mentor → Choose Language → Pick Input Mode → Chat
- 4 AI Mentors with expertise (Dairy, Textile, Food Processing, Retail)
- **WhatsApp-style UI** with suggestion chips & animated typing indicator
- Voice recognition in Tamil (ta-IN), Hindi (hi-IN), English (en-US)
- AI respects income/expense context from dashboard

### 2. **Market Price Tracking**
- 27 commodities with real-time prices
- Price trends (↑ up, ↓ down, → stable)
- Market analysis and recommendations

### 3. **Government Schemes**
- 10+ women entrepreneurship schemes
- Eligibility checker with loan amounts
- Subsidy calculator
- **Pure Tamil UI**: All scheme names & descriptions translated

### 4. **Income/Expense Dashboard**
- Daily financial tracking
- Profit calculation
- Monthly analysis charts
- Context for AI mentor guidance

### 5. **Voice Assistant**
- Web Speech API (browser-native, no external API)
- Speech recognition in Tamil/Hindi/English
- Auto text-to-speech responses in selected language
- Works offline

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Django 4.2.7, Python 3.8+, MySQL 8.0+ |
| **Frontend** | React 18+, JavaScript, CSS3 |
| **AI** | Google Gemini API |
| **Voice** | Web Speech API (browser-native) |
| **Database** | MySQL with UTF-8 support |
| **Version Control** | Git + GitHub |

---

## 📊 Project Stats

- **Total Code Files**: 60+
- **Backend Endpoints**: 15+ REST APIs
- **React Components**: 20+ reusable components
- **Database Models**: 8 core models
- **Languages Supported**: Tamil (Primary), Hindi, English
- **AI Mentor Mentors**: 4 specialized mentors
- **Market Commodities**: 27 items tracked
- **Government Schemes**: 10 schemes indexed
- **Lines of Code**: 5,000+ (backend + frontend)

---

## 📋 Prerequisites

- **Python 3.8+** | **Node.js 14+** | **MySQL 8.0+** | **Git**
- **Google Gemini API Key** (free from https://makersuite.google.com/app/apikey)

See **[README_SETUP.md](./README_SETUP.md#-prerequisites)** for detailed verification steps.

---

## 🚀 Installation & Running

**Full Instructions**: See [README_SETUP.md](./README_SETUP.md) for complete step-by-step guide.

**Quick Command Summary:**
```bash
# Backend
cd backend && python -m venv venv_new && .\venv_new\Scripts\activate
pip install -r requirements.txt
# Add .env file with MySQL password & Gemini API key
python manage.py migrate
python manage.py runserver

# Frontend (new terminal)
cd frontend && npm install && npm start
```

---

## 🧪 Testing

The application is **fully tested and production-ready**. See [README_SETUP.md - Testing Workflow](./README_SETUP.md#-testing-workflow) for:

✅ Mentor Chat voice/text test  
✅ Market Price tracking test  
✅ Government Schemes page test  
✅ Income/Expense tracking test  
✅ API endpoint verification tests  

**Run tests with examples:**
```bash
# Test Mentor Chat API
curl -X POST http://localhost:8000/api/mentor-chat/ \
  -H "Content-Type: application/json" \
  -d '{"device_id":"test","mentor_id":2,"message":"என் வருமானத்தை...","language":"ta"}'

# Test Schemes in Tamil
curl "http://localhost:8000/api/schemes/?language=ta"

# Test Market Prices
curl http://localhost:8000/api/market-prices/
```

---

## ❌ Troubleshooting

**Common Issues & Solutions**: See [README_SETUP.md - Troubleshooting](./README_SETUP.md#-troubleshooting)

- MySQL connection errors
- Missing Gemini API key
- Port already in use (3002)
- Module not found errors
- Database migration issues

---

## 📁 Project Structure

```
MahilaUdyam/
├── backend/              # Django REST API
│   ├── api/             # Main Django app with models/views
│   ├── ml_models/       # AI & Gemini integration
│   ├── venv_new/        # Python virtual environment
│   └── manage.py
│
├── frontend/            # React application
│   ├── src/
│   │   ├── pages/       # MentorChat, MarketPrice, Schemes, Dashboard
│   │   └── components/  # Reusable React components
│   └── package.json
│
├── documentation/       # Extended guides
├── README.md           # This file
├── README_SETUP.md     # ⭐ Complete setup guide
├── QUICKSTART.md       # 5-minute setup
└── .gitignore          # Clean repo (no node_modules, .env, __pycache__)
```

---

## 🌍 Language Support

**Strict Language Purity** - No mixing languages:

| Language | Code | Support | Status |
|----------|------|---------|--------|
| தமிழ் (Tamil) | `ta` | Full | ✅ PRIMARY |
| हिंदी (Hindi) | `hi` | Full | ✅ COMPLETE |
| English | `en` | Full | ✅ COMPLETE |

Backend enforces pure-language responses through:
- Character encoding detection (Tamil: 0x0B80-0x0BFF, Devanagari: 0x0900-0x097F)
- Gemini API initialization with strict language-only prompts
- Per-message language validation

---

## 🔐 Security

- ✅ `.env` excluded from Git (sensitive data safe)
- ✅ CORS configured for frontend-backend communication
- ✅ MySQL password in .env (not hardcoded)
- ✅ Gemini API key in .env (not in code)
- ⚠️ **Production Setup**: See [README_SETUP.md - Security Notes](./README_SETUP.md#-security-notes)

---

## 🤝 Contributing

1. **Fork**: https://github.com/rupali1802/THE_MAHILAUDYAM/fork
2. **Branch**: `git checkout -b feature/your-feature`
3. **Commit**: `git commit -m "Add feature"`
4. **Push**: `git push origin feature/your-feature`
5. **PR**: Create pull request for review

---

## 📞 Support

- **Issues**: https://github.com/rupali1802/THE_MAHILAUDYAM/issues
- **Documentation**: All files in this repo
- **Setup Help**: See [README_SETUP.md](./README_SETUP.md)

---

## 📄 License

**Villupuram Hackathon 2026** | Open source for community benefit.

---

## ❤️ About

Built with passion for **women entrepreneurs** to break barriers and scale their businesses through:
- Expert AI mentorship (income-aware)
- Real-time market intelligence
- Government scheme guidance
- Voice accessibility in native languages

**Mission**: Empower 1,000+ women entrepreneurs with digital tools & knowledge.

**Happy Entrepreneurship! 💪**

---

**Made with ❤️ for the community** | [GitHub](https://github.com/rupali1802/THE_MAHILAUDYAM)
