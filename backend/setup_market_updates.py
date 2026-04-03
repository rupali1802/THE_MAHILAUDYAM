#!/usr/bin/env python
"""
Setup script for daily market price updates with real-time analysis
Includes: migrations, initial data setup, and scheduler configuration
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mahila_udyam_backend.settings')
django.setup()

from django.core.management import call_command
from django.db import connection
from api.models import (
    MarketPrice, PriceHistory, MarketPriceAnalysis, User
)
from datetime import date, timedelta
from decimal import Decimal
import random

def run_migrations():
    """Run Django migrations"""
    print("📋 Running migrations...")
    try:
        call_command('migrate', verbosity=1)
        print("✅ Migrations completed")
        return True
    except Exception as e:
        print(f"❌ Migration error: {e}")
        return False

def initialize_price_history():
    """Initialize price history from current market prices"""
    print("📊 Initializing price history...")
    
    try:
        today = date.today()
        active_prices = MarketPrice.objects.filter(is_active=True)
        
        created_count = 0
        for market_price in active_prices:
            # Create history entry if not exists
            ph, created = PriceHistory.objects.get_or_create(
                commodity_name=market_price.commodity_name,
                market_date=today,
                defaults={
                    'price': market_price.price,
                    'unit': market_price.unit,
                    'market_location': market_price.market_location,
                    'source': 'Initial'
                }
            )
            if created:
                created_count += 1
        
        # Also create historical data for the past 7 days
        for day_offset in range(1, 8):
            past_date = today - timedelta(days=day_offset)
            for market_price in active_prices:
                # Check if already exists
                if not PriceHistory.objects.filter(
                    commodity_name=market_price.commodity_name,
                    market_date=past_date
                ).exists():
                    # Create with slightly varied price
                    variation = random.uniform(-3, 3)
                    varied_price = market_price.price * (1 + Decimal(str(variation)) / 100)
                    
                    PriceHistory.objects.create(
                        commodity_name=market_price.commodity_name,
                        price=varied_price,
                        unit=market_price.unit,
                        market_date=past_date,
                        market_location=market_price.market_location,
                        source='Historical'
                    )
                    created_count += 1
        
        print(f"✅ Created {created_count} historical price records")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing price history: {e}")
        return False

def verify_tables():
    """Verify that all tables were created"""
    print("🔍 Verifying database tables...")
    
    required_tables = [
        'mu_market_price',
        'mu_price_history',
        'mu_market_price_analysis'
    ]
    
    with connection.cursor() as cursor:
        # Get existing tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        existing_tables = [row[0] for row in cursor.fetchall()]
        
        missing = [t for t in required_tables if t not in existing_tables]
        if missing:
            print(f"❌ Missing tables: {missing}")
            return False
        else:
            print(f"✅ All required tables exist")
            return True

def setup_scheduler():
    """Setup APScheduler for daily updates"""
    print("⏰ Setting up daily price update scheduler...")
    
    try:
        # Check if APScheduler is installed
        import apscheduler
        print("✅ APScheduler is available")
        
        scheduler_code = '''
# Add to your Django settings or a separate scheduler file:
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management import call_command
import atexit

def start_scheduler():
    """Start the background scheduler for daily price updates"""
    scheduler = BackgroundScheduler()
    
    # Schedule daily update at 8:00 AM
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

# In your Django app's apps.py ready() method:
def ready(self):
    try:
        from .scheduler import start_scheduler
        start_scheduler()
    except:
        pass
'''
        print(scheduler_code)
        return True
        
    except ImportError:
        print("⚠️  APScheduler not installed. Install with: pip install apscheduler")
        print("   Or use celery/celery-beat for production environments")
        return False

def main():
    print("=" * 60)
    print("🌾 Mahila Udyam - Market Price Update Setup")
    print("=" * 60)
    print()
    
    steps = [
        ("Running migrations", run_migrations),
        ("Verifying tables", verify_tables),
        ("Initializing price history", initialize_price_history),
        ("Setting up scheduler", setup_scheduler),
    ]
    
    results = []
    for step_name, step_func in steps:
        print(f"\n📌 {step_name}...")
        result = step_func()
        results.append(result)
        if not result:
            print(f"⚠️  {step_name} partially completed")
    
    print()
    print("=" * 60)
    if all(results):
        print("✅ Setup completed successfully!")
        print("\n Next steps:")
        print("1. Run first update: python manage.py update_market_prices")
        print("2. Check frontend: http://localhost:3000/market-price")
        print("3. Monitor prices: http://localhost:8000/api/market-realtime/")
    else:
        print("⚠️  Setup completed with some warnings. Check above for details.")
    print("=" * 60)

if __name__ == '__main__':
    main()
