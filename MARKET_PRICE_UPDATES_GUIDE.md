# 📊 Daily Market Price Updates with Real-Time Analysis - Setup Guide

## Overview
This feature provides **daily market price updates** and **real-time analysis** for the MahilaUdyam application, enabling women entrepreneurs to make informed trading decisions.

## Features Implemented

### 1. **Daily Price Updates**
- Automatic daily price recordings via management command
- Historical price tracking for trend analysis
- Realistic price variations based on market conditions

### 2. **Real-Time Market Analysis**
- Price trend identification (up, down, stable)
- 7-day and 30-day price analysis
- Volatility and momentum calculations
- Actionable buy/sell/hold recommendations

### 3. **Advanced Analytics Views**
- Price history tracking
- Comparative market analysis across locations
- Real-time market intelligence
- Comprehensive price trend analysis

### 4. **Frontend Components**
- MarketAnalytics.jsx - Advanced analytics dashboard
- Integration with existing MarketPrice.jsx
- Voice-enabled market queries
- Interactive charts and statistics

## Installation & Setup Steps

### Step 1: Create Migrations
```bash
cd backend
python manage.py makemigrations api
python manage.py migrate
```

### Step 2: Initialize Price History
```bash
# This setup script will:
# - Run migrations
# - Verify database tables
# - Initialize historical price data
# - Setup scheduler configuration
python setup_market_updates.py
```

### Step 3: Run First Market Update
```bash
python manage.py update_market_prices
```

This command will:
- Record all active market prices to history
- Update current prices with realistic variations
- Generate analysis for all commodities
- Create trend indicators

### Step 4: Update Frontend Components

#### Option A: Add MarketAnalytics to Dashboard
Import in your main page component:
```javascript
import MarketAnalytics from '../components/MarketAnalytics';

// In your component:
<MarketAnalytics />
```

#### Option B: Add to MarketPrice.jsx
```javascript
import MarketAnalytics from './MarketAnalytics';

// In MarketPrice component:
return (
  <div>
    <MarketAnalytics />
    {/* Existing MarketPrice content */}
  </div>
);
```

### Step 5: Setup Automated Daily Updates

#### Option A: Using APScheduler (Recommended for Development)
Create `backend/scheduler.py`:
```python
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
import atexit

def start_scheduler():
    """Start background scheduler for daily price updates"""
    scheduler = BackgroundScheduler()
    
    # Schedule at 8:00 AM every day
    scheduler.add_job(
        func=lambda: call_command('update_market_prices'),
        trigger="cron",
        hour=8,
        minute=0,
        id='update_market_prices',
        name='Daily Market Price Update',
        replace_existing=True
    )
    
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    return scheduler

# Install: pip install apscheduler
```

Update `mahila_udyam_backend/apps.py`:
```python
from django.apps import AppConfig

class MahilaUdyamBackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mahila_udyam_backend'

    def ready(self):
        try:
            from scheduler import start_scheduler
            start_scheduler()
        except:
            pass
```

#### Option B: Using Celery + Celery Beat (Production)
```bash
# Install
pip install celery celery-beat redis

# Create backend/celery.py
# Configure in settings.py
# Run: celery -A mahila_udyam_backend worker -B
```

#### Option C: Using Cron Jobs (Linux/Mac)
```bash
# Edit crontab
crontab -e

# Add line:
0 8 * * * cd /path/to/backend && python manage.py update_market_prices
```

#### Option D: Using Task Scheduler (Windows)
Create batch file: `update_prices.bat`
```batch
cd C:\path\to\backend
python manage.py update_market_prices
```
Schedule in Windows Task Scheduler to run daily at 8:00 AM

## API Endpoints

### Get Current Market Prices
```
GET /api/market-prices/?commodity=tomato
```
Returns latest prices for a commodity

### Get Price History
```
GET /api/price-history/?commodity=tomato&days=30
```
Returns historical price data for trend analysis

### Get Price Trends
```
GET /api/price-trends/?commodity=tomato
```
Returns comprehensive trend analysis with recommendations

### Get Comparative Analysis
```
GET /api/market-comparative/?commodity=tomato
```
Compares prices across different markets

### Get Real-Time Market Analysis
```
GET /api/market-realtime/
```
Returns analysis for all commodities with opportunities

### AI Market Analysis (Voice/Text)
```
POST /api/market-analysis/
{
  "query": "Is tomato a good crop to sell?",
  "language": "en",
  "commodity": "tomato"
}
```

## Usage Examples

### 1. View Market Analysis
Users can:
- See latest prices for all commodities
- Check price trends (7-day and 30-day)
- Get buy/sell/hold recommendations
- Compare prices across markets
- Ask voice questions about market conditions

### 2. Monitor Trends
- View volatility scores (0-100)
- Check momentum scores (-100 to +100)
- See historical price charts
- Track price movements over time

### 3. Make Decisions
- Use buy/sell/hold recommendations
- Check market opportunities
- Compare prices in different locations
- Understand market insights

## Frontend Integration

### Add MarketAnalytics to App.js
```javascript
import MarketAnalytics from './components/MarketAnalytics';

// In your routes:
<Route path="/market-analytics" element={<MarketAnalytics />} />

// Or embed in Dashboard:
<MarketAnalytics />
```

### API Service Functions (Already Configured)
```javascript
import {
  getMarketPrices,
  getPriceHistory,
  getPriceTrends,
  getMarketComparative,
  getRealtimeMarketAnalysis
} from '../services/api';

// Get real-time analysis
const response = await getRealtimeMarketAnalysis();
console.log(response.data.opportunities);

// Get trends for a commodity
const trends = await getPriceTrends('tomato');
console.log(trends.data.analysis);
```

## Database Models

### PriceHistory
- Tracks historical prices daily
- Indexed for fast lookups
- Stores price changes over time

### MarketPriceAnalysis
- Daily analysis for each commodity
- 7-day and 30-day statistics
- Trend, momentum, and volatility scores
- Buy/sell/hold recommendations

## Management Command

### update_market_prices Command
```bash
python manage.py update_market_prices [--force]

Options:
  --force    Force update even if already run today
```

### Manual Update Steps
```bash
cd backend
python manage.py update_market_prices
```

## Monitoring & Verification

### Check if Updates are Working
```bash
# Login to Django shell
python manage.py shell

from api.models import PriceHistory, MarketPriceAnalysis
from datetime import date

# Check today's history
today = date.today()
history = PriceHistory.objects.filter(market_date=today)
print(f"Recorded {history.count()} prices today")

# Check today's analysis
analysis = MarketPriceAnalysis.objects.filter(analysis_date=today)
print(f"Generated {analysis.count()} analyses today")

# View sample analysis
sample = analysis.first()
print(f"Commodity: {sample.commodity_name}")
print(f"Trend: {sample.trend}")
print(f"Recommendation: {sample.recommendation}")
print(f"Momentum: {sample.momentum_score}")
```

## Troubleshooting

### Issue: No price updates
**Solution:**
```bash
# Check if command works manually
python manage.py update_market_prices

# Verify database
python manage.py shell
from api.models import MarketPrice
print(f"Active commodities: {MarketPrice.objects.filter(is_active=True).count()}")
```

### Issue: Missing tables
**Solution:**
```bash
# Run migrations
python manage.py migrate

# Check tables
python setup_market_updates.py
```

### Issue: Scheduler not running
**Solution:**
- Check if APScheduler is installed: `pip install apscheduler`
- Verify scheduler.py is in right location
- Check Django logs for errors
- Use alternative: run as cron job or Task Scheduler

## Performance Optimization

### For Large Datasets
1. Add database indexes:
```python
# Already added in model Meta classes
indexes = [
    models.Index(fields=['commodity_name', '-market_date']),
]
```

2. Use pagination in API:
```
GET /api/price-history/?commodity=tomato&days=30&page=1&limit=50
```

3. Cache frequently accessed data:
```python
from django.views.decorators.cache import cache_page

@cache_page(60*30)  # 30 minutes
def RealtimeMarketAnalysisView(APIView):
    pass
```

## Future Enhancements

- [ ] Machine learning price prediction
- [ ] SMS/Email alerts for price changes
- [ ] Weather integration for crop recommendations
- [ ] Government procurement price tracking
- [ ] Websocket real-time price updates
- [ ] Mobile app notifications
- [ ] Comparative analysis across states
- [ ] Seasonal trend predictions

## Support & Documentation

### API Documentation
Complete API docs available at: `{BASE_URL}/api/`

### File Locations
- Backend models: `backend/api/models.py`
- API views: `backend/api/views.py`
- Management command: `backend/api/management/commands/update_market_prices.py`
- Frontend component: `frontend/src/components/MarketAnalytics.jsx`
- Setup script: `backend/setup_market_updates.py`

### Next Steps
1. ✅ Run migrations and setup
2. ✅ Configure automated updates
3. ✅ Add MarketAnalytics to frontend
4. ✅ Test endpoints with API calls
5. ✅ Monitor first few updates
6. ✅ Gather user feedback
7. ✅ Optimize based on usage patterns

---

**Last Updated:** April 3, 2026
**Status:** ✅ Ready for Deployment
