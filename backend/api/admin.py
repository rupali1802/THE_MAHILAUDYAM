from django.contrib import admin
from .models import User, Income, Expense, Sales, Payment, MarketPrice, Scheme, Mentor, MentorChat

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'device_id', 'business_type', 'language', 'location', 'created_at']
    list_filter = ['business_type', 'language', 'state']
    search_fields = ['name', 'device_id', 'phone', 'email']

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'amount', 'source', 'category', 'date']
    list_filter = ['category', 'date']
    search_fields = ['device_id', 'source', 'description']

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'amount', 'category', 'payment_method', 'date']
    list_filter = ['category', 'payment_method', 'date']
    search_fields = ['device_id', 'description']

@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'product_name', 'quantity', 'total_amount', 'sale_date', 'status']
    list_filter = ['status', 'sale_date']
    search_fields = ['device_id', 'product_name', 'customer_name']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'amount', 'method', 'payment_type', 'status', 'date']
    list_filter = ['method', 'status', 'payment_type']

@admin.register(MarketPrice)
class MarketPriceAdmin(admin.ModelAdmin):
    list_display = ['commodity_name', 'price', 'unit', 'market_date', 'trend', 'market_location']
    list_filter = ['unit', 'trend', 'market_date']
    search_fields = ['commodity_name']

@admin.register(Scheme)
class SchemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'agency', 'category', 'status', 'deadline']
    list_filter = ['category', 'status']
    search_fields = ['name', 'agency', 'description']

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'experience_years', 'rating', 'availability']
    list_filter = ['availability', 'is_active']
    search_fields = ['name', 'expertise', 'specialization']

@admin.register(MentorChat)
class MentorChatAdmin(admin.ModelAdmin):
    list_display = ['device_id', 'mentor', 'message_type', 'status', 'timestamp']
    list_filter = ['message_type', 'status']
    search_fields = ['device_id', 'message']
