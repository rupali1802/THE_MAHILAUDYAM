# MahilaUdyam - Copilot Instructions

## Project Overview

**MahilaUdyam** is a mobile-first platform empowering women entrepreneurs with comprehensive financial and business management tools. The platform offers real-time market prices, government schemes information, expert mentorship, and a voice-enabled AI assistant (SAKHI) available in Tamil, Hindi, and English.

### Key Features
- 📊 Financial tracking (income, expenses, profit analysis)
- 🛒 Sales management
- 💹 Real-time market prices
- 🎯 Government schemes discovery
- 👥 Expert mentorship
- 🎤 Voice-enabled AI assistant (SAKHI)
- 🌍 Multi-language support (Tamil, Hindi, English)

---

## Tech Stack

### Frontend
- **Framework**: React 18.2.0 with React Router 6
- **UI Components**: Lucide React icons
- **Animations**: Framer Motion
- **Charts**: Recharts
- **Styling**: CSS with glassmorphism and modern animations
- **Port**: 3000

### Backend
- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Database**: SQLite (dev), MySQL (production)
- **CORS**: django-cors-headers
- **Port**: 8000

### ML & Voice
- **Speech Recognition**: SpeechRecognition 3.10.0
- **Audio Processing**: pydub
- **Language Detection**: Custom language_detection module
- **Number Conversion**: num2words
- **Data Processing**: pandas

---

## Project Structure

```
MahilaUdyam/
├── backend/                 # Django REST API
│   ├── api/                # API apps and models
│   ├── ml_models/          # ML, speech, language modules
│   ├── mahila_udyam_backend/  # Django settings & config
│   ├── manage.py
│   ├── requirements.txt
│   ├── db.sqlite3          # SQLite database
│   └── venv_new/           # Virtual environment
├── frontend/               # React application
│   ├── src/
│   │   ├── components/     # Reusable React components
│   │   ├── pages/          # Page components
│   │   ├── context/        # Language context
│   │   ├── hooks/          # Custom hooks (useLanguage)
│   │   └── App.js
│   ├── public/
│   └── package.json
├── documentation/          # Setup guides
│   ├── SAKHI_INTEGRATION_GUIDE.md
│   ├── SAKHI_QUICK_REFERENCE.md
│   ├── VOICE_ASSISTANT_SETUP_GUIDE.md
│   └── SAKHI_SYSTEM_PROMPT.md
└── setup.sh               # Quick setup script
```

---

## Setup & Running

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Quick Setup (Unix/Linux/Mac)
```bash
bash setup.sh
```

### Manual Setup

#### Backend Setup
```bash
# Navigate to backend
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start Django server
python manage.py runserver 0.0.0.0:8000
```

#### Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start React dev server (runs on port 3000)
npm start
```

### Running Both Simultaneously
In two separate terminals:
1. Terminal 1: `cd backend && source venv/bin/activate && python manage.py runserver`
2. Terminal 2: `cd frontend && npm start`

The frontend will proxies API requests to `http://localhost:8000` (via proxy setting in package.json)

---

## Key Development Files

### Frontend Components
- [DashboardHeader.jsx](./frontend/src/components/DashboardHeader.jsx) - Header with notifications
- [SummaryCards.jsx](./frontend/src/components/SummaryCards.jsx) - Financial summary cards
- [QuickActionsGrid.jsx](./frontend/src/components/QuickActionsGrid.jsx) - Action buttons
- [ChartsSection.jsx](./frontend/src/components/ChartsSection.jsx) - Data visualization
- [FloatingVoiceButton.jsx](./frontend/src/components/FloatingVoiceButton.jsx) - Voice assistant UI
- [LanguageContext.js](./frontend/src/context/LanguageContext.js) - Language/i18n management

### Backend Models & APIs
- [models.py](./backend/api/models.py) - Database schemas
- [views.py](./backend/api/views.py) - API endpoints
- [serializers.py](./backend/api/serializers.py) - Request/response serialization
- [urls.py](./backend/api/urls.py) - URL routing

### ML & Voice Modules
- [language_detection.py](./backend/ml_models/language_detection.py) - Language identification
- [recognize_speech.py](./backend/ml_models/recognize_speech.py) - Speech-to-text
- [language_responses.py](./backend/ml_models/language_responses.py) - Multi-language responses
- [rule_engine.py](./backend/ml_models/rule_engine.py) - Business logic

---

## Common Development Tasks

### Add a New API Endpoint
1. Define model in `backend/api/models.py`
2. Create serializer in `backend/api/serializers.py`
3. Add viewset in `backend/api/views.py`
4. Register in `backend/api/urls.py`
5. Run `python manage.py makemigrations` → `python manage.py migrate`

### Add a New Frontend Page
1. Create component in `frontend/src/pages/`
2. Add route in `frontend/src/App.js`
3. Update navigation in `frontend/src/components/Navbar.jsx`
4. Use `useLanguage()` hook for language support

### Add Language Support
- Update `backend/ml_models/language_responses.py` for new language
- Add language code to `frontend/src/context/LanguageContext.js`
- Update language selection UI in `frontend/src/pages/LanguageSelection.jsx`

---

## API Communication

### Base URL
- Development: `http://localhost:8000/api/`
- Frontend proxies requests automatically

### Common Endpoints
- `GET /api/income/` - Get income records
- `POST /api/income/` - Create income record
- `GET /api/expense/` - Get expense records
- `GET /api/sales/` - Get sales records
- `GET /api/market-prices/` - Get market prices
- `POST /api/voice/` - Process voice commands

---

## Environment Configuration

### Backend (.env or settings.py)
- `DEBUG=True` (development)
- `SECRET_KEY` - Django secret key
- `ALLOWED_HOSTS` - Comma-separated hosts
- Database credentials (if using MySQL)

### Frontend
- API proxy configured in `package.json`: `"proxy": "http://localhost:8000"`
- Language stored in localStorage via LanguageContext

---

## Testing

### Backend (Django)
```bash
python manage.py test
```

### Frontend (React)
```bash
npm test
```

---

## Important Notes

### Database
- **Development**: Uses SQLite (file: `backend/db.sqlite3`)
- **Production**: Configure MySQL in `backend/mahila_udyam_backend/settings.py`
- Run migrations after model changes: `python manage.py makemigrations && python manage.py migrate`

### Voice/SAKHI Integration
- See [documentation/VOICE_ASSISTANT_SETUP_GUIDE.md](./documentation/VOICE_ASSISTANT_SETUP_GUIDE.md)
- Speech Recognition requires microphone access
- Language detection handles Tamil, Hindi, English

### CORS Settings
- Frontend (3000) ↔ Backend (8000) communication enabled via `django-cors-headers`
- Configure in `settings.py` if needed

### Mobile-First Design
- All components use responsive CSS
- Test on mobile/tablet viewports
- Voice assistant optimized for mobile

---

## Documentation Links

- [Dashboard Redesign Summary](./DASHBOARD_REDESIGN_SUMMARY.md)
- [Voice Assistant Setup](./documentation/VOICE_ASSISTANT_SETUP_GUIDE.md)
- [SAKHI Integration Guide](./documentation/SAKHI_INTEGRATION_GUIDE.md)
- [SAKHI Quick Reference](./documentation/SAKHI_QUICK_REFERENCE.md)
- [Flowcharts](./FLOWCHARTS.md)

---

## Troubleshooting

### Backend won't start
- Activate virtual environment: `. venv/Scripts/activate`
- Check Python version: `python --version` (need 3.10+)
- Clear cached files: `find . -type d -name __pycache__ -exec rm -r {} +`

### Frontend won't start
- Clear npm cache: `npm cache clean --force`
- Delete `node_modules` and `package-lock.json`, then `npm install`
- Ensure backend is running (frontend proxies to it)

### Database issues
- Reset database: `python manage.py migrate zero && python manage.py migrate`
- Check migrations: `python manage.py showmigrations`

### Voice not working
- Check microphone permissions (browser/OS level)
- Verify `SpeechRecognition` package installed
- Test with `backend/ml_models/recognize_speech.py`

---

## Code Conventions

- **Component Names**: PascalCase (e.g., `DashboardHeader.jsx`)
- **Hooks**: camelCase with `use` prefix (e.g., `useLanguage()`)
- **Model Names**: PascalCase, singular (e.g., `Income`, `Expense`)
- **API Endpoints**: lowercase, plural (e.g., `/api/income/`, `/api/expenses/`)
- **Branch naming**: `feature/description` or `bugfix/description`
- **Commits**: Conventional commits (feat:, fix:, docs:, refactor:, test:)

---

## Contact & Support

For issues or questions about the project, refer to documentation in `./documentation/` folder or check component docstrings.
