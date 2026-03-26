"""
Mahila Udyam - Rule Engine
Handles 9 intent handlers with entity extraction and response generation
"""
from .language_support import get_template, extract_entities_from_text
from .language_responses import LanguageResponses
from .number_converter import NumberConverter
from datetime import date


class RuleEngine:
    """
    Rule-based intent handler.
    Each handler validates input, extracts entities, and returns a structured response.
    """

    def __init__(self, language='en'):
        self.language = language

    def handle(self, intent, text, extracted_data=None):
        """Route intent to appropriate handler"""
        handlers = {
            'income': self.handle_income,
            'expense': self.handle_expense,
            'sales': self.handle_sales,
            'profit': self.handle_profit,
            'market': self.handle_market,
            'schemes': self.handle_schemes,
            'mentor': self.handle_mentor,
            'payment': self.handle_payment,
            'training': self.handle_training,
        }

        handler = handlers.get(intent, self.handle_general)
        return handler(text, extracted_data or {})

    def handle_income(self, text, extracted_data):
        entities = extract_entities_from_text(text, self.language)
        entities.update(extracted_data)

        if 'amount' in entities:
            amount = entities['amount']
            source = entities.get('source', 'business')
            amount_words = NumberConverter.convert(amount, self.language)

            response = get_template('income', 'success', self.language,
                                    amount=f"{amount:,.0f}", source=source)
            return {
                'status': 'success',
                'message': response,
                'action': 'record_income',
                'extracted_data': {
                    'amount': amount,
                    'source': source,
                    'date': str(date.today()),
                    'category': entities.get('category', 'sales'),
                },
                'amount_words': amount_words,
            }
        else:
            response = get_template('income', 'query', self.language)
            return {
                'status': 'query',
                'message': response,
                'action': 'ask_income_details',
                'extracted_data': {},
            }

    def handle_expense(self, text, extracted_data):
        entities = extract_entities_from_text(text, self.language)
        entities.update(extracted_data)

        if 'amount' in entities:
            amount = entities['amount']
            category = entities.get('category', 'other')
            amount_words = NumberConverter.convert(amount, self.language)

            response = get_template('expense', 'success', self.language,
                                    amount=f"{amount:,.0f}", category=category)
            return {
                'status': 'success',
                'message': response,
                'action': 'record_expense',
                'extracted_data': {
                    'amount': amount,
                    'category': category,
                    'date': str(date.today()),
                    'payment_method': entities.get('payment_method', 'cash'),
                },
                'amount_words': amount_words,
            }
        else:
            response = get_template('expense', 'query', self.language)
            return {
                'status': 'query',
                'message': response,
                'action': 'ask_expense_details',
                'extracted_data': {},
            }

    def handle_sales(self, text, extracted_data):
        entities = extract_entities_from_text(text, self.language)
        entities.update(extracted_data)

        if 'amount' in entities:
            amount = entities['amount']
            product = entities.get('source', entities.get('product', 'product'))
            quantity = entities.get('quantity', 1)

            response = get_template('sales', 'success', self.language,
                                    amount=f"{amount:,.0f}", product=product,
                                    total=f"{amount:,.0f}", quantity=quantity)
            return {
                'status': 'success',
                'message': response,
                'action': 'record_sale',
                'extracted_data': {
                    'product_name': product,
                    'quantity': quantity,
                    'price_per_unit': amount / quantity if quantity else amount,
                    'total_amount': amount,
                    'sale_date': str(date.today()),
                },
            }
        else:
            response = get_template('sales', 'query', self.language)
            return {
                'status': 'query',
                'message': response,
                'action': 'ask_sale_details',
                'extracted_data': {},
            }

    def handle_profit(self, text, extracted_data):
        # Determine period
        text_lower = text.lower()
        if any(w in text_lower for w in ['today', 'aaj', 'indru']):
            period = 'today'
        elif any(w in text_lower for w in ['week', 'hafte', 'vaaram']):
            period = 'weekly'
        elif any(w in text_lower for w in ['year', 'saal', 'varudam']):
            period = 'yearly'
        else:
            period = 'monthly'

        period_labels = {
            'en': {'today': 'today', 'weekly': 'this week', 'monthly': 'this month', 'yearly': 'this year'},
            'hi': {'today': 'aaj', 'weekly': 'is hafte', 'monthly': 'is mahine', 'yearly': 'is saal'},
            'ta': {'today': 'indru', 'weekly': 'indha vaaram', 'monthly': 'indha maadham', 'yearly': 'indha varudam'},
        }
        period_label = period_labels.get(self.language, period_labels['en'])[period]

        response = get_template('profit', 'query', self.language, period=period_label)
        return {
            'status': 'success',
            'message': response,
            'action': 'show_profit',
            'extracted_data': {'period': period},
        }

    def handle_market(self, text, extracted_data):
        response = get_template('market', 'query', self.language)
        return {
            'status': 'success',
            'message': response,
            'action': 'show_market_prices',
            'extracted_data': {},
        }

    def handle_schemes(self, text, extracted_data):
        # Detect scheme type
        text_lower = text.lower()
        if any(w in text_lower for w in ['loan', 'karz', 'kadhan']):
            response = LanguageResponses.get_message('schemes_loan', self.language)
        else:
            response = LanguageResponses.get_message('schemes_list', self.language, count='several')

        return {
            'status': 'success',
            'message': response,
            'action': 'show_schemes',
            'extracted_data': {},
        }

    def handle_mentor(self, text, extracted_data):
        response = LanguageResponses.get_message('mentor_connect', self.language)
        return {
            'status': 'success',
            'message': response,
            'action': 'show_mentors',
            'extracted_data': {},
        }

    def handle_payment(self, text, extracted_data):
        entities = extract_entities_from_text(text, self.language)
        entities.update(extracted_data)

        if 'amount' in entities:
            amount = entities['amount']
            method = 'upi' if 'upi' in text.lower() else 'cash'
            response = LanguageResponses.get_message('payment_success', self.language,
                                                     amount=f"{amount:,.0f}", method=method)
            return {
                'status': 'success',
                'message': response,
                'action': 'record_payment',
                'extracted_data': {'amount': amount, 'method': method},
            }
        else:
            response = get_template('payment', 'query', self.language)
            return {
                'status': 'query',
                'message': response,
                'action': 'show_payment',
                'extracted_data': {},
            }

    def handle_training(self, text, extracted_data):
        response = LanguageResponses.get_message('training_info', self.language)
        return {
            'status': 'success',
            'message': response,
            'action': 'show_training',
            'extracted_data': {},
        }

    def handle_general(self, text, extracted_data):
        response = LanguageResponses.get_message('greeting', self.language)
        return {
            'status': 'info',
            'message': response,
            'action': 'none',
            'extracted_data': {},
        }
