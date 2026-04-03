"""
Management command to seed the database with comprehensive market data
Run with: python manage.py seed_market_data
"""
from django.core.management.base import BaseCommand
from api.models import MarketPrice
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Seed the database with comprehensive market data'
    
    def handle(self, *args, **options):
        # Clear existing data
        MarketPrice.objects.all().delete()
        
        market_data = [
            # Vegetables & Agriculture
            {'commodity_name': 'Rice', 'price': 50, 'unit': 'kg', 'market_location': 'Local Market', 'trend': 'stable'},
            {'commodity_name': 'Wheat', 'price': 35, 'unit': 'kg', 'market_location': 'Local Market', 'trend': 'up'},
            {'commodity_name': 'Onion', 'price': 30, 'unit': 'kg', 'market_location': 'Chennai Mandi', 'trend': 'down'},
            {'commodity_name': 'Carrot', 'price': 25, 'unit': 'kg', 'market_location': 'Local Market', 'trend': 'stable'},
            {'commodity_name': 'Tomato', 'price': 20, 'unit': 'kg', 'market_location': 'Chennai Mandi', 'trend': 'up'},
            {'commodity_name': 'Potato', 'price': 18, 'unit': 'kg', 'market_location': 'Local Market', 'trend': 'stable'},
            
            # Fruits
            {'commodity_name': 'Banana', 'price': 40, 'unit': 'dozen', 'market_location': 'Fruit Market', 'trend': 'stable'},
            {'commodity_name': 'Mango', 'price': 60, 'unit': 'kg', 'market_location': 'Local Market', 'trend': 'up'},
            {'commodity_name': 'Apple', 'price': 120, 'unit': 'kg', 'market_location': 'Premium Market', 'trend': 'stable'},
            {'commodity_name': 'Orange', 'price': 45, 'unit': 'kg', 'market_location': 'Local Market', 'trend': 'down'},
            
            # Dairy Products
            {'commodity_name': 'Milk', 'price': 65, 'unit': 'litre', 'market_location': 'Local Dairy', 'trend': 'stable'},
            {'commodity_name': 'Ghee', 'price': 600, 'unit': 'kg', 'market_location': 'Premium Market', 'trend': 'up'},
            {'commodity_name': 'Yogurt', 'price': 80, 'unit': 'kg', 'market_location': 'Local Market', 'trend': 'stable'},
            {'commodity_name': 'Paneer', 'price': 300, 'unit': 'kg', 'market_location': 'Local Market', 'trend': 'stable'},
            
            # Spices
            {'commodity_name': 'Turmeric', 'price': 250, 'unit': 'kg', 'market_location': 'Spice Market', 'trend': 'stable'},
            {'commodity_name': 'Chili Powder', 'price': 200, 'unit': 'kg', 'market_location': 'Spice Market', 'trend': 'down'},
            {'commodity_name': 'Coriander', 'price': 180, 'unit': 'kg', 'market_location': 'Spice Market', 'trend': 'up'},
            {'commodity_name': 'Black Pepper', 'price': 500, 'unit': 'kg', 'market_location': 'Premium Market', 'trend': 'stable'},
            
            # Oil & Seeds
            {'commodity_name': 'Coconut Oil', 'price': 150, 'unit': 'litre', 'market_location': 'Local Market', 'trend': 'stable'},
            {'commodity_name': 'Sesame Oil', 'price': 200, 'unit': 'litre', 'market_location': 'Premium Market', 'trend': 'up'},
            
            # Processed Foods
            {'commodity_name': 'Pickle (Mango)', 'price': 150, 'unit': 'kg', 'market_location': 'Local Market', 'trend': 'stable'},
            {'commodity_name': 'Jams', 'price': 250, 'unit': 'kg', 'market_location': 'Premium Market', 'trend': 'stable'},
            {'commodity_name': 'Dry Snacks', 'price': 300, 'unit': 'kg', 'market_location': 'Local Market', 'trend': 'up'},
            
            # Handicraft Products (Representative Prices)
            {'commodity_name': 'Handmade Cloth', 'price': 400, 'unit': 'piece', 'market_location': 'Online Market', 'trend': 'up'},
            {'commodity_name': 'Embroidered Saree', 'price': 2500, 'unit': 'piece', 'market_location': 'Premium Market', 'trend': 'up'},
            {'commodity_name': 'Handmade Jewelry', 'price': 1500, 'unit': 'piece', 'market_location': 'Online Market', 'trend': 'stable'},
            {'commodity_name': 'Wooden Craft', 'price': 800, 'unit': 'piece', 'market_location': 'Local Market', 'trend': 'stable'},
        ]
        
        today = date.today()
        created_count = 0
        
        for item in market_data:
            market_price = MarketPrice.objects.create(
                commodity_name=item['commodity_name'],
                price=item['price'],
                unit=item['unit'],
                market_location=item['market_location'],
                trend=item['trend'],
                market_date=today,
                is_active=True,
                source='Admin Seed Data'
            )
            created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Successfully seeded {created_count} market price records')
        )
