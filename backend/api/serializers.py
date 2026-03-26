"""
Mahila Udyam - Django REST Framework Serializers
"""
from rest_framework import serializers
from .models import User, Income, Expense, Sales, Payment, MarketPrice, Scheme, Mentor, MentorChat
from datetime import date


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'device_id': {'required': True},
        }


class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'
        extra_kwargs = {
            'device_id': {'required': True},
            'amount': {'required': True},
            'source': {'required': True},
            'date': {'required': True},
        }

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value

    def validate_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Date cannot be in the future.")
        return value


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        extra_kwargs = {
            'device_id': {'required': True},
            'amount': {'required': True},
            'date': {'required': True},
        }

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")
        return value


class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'
        extra_kwargs = {
            'device_id': {'required': True},
            'product_name': {'required': True},
            'price_per_unit': {'required': True},
            'total_amount': {'required': True},
            'sale_date': {'required': True},
        }

    def validate(self, data):
        if data.get('quantity', 1) <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        if data.get('price_per_unit', 0) <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return data


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class MarketPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketPrice
        fields = '__all__'


class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheme
        fields = '__all__'


class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = '__all__'


class MentorChatSerializer(serializers.ModelSerializer):
    mentor_name = serializers.SerializerMethodField()

    class Meta:
        model = MentorChat
        fields = '__all__'

    def get_mentor_name(self, obj):
        return obj.mentor.name if obj.mentor else ''


class ProfitSummarySerializer(serializers.Serializer):
    period = serializers.CharField()
    total_income = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_expense = serializers.DecimalField(max_digits=15, decimal_places=2)
    net_profit = serializers.DecimalField(max_digits=15, decimal_places=2)
    profit_margin = serializers.FloatField()
    expense_ratio = serializers.FloatField()
    income_count = serializers.IntegerField()
    expense_count = serializers.IntegerField()
    daily_average_profit = serializers.DecimalField(max_digits=12, decimal_places=2)
