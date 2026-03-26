# 🌸 Mahila Udyam — महिला उद्यम — மகிளா உத்யம்

> **Voice-Controlled Business Management for Rural Indian Women Entrepreneurs**

[![License: MIT](https://img.shields.io/badge/License-MIT-pink.svg)](LICENSE)
[![Django](https://img.shields.io/badge/Django-4.2+-green)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18+-blue)](https://reactjs.org/)

---

## 🎯 What is Mahila Udyam?

Mahila Udyam empowers rural women entrepreneurs to manage their small businesses through:
- 🎤 **Voice commands** in their native language
- 📱 **Mobile-first UI** designed for rural users  
- 🌐 **3-language support**: English, हिन्दी, தமிழ்
- 📡 **Offline ML** — works without internet
- 📊 **Complete financial tracking** — income, expenses, sales, profit

---

## ✨ Features

| Feature | Description |
|---|---|
| 💰 Income Tracking | Record all income with source and category |
| 💸 Expense Tracking | Log expenses with category and payment method |
| 🛍️ Sales Recording | Track product sales with quantities and prices |
| 📊 Profit Analysis | Real-time P&L with charts and trends |
| 💳 Payment Tracking | UPI, Cash, Bank transfer records + QR code |
| 🌾 Market Prices | Live commodity prices from local mandis |
| 📋 Government Schemes | Curated schemes for women entrepreneurs |
| 👩‍🏫 Mentors | Connect with business experts via chat |
| 🎤 Voice Assistant | Speak commands, get instant responses |

---

## 🛠️ Tech Stack

**Backend**
- Python 3.10+ / Django 4.2 / Django REST Framework
- MySQL 8.0 (SQLite fallback for dev)
- scikit-learn (TF-IDF + Logistic Regression)
- 92.31% ML accuracy, <200ms inference

**Frontend**
- React 18 / React Router v6
- Web Speech API (voice input, offline)
- SpeechSynthesis API (voice output)
- CSS3 responsive design

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- MySQL 8.0+ (or use SQLite fallback)

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt

# Configure database
# Option A: MySQL (edit settings.py with your credentials)
mysql -u root -p -e "CREATE DATABASE mahila_udyam_db CHARACTER SET utf8mb4;"

# Option B: SQLite (uncomment SQLite config in settings.py)

# Run migrations
python manage.py migrate

# Train ML model (IMPORTANT - do this before starting server)
python ml_models/model_training.py

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver 0.0.0.0:8000
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
# Opens at http://localhost:3001
```

### Access Points

| Service | URL |
|---|---|
| Frontend App | http://localhost:3001 |
| Backend API | http://localhost:8000/api/ |
| Django Admin | http://localhost:8000/admin/ |

---

## 📁 Project Structure

```
MahilaUdyam/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   ├── mahila_udyam_backend/    # Django project config
│   │   ├── settings.py
│   │   └── urls.py
│   ├── api/                     # Main app
│   │   ├── models.py            # 9 database models
│   │   ├── views.py             # REST API endpoints
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── admin.py
│   └── ml_models/              # AI/ML module
│       ├── model_training.py   # Train intent classifier
│       ├── model_predict.py    # Singleton predictor
│       ├── voice_views.py      # Voice pipeline
│       ├── rule_engine.py      # Intent handlers
│       ├── language_responses.py # Multi-lang responses
│       ├── language_support.py  # Templates
│       ├── number_converter.py  # Number→words
│       └── saved_models/       # Trained model files
│
└── frontend/
    └── src/
        ├── App.js               # Router
        ├── context/             # Language state
        ├── hooks/               # useLanguage hook
        ├── pages/               # 12 page components
        ├── components/          # Shared components
        ├── services/            # API client
        ├── utils/               # Device, translations
        └── styles/              # CSS design system
```

---

## 🗄️ Database Models

| Model | Description |
|---|---|
| User | Device-based profile (no login) |
| Income | Revenue records |
| Expense | Cost records |
| Sales | Product transactions |
| Payment | UPI/Cash/Bank payments |
| MarketPrice | Commodity prices (admin-managed) |
| Scheme | Government schemes (admin-managed) |
| Mentor | Business mentors |
| MentorChat | User-mentor conversations |

---

## 🎤 Voice Commands (Examples)

**English**
- *"Record income 500 rupees from vegetable sale"*
- *"Expense 200 rupees for transport"*
- *"I sold 10 kg tomatoes at 40 rupees"*
- *"Show my profit this month"*

**Hindi**
- *"Paanch sau rupaye ki aay record karo"*
- *"Kharcha 200 transport ke liye"*
- *"Mera mahine ka laabh batao"*

**Tamil**
- *"Ainjoothu roopaay varumanam padhivu"*
- *"Selavu 200 payanam"*
- *"Indha maadham laabham kaattu"*

---

## 🌐 API Endpoints

```
POST /api/predict-intent/       Voice command → intent + response
GET  /api/dashboard/            Summary stats
GET  /api/income/               List income records
POST /api/income/add/           Add income
GET  /api/expense/              List expenses
POST /api/expense/add/          Add expense
GET  /api/sales/                List sales
POST /api/sales/add/            Add sale
GET  /api/profit/               Profit analysis
GET  /api/payment/              Payments
POST /api/payment/add/          Add payment
GET  /api/market-prices/        Commodity prices
GET  /api/schemes/              Government schemes
GET  /api/mentors/              Business mentors
POST /api/mentor-chat/          Send mentor message
GET  /api/user/                 User profile
POST /api/user/                 Update profile
```

---

## 🧠 ML Model

- **Algorithm**: TF-IDF + Logistic Regression
- **Accuracy**: 92.31% test, 94.87% training
- **Intents**: income, expense, sales, profit, market, schemes, mentor, payment, training
- **Features**: 500 TF-IDF features, 1-2 grams
- **Training data**: 200+ examples, 9 intents
- **Inference**: <200ms, 100% offline

To retrain:
```bash
python ml_models/model_training.py
```

---

## 🔧 Configuration

Edit `backend/mahila_udyam_backend/settings.py`:

```python
# MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'mahila_udyam_db',
        'USER': 'root',
        'PASSWORD': 'your_password',
        ...
    }
}

# Or SQLite (development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

## 📱 Mobile Support

- Responsive: 320px → 1440px
- PWA-ready (add to home screen)
- Touch-optimized UI
- Bottom navigation for thumb reach
- Large tap targets (44px minimum)

---

## 🛡️ Security

- Device UUID authentication (no passwords to forget)
- CORS configured for frontend origin
- Input validation on all API endpoints
- SQL injection protection via Django ORM

---

## 🔮 Future Roadmap

1. Analytics dashboard with charts
2. PDF/Excel export
3. Real UPI payment gateway
4. Native mobile app (React Native)
5. Government portal integration
6. Community / peer support groups
7. AI chatbot for general business advice

---

## 📞 Support

Built for rural Indian women entrepreneurs. 
For issues, feature requests, or contributions, please open a GitHub issue.

---

*Made with 💕 to empower rural women entrepreneurs across India*
