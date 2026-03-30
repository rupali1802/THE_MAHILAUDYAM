"""
Mahila Udyam - Model Prediction
Singleton pattern for efficient model loading, <200ms inference
"""
import os
import pickle
import re
import json
import numpy as np


class IntentPredictor:
    """Singleton ML model predictor with confidence calibration"""
    _instance = None
    _model = None
    _vectorizer = None
    _model_info = None
    
    # Confidence thresholds
    CONFIDENCE_THRESHOLD = 0.75  # Minimum confidence to trust ML prediction
    HIGH_CONFIDENCE_THRESHOLD = 0.90  # High confidence level

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_model(self):
        if self._model is not None:
            return True
        save_dir = os.path.join(os.path.dirname(__file__), 'saved_models')
        model_path = os.path.join(save_dir, 'mahila_intent_model.pkl')
        vectorizer_path = os.path.join(save_dir, 'mahila_intent_model_vectorizer.pkl')
        info_path = os.path.join(save_dir, 'model_info.json')

        if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
            return False

        try:
            # Try standard pickle loading
            with open(model_path, 'rb') as f:
                self._model = pickle.load(f)
            with open(vectorizer_path, 'rb') as f:
                self._vectorizer = pickle.load(f)
            if os.path.exists(info_path):
                with open(info_path) as f:
                    self._model_info = json.load(f)
            return True
        except (ImportError, AttributeError, ModuleNotFoundError) as e:
            # Handle numpy version compatibility issues
            print(f"⚠️  Pickle load error (likely numpy version issue): {e}")
            print("🔧 Attempting to fix numpy compatibility...")
            try:
                import pickle5 as pkl
                print("📦 Using pickle5 for legacy compatibility...")
                with open(model_path, 'rb') as f:
                    self._model = pkl.load(f)
                with open(vectorizer_path, 'rb') as f:
                    self._vectorizer = pkl.load(f)
                if os.path.exists(info_path):
                    with open(info_path) as f:
                        self._model_info = json.load(f)
                return True
            except ImportError:
                print("❌ pickle5 not available, using rule-based fallback only")
                return False
            except Exception as e2:
                print(f"❌ pickle5 also failed: {e2}")
                return False
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            return False

    def preprocess(self, text):
        text = text.lower()
        text = re.sub(r'[^\w\s₹]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def _calibrate_confidence(self, raw_confidence):
        """
        Calibrate raw model confidence based on model quality.
        If test accuracy is 100%, we may have overfitting - slightly reduce confidence.
        """
        if self._model_info is None:
            return raw_confidence
        
        test_accuracy = self._model_info.get('test_accuracy', 1.0)
        
        # If test accuracy is suspiciously perfect (99%+), reduce confidence slightly
        if test_accuracy >= 0.99:
            calibrated = raw_confidence * 0.95  # Penalty for potential overfitting
            print(f"🔄 Confidence calibrated: {raw_confidence:.2%} → {calibrated:.2%} (model quality: {test_accuracy:.2%})")
            return calibrated
        
        return raw_confidence

    def predict(self, text, return_low_confidence_flag=False):
        """
        Predict intent with confidence threshold and fallback handling.
        
        Args:
            text: Input text to classify
            return_low_confidence_flag: If True, include 'use_rule_based' flag
            
        Returns:
            dict with keys:
                - intent: Predicted intent
                - confidence: Confidence score
                - probabilities: All intent probabilities
                - model_used: 'ml' or 'rule_based'
                - use_rule_based: (if return_low_confidence_flag=True) Boolean indicating fallback
        """
        if not self.load_model():
            return self._rule_based_fallback(text, reason="Model not loaded")

        try:
            processed = self.preprocess(text)
            vec = self._vectorizer.transform([processed])
            intent = self._model.predict(vec)[0]
            probas = self._model.predict_proba(vec)[0]
            raw_confidence = float(np.max(probas))
            
            # Calibrate confidence
            confidence = self._calibrate_confidence(raw_confidence)
            
            classes = self._model.classes_
            all_probas = {cls: float(prob) for cls, prob in zip(classes, probas)}
            
            result = {
                'intent': intent,
                'confidence': confidence,
                'raw_confidence': raw_confidence,
                'probabilities': all_probas,
                'model_used': 'ml',
                'threshold_passed': confidence >= self.CONFIDENCE_THRESHOLD,
            }
            
            # Check if confidence meets threshold
            if return_low_confidence_flag:
                use_rule = confidence < self.CONFIDENCE_THRESHOLD
                result['use_rule_based'] = use_rule
                if use_rule:
                    print(f"⚠️  Low confidence ({confidence:.2%}) - will use rule-based fallback")
            
            return result
        except Exception as e:
            print(f"❌ ML prediction error: {e}")
            return self._rule_based_fallback(text, reason=f"ML error: {str(e)}")

    def get_confidence_level(self, confidence):
        """
        Categorize confidence level for user feedback.
        
        Returns: 'high', 'medium', or 'low'
        """
        if confidence >= self.HIGH_CONFIDENCE_THRESHOLD:
            return 'high'
        elif confidence >= self.CONFIDENCE_THRESHOLD:
            return 'medium'
        else:
            return 'low'

    def _rule_based_fallback(self, text, reason=""):
        """Rule-based fallback for when ML model is unavailable or low confidence"""
        text_lower = text.lower()
        keywords = {
            'income': ['income', 'earning', 'received', 'aay', 'varumanam', 'mila', 'kamai', 'padhivu', 'earni'],
            'expense': ['expense', 'spent', 'kharcha', 'selavu', 'paid', 'pay', 'bill', 'diya'],
            'sales': ['sale', 'sold', 'vikri', 'vittirkai', 'becha', 'sell', 'customer', 'khareed'],
            'profit': ['profit', 'laabh', 'laabham', 'loss', 'nuksan', 'earn', 'minus', 'kamai'],
            'market': ['market', 'price', 'rate', 'mandi', 'santhai', 'vilai', 'bhav', 'commodity', 'current'],
            'schemes': ['scheme', 'yojana', 'thittam', 'loan', 'government', 'subsidy', 'eligible', 'benefit'],
            'mentor': ['mentor', 'advice', 'help', 'aalochanai', 'salah', 'expert', 'connect', 'guidance'],
            'payment': ['payment', 'upi', 'transfer', 'cash', 'parivarthanai', 'thilam', 'method', 'paid'],
            'training': ['training', 'learn', 'payirchi', 'seekhna', 'skill', 'course', 'improve', 'digital'],
        }
        
        best_intent = 'income'
        best_score = 0
        
        for intent, kws in keywords.items():
            score = sum(1 for kw in kws if kw in text_lower)
            if score > best_score:
                best_score = score
                best_intent = intent

        # Confidence based on keyword match strength
        if best_score >= 2:
            confidence = 0.80
        elif best_score == 1:
            confidence = 0.60
        else:
            confidence = 0.40
        
        print(f"📋 Rule-based prediction: {best_intent} (score: {best_score}, reason: {reason})")
        
        return {
            'intent': best_intent,
            'confidence': confidence,
            'raw_confidence': confidence,
            'probabilities': {best_intent: confidence},
            'model_used': 'rule_based',
            'threshold_passed': confidence >= self.CONFIDENCE_THRESHOLD,
            'reason': reason,
        }


# Global singleton
predictor = IntentPredictor()


def predict_intent(text, return_low_confidence_flag=False):
    return predictor.predict(text, return_low_confidence_flag=return_low_confidence_flag)
