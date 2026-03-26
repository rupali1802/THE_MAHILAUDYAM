"""
Mahila Udyam - API Views
All REST endpoints for the business management system
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import date, timedelta, datetime
from decimal import Decimal
import sys
import os

from .models import User, Income, Expense, Sales, Payment, MarketPrice, Scheme, Mentor, MentorChat
from .serializers import (
    UserSerializer, IncomeSerializer, ExpenseSerializer, SalesSerializer,
    PaymentSerializer, MarketPriceSerializer, SchemeSerializer,
    MentorSerializer, MentorChatSerializer
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


# ==================== PAYMENT VIEWS ====================

class PaymentListView(APIView):
    def get(self, request):
        try:
            device_id = request.query_params.get('device_id')
            if not device_id:
                return Response({'error': 'device_id required'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = Payment.objects.filter(device_id=device_id)
            serializer = PaymentSerializer(queryset, many=True)
            return Response({'results': serializer.data, 'count': queryset.count()})
        except Exception as e:
            return Response(
                {'error': 'Error fetching payments', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PaymentAddView(APIView):
    def post(self, request):
        try:
            data = request.data.copy()
            if not data.get('date'):
                data['date'] = date.today().isoformat()
            serializer = PaymentSerializer(data=data)
            if serializer.is_valid():
                payment = serializer.save()
                return Response({'success': True, 'data': PaymentSerializer(payment).data}, status=status.HTTP_201_CREATED)
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': 'Error adding payment', 'details': str(e)},
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


# ==================== SCHEME VIEWS ====================

class SchemeListView(APIView):
    def get(self, request):
        try:
            queryset = Scheme.objects.filter(status='active')
            category = request.query_params.get('category')
            if category:
                queryset = queryset.filter(category=category)
            serializer = SchemeSerializer(queryset, many=True)
            return Response({'results': serializer.data, 'count': queryset.count()})
        except Exception as e:
            return Response(
                {'error': 'Error fetching schemes', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ==================== MENTOR VIEWS ====================

class MentorListView(APIView):
    def get(self, request):
        try:
            queryset = Mentor.objects.filter(is_active=True)
            expertise = request.query_params.get('expertise')
            if expertise:
                queryset = queryset.filter(expertise__icontains=expertise)
            availability = request.query_params.get('availability')
            if availability:
                queryset = queryset.filter(availability=availability)
            serializer = MentorSerializer(queryset, many=True)
            return Response({'results': serializer.data, 'count': queryset.count()})
        except Exception as e:
            return Response(
                {'error': 'Error fetching mentors', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MentorChatView(APIView):
    def get(self, request):
        try:
            device_id = request.query_params.get('device_id')
            mentor_id = request.query_params.get('mentor_id')
            if not device_id or not mentor_id:
                return Response({'error': 'device_id and mentor_id required'}, status=status.HTTP_400_BAD_REQUEST)
            queryset = MentorChat.objects.filter(device_id=device_id, mentor_id=mentor_id)
            serializer = MentorChatSerializer(queryset, many=True)
            return Response({'results': serializer.data})
        except Exception as e:
            return Response(
                {'error': 'Error fetching mentor chat', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            data = request.data.copy()
            serializer = MentorChatSerializer(data=data)
            if serializer.is_valid():
                chat = serializer.save()
                return Response({'success': True, 'data': MentorChatSerializer(chat).data}, status=status.HTTP_201_CREATED)
            return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {'error': 'Error adding mentor chat', 'details': str(e)},
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
            'payment': ['payment', 'upi', 'transfer', 'bhugtan', 'பணம்', 'பணப்பரிமாற்றம்'],
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
                'payment': 'I can help you track payments. Please use the Payment section.',
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
                'payment': 'Payment record karne ke liye Payment section use karein.',
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
                'payment': 'Pana parivarthanai paarkka Payment pakkam sellungal.',
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
