# MahilaUdyam - Tech Stack Architecture

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                               │
│  ┌──────────────────────┐    ┌──────────────────────┐                       │
│  │  Frontend            │    │  Data Integration    │    ┌──────────────────┐│
│  │  Development         │    │                      │    │ Security &       ││
│  │                      │    │ • Agmarket API       │    │ Monitoring       ││
│  │ • React.js           │    │ • Government Schemes │    │                  ││
│  │ • React Router       │    │ • Market Prices API  │    │ • JWT Auth       ││
│  │ • Axios (HTTP)       │    │ • ML Models          │    │ • OTP Login      ││
│  │ • Tailwind CSS       │    │ • Data Processing    │    │ • Encryption     ││
│  │ • Web Speech API     │    │ • CSV Data Handling  │    │ • Input Validation
│  │ • Responsive UI      │    │ • Python Pandas      │    │ • Role-Based AC  ││
│  │ • Lucide Icons       │    │                      │    │                  ││
│  └──────────────────────┘    └──────────────────────┘    └──────────────────┘│
│                                                                               │
│  ┌──────────────────────┐    ┌──────────────────────┐    ┌──────────────────┐│
│  │  Voice Processing    │    │  Payments & External │    │ Backend & API    ││
│  │                      │    │  Services            │    │                  ││
│  │ • Speech-to-Text     │    │                      │    │ • Django 4.2     ││
│  │ • Google API         │    │ • UPI QR Code        │    │ • Django REST    ││
│  │ • Text-to-Speech     │    │ • Payment Logging    │    │ • Python 3.10+   ││
│  │ • Language Detection │    │ • Transaction Mgmt   │    │ • PyMySQL        ││
│  │ • num2words          │    │ • Payment Gateway    │    │ • Pandas         ││
│  │ • Multi-language     │    │ • Error Handling     │    │ • REST APIs      ││
│  │   (EN, HI, TA)       │    │                      │    │ • CORS Support   ││
│  └──────────────────────┘    └──────────────────────┘    └──────────────────┘│
│                                                                               │
│  ┌──────────────────────────────────────────────────────────────────────────┐│
│  │ Database & Storage                    │ AI & Machine Learning Models      ││
│  │                                       │                                   ││
│  │ • SQLite (Development)                │ • Intent Prediction                ││
│  │ • MySQL (Production)                  │ • Language Detection               ││
│  │ • Structured Tables                   │ • Scikit-learn                     ││
│  │ • User Profiles                       │ • TensorFlow/Keras (Optional)      ││
│  │ • Financial Transactions              │ • Rule-based Logic                 ││
│  │ • Voice Logs                          │ • Context-aware Responses          ││
│  │ • Backup Mechanisms                   │ • Multi-label Classification       ││
│  │ • Local Storage                       │ • Confidence Scoring               ││
│  └──────────────────────────────────────────────────────────────────────────┘│
│                                                                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Detailed Tech Stack

### 🖥️ **Frontend Development**
| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Framework** | React.js 18+ | UI library with hooks |
| **Routing** | React Router v6 | Client-side navigation |
| **HTTP Client** | Axios | API requests with interceptors |
| **Styling** | Tailwind CSS | Utility-first CSS framework |
| **Icons** | Lucide React | Beautiful SVG icons |
| **Voice I/O** | Web Speech API | Browser built-in speech capabilities |
| **State Management** | Context API | Global state management |
| **Build Tool** | Create React App | Webpack-based bundling |
| **Package Manager** | npm | Dependency management |

**Key Features:**
- Mobile-first responsive design
- Real-time voice input/output
- Multi-language UI (EN, HI, TA)
- Offline capability with localStorage
- Progressive Web App support

---

### 🔗 **Data Integration**
| Component | Technology | Data Source |
|-----------|-----------|-------------|
| **Government Schemes** | Django ORM | SQLite/MySQL database |
| **Market Prices** | CSV Parser + Pandas | Stored market data (Agmarket) |
| **Voice Analysis** | ML Models | Intent classification system |
| **Data Processing** | Python Pandas | ETL pipelines |
| **Caching** | Django Cache | Reduced API calls |

**Data Flow:**
1. Frontend requests data via REST API
2. Backend processes through Django views
3. ML models predict user intent
4. Response formatted and sent back
5. Frontend renders with caching

---

### 🔐 **Security & Monitoring**

| Security Layer | Implementation |
|---|---|
| **Authentication** | JWT tokens (djangorestframework) |
| **Device ID** | UUID-based device tracking |
| **OTP** | SMS-based two-factor auth (optional) |
| **Password Security** | Bcrypt hashing (Django default) |
| **Data Encryption** | HTTPS/TLS in production |
| **CORS Policy** | django-cors-headers |
| **Input Validation** | Django validators + frontend validation |
| **Role-based Access** | User groups and permissions |
| **Rate Limiting** | API throttling policies |
| **Logging** | Django debug toolbar + custom logging |

**Monitoring Tools:**
- Django admin panel for user management
- error logging system
- Transaction audit trails
- Voice command logging

---

### 💾 **Database & Storage**

#### **Development Database (SQLite)**
```
db.sqlite3
├── User Profiles
├── Income Records
├── Expense Records
├── Sales Transactions
├── Payment Logs
├── Voice Command History
└── ML Model Training Data
```

#### **Production Database (MySQL)**
```
mahila_udyam_db
├── users (profiles, authentication)
├── transactions (income, expense, sales)
├── payments (UPI logs, history)
├── voice_logs (voice commands, responses)
├── schemes (government schemes data)
├── market_prices (commodity pricing)
├── ml_predictions (intent logs)
└── mentors (expert profiles)
```

**Storage Features:**
- Automatic backups
- Transaction logging
- Data integrity constraints
- Relationship management with Foreign Keys

---

### 🎤 **Voice Processing Pipeline**

```
User Speech
    ↓
[Speech-to-Text API] (Google Cloud Speech-to-Text)
    ↓
Text Input (EN/HI/TA)
    ↓
[Language Detection] 
    ↓
[Intent Classification] (ML Model)
    ↓
[Rule Engine] 
    ↓
[Response Generation]
    ↓
[Text-to-Speech] (Google Cloud TTS / Web Speech API)
    ↓
Audio Output
```

**Technologies:**
- **Speech Recognition:** SpeechRecognition library (pydub support)
- **Language Detection:** textblob, langdetect
- **Text Processing:** NLTK, Regex patterns
- **Text-to-Speech:** Web Speech API (browser), Google TTS (fallback)
- **Number Conversion:** num2words (convert digits to words)

---

### 💳 **Payments & External Services**

| Service | Integration | Purpose |
|---------|-----------|---------|
| **UPI/QR Code** | Payment Gateway Integration | Digital payments |
| **Payment Logging** | Custom Django Model | Audit trail |
| **Transaction Mgmt** | Atomic DB transactions | Data consistency |
| **External APIs** | REST API calls | Third-party data |

---

### 🔧 **Backend & API**

```python
MahilaUdyam Backend Architecture
├── Django 4.2.7
│   ├── Django REST Framework (3.14.0)
│   ├── django-cors-headers
│   └── python-decouple
├── Python Ecosystem
│   ├── Pandas (data processing)
│   ├── joblib (ML model persistence)
│   ├── Pillow (image handling)
│   └── PyMySQL (database driver)
└── API Endpoints
    ├── /api/dashboard/
    ├── /api/income/
    ├── /api/expense/
    ├── /api/sales/
    ├── /api/profit/
    ├── /api/market-prices/
    ├── /api/schemes/
    ├── /api/mentors/
    ├── /api/predict-intent/ (Voice)
    ├── /api/payment/
    └── /api/user/
```

**Key Features:**
- RESTful API design
- Request/response validation
- Error handling with proper HTTP status codes
- Async task processing capability
- Database query optimization

---

### 🤖 **AI & Machine Learning Models**

#### **Intent Classification Model**
```
Training Data
    ↓
[Feature Extraction]
    ↓
[Scikit-learn TF-IDF Vectorizer]
    ↓
[Naive Bayes / SVM Classifier]
    ↓
[Model Serialization] (joblib)
    ↓
Production Model
```

**Intent Categories:**
- Income recording
- Expense tracking
- Sales logging
- Profit calculation
- Market prices query
- Government schemes info
- Mentor connection
- Payment processing

#### **Feature Extraction:**
- TF-IDF (Term Frequency-Inverse Document Frequency)
- N-gram analysis
- Text normalization

#### **Language Support:**
- English (EN)
- Hindi (HI) - transliteration support
- Tamil (TA)

#### **Rule-based Fallback:**
```
If ML Confidence < Threshold:
    → Apply Rule Engine
    → Pattern matching
    → Keyword extraction
    → Fallback response
```

**Model Files:**
```
ml_models/saved_models/
├── mahila_intent_model.pkl (trained classifier)
├── mahila_intent_model_vectorizer.pkl (TF-IDF vectorizer)
├── model_info.json (metadata)
└── backup/ (previous versions)
```

---

## Technology Stack Summary Table

| Category | Tech | Version | Purpose |
|----------|------|---------|---------|
| **Frontend** | React | 18+ | UI Framework |
| | React Router | 6+ | Navigation |
| | Tailwind CSS | 3+ | Styling |
| | Axios | Latest | HTTP Client |
| **Backend** | Django | 4.2.7 | Web Framework |
| | DRF | 3.14.0 | REST APIs |
| | Python | 3.10+ | Language |
| **Database** | SQLite | Built-in | Development |
| | MySQL | 5.7+ | Production |
| **ML/AI** | Scikit-learn | Latest | ML Models |
| | Pandas | 2.1.3 | Data Processing |
| | num2words | 0.5.13 | Number to Words |
| **Voice** | SpeechRecognition | 3.10.0 | Speech-to-Text |
| | pydub | 0.25.1 | Audio Processing |
| **External** | Google APIs | Latest | Speech/Translation |
| **DevOps** | npm | Latest | Package Manager |
| | pip | Latest | Python PKG Manager |

---

## Deployment Architecture

```
Frontend (React Build)
    ↓
Hosted on: Vercel / Firebase Hosting / GitHub Pages
    ↓
API Requests (HTTPS)
    ↓
Backend (Django Server)
    ↓
Hosted on: Heroku / PythonAnywhere / AWS / Azure
    ↓
Database (MySQL)
    ↓
External APIs (Google Cloud, etc.)
```

---

## Development Workflow

```
1. Feature Development
   └── Frontend (React) + Backend (Django)

2. Testing
   └── Unit tests + Integration tests

3. Version Control
   └── Git → GitHub (rupali1802/MahilaUdyam)

4. Deployment
   └── Frontend → npm run build
   └── Backend → gunicorn/uwsgi + nginx

5. Monitoring
   └── Logs + Error tracking
```

---

## Environment Configuration

**.env File (Backend)**
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=mysql://user:pass@localhost/mahila_udyam
GOOGLE_API_KEY=your-google-api-key
```

**.env File (Frontend)**
```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_ENVIRONMENT=development
```

---

## Scale & Performance

- **Concurrent Users:** 1000+ with optimization
- **Database Queries:** Optimized with indexing
- **API Response Time:** < 500ms (target)
- **Frontend Load Time:** < 3s (target)
- **Cache Strategy:** Redis (optional for production)

---

## Future Enhancement Opportunities

- [ ] Implement GraphQL layer
- [ ] Add PWA offline support
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced analytics dashboard
- [ ] Real-time notifications (WebSocket)
- [ ] Blockchain for payment transparency
- [ ] Advanced NLP with transformers
- [ ] Video tutorials integration
- [ ] Community marketplace
- [ ] Blockchain-based certificates

---

**Last Updated:** March 30, 2026  
**Project:** MahilaUdyam - Women Entrepreneur Platform  
**Repository:** https://github.com/rupali1802/MahilaUdyam
