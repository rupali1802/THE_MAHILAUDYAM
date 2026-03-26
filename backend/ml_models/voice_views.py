"""
Mahila Udyam - Voice Views
Complete voice command processing pipeline with auto-language detection
Includes prediction logging for continuous model improvement
"""
from .model_predict import predict_intent
from .rule_engine import RuleEngine
from .language_responses import LanguageResponses
from .language_detection import LanguageDetector, LanguageResponseHandler


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

        # Step 1: Predict intent with confidence threshold
        print(f"🔍 Predicting intent for: '{text}'")
        prediction = predict_intent(text, return_low_confidence_flag=True)
        intent = prediction['intent']
        confidence = prediction['confidence']
        threshold_passed = prediction.get('threshold_passed', True)
        
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

        return {
            'intent': intent,
            'confidence': confidence,
            'response': result['message'],
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
        }
    except Exception as e:
        import traceback
        print(f"❌ Error in process_voice_command: {str(e)}")
        print(f"📋 Traceback:\n{traceback.format_exc()}")
        raise
