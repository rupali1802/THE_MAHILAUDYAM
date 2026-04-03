#!/usr/bin/env python
"""
Test MySQL database connection for Mahila Udyam project
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mahila_udyam_backend.settings')
django.setup()

from api.models import User, Income, Expense, Sales, Scheme, MarketPrice, Mentor, MentorChat

try:
    print("="*60)
    print("✅ MySQL Database Connection Test")
    print("="*60)
    
    # Test model access
    user_count = User.objects.count()
    income_count = Income.objects.count()
    expense_count = Expense.objects.count()
    sales_count = Sales.objects.count()
    scheme_count = Scheme.objects.count()
    market_count = MarketPrice.objects.count()
    mentor_count = Mentor.objects.count()
    chat_count = MentorChat.objects.count()
    
    print("\n📊 Database Statistics:")
    print(f"  👥 Users: {user_count}")
    print(f"  💰 Incomes: {income_count}")
    print(f"  💸 Expenses: {expense_count}")
    print(f"  🛍️ Sales: {sales_count}")
    print(f"  📋 Schemes: {scheme_count}")
    print(f"  📈 Market Prices: {market_count}")
    print(f"  👨‍🏫 Mentors: {mentor_count}")
    print(f"  💬 Mentor Chats: {chat_count}")
    
    print("\n✅ All Models Connected Successfully!")
    print("✅ MySQL Database Setup Complete!\n")
    
except Exception as e:
    print(f"\n❌ Error: {str(e)}\n")
    import traceback
    traceback.print_exc()
