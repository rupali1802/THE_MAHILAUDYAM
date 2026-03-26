"""
Mahila Udyam - Language Detection & Auto-Response
Detects language of input and responds in the same language
"""
import re
import json


class LanguageDetector:
    """Detect language from text input"""

    # Language detection patterns - optimized for Indian languages
    PATTERNS = {
        'hi': {
            # Hindi-specific characters and words
            'chars': r'[\u0900-\u097F]',  # Devanagari script
            'keywords': [
                'aay', 'kharcha', 'becha', 'laabh', 'yojana', 'bhav', 'mentor',
                'aaj', 'kal', 'mahine', 'rupaye', 'hai', 'mein', 'hain', 'kya',
                'kaise', 'kitna', 'karo', 'batao', 'dikhao', 'chahiye', 'chahta',
                'hua', 'gayi', 'raha', 'sakta', 'sakte', 'saktein', 'banao',
            ]
        },
        'ta': {
            # Tamil-specific characters and words
            'chars': r'[\u0B80-\u0BFF]',  # Tamil script
            'keywords': [
                'varumanam', 'selavu', 'vittira', 'laabham', 'thittagal', 'vilai',
                'mentor', 'indru', 'maadham', 'roopaay', 'enna', 'ethanai', 'eppadi',
                'sollunga', 'kattu', 'parunga', 'seyyungal', 'kittum', 'aagiyirukku',
                'irukka', 'vittirukka', 'padhivu', 'kekkanum', 'solren',
            ]
        },
        'en': {
            # English keywords
            'keywords': [
                'income', 'expense', 'sales', 'profit', 'market', 'price', 'scheme',
                'mentor', 'payment', 'today', 'record', 'add', 'show', 'tell',
                'rupees', 'what', 'how', 'when', 'money', 'sold', 'spent',
                'received', 'earned', 'check', 'help', 'question',
            ]
        }
    }

    @classmethod
    def detect(cls, text):
        """
        Detect language from text
        Returns: ('en', 'hi', 'ta', or 'unknown')
        """
        if not text or not isinstance(text, str):
            return 'en'

        text_lower = text.lower()

        # Check for script presence (most reliable)
        if re.search(cls.PATTERNS['hi']['chars'], text):
            return 'hi'
        if re.search(cls.PATTERNS['ta']['chars'], text):
            return 'ta'

        # Check for keyword matches
        scores = {'en': 0, 'hi': 0, 'ta': 0}

        for keyword in cls.PATTERNS['hi']['keywords']:
            if keyword in text_lower:
                scores['hi'] += 1

        for keyword in cls.PATTERNS['ta']['keywords']:
            if keyword in text_lower:
                scores['ta'] += 1

        for keyword in cls.PATTERNS['en']['keywords']:
            if keyword in text_lower:
                scores['en'] += 1

        # Return language with highest score
        if max(scores.values()) == 0:
            return 'en'  # Default to English if no matches

        max_score = max(scores.values())
        detected = [lang for lang, score in scores.items() if score == max_score]

        if len(detected) == 1:
            return detected[0]

        # Tiebreaker: English is default
        return 'en' if 'en' in detected else detected[0]

    @classmethod
    def get_confidence(cls, text):
        """Get language detection confidence (0-100)"""
        if not text:
            return 0

        text_lower = text.lower()
        lang = cls.detect(text)

        # Script match = high confidence
        if lang == 'hi' and re.search(cls.PATTERNS['hi']['chars'], text):
            return 95
        if lang == 'ta' and re.search(cls.PATTERNS['ta']['chars'], text):
            return 95

        # Keyword count
        pattern = cls.PATTERNS[lang]
        matches = sum(1 for kw in pattern['keywords'] if kw in text_lower)

        # Score based on keyword matches
        confidence = min(95, 50 + (matches * 5))
        return confidence


class LanguageResponseHandler:
    """Handle responses in detected language"""

    def __init__(self, text):
        """Initialize with user input text"""
        self.text = text
        self.language = LanguageDetector.detect(text)
        self.confidence = LanguageDetector.get_confidence(text)

    def get_language(self):
        """Get detected language code"""
        return self.language

    def get_language_name(self):
        """Get human-readable language name"""
        names = {
            'en': 'English',
            'hi': 'Hindi',
            'ta': 'Tamil',
        }
        return names.get(self.language, 'Unknown')

    def get_info(self):
        """Get language detection info"""
        return {
            'detected_language': self.language,
            'language_name': self.get_language_name(),
            'confidence': self.confidence,
            'text': self.text,
        }


# Test examples
if __name__ == '__main__':
    test_cases = [
        # English
        "What is the market price of tomato?",
        "Record income of 500 rupees",
        "Show my profit for this month",

        # Hindi (Romanized)
        "Mujhe 500 rupaye ki aay record karni hai",
        "Tamatar ka bhav batao",
        "Mera profit dikhao",
        "Kharcha 200 rupaye khana ke liye",

        # Tamil (Romanized)
        "Varumanam 500 roopaay padhivu",
        "Indru thaakkali vilai ethanai",
        "Laabham sollunga",
        "Selavu 300 roopaay",
    ]

    print("=" * 70)
    print("LANGUAGE DETECTION TEST")
    print("=" * 70)

    for text in test_cases:
        detector = LanguageResponseHandler(text)
        info = detector.get_info()
        print(f"\nText: {text}")
        print(f"  Detected: {info['language_name']} ({info['detected_language']})")
        print(f"  Confidence: {info['confidence']}%")
