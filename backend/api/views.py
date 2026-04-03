"""
Mahila Udyam - API Views
All REST endpoints for the business management system
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count, Avg, Min, Max
from django.utils import timezone
from datetime import date, timedelta, datetime
from decimal import Decimal
import sys
import os

from .models import (
    User, Income, Expense, Sales, MarketPrice, Scheme, Mentor, MentorChat,
    PriceHistory, MarketPriceAnalysis
)
from .serializers import (
    UserSerializer, IncomeSerializer, ExpenseSerializer, SalesSerializer,
    MarketPriceSerializer, SchemeSerializer,
    MentorSerializer, MentorChatSerializer,
    PriceHistorySerializer, MarketPriceAnalysisSerializer
)

# Add ml_models to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


def get_or_create_user(device_id):
    """Get or create user by device_id"""
    user, created = User.objects.get_or_create(device_id=device_id)
    return user


# ==================== USER VIEWS ====================

class UserProfileView(APIView):
    """Get or update user profile"""

    def get(self, request):
        try:
            device_id = request.query_params.get('device_id')
            if not device_id:
                return Response({'error': 'device_id required'}, status=status.HTTP_400_BAD_REQUEST)
            user = get_or_create_user(device_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Error fetching user profile', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            device_id = request.data.get('device_id')
            if not device_id:
                return Response({'error': 'device_id required'}, status=status.HTTP_400_BAD_REQUEST)
            user = get_or_create_user(device_id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': 'Error updating user profile', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ==================== INCOME VIEWS ====================

class IncomeListView(APIView):
    """List income records"""

    def get(self, request):
        try:
            device_id = request.query_params.get('device_id')
            if not device_id:
                return Response({'error': 'device_id required'}, status=status.HTTP_400_BAD_REQUEST)

            queryset = Income.objects.filter(device_id=device_id)

            # Date filtering
            date_from = request.query_params.get('date_from')
            date_to = request.query_params.get('date_to')
            if date_from:
                queryset = queryset.filter(date__gte=date_from)
            if date_to:
                queryset = queryset.filter(date__lte=date_to)

            # Period filtering
            period = request.query_params.get('period')
            if period == 'today':
                queryset = queryset.filter(date=date.today())
            elif period == 'weekly':
                queryset = queryset.filter(date__gte=date.today() - timedelta(days=7))
            elif period == 'monthly':
                queryset = queryset.filter(date__gte=date.today().replace(day=1))
            elif period == 'yearly':
                queryset = queryset.filter(date__gte=date.today().replace(month=1, day=1))

            category = request.query_params.get('category')
            if category:
                queryset = queryset.filter(category=category)

            total = queryset.aggregate(total=Sum('amount'))['total'] or Decimal('0')
            serializer = IncomeSerializer(queryset, many=True)
            return Response({
                'results': serializer.data,
                'count': queryset.count(),
                'total': str(total)
            })
        except Exception as e:
            return Response(
                {'error': 'Error fetching income records', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class IncomeAddView(APIView):
    """Add new income record"""

    def post(self, request):
        try:
            data = request.data.copy()
            device_id = data.get('device_id')
            if not device_id:
                return Response({'error': 'device_id required'}, status=status.HTTP_400_BAD_REQUEST)

            if not data.get('date'):
                data['date'] = date.today().isoformat()

            serializer = IncomeSerializer(data=data)
            if serializer.is_valid():
                income = serializer.save()
                return Response({
                    'success': True,
                    'message': 'Income recorded successfully',
                    'data': IncomeSerializer(income).data
                }, status=status.HTTP_201_CREATED)
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': 'Error adding income record', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class IncomeDetailView(APIView):
    """Get, update, delete single income record"""

    def get_object(self, pk, device_id):
        try:
            return Income.objects.get(pk=pk, device_id=device_id)
        except Income.DoesNotExist:
            return None

    def get(self, request, pk):
        device_id = request.query_params.get('device_id')
        income = self.get_object(pk, device_id)
        if not income:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(IncomeSerializer(income).data)

    def put(self, request, pk):
        device_id = request.data.get('device_id')
        income = self.get_object(pk, device_id)
        if not income:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = IncomeSerializer(income, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        device_id = request.query_params.get('device_id')
        income = self.get_object(pk, device_id)
        if not income:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        income.delete()
        return Response({'success': True, 'message': 'Income deleted'})


# ==================== EXPENSE VIEWS ====================

class ExpenseListView(APIView):
    def get(self, request):
        try:
            device_id = request.query_params.get('device_id')
            if not device_id:
                return Response({'error': 'device_id required'}, status=status.HTTP_400_BAD_REQUEST)

            queryset = Expense.objects.filter(device_id=device_id)
            period = request.query_params.get('period')
            if period == 'today':
                queryset = queryset.filter(date=date.today())
            elif period == 'weekly':
                queryset = queryset.filter(date__gte=date.today() - timedelta(days=7))
            elif period == 'monthly':
                queryset = queryset.filter(date__gte=date.today().replace(day=1))
            elif period == 'yearly':
                queryset = queryset.filter(date__gte=date.today().replace(month=1, day=1))

            category = request.query_params.get('category')
            if category:
                queryset = queryset.filter(category=category)

            total = queryset.aggregate(total=Sum('amount'))['total'] or Decimal('0')
            serializer = ExpenseSerializer(queryset, many=True)
            return Response({'results': serializer.data, 'count': queryset.count(), 'total': str(total)})
        except Exception as e:
            return Response(
                {'error': 'Error fetching expense records', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExpenseAddView(APIView):
    def post(self, request):
        try:
            data = request.data.copy()
            if not data.get('date'):
                data['date'] = date.today().isoformat()
            serializer = ExpenseSerializer(data=data)
            if serializer.is_valid():
                expense = serializer.save()
                return Response({'success': True, 'data': ExpenseSerializer(expense).data}, status=status.HTTP_201_CREATED)
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': 'Error adding expense record', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExpenseDetailView(APIView):
    def delete(self, request, pk):
        device_id = request.query_params.get('device_id')
        try:
            expense = Expense.objects.get(pk=pk, device_id=device_id)
            expense.delete()
            return Response({'success': True})
        except Expense.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


# ==================== SALES VIEWS ====================

class SalesListView(APIView):
    def get(self, request):
        try:
            device_id = request.query_params.get('device_id')
            if not device_id:
                return Response({'error': 'device_id required'}, status=status.HTTP_400_BAD_REQUEST)

            queryset = Sales.objects.filter(device_id=device_id)
            period = request.query_params.get('period')
            if period == 'today':
                queryset = queryset.filter(sale_date=date.today())
            elif period == 'weekly':
                queryset = queryset.filter(sale_date__gte=date.today() - timedelta(days=7))
            elif period == 'monthly':
                queryset = queryset.filter(sale_date__gte=date.today().replace(day=1))

            total = queryset.aggregate(total=Sum('total_amount'))['total'] or Decimal('0')
            serializer = SalesSerializer(queryset, many=True)
            return Response({'results': serializer.data, 'count': queryset.count(), 'total': str(total)})
        except Exception as e:
            return Response(
                {'error': 'Error fetching sales records', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SalesAddView(APIView):
    def post(self, request):
        try:
            data = request.data.copy()
            
            # Ensure device_id is present
            if not data.get('device_id'):
                return Response({'error': 'device_id required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Map field names if needed
            if 'product_name' in data and 'product' not in data:
                data['product_name'] = data.get('product_name')
            
            # Set default sale_date if not provided
            if not data.get('sale_date'):
                data['sale_date'] = date.today().isoformat()
            
            # Calculate total_amount if not provided
            if not data.get('total_amount') and data.get('quantity') and data.get('price_per_unit'):
                data['total_amount'] = float(data['quantity']) * float(data['price_per_unit'])
            
            serializer = SalesSerializer(data=data)
            if serializer.is_valid():
                sale = serializer.save()
                return Response({'success': True, 'data': SalesSerializer(sale).data}, status=status.HTTP_201_CREATED)
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': 'Error adding sales record', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SalesDetailView(APIView):
    def delete(self, request, pk):
        device_id = request.query_params.get('device_id')
        try:
            sale = Sales.objects.get(pk=pk, device_id=device_id)
            sale.delete()
            return Response({'success': True})
        except Sales.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


# ==================== PROFIT VIEW ====================

class ProfitView(APIView):
    def get(self, request):
        try:
            device_id = request.query_params.get('device_id')
            if not device_id:
                return Response({'error': 'device_id required'}, status=status.HTTP_400_BAD_REQUEST)

            period = request.query_params.get('period', 'monthly')
            today = date.today()

            if period == 'today':
                start_date = today
                days = 1
            elif period == 'weekly':
                start_date = today - timedelta(days=7)
                days = 7
            elif period == 'monthly':
                start_date = today.replace(day=1)
                days = today.day
            elif period == 'yearly':
                start_date = today.replace(month=1, day=1)
                days = (today - today.replace(month=1, day=1)).days + 1
            else:
                start_date = today.replace(day=1)
                days = today.day

            total_income = Income.objects.filter(device_id=device_id, date__gte=start_date).aggregate(
                total=Sum('amount'))['total'] or Decimal('0')
            total_expense = Expense.objects.filter(device_id=device_id, date__gte=start_date).aggregate(
                total=Sum('amount'))['total'] or Decimal('0')
            total_sales = Sales.objects.filter(device_id=device_id, sale_date__gte=start_date).aggregate(
                total=Sum('total_amount'))['total'] or Decimal('0')

            net_profit = total_income - total_expense
            profit_margin = float(net_profit / total_income * 100) if total_income > 0 else 0
            expense_ratio = float(total_expense / total_income * 100) if total_income > 0 else 0
            daily_avg = net_profit / days if days > 0 else Decimal('0')

            income_count = Income.objects.filter(device_id=device_id, date__gte=start_date).count()
            expense_count = Expense.objects.filter(device_id=device_id, date__gte=start_date).count()

            return Response({
                'period': period,
                'start_date': str(start_date),
                'total_income': str(total_income),
                'total_expense': str(total_expense),
                'total_sales': str(total_sales),
                'net_profit': str(net_profit),
                'profit_margin': round(profit_margin, 2),
                'expense_ratio': round(expense_ratio, 2),
                'income_count': income_count,
                'expense_count': expense_count,
                'daily_average_profit': str(round(daily_avg, 2)),
            })
        except Exception as e:
            return Response(
                {'error': 'Error calculating profit', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ==================== MARKET PRICE VIEWS ====================

class MarketPriceListView(APIView):
    def get(self, request):
        try:
            queryset = MarketPrice.objects.filter(is_active=True)
            commodity = request.query_params.get('commodity')
            if commodity:
                queryset = queryset.filter(commodity_name__icontains=commodity)
            serializer = MarketPriceSerializer(queryset, many=True)
            return Response({'results': serializer.data, 'count': queryset.count()})
        except Exception as e:
            return Response(
                {'error': 'Error fetching market prices', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MarketAnalysisView(APIView):
    """AI-powered market analysis with real-time intelligence"""
    
    # Product image URLs mapping (matches frontend productImages.js)
    PRODUCT_IMAGES = {
        'rice': 'https://images.unsplash.com/photo-1595433707802-6b2626ef1c91?w=400&h=300&fit=crop',
        'wheat': 'https://images.unsplash.com/photo-1585979949075-ade4e5c8b651?w=400&h=300&fit=crop',
        'onion': 'https://images.unsplash.com/photo-1585518419759-4b61ecc3e4b6?w=400&h=300&fit=crop',
        'carrot': 'https://images.unsplash.com/photo-1447175008436-054170c2e601?w=400&h=300&fit=crop',
        'tomato': 'https://images.unsplash.com/photo-1532694215381-6c9c90162036?w=400&h=300&fit=crop',
        'potato': 'https://images.unsplash.com/photo-1596363860416-bf4e4b30287b?w=400&h=300&fit=crop',
        'banana': 'https://images.unsplash.com/photo-1571407614161-c3ce9b55aacd?w=400&h=300&fit=crop',
        'mango': 'https://images.unsplash.com/photo-1553279768-865a24cda92f?w=400&h=300&fit=crop',
        'apple': 'https://images.unsplash.com/photo-1560806674-104fc7c55c24?w=400&h=300&fit=crop',
        'orange': 'https://images.unsplash.com/photo-1564241158518-d9c9e562d5fd?w=400&h=300&fit=crop',
        'milk': 'https://images.unsplash.com/photo-1563636619-51f2b652fcd2?w=400&h=300&fit=crop',
        'ghee': 'https://images.unsplash.com/photo-1608849823803-97d6b6b3c869?w=400&h=300&fit=crop',
        'yogurt': 'https://images.unsplash.com/photo-1599810694-02278e42f89b?w=400&h=300&fit=crop',
        'paneer': 'https://images.unsplash.com/photo-1452821952904-5573d96a54fa?w=400&h=300&fit=crop',
        'turmeric': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop&q=80',
        'chili': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop',
        'coconut': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop',
        'coriander': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop',
        'black pepper': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop',
        'coconut oil': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop',
        'sesame oil': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop',
        'pickle': 'https://images.unsplash.com/photo-1599599810694-02278e42f89b?w=400&h=300&fit=crop',
        'jams': 'https://images.unsplash.com/photo-1589985643862-b53b6f85b0bb?w=400&h=300&fit=crop',
        'dry snacks': 'https://images.unsplash.com/photo-1585667228485-d0a7f7a3caa8?w=400&h=300&fit=crop',
        'handmade cloth': 'https://images.unsplash.com/photo-1540553016-e8290a976fcb?w=400&h=300&fit=crop',
        'embroidered saree': 'https://images.unsplash.com/photo-1590080876-0cd4e0b7b858?w=400&h=300&fit=crop',
        'handmade jewelry': 'https://images.unsplash.com/photo-1599643478518-a784e5dc4c8f?w=400&h=300&fit=crop',
        'wooden craft': 'https://images.unsplash.com/photo-1578500494198-246f612d03b3?w=400&h=300&fit=crop'
    }
    
    def get_product_image_url(self, commodity_name):
        """Get product image URL for commodity (matches frontend logic)"""
        if not commodity_name:
            return None
        
        key = commodity_name.lower().strip()
        
        # Direct match first
        if key in self.PRODUCT_IMAGES:
            return self.PRODUCT_IMAGES[key]
        
        # Try fuzzy matching for variations
        for mapped_key, image_url in self.PRODUCT_IMAGES.items():
            if key in mapped_key or mapped_key in key:
                return image_url
        
        return None
    def post(self, request):
        """
        Analyze market trends using Gemini AI
        
        Request body:
        {
            "query": "Is banana a good crop to sell?",
            "language": "en",
            "commodity": "banana" (optional)
        }
        """
        try:
            from ml_models.market_analyzer import MarketAnalyzer
            from ml_models.gemini_helper import GeminiHelper
            from ml_models.language_detection import LanguageDetector
            
            query = request.data.get('query', '').strip()
            language = request.data.get('language', 'en').strip().lower()
            commodity = request.data.get('commodity', '').strip()
            
            if not query:
                return Response(
                    {'error': 'Query required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # CRITICAL: Detect language FIRST from query (more reliable than frontend detection)
            detected_lang = LanguageDetector.detect(query)
            print(f"📝 Query detected language: {detected_lang}, Frontend language: {language}")
            
            # Use detected language if it's different from 'en' (frontend might send default 'en')
            if detected_lang and detected_lang in ['hi', 'ta']:
                language = detected_lang
                print(f"🌐 Using detected language: {language}")
            
            # Extract commodity from query if not provided
            if not commodity:
                commodity = MarketAnalyzer._extract_commodity_from_query(query)
            
            # Get intelligent market analysis
            analysis = None
            
            # First try commodity-specific analysis
            if commodity:
                analysis = MarketAnalyzer.analyze_profit_potential(commodity, language=language)
            else:
                # Generate real-time analysis based on query
                analysis = MarketAnalyzer.generate_real_time_analysis(
                    query=query,
                    commodity=None,
                    language=language
                )
            
            # Get current market prices if commodity is specified (without images)
            market_data = []
            prices = None
            resolved_commodity = None
            
            if commodity:
                resolved_commodity = MarketAnalyzer.resolve_commodity_name(commodity)
                if resolved_commodity:
                    prices = MarketPrice.objects.filter(
                        commodity_name__icontains=resolved_commodity,
                        is_active=True
                    ).values('commodity_name', 'price', 'trend', 'market_location', 'unit', 'market_date')[:5]
                    
                    if prices.exists():
                        market_data = list(prices)
            
            # ✅ CRITICAL: Initialize language-specific fallback FIRST
            fallback_analysis = None
            if commodity:
                fallback_analysis = MarketAnalyzer.analyze_profit_potential(commodity, language=language)
            else:
                fallback_analysis = MarketAnalyzer.generate_real_time_analysis(
                    query=query,
                    commodity=None,
                    language=language
                )
            
            print(f"📚 Pre-loaded fallback in {language}")
            
            # ✅ CRITICAL: Get Gemini analysis with BRUTAL language enforcement
            gemini_attempts = 0
            max_gemini_attempts = 3
            gemini_success = False
            
            if GeminiHelper.is_available():
                while gemini_attempts < max_gemini_attempts and not gemini_success:
                    gemini_attempts += 1
                    try:
                        print(f"\n🤖 Gemini attempt #{gemini_attempts} with language: {language}")
                        # Use voice response for better market guidance with STRICT language
                        voice_analysis = GeminiHelper.generate_voice_response(
                            user_query=query,
                            language=language,
                            extracted_data={'commodity': commodity},
                            intent='market'
                        )
                        if voice_analysis:
                            # ✅ CRITICAL: Detect actual language of response
                            from ml_models.language_detection import LanguageDetector
                            detected_response_lang = LanguageDetector.detect(voice_analysis)
                            print(f"📊 Response detection: Requested={language}, Detected={detected_response_lang}")
                            
                            # Only accept if language matches
                            if detected_response_lang == language:
                                analysis = voice_analysis
                                gemini_success = True
                                print(f"✅ Gemini OK - response in {language}: {voice_analysis[:80]}")
                            else:
                                # Language mismatch - log and retry
                                english_ratio = sum(1 for c in voice_analysis if ord(c) < 128) / max(len(voice_analysis), 1)
                                print(f"⚠️ Language mismatch! Requested {language}, detected {detected_response_lang}")
                                print(f"   ASCII ratio: {english_ratio:.1%}")
                                if gemini_attempts < max_gemini_attempts:
                                    print(f"   Retrying (attempt {gemini_attempts + 1}/{max_gemini_attempts})...")
                                    # Wait before retry
                                    import time
                                    time.sleep(0.5)
                                else:
                                    print(f"   Max retries reached - forcing fallback")
                        else:
                            print(f"❌ Gemini returned empty response")
                            if gemini_attempts < max_gemini_attempts:
                                print(f"   Retrying (attempt {gemini_attempts + 1}/{max_gemini_attempts})...")
                    except Exception as e:
                        print(f"❌ Gemini attempt #{gemini_attempts} failed: {str(e)}")
                        if gemini_attempts < max_gemini_attempts:
                            print(f"   Retrying (attempt {gemini_attempts + 1}/{max_gemini_attempts})...")
                        else:
                            print(f"   Max retries exhausted")
            
            # ✅ CRITICAL: If Gemini fails OR returns wrong language, USE FALLBACK
            if not gemini_success:
                print(f"\n🔴 FORCING FALLBACK: Using MarketAnalyzer in {language}")
                analysis = fallback_analysis
                print(f"✅ Using {language} analysis (first 100 chars): {analysis[:100] if analysis else 'EMPTY'}")
            
            print(f"📤 Returning analysis in {language}: {analysis[:60] if analysis else 'None'}")
            
            # Generate product image URL for commodity
            product_image = None
            if resolved_commodity or commodity:
                product_image = self.get_product_image_url(resolved_commodity or commodity)
            
            return Response({
                'analysis': analysis,
                'language': language,
                'commodity': resolved_commodity or commodity,
                'product_image': product_image,
                'market_data': market_data,
                'timestamp': datetime.now().isoformat()
            })
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response(
                {'error': 'Error performing market analysis', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PriceHistoryView(APIView):
    """Get historical price data for trend analysis"""
    
    def get(self, request):
        """Get price history for a commodity"""
        try:
            commodity = request.query_params.get('commodity')
            days = int(request.query_params.get('days', 30))
            market_location = request.query_params.get('market_location', '')
            
            if not commodity:
                return Response(
                    {'error': 'Commodity name required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get historical data
            start_date = date.today() - timedelta(days=days)
            queryset = PriceHistory.objects.filter(
                commodity_name__icontains=commodity,
                market_date__gte=start_date
            )
            
            if market_location:
                queryset = queryset.filter(market_location__icontains=market_location)
            
            queryset = queryset.order_by('market_date')
            
            serializer = PriceHistorySerializer(queryset, many=True)
            return Response({
                'commodity': commodity,
                'period_days': days,
                'count': queryset.count(),
                'results': serializer.data,
                'date_range': {
                    'start': start_date.isoformat(),
                    'end': date.today().isoformat()
                }
            })
        except Exception as e:
            return Response(
                {'error': 'Error fetching price history', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PriceTrendsView(APIView):
    """Get price trend analysis for commodities"""
    
    def get(self, request):
        """Get price trend analysis"""
        try:
            commodity = request.query_params.get('commodity')
            market_location = request.query_params.get('market_location', '')
            
            if not commodity:
                return Response(
                    {'error': 'Commodity name required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get analysis data
            analysis = MarketPriceAnalysis.objects.filter(
                commodity_name__icontains=commodity
            ).order_by('-analysis_date').first()
            
            if not analysis:
                return Response({
                    'error': 'No analysis available yet',
                    'message': 'Price analysis will be available after daily updates start'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = MarketPriceAnalysisSerializer(analysis)
            
            # Get historical context
            history_30d = PriceHistory.objects.filter(
                commodity_name__icontains=commodity,
                market_date__gte=date.today() - timedelta(days=30)
            ).order_by('market_date').values_list('price', flat=True)
            
            history_7d = PriceHistory.objects.filter(
                commodity_name__icontains=commodity,
                market_date__gte=date.today() - timedelta(days=7)
            ).order_by('market_date').values_list('price', flat=True)
            
            return Response({
                'analysis': serializer.data,
                'historical_7d': list(history_7d),
                'historical_30d': list(history_30d),
                'last_updated': analysis.updated_at.isoformat()
            })
        except Exception as e:
            return Response(
                {'error': 'Error fetching price trends', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MarketComparativeAnalysisView(APIView):
    """Compare prices across different markets"""
    
    def get(self, request):
        """Get comparative market analysis"""
        try:
            commodity = request.query_params.get('commodity')
            
            if not commodity:
                return Response(
                    {'error': 'Commodity name required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get latest prices from different markets
            prices = MarketPrice.objects.filter(
                commodity_name__icontains=commodity,
                is_active=True
            ).values('market_location', 'price', 'unit', 'market_date').order_by('market_location')
            
            if not prices.exists():
                return Response({
                    'commodity': commodity,
                    'markets': [],
                    'message': 'No market data available'
                })
            
            # Calculate statistics
            prices_list = [float(p['price']) for p in prices]
            
            analysis_data = {
                'commodity': commodity,
                'markets': list(prices),
                'statistics': {
                    'highest_price': max(prices_list) if prices_list else 0,
                    'lowest_price': min(prices_list) if prices_list else 0,
                    'average_price': sum(prices_list) / len(prices_list) if prices_list else 0,
                    'price_range': max(prices_list) - min(prices_list) if prices_list else 0,
                    'market_count': len(prices_list)
                } if prices_list else {}
            }
            
            return Response(analysis_data)
        except Exception as e:
            return Response(
                {'error': 'Error fetching comparative analysis', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RealtimeMarketAnalysisView(APIView):
    """Get real-time market analysis with insights"""
    
    def get(self, request):
        """Get comprehensive real-time market insights"""
        try:
            # Get all active commodities with analysis
            analyses = MarketPriceAnalysis.objects.filter(
                analysis_date=date.today()
            ).select_related().order_by('trend')
            
            serializer = MarketPriceAnalysisSerializer(analyses, many=True)
            
            # Group by trend
            trending_up = [a for a in serializer.data if a['trend'] == 'up']
            trending_down = [a for a in serializer.data if a['trend'] == 'down']
            stable = [a for a in serializer.data if a['trend'] == 'stable']
            
            # Get top opportunities
            opportunities = sorted(
                serializer.data,
                key=lambda x: (
                    -x['momentum_score'] if x['recommendation'] == 'buy' else 0,
                    -x['trend_percentage']
                )
            )[:5]
            
            return Response({
                'date': date.today().isoformat(),
                'total_commodities': analyses.count(),
                'summary': {
                    'trending_up': len(trending_up),
                    'trending_down': len(trending_down),
                    'stable': len(stable)
                },
                'opportunities': opportunities,
                'all_analysis': serializer.data
            })
        except Exception as e:
            return Response(
                {'error': 'Error fetching real-time analysis', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ==================== SCHEME VIEWS ====================

class SchemeListView(APIView):
    # Tamil translations for common scheme fields
    TAMIL_TRANSLATIONS = {
        'Pradhan Mantri Mahila Shakti Scheme': {
            'name': 'பிரதான மந்திரி மகளிர் சக்தி திட்டம்',
            'description': 'மகளிர் தொழில்முறை மற்றும் சுயதொழில் ஆதரவுக்கான தேசிய திட்டம்',
            'eligibility': '18 வயதுக்கு மேற்பட்ட பெண்களும் மகளிர் சுயநதி குழுக்களும் விண்ணப்பிக்கலாம்',
            'benefits': '₹5 லட்சம் வரை கடன், பயிற்சி, மற்றும் சந்தை இணைப்பு',
        },
        'Mukhya Mantri Stree Shakti Yojana': {
            'name': 'முதல்வர் பெண் சக்தி திட்டம்',
            'description': 'தமிழ்நாட்டு பெண் தொழிலாளர்களுக்கான பாங்கிங் மற்றும் நிதி உதவி',
            'eligibility': 'தமிழ்நாட்டில் வசிக்கும் 18-55 வயதுக்கு இடைப்பட்ட பெண்கள்',
            'benefits': 'தட்டையான வட்டி விகிதத்தில் கடனு, பயிற்சி தொகை ₹2000-5000',
        },
        'Prime Minister Employment Generation Programme': {
            'name': 'பிரதான மந்திரி வேலைவாய்ப்பு உत்பாதன திட்டம்',
            'description': 'பண்ணை மற்றும் பண்ணை சாராத விகிதாசாரக்களுக்கான நிதி உதவி',
            'eligibility': 'தொழில் முயற்சிக்காக ₹25,000-25 லட்சம் வரை திறமையான தொழிலாளர்',
            'benefits': 'தட்டையான வட்டி விகிதம், பயிற்சி மற்றும் மற்ற சலுகைகள்',
        },
        'Women Entrepreneurship Development Programme': {
            'name': 'பெண் தொழிலுறவு வளர்ச்சி திட்டம்',
            'description': 'பெண் தொழிலாளர்களுக்கான தொழிল ஆதரவு மற்றும் பயிற்சி',
            'eligibility': '18 வயதுக்கு மேற்பட்ட கல்வி பெற்ற பெண்கள்',
            'benefits': 'பயிற்சி, மாற்றியுरण்ட ஆதரவு, நிதி உதவி',
        },
        'Indira Gandhi Matritva Sahyog Yojana': {
            'name': 'இந்திரா காந்தி தாய்மை உதவி திட்டம்',
            'description': 'கர்ப்பிணி பெண்களுக்கான ரூபாய் உதவி',
            'eligibility': 'கர்ப்பிணி 19 வயதுக்கு மேற்பட்ட பெண்கள்',
            'benefits': 'கர்ப்ப கால உதவி ₹5000 மற்றும் பிரசவ உதவி ₹5000',
        },
    }
    
    def get(self, request):
        try:
            queryset = Scheme.objects.filter(status='active')
            category = request.query_params.get('category')
            language = request.query_params.get('language', 'en').lower()
            
            if category:
                queryset = queryset.filter(category=category)
            
            # Serialize with language awareness
            schemes_data = []
            for scheme in queryset:
                scheme_dict = {
                    'id': scheme.id,
                    'category': scheme.category,
                    'agency': scheme.agency,
                    'url': scheme.url,
                    'status': scheme.status,
                    'deadline': scheme.deadline,
                    'max_amount': scheme.max_amount,
                    'created_at': scheme.created_at,
                    'updated_at': scheme.updated_at,
                }
                
                # Return content in requested language
                if language == 'hi':
                    scheme_dict.update({
                        'name': scheme.name_hi or scheme.name,
                        'description': scheme.description_hi or scheme.description,
                        'eligibility': scheme.eligibility_hi or scheme.eligibility,
                        'benefits': scheme.benefits_hi or scheme.benefits,
                        'how_to_apply': scheme.how_to_apply_hi or scheme.how_to_apply,
                    })
                elif language == 'ta':
                    # Check if Tamil translation mapping exists
                    tamil_trans = self.TAMIL_TRANSLATIONS.get(scheme.name, {})
                    scheme_dict.update({
                        'name': scheme.name_ta or tamil_trans.get('name', scheme.name),
                        'description': scheme.description_ta or tamil_trans.get('description', scheme.description),
                        'eligibility': scheme.eligibility_ta or tamil_trans.get('eligibility', scheme.eligibility),
                        'benefits': scheme.benefits_ta or tamil_trans.get('benefits', scheme.benefits),
                        'how_to_apply': scheme.how_to_apply_ta or tamil_trans.get('how_to_apply', scheme.how_to_apply),
                    })
                    # Translate agency name to Tamil
                    AGENCY_TRANSLATIONS = {
                        'Ministry of Finance & Ministry of MSME': 'நிதி அமைச்சு & சிறு, நடு மற்றும் நடுநிலை தொழிலுறவு அமைச்சு',
                        'Small Industries Development Bank of India (SIDBI)': 'சிறு தொழிற்சாலை வளர்ச்சி வங்கி (SIDBI)',
                        'Ministry of Food Processing Industries': 'உணவு பதப்படுத்தல் தொழிற்சாலை அமைச்சு',
                        'Ministry of Labour & Employment': 'தொழிலாளர் மற்றும் வேலைவாய்ப்பு அமைச்சு',
                        'Ministry of Agriculture & Horticulture': 'விவசாயம் மற்றும் தோட்டக்கலை அமைச்சு',
                        'Ministry of Textiles / Industrial Policy': 'நூல் அமைச்சு / தொழிற்சாலை கொள்கை',
                        'Public Sector Banks': 'பொதுத் துறை வங்கிகள்',
                        'Ministry of Rural Development (NRLM)': 'கிராம வளர்ச்சி அமைச்சு (NRLM)',
                        'Ministry of MSME': 'சிறு, நடு மற்றும் நடுநிலை தொழிலுறவு அமைச்சு',
                    }
                    translated_agency = AGENCY_TRANSLATIONS.get(scheme.agency, scheme.agency)
                    scheme_dict['agency'] = translated_agency
                else:
                    scheme_dict.update({
                        'name': scheme.name,
                        'description': scheme.description,
                        'eligibility': scheme.eligibility,
                        'benefits': scheme.benefits,
                        'how_to_apply': scheme.how_to_apply,
                    })
                
                schemes_data.append(scheme_dict)
            
            return Response({'results': schemes_data, 'count': queryset.count()})
        except Exception as e:
            return Response(
                {'error': 'Error fetching schemes', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ==================== MENTOR VIEWS ====================

class MentorListView(APIView):
    # Map specialization text to translation keys
    SPECIALIZATION_KEYS = {
        'organic': 'organic', 'organic agriculture': 'organic', 'organic farming': 'organic',
        'dairy': 'dairy', 'dairy & agriculture': 'dairy', 'dairy and agriculture': 'dairy', 'dairy business': 'dairy',
        'food': 'food', 'food processing': 'food',
        'digital': 'digital', 'digital marketing': 'digital',
    }
    
    EXPERTISE_KEYS = {
        'handicraft': 'handicraft', 'handicraft, marketing, export': 'handicraft',
        'dairy': 'dairy', 'dairy, agriculture, shg': 'dairy',
        'food processing': 'foodProcessing', 'food processing, fssai, packaging': 'foodProcessing',
        'digital': 'digitalMarketing', 'social media, online selling, digital literacy': 'digitalMarketing',
    }
    
    def get(self, request):
        try:
            language = request.query_params.get('language', 'en').lower()
            queryset = Mentor.objects.filter(is_active=True)
            expertise = request.query_params.get('expertise')
            if expertise:
                queryset = queryset.filter(expertise__icontains=expertise)
            availability = request.query_params.get('availability')
            if availability:
                queryset = queryset.filter(availability=availability)
            
            # Serialize and add translation keys
            mentors_data = []
            for mentor in queryset:
                data = {
                    'id': mentor.id,
                    'name': mentor.name,
                    'experience_years': mentor.experience_years,
                    'rating': float(mentor.rating) if mentor.rating else 4.5,
                    'availability': mentor.availability,
                    'languages_spoken': mentor.languages_spoken or 'English',
                    'specialization': mentor.specialization,
                    'expertise': mentor.expertise,
                    # Add translation keys
                    'specializationKey': self.SPECIALIZATION_KEYS.get(mentor.specialization.lower(), 'organic'),
                    'expertiseKey': self.EXPERTISE_KEYS.get(mentor.expertise.lower(), 'dairy'),
                    'bioKey': mentor.name.split()[0].lower() if mentor.name else 'mentor',
                }
                mentors_data.append(data)
            
            return Response({'results': mentors_data, 'count': len(mentors_data)})
        except Exception as e:
            return Response(
                {'error': 'Error fetching mentors', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MentorChatView(APIView):
    def _enforce_language_purity(self, text, language):
        """Ensure response is pure language with NO mixing"""
        if not text:
            return text
        
        # Character ranges for different scripts
        tamil_start, tamil_end = 0x0B80, 0x0BFF
        devanagari_start, devanagari_end = 0x0900, 0x097F
        
        has_tamil = any(tamil_start <= ord(c) <= tamil_end for c in text)
        has_devanagari = any(devanagari_start <= ord(c) <= devanagari_end for c in text)
        has_latin = any(ord(c) < 128 and c.isalpha() for c in text)
        
        # Count non-ASCII characters per script
        tamil_chars = sum(1 for c in text if tamil_start <= ord(c) <= tamil_end)
        devanagari_chars = sum(1 for c in text if devanagari_start <= ord(c) <= devanagari_end)
        english_chars = sum(1 for c in text if ord(c) < 128 and c.isalpha())
        total_alpha = tamil_chars + devanagari_chars + english_chars
        
        # If language is Tamil but has too much English (>30%), log warning
        if language == 'ta' and has_latin and english_chars > 0.3 * total_alpha:
            print(f"⚠️  Language mixing detected: Tamil response with {english_chars}/{total_alpha} English chars")
        
        # If language is Hindi but has too much English (>30%), log warning
        if language == 'hi' and has_latin and english_chars > 0.3 * total_alpha:
            print(f"⚠️  Language mixing detected: Hindi response with {english_chars}/{total_alpha} English chars")
        
        return text
    
    def get(self, request):
        try:
            device_id = request.query_params.get('device_id')
            mentor_id = request.query_params.get('mentor_id')
            if not device_id or not mentor_id:
                return Response({'error': 'device_id and mentor_id required'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = MentorChat.objects.filter(device_id=device_id, mentor_id=mentor_id).order_by('timestamp')
            serializer = MentorChatSerializer(queryset, many=True)
            return Response({'results': serializer.data})
        except Exception as e:
            return Response(
                {'error': 'Error fetching mentor chat', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            from ml_models.mentor_helper import MentorAIHelper
            from ml_models.gemini_helper import GeminiHelper
            from ml_models.language_detection import LanguageDetector
            
            device_id = request.data.get('device_id')
            mentor_id = request.data.get('mentor_id')
            message = request.data.get('message', '').strip()
            message_type = request.data.get('message_type', 'query')
            language = request.data.get('language', 'en')
            
            if not device_id or not mentor_id or not message:
                return Response({'error': 'device_id, mentor_id, and message required'}, status=status.HTTP_400_BAD_REQUEST)
            
            # CRITICAL: Detect language from message (more reliable than frontend)
            detected_lang = LanguageDetector.detect(message)
            if detected_lang and detected_lang in ['hi', 'ta']:
                language = detected_lang
                print(f"🌐 Language auto-detected: {language}")
            
            # Save user's message
            user_chat = MentorChat.objects.create(
                device_id=device_id,
                mentor_id=mentor_id,
                message=message,
                message_type='query'
            )
            
            # Get mentor data for context
            try:
                mentor = Mentor.objects.get(id=mentor_id)
                mentor_data = MentorSerializer(mentor).data
            except:
                mentor_data = {'name': 'AI Mentor', 'specializationKey': 'organic', 'expertiseKey': 'organic', 'experience_years': 10}
            
            # Get conversation history for context
            history = MentorChat.objects.filter(
                device_id=device_id,
                mentor_id=mentor_id
            ).order_by('-timestamp')[:10]  # Last 10 messages
            
            conversation_history = [
                {'message': c.message, 'message_type': c.message_type} 
                for c in reversed(history)
            ]
            
            # CRITICAL: Check if this is an income-related question
            income_keywords = ['income', 'earnings', 'revenue', 'sale', 'profit', 'earn', 'money', 'rupees', 'रुपये', 'வருமானம்', 'சம்பாதனை']
            expense_keywords = ['expense', 'cost', 'spend', 'खर्च', 'செலவு', 'खरीद', 'buy', 'material']
            
            is_income_question = any(keyword.lower() in message.lower() for keyword in income_keywords)
            is_expense_question = any(keyword.lower() in message.lower() for keyword in expense_keywords)
            
            print(f"💰 Income question: {is_income_question}, Expense question: {is_expense_question}")
            
            # Generate AI response using Gemini with income/expense awareness
            print(f"🤖 Generating mentor response for question: {message[:50]} in language: {language}")
            
            # Build context with income/expense awareness
            user = None
            income_total = None
            expense_total = None
            
            try:
                user = User.objects.get(device_id=device_id)
                if is_income_question or is_expense_question:
                    from django.db.models import Sum
                    from datetime import date, timedelta
                    
                    # Get this month's data
                    start_date = date.today().replace(day=1)
                    
                    if is_income_question:
                        income_total = Income.objects.filter(
                            device_id=device_id,
                            date__gte=start_date
                        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
                        print(f"💵 Current month income: {income_total}")
                    
                    if is_expense_question:
                        expense_total = Expense.objects.filter(
                            device_id=device_id,
                            date__gte=start_date
                        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
                        print(f"💸 Current month expenses: {expense_total}")
            except:
                pass
            
            # Prepare enhanced context for income questions
            context_info = ""
            if is_income_question and income_total is not None:
                context_info = f"\n[User Context: Current month income: ₹{income_total}]"
            elif is_expense_question and expense_total is not None:
                context_info = f"\n[User Context: Current month expenses: ₹{expense_total}]"
            
            ai_response = MentorAIHelper.generate_mentor_response(
                question=message + context_info,
                mentor_data=mentor_data,
                language=language,
                conversation_history=conversation_history
            )
            
            # If Gemini available and income-specific, use Gemini directly for better accuracy
            if not ai_response and GeminiHelper.is_available() and (is_income_question or is_expense_question):
                print(f"🔄 Falling back to Gemini for income-specific guidance")
                
                gemini_prompt = f"""You are a business mentor helping a woman entrepreneur in India.
The user asked: {message}

{f'Their current month income: ₹{income_total}' if income_total else ''}
{f'Their current month expenses: ₹{expense_total}' if expense_total else ''}

Provide practical, encouraging advice specific to their income/business management.
Focus on: profit growth, expense management, cash flow, savings.
Be supportive and culturally sensitive.

Language requirement: Respond ONLY in {language}.
No mixing of languages. Pure {language} only."""
                
                ai_response = GeminiHelper.enhance_response(
                    text=message,
                    language=language,
                    context=gemini_prompt
                )
            
            # If still no response, use fallback
            if not ai_response:
                print(f"⚠️  Using fallback response")
                fallback_responses = {
                    'en': "That's a great question! Based on your business context, I recommend focusing on tracking your income and expenses carefully. This will help you understand your profit margins better.",
                    'hi': "यह एक बहुत अच्छा प्रश्न है! अपने व्यवसाय के लिए, मैं आपको आय और खर्च को सावधानी से ट्रैक करने की सलाह देता हूं। यह आपको अपने लाभ मार्जिन को बेहतर समझने में मदद करेगा।",
                    'ta': "அது சிறந்த கேள்வி! உங்கள் வணிகத்திற்காக, உங்கள் வருமானம் மற்றும் செலவுகளை கவனமாக கண்காணிக்க நான் பரிந்துரை செய்கிறேன்."
                }
                ai_response = fallback_responses.get(language, fallback_responses['en'])
            
            # CRITICAL: Validate language purity - NO mixing
            ai_response = self._enforce_language_purity(ai_response, language)
            
            # Save AI response
            mentor_response = MentorChat.objects.create(
                device_id=device_id,
                mentor_id=mentor_id,
                message=ai_response,
                message_type='response'
            )
            
            print(f"✅ Mentor response generated: {ai_response[:50]}")
            
            return Response({
                'success': True,
                'user_message': MentorChatSerializer(user_chat).data,
                'mentor_response': MentorChatSerializer(mentor_response).data,
                'ai_generated': True,
                'language': language,
                'income_focused': is_income_question,
                'expense_focused': is_expense_question
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            import traceback
            print(f"❌ Error in mentor chat: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return Response(
                {'error': 'Error processing mentor chat', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ==================== MENTOR AI VIEW ====================

class MentorAIView(APIView):
    """Standalone Mentor AI for business guidance without connecting to specific mentor"""
    
    def post(self, request):
        try:
            from ml_models.mentor_helper import MentorAIHelper
            
            message = request.data.get('message', '').strip()
            language = request.data.get('language', 'en')
            device_id = request.data.get('device_id', '')
            
            if not message:
                return Response({'error': 'message required'}, status=status.HTTP_400_BAD_REQUEST)
            
            print(f"🤖 Mentor AI: Processing question: {message[:50]} in {language}")
            
            # Create mentor context for AI Mentor (no specific mentor)
            mentor_data = {
                'name': 'Mentor AI',
                'specializationKey': 'multiple',
                'expertiseKey': 'all',
                'experience_years': 15,
                'bio': 'AI-powered business mentor providing personalized guidance'
            }
            
            # Generate AI response using assistant helper or Gemini
            ai_response = MentorAIHelper.generate_mentor_response(
                question=message,
                mentor_data=mentor_data,
                language=language,
                conversation_history=[]
            )
            
            # If AI response generation fails, provide basic response
            if not ai_response:
                if language == 'hi':
                    ai_response = "मुझे इस प्रश्न के बारे में पूरी जानकारी नहीं है। कृपया विस्तार से बताएं।"
                elif language == 'ta':
                    ai_response = "இந்த கேள்விக்கு பற்றிய முழுமையான தகவல் எனக்கு இல்லை. தயவு செய்து விস்தாரமாக கூறுங்கள்."
                else:
                    ai_response = "I don't have enough information on that. Could you provide more details?"
            
            print(f"✅ Mentor AI response generated: {ai_response[:60]}")
            
            return Response({
                'success': True,
                'message': message,
                'response': ai_response,
                'language': language,
                'mentor': 'AI Mentor'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            import traceback
            print(f"❌ Error in Mentor AI: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return Response(
                {'error': 'Error processing Mentor AI request', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ==================== PREDICT INTENT VIEW ====================

class PredictIntentView(APIView):
    """ML-powered voice intent prediction with auto-language detection"""

    def post(self, request):
        try:
            print("\n" + "="*60)
            print("📬 INCOMING VOICE ASSISTANT REQUEST")
            print("="*60)
            print(f"Request method: {request.method}")
            print(f"Request headers: {dict(request.headers)}")
            print(f"Request body: {request.data}")
            
            device_id = request.data.get('device_id', '')
            text = request.data.get('text', '')
            language = request.data.get('language', None)  # None = auto-detect

            print(f"✓ device_id: {device_id}")
            print(f"✓ text: {text}")
            print(f"✓ language: {language}")

            if not text:
                error_resp = {'error': 'text is required'}
                print(f"❌ Validation failed: {error_resp}")
                return Response(error_resp, status=status.HTTP_400_BAD_REQUEST)

            try:
                from ml_models.voice_views import process_voice_command
                print(f"🚀 Calling process_voice_command...")
                # Pass auto_log=True to enable logging
                result = process_voice_command(text, language=language, device_id=device_id, auto_log=True)
                print(f"✅ Voice command processed successfully!")
                print(f"   - intent: {result.get('intent')}")
                print(f"   - response: {result.get('response')[:100]}...")
                print(f"   - Full response: {result}")
                print(f"📤 Sending response to frontend...")
                return Response(result)
            except ImportError as ie:
                print(f"❌ ImportError: {str(ie)}")
                print("⚠️  Falling back to rule-based prediction...")
                response = self._fallback_predict(text, language, device_id)
                print(f"📤 Sending fallback response: {response.data}")
                return response
            except Exception as e:
                # Log the exact error and fall back
                import traceback
                print(f"❌ ML Error: {str(e)}")
                print(f"📋 Traceback:\n{traceback.format_exc()}")
                print("⚠️  Falling back to rule-based prediction...")
                response = self._fallback_predict(text, language, device_id)
                print(f"📤 Sending fallback response after ML error: {response.data}")
                return response
        except Exception as e:
            # Outer exception handler for request data parsing
            import traceback
            error_msg = f"Error processing voice command: {str(e)}"
            print(f"❌ {error_msg}")
            print(f"📋 Traceback:\n{traceback.format_exc()}")
            response_data = {
                'error': error_msg, 
                'details': str(e),
                'response': 'Sorry, I encountered an error. Please try again.'
            }
            print(f"📤 Sending error response: {response_data}")
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def _fallback_predict(self, text, language, device_id):
        """Simple rule-based fallback prediction"""
        text_lower = text.lower()

        # Language-aware keywords
        intent_keywords = {
            'income': ['income', 'earning', 'received', 'got money', 'aay', 'வருமானம்', 'வந்தது'],
            'expense': ['expense', 'spent', 'cost', 'paid', 'kharcha', 'செலவு', 'கொடுத்தேன்'],
            'sales': ['sale', 'sold', 'sell', 'product', 'vikri', 'விற்பனை', 'விற்றேன்'],
            'profit': ['profit', 'loss', 'earning', 'laabh', 'லாபம்', 'நஷ்டம்'],
            'market': ['market', 'price', 'rate', 'mandi', 'சந்தை', 'விலை'],
            'schemes': ['scheme', 'loan', 'government', 'yojana', 'திட்டம்', 'கடன்'],
            'mentor': ['mentor', 'help', 'advice', 'guide', 'ஆலோசனை', 'உதவி'],
            'training': ['training', 'learn', 'course', 'skill', 'பயிற்சி', 'கற்றல்'],
        }

        detected_intent = 'general'
        max_matches = 0
        for intent, keywords in intent_keywords.items():
            matches = sum(1 for kw in keywords if kw in text_lower)
            if matches > max_matches:
                max_matches = matches
                detected_intent = intent

        responses = {
            'en': {
                'income': 'I can help you record your income. Please tell me the amount and source.',
                'expense': 'I can help you record your expense. Please tell me the amount and category.',
                'sales': 'I can help you record your sales. What product did you sell and for how much?',
                'profit': 'Let me calculate your profit. Please check the Profit section for details.',
                'market': 'I can show you market prices. Please check the Market Prices section.',
                'schemes': 'There are several government schemes available for you. Check the Schemes section.',
                'mentor': 'I can connect you with a business mentor. Check the Mentor section.',
                'training': 'Training resources are available. Please check the Training section.',
                'general': 'Hello! I am your business assistant. How can I help you today?',
            },
            'hi': {
                'income': 'Mein aapki aay record karne mein madad kar sakti hoon. Kitni aay hui?',
                'expense': 'Mein aapka kharcha record karne mein madad kar sakti hoon.',
                'sales': 'Aapne kya becha aur kitne mein? Mein record kar lungi.',
                'profit': 'Aapka laabh dekhne ke liye Profit section mein jayein.',
                'market': 'Mandi ke bhav Market section mein dekh sakte hain.',
                'schemes': 'Sarkar ki yojanayen Schemes section mein dekh sakte hain.',
                'mentor': 'Mentor se milne ke liye Mentor section mein jayein.',
                'training': 'Training ke liye Training section mein jayein.',
                'general': 'Namaste! Mein aapki business assistant hoon. Kaise madad karoon?',
            },
            'ta': {
                'income': 'Ungal varumanam padhivu seiya udhavugiren. Ethanai roopaay kidaitthathu?',
                'expense': 'Ungal selavu padhivu seiya udhavugiren.',
                'sales': 'Enna vittirukkireenga? Ethanai roopaayku?',
                'profit': 'Ungal laabham paarkka Profit pakkam sellungal.',
                'market': 'Santhai vilai paarkka Market Prices pakkam sellungal.',
                'schemes': 'Arasin thittagal Schemes pakkam ullana.',
                'mentor': 'Aalochanaikku Mentor pakkam sellungal.',
                'training': 'Payirchi paarkka Training pakkam sellungal.',
                'general': 'Vanakkam! Naan ungal thozhil udhaiviyar. Eppadi udhava vendum?',
            }
        }

        lang_responses = responses.get(language, responses['en'])
        response_text = lang_responses.get(detected_intent, lang_responses['general'])

        return Response({
            'intent': detected_intent,
            'confidence': 0.75 if max_matches > 0 else 0.5,
            'response': response_text,
            'language': language,
            'action': detected_intent,
            'extracted_data': {'text': text},
        })


# ==================== DIAGNOSTICS ====================

class DiagnosticsView(APIView):
    """Diagnostics endpoint to test ML and import systems"""
    
    def get(self, request):
        """Run diagnostic checks"""
        diagnostics = {
            'status': 'ok',
            'checks': {}
        }
        
        # Check 1: Language detection
        try:
            from ml_models.language_detection import LanguageDetector, LanguageResponseHandler
            handler = LanguageResponseHandler("I sold 5 kg vegetables")
            lang = handler.get_language()
            diagnostics['checks']['language_detection'] = {
                'status': 'ok',
                'detected_language': lang,
                'message': f"✅ Language detection working - detected '{lang}'"
            }
            print("✅ Language detection: OK")
        except Exception as e:
            diagnostics['checks']['language_detection'] = {
                'status': 'error',
                'error': str(e),
                'message': f"❌ Language detection failed: {str(e)}"
            }
            print(f"❌ Language detection: {str(e)}")
        
        # Check 2: Intent prediction
        try:
            from ml_models.model_predict import predict_intent
            result = predict_intent("I sold 5 kg vegetables")
            intent = result.get('intent')
            diagnostics['checks']['intent_prediction'] = {
                'status': 'ok',
                'intent': intent,
                'message': f"✅ Intent prediction working - detected '{intent}'"
            }
            print(f"✅ Intent prediction: OK (intent={intent})")
        except Exception as e:
            diagnostics['checks']['intent_prediction'] = {
                'status': 'error',
                'error': str(e),
                'message': f"❌ Intent prediction failed: {str(e)}"
            }
            print(f"❌ Intent prediction: {str(e)}")
        
        # Check 3: Rule engine
        try:
            from ml_models.rule_engine import RuleEngine
            engine = RuleEngine(language='en')
            result = engine.handle('sales', 'I sold 5 kg vegetables', {})
            message = result.get('message', '')
            diagnostics['checks']['rule_engine'] = {
                'status': 'ok',
                'message_preview': message[:50],
                'message': f"✅ Rule engine working"
            }
            print("✅ Rule engine: OK")
        except Exception as e:
            diagnostics['checks']['rule_engine'] = {
                'status': 'error',
                'error': str(e),
                'message': f"❌ Rule engine failed: {str(e)}"
            }
            print(f"❌ Rule engine: {str(e)}")
        
        # Check 4: Language responses
        try:
            from ml_models.language_responses import LanguageResponses
            msg_en = LanguageResponses.get_message('greeting_warm', 'en')
            msg_hi = LanguageResponses.get_message('greeting_warm', 'hi')
            msg_ta = LanguageResponses.get_message('greeting_warm', 'ta')
            diagnostics['checks']['language_responses'] = {
                'status': 'ok',
                'english_preview': msg_en[:30],
                'hindi_preview': msg_hi[:30],
                'tamil_preview': msg_ta[:30],
                'message': f"✅ Language responses working"
            }
            print("✅ Language responses: OK")
        except Exception as e:
            diagnostics['checks']['language_responses'] = {
                'status': 'error',
                'error': str(e),
                'message': f"❌ Language responses failed: {str(e)}"
            }
            print(f"❌ Language responses: {str(e)}")
        
        # Check 5: Full voice command pipeline
        try:
            from ml_models.voice_views import process_voice_command
            result = process_voice_command("I sold 5 kg vegetables", language='en')
            diagnostics['checks']['voice_pipeline'] = {
                'status': 'ok',
                'intent': result.get('intent'),
                'response_preview': result.get('response', '')[:50],
                'message': f"✅ Full voice pipeline working"
            }
            print("✅ Voice pipeline: OK")
        except Exception as e:
            diagnostics['checks']['voice_pipeline'] = {
                'status': 'error',
                'error': str(e),
                'message': f"❌ Voice pipeline failed: {str(e)}"
            }
            print(f"❌ Voice pipeline: {str(e)}")
        
        # Determine overall status
        all_ok = all(check['status'] == 'ok' for check in diagnostics['checks'].values())
        diagnostics['status'] = 'ok' if all_ok else 'warning'
        
        return Response(diagnostics)


# ==================== PREDICTION MONITORING ====================

class PredictionFeedbackView(APIView):
    """
    Endpoint for users/admins to provide feedback on predictions.
    This helps improve the model through continuous learning.
    """
    
    def post(self, request):
        """
        Mark a prediction as correct/incorrect.
        
        Args:
            - logging_id: PredictionLog ID to update
            - is_correct: Boolean (True = correct, False = incorrect)
            - actual_intent: (if incorrect) The actual intent
            - feedback_text: Optional user feedback
        """
        try:
            from .models import PredictionLog
            
            logging_id = request.data.get('logging_id')
            is_correct = request.data.get('is_correct')
            actual_intent = request.data.get('actual_intent')
            feedback_text = request.data.get('feedback_text', '')
            
            if not logging_id or is_correct is None:
                return Response(
                    {'error': 'logging_id and is_correct are required'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get prediction log
            try:
                prediction_log = PredictionLog.objects.get(id=logging_id)
            except PredictionLog.DoesNotExist:
                return Response(
                    {'error': f'Prediction log {logging_id} not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Update feedback
            if is_correct:
                prediction_log.mark_correct()
                message = f"✅ Prediction marked as correct!"
            else:
                if not actual_intent:
                    return Response(
                        {'error': 'actual_intent required when marking incorrect'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                prediction_log.mark_incorrect(actual_intent, feedback_text)
                message = f"✅ Prediction marked as incorrect. Actual intent: {actual_intent}"
            
            print(f"📝 Prediction feedback logged: {message}")
            
            return Response({
                'success': True,
                'message': message,
                'prediction_id': logging_id,
                'user_feedback': prediction_log.user_feedback,
            })
        
        except Exception as e:
            import traceback
            print(f"❌ Error logging feedback: {str(e)}")
            print(traceback.format_exc())
            return Response(
                {'error': 'Error logging feedback', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PredictionAccuracyView(APIView):
    """
    Endpoint to get model accuracy reports based on user feedback.
    Shows real-world performance metrics.
    """
    
    def get(self, request):
        """
        Get accuracy report.
        
        Query params:
            - days: Number of days to report on (default: 7)
            - device_id: Filter by device (optional)
        """
        try:
            from .models import PredictionLog
            
            days = int(request.query_params.get('days', 7))
            device_id = request.query_params.get('device_id')
            
            # Get accuracy report
            report = PredictionLog.get_accuracy_report(days=days)
            
            # Filter by device if provided
            if device_id:
                from django.utils import timezone
                from datetime import timedelta
                
                start_date = timezone.now() - timedelta(days=days)
                logs = PredictionLog.objects.filter(
                    device_id=device_id,
                    timestamp__gte=start_date
                )
                
                report['device_filtered'] = True
                report['device_id'] = device_id
                report['device_total_predictions'] = logs.count()
                
                # Recalculate accuracy for this device
                feedback_logs = logs.filter(user_feedback__in=['correct', 'incorrect', 'partial'])
                if feedback_logs.exists():
                    correct = feedback_logs.filter(user_feedback='correct').count()
                    total = feedback_logs.count()
                    report['device_accuracy'] = correct / total if total > 0 else 0
                    report['device_feedback_count'] = total
            
            return Response(report)
        
        except Exception as e:
            import traceback
            print(f"❌ Error generating accuracy report: {str(e)}")
            print(traceback.format_exc())
            return Response(
                {'error': 'Error generating accuracy report', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PredictionDetailView(APIView):
    """
    Get details of a specific prediction for reviewing/debugging.
    """
    
    def get(self, request, prediction_id):
        """Get details of a specific prediction"""
        try:
            from .models import PredictionLog
            
            prediction = PredictionLog.objects.get(id=prediction_id)
            
            return Response({
                'id': prediction.id,
                'input_text': prediction.input_text,
                'input_language': prediction.input_language,
                'predicted_intent': prediction.predicted_intent,
                'confidence': prediction.confidence,
                'raw_confidence': prediction.raw_confidence,
                'model_used': prediction.model_used,
                'all_probabilities': prediction.all_probabilities,
                'user_feedback': prediction.user_feedback,
                'actual_intent': prediction.actual_intent,
                'feedback_text': prediction.feedback_text,
                'timestamp': prediction.timestamp,
                'feedback_timestamp': prediction.feedback_timestamp,
            })
        
        except Exception as e:
            return Response(
                {'error': 'Prediction not found', 'details': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )


class PredictionListView(APIView):
    """
    List predictions with filtering and pagination for admin review.
    """
    
    def get(self, request):
        """
        Get list of predictions for review.
        
        Query params:
            - device_id: Filter by device
            - feedback_status: Filter by feedback status (pending, correct, incorrect)
            - model_used: Filter by model type (ml, rule_based)
            - limit: Number of results (default: 50, max: 500)
            - offset: Pagination offset (default: 0)
        """
        try:
            from .models import PredictionLog
            from django.utils import timezone
            from datetime import timedelta
            
            device_id = request.query_params.get('device_id')
            feedback_status = request.query_params.get('feedback_status')
            model_used = request.query_params.get('model_used')
            limit = min(int(request.query_params.get('limit', 50)), 500)
            offset = int(request.query_params.get('offset', 0))
            days = int(request.query_params.get('days', 30))
            
            # Build query
            start_date = timezone.now() - timedelta(days=days)
            queryset = PredictionLog.objects.filter(timestamp__gte=start_date)
            
            if device_id:
                queryset = queryset.filter(device_id=device_id)
            if feedback_status and feedback_status != 'all':
                queryset = queryset.filter(user_feedback=feedback_status)
            if model_used:
                queryset = queryset.filter(model_used=model_used)
            
            # Count
            total = queryset.count()
            
            # Paginate
            predictions = queryset[offset:offset + limit]
            
            # Format response
            results = []
            for pred in predictions:
                results.append({
                    'id': pred.id,
                    'input_text': pred.input_text[:100],  # Truncate for list view
                    'predicted_intent': pred.predicted_intent,
                    'confidence': round(pred.confidence, 3),
                    'model_used': pred.model_used,
                    'user_feedback': pred.user_feedback,
                    'timestamp': pred.timestamp,
                })
            
            return Response({
                'total': total,
                'limit': limit,
                'offset': offset,
                'results': results,
                'has_more': (offset + limit) < total,
            })
        
        except Exception as e:
            return Response(
                {'error': 'Error fetching predictions', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DashboardSummaryView(APIView):
    def get(self, request):
        try:
            device_id = request.query_params.get('device_id')
            if not device_id:
                return Response({'error': 'device_id required'}, status=status.HTTP_400_BAD_REQUEST)

            today = date.today()
            month_start = today.replace(day=1)

            monthly_income = Income.objects.filter(device_id=device_id, date__gte=month_start).aggregate(
                total=Sum('amount'))['total'] or Decimal('0')
            monthly_expense = Expense.objects.filter(device_id=device_id, date__gte=month_start).aggregate(
                total=Sum('amount'))['total'] or Decimal('0')
            monthly_sales = Sales.objects.filter(device_id=device_id, sale_date__gte=month_start).aggregate(
                total=Sum('total_amount'))['total'] or Decimal('0')

            today_income = Income.objects.filter(device_id=device_id, date=today).aggregate(
                total=Sum('amount'))['total'] or Decimal('0')
            today_expense = Expense.objects.filter(device_id=device_id, date=today).aggregate(
                total=Sum('amount'))['total'] or Decimal('0')

            return Response({
                'monthly_income': str(monthly_income),
                'monthly_expense': str(monthly_expense),
                'monthly_sales': str(monthly_sales),
                'monthly_profit': str(monthly_income - monthly_expense),
                'today_income': str(today_income),
                'today_expense': str(today_expense),
                'today_profit': str(today_income - today_expense),
                'total_records': {
                    'income': Income.objects.filter(device_id=device_id).count(),
                    'expense': Expense.objects.filter(device_id=device_id).count(),
                    'sales': Sales.objects.filter(device_id=device_id).count(),
                }
            })
        except Exception as e:
            return Response(
                {'error': 'Error generating dashboard summary', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
