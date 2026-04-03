"""
Mahila Udyam - Voice Views
Complete voice command processing pipeline with auto-language detection
Includes prediction logging for continuous model improvement
Optional Gemini AI enhancement for richer responses
"""
from .model_predict import predict_intent
from .rule_engine import RuleEngine
from .language_responses import LanguageResponses
from .language_detection import LanguageDetector, LanguageResponseHandler
from .gemini_helper import GeminiHelper
from datetime import datetime


def log_prediction(text, language, prediction, device_id=''):
    """
    Log prediction to database for monitoring and continuous improvement.
    
    Args:
        text: Input text
        language: Detected language
        prediction: Prediction result dict
        device_id: Device ID for tracking
    """
    try:
        # Import here to avoid circular imports
        from api.models import PredictionLog
        
        log_entry = PredictionLog(
            device_id=device_id or 'unknown',
            input_text=text,
            input_language=language,
            predicted_intent=prediction.get('intent', 'unknown'),
            confidence=prediction.get('confidence', 0),
            raw_confidence=prediction.get('raw_confidence', None),
            model_used=prediction.get('model_used', 'ml'),
            all_probabilities=prediction.get('probabilities', {}),
        )
        log_entry.save()
        print(f"📊 Prediction logged: {prediction.get('intent')} (ID: {log_entry.id})")
        return log_entry.id
    except Exception as e:
        print(f"⚠️  Failed to log prediction: {str(e)}")
        return None


def save_voice_recorded_data(intent, extracted_data, device_id=''):
    """
    Save voice-recorded data to database for income/expense/sales.
    
    Args:
        intent: The intent (income, expense, sales, etc.)
        extracted_data: Dict with 'amount', 'category', 'date', etc.
        device_id: Device ID of the user
        
    Returns:
        dict with 'success', 'record_id', 'record_type', and message
    """
    try:
        from api.models import User, Income, Expense, Sales
        
        if not device_id:
            return {
                'success': False,
                'message': '❌ Device ID required for saving data',
                'record_id': None,
                'record_type': None,
            }
        
        # Get or create user
        user, _ = User.objects.get_or_create(device_id=device_id)
        print(f"👤 User: {user.device_id}")
        
        # Save based on intent
        if intent == 'income' and extracted_data.get('amount'):
            record = Income.objects.create(
                device_id=device_id,
                user=user,
                amount=extracted_data.get('amount'),
                source=extracted_data.get('source', 'business'),
                category=extracted_data.get('category', 'sales'),
                date=extracted_data.get('date', datetime.now().date()),
                description=f"Voice recorded: {extracted_data.get('amount')} from {extracted_data.get('source', 'business')}",
            )
            print(f"✅ Income recorded: {record.id} - {record.amount}")
            return {
                'success': True,
                'message': f'✅ Income of ₹{record.amount} recorded',
                'record_id': record.id,
                'record_type': 'income',
            }
        
        elif intent == 'expense' and extracted_data.get('amount'):
            record = Expense.objects.create(
                device_id=device_id,
                user=user,
                amount=extracted_data.get('amount'),
                category=extracted_data.get('category', 'other'),
                date=extracted_data.get('date', datetime.now().date()),
                payment_method=extracted_data.get('payment_method', 'cash'),
                description=f"Voice recorded: {extracted_data.get('amount')} for {extracted_data.get('category', 'other')}",
            )
            print(f"✅ Expense recorded: {record.id} - {record.amount}")
            return {
                'success': True,
                'message': f'✅ Expense of ₹{record.amount} recorded',
                'record_id': record.id,
                'record_type': 'expense',
            }
        
        elif intent == 'sales' and extracted_data.get('total_amount'):
            record = Sales.objects.create(
                device_id=device_id,
                user=user,
                product_name=extracted_data.get('product_name', 'Product'),
                quantity=extracted_data.get('quantity', 1),
                unit=extracted_data.get('unit', 'piece'),
                price_per_unit=extracted_data.get('price_per_unit', extracted_data.get('total_amount', 0)),
                total_amount=extracted_data.get('total_amount'),
                sale_date=extracted_data.get('sale_date', datetime.now().date()),
                description=f"Voice recorded: {extracted_data.get('quantity', 1)} {extracted_data.get('unit', 'piece')} of {extracted_data.get('product_name')} at ₹{extracted_data.get('price_per_unit', extracted_data.get('total_amount'))}",
            )
            print(f"✅ Sale recorded: {record.id} - {record.total_amount}")
            return {
                'success': True,
                'message': f'✅ Sale of ₹{record.total_amount} recorded',
                'record_id': record.id,
                'record_type': 'sales',
            }
        
        else:
            print(f"⚠️  No data to save for intent: {intent}")
            return {
                'success': False,
                'message': f'⚠️  Could not save {intent} - missing amount or unsupported intent',
                'record_id': None,
                'record_type': None,
            }
    
    except Exception as e:
        import traceback
        print(f"❌ Error saving voice data: {str(e)}")
        print(f"📋 Traceback:\n{traceback.format_exc()}")
        return {
            'success': False,
            'message': f'❌ Error saving data: {str(e)}',
            'record_id': None,
            'record_type': None,
        }


def process_voice_command(text, language=None, device_id='', auto_log=True):
    """
    Full pipeline: text -> language detection -> intent -> rule handling -> response
    If language is not provided, auto-detects from text
    
    Args:
        text: Input voice transcription
        language: Language code ('en', 'hi', 'ta') or None for auto-detect
        device_id: Device identifier for tracking
        auto_log: Whether to log predictions to database
        
    Returns:
        dict with intent, confidence, response, action, extracted_data, and logging_id
    """
    try:
        if not text or not text.strip():
            # Auto-detect language even for empty
            detected_lang = 'en'
            return {
                'intent': 'general',
                'confidence': 0,
                'response': LanguageResponses.get_message('error_general', detected_lang),
                'language': detected_lang,
                'detected_language': detected_lang,
                'language_name': 'English',
                'language_confidence': 0,
                'action': 'none',
                'extracted_data': {},
                'logging_id': None,
            }

        # Step 0: Auto-detect language if not provided
        if language is None or language == 'auto':
            handler = LanguageResponseHandler(text)
            language = handler.get_language()
            language_name = handler.get_language_name()
            language_confidence = handler.confidence
            print(f"📝 Language detected: {language} ({language_name}) - confidence: {language_confidence}%")
        else:
            handler = None
            language_name = {'en': 'English', 'hi': 'Hindi', 'ta': 'Tamil'}.get(language, 'Unknown')
            language_confidence = 100  # User provided language
            print(f"📝 Language provided: {language}")

        # Ensure language is valid
        if language not in ['en', 'hi', 'ta']:
            print(f"⚠️  Invalid language: {language}, defaulting to English")
            language = 'en'
            language_confidence = 50

        # Step 1: CONTEXT-AWARE INTENT CORRECTION
        # Add context awareness to distinguish similar intents
        print(f"🔍 Original text: '{text}'")
        
        # Income keywords (excluding expense contexts)
        income_keywords = ['earn', 'earned', 'received', 'got', 'income', 'made', 'sale', 'sold', 'sold it', 'sold for', 'bought', 'got from', 'earned from', 'revenue', 'selling', 'commerce']
        expense_keywords = ['spent', 'paid', 'cost', 'expense', 'buy', 'bought', 'used for', 'spent on', 'gave', 'transfer', 'sent to', 'charged', 'paid for']
        sales_keywords = ['sold', 'sale', 'sell', 'customer', 'bought', 'sold it', 'sold to', 'product', 'quantity', 'units', 'pieces', 'kilos']
        
        text_lower = text.lower()
        
        # Context-aware correction
        if 'income' in text_lower or 'earned' in text_lower or 'received' in text_lower or 'got' in text_lower:
            # Check if it's not an expense context
            if not any(word in text_lower for word in ['spent', 'paid', 'cost', 'buy']):
                print("🎯 Context analysis: This appears to be an INCOME entry")
        elif any(word in text_lower for word in sales_keywords):
            # Check if it mentions quantity or product-specific sales
            if any(word in text_lower for word in ['sold', 'sale', 'sold it', 'sold for', 'customer', 'pieces', 'kilos', 'quantity']):
                print("🎯 Context analysis: This appears to be a SALES entry")
        print(f"🔍 Predicting intent for: '{text}'")
        prediction = predict_intent(text, return_low_confidence_flag=True)
        intent = prediction['intent']
        confidence = prediction['confidence']
        threshold_passed = prediction.get('threshold_passed', True)
        
        # CONTEXT-AWARE INTENT CORRECTION
        # If confidence is low, use keyword matching to correct prediction
        text_lower = text.lower()
        
        # Income keywords analysis
        income_keywords = ['earn', 'earned', 'received', 'got', 'income', 'made', 'revenue', 'came']
        expense_keywords = ['spent', 'paid', 'cost', 'expense', 'charge', 'transfer']
        sales_keywords = ['sold', 'sale', 'sell', 'customer', 'bought', 'product', 'quantity']
        
        # Apply context correction for low confidence predictions
        if not threshold_passed or confidence < 0.6:
            print(f"⚠️  Low confidence ({confidence:.2%}) - checking context keywords...")
            
            # Check for income keywords
            if any(keyword in text_lower for keyword in income_keywords):
                if not any(keyword in text_lower for keyword in expense_keywords):
                    intent = 'income'
                    confidence = min(0.85, confidence + 0.2)
                    print(f"✅ Corrected to INCOME based on keywords (new confidence: {confidence:.2%})")
            
            # Check for sales keywords (quantity + product + sell)
            elif any(keyword in text_lower for keyword in ['sold', 'sell', 'sale', 'shipped']):
                if any(keyword in text_lower for keyword in ['quantity', 'pieces', 'kg', 'kilos', 'units', 'dozen', 'customer']):
                    intent = 'sales'
                    confidence = min(0.85, confidence + 0.2)
                    print(f"✅ Corrected to SALES based on keywords (new confidence: {confidence:.2%})")
            
            # Check for expense keywords
            elif any(keyword in text_lower for keyword in expense_keywords):
                intent = 'expense'
                confidence = min(0.85, confidence + 0.2)
                print(f"✅ Corrected to EXPENSE based on keywords (new confidence: {confidence:.2%})")
        
        print(f"✅ Intent predicted: {intent} (confidence: {confidence:.2%})")
        
        # Log prediction if enabled
        logging_id = None
        if auto_log and device_id:
            logging_id = log_prediction(text, language, prediction, device_id)

        # Check if we should use rule-based for low confidence
        if not threshold_passed:
            print(f"⚠️  Low confidence ({confidence:.2%}) - using enhanced rule-based handling")
            # Could enhance rule engine or re-query here if needed
        
        # Step 2: Handle via rule engine with detected language
        print(f"⚙️  Processing intent '{intent}' with rule engine...")
        engine = RuleEngine(language=language)
        result = engine.handle(intent, text, {})
        print(f"✅ Rule engine result: {result.get('message')[:50]}...")

        # Step 3: Save voice-recorded data to database (for income/expense/sales)
        record_info = None
        extracted = result.get('extracted_data', {})
        
        # Check if we should save based on intent and available data
        should_save = False
        if intent == 'income' and extracted.get('amount'):
            should_save = True
        elif intent == 'expense' and extracted.get('amount'):
            should_save = True
        elif intent == 'sales' and extracted.get('total_amount'):
            should_save = True
        
        if should_save:
            print(f"💾 Saving {intent} record to database...")
            record_info = save_voice_recorded_data(intent, extracted, device_id)
            if record_info['success']:
                print(f"✅ Record saved: {record_info}")

        # Step 4: Optional Gemini AI enhancement for richer responses
        base_response = result['message']
        gemini_enhanced = False
        
        if GeminiHelper.is_available():
            print(f"🤖 Attempting to enhance response with Gemini AI...")
            try:
                # Use voice-optimized Gemini response for better answers
                voice_response = GeminiHelper.generate_voice_response(
                    user_query=text,
                    language=language,
                    extracted_data=extracted,
                    intent=intent
                )
                
                if voice_response:
                    print(f"✅ Response enhanced with Gemini AI")
                    base_response = voice_response
                    gemini_enhanced = True
                else:
                    print(f"ℹ️  Gemini enhancement returned no result, using rule-based response")
            except Exception as e:
                print(f"⚠️  Gemini enhancement failed: {str(e)}, falling back to rule-based response")
        else:
            print(f"ℹ️  Gemini AI not available, using rule-based response")

        return {
            'intent': intent,
            'confidence': confidence,
            'response': base_response,
            'language': language,
            'detected_language': language,
            'language_name': language_name,
            'language_confidence': language_confidence,
            'action': result.get('action', intent),
            'extracted_data': result.get('extracted_data', {}),
            'amount_words': result.get('amount_words', ''),
            'model_used': prediction.get('model_used', 'ml'),
            'probabilities': prediction.get('probabilities', {}),
            'threshold_passed': threshold_passed,
            'logging_id': logging_id,
            'record_info': record_info,  # Include record save status
            'gemini_enhanced': gemini_enhanced,  # Whether Gemini enhanced the response
        }
    except Exception as e:
        import traceback
        print(f"❌ Error in process_voice_command: {str(e)}")
        print(f"📋 Traceback:\n{traceback.format_exc()}")
        raise
