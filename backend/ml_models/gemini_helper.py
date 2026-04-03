"""
Mahila Udyam - Google Gemini API Integration
Safe, optional integration that doesn't break if API key is missing
"""
import os
import logging
from typing import Optional

# Set up logging
logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("google-generativeai not installed. Gemini features disabled.")

API_KEY = os.environ.get('GEMINI_API_KEY', '').strip()

# Configure if API key exists
if API_KEY and GEMINI_AVAILABLE:
    try:
        genai.configure(api_key=API_KEY)
        GEMINI_ENABLED = True
        logger.info("✅ Gemini API initialized successfully")
    except Exception as e:
        GEMINI_ENABLED = False
        logger.warning(f"⚠️  Failed to initialize Gemini API: {str(e)}")
else:
    GEMINI_ENABLED = False
    if not API_KEY:
        logger.info("ℹ️  Gemini API key not found. Set GEMINI_API_KEY in .env to enable AI features.")
    if not GEMINI_AVAILABLE:
        logger.info("ℹ️  google-generativeai not installed. Install with: pip install google-generativeai")


class GeminiHelper:
    """
    Helper class for Gemini API interactions
    Falls back gracefully if API is unavailable
    """

    @staticmethod
    def is_available() -> bool:
        """Check if Gemini API is available and configured"""
        return GEMINI_ENABLED

    @staticmethod
    def enhance_response(text: str, language: str = 'en', context: str = '') -> Optional[str]:
        """
        Enhance a response using Gemini AI
        
        Args:
            text: The text to enhance
            language: Language code (en, hi, ta)
            context: Additional context for better responses
            
        Returns:
            Enhanced text in the specified language or None if Gemini is unavailable
        """
        if not GEMINI_ENABLED:
            logger.debug("Gemini not available, returning original text")
            return None

        try:
            model = genai.GenerativeModel('gemini-pro')
            
            # ULTRA-STRICT Language-specific instructions (NO MIXING)
            lang_instructions = {
                'en': """✋ CRITICAL - ENGLISH ONLY:
You MUST respond ONLY in English.
- Never use Hindi, Tamil, or other languages
- No mixing languages
- Pure English only.

Your response in English:""",
                'hi': """✋ गंभीर - केवल हिंदी:
आप केवल हिंदी में जवाब दें।
- कभी अंग्रेजी या तमिल न लिखें
- कोई मिश्रण न करें
- केवल शुद्ध हिंदी

अपना जवाब हिंदी में:""",
                'ta': """✋ முக்கியம் - தமிழ் மட்டும்:
தமிழ் மொழியில் மட்டுமே பதிலளிக்கவும்.
- ஆங்கிலம் அல்லது இந்தி எழுத வேண்டாம்
- கலக்க வேண்டாம்
- தெளிவான தமிழ்

தமிழ் மொழியில் பதிலளிக்கவும்:""",
            }
            
            instruction = lang_instructions.get(language, 'Respond in English only.')
            
            # Determine language name
            lang_names = {
                'en': 'English',
                'hi': 'हिंदी (Hindi)',
                'ta': 'தமிழ் (Tamil)'
            }
            lang_name = lang_names.get(language, language)
            
            # Construct prompt with explicit language instruction at the beginning
            prompt = f"""LANGUAGE: {lang_name}

{instruction}

Context: {context}

Please enhance and provide more details about: {text}

---RULES---
✓ Respond ONLY in {lang_name}
✓ NO mixing languages
✓ NO English if responding in Hindi/Tamil
✓ NO Hindi if responding in English/Tamil
✓ NO Tamil if responding in English/Hindi

Your response in {lang_name} only:"""
            
            logger.debug(f"Calling Gemini with language={language}")
            response = model.generate_content(prompt)
            
            if response.text:
                logger.info(f"✅ Gemini response generated in {language}")
                return response.text
            return None
            
        except Exception as e:
            logger.error(f"❌ Gemini API error: {str(e)}")
            return None

    @staticmethod
    def generate_voice_response(user_query: str, language: str = 'en', extracted_data: dict = None, intent: str = 'general') -> Optional[str]:
        """
        Generate a response specifically for voice assistant interactions.
        Optimized for voice delivery with shorter, more direct answers.
        STRICT: Only answers the specific question asked - no extra information.
        
        Args:
            user_query: The user's original voice query
            language: Language code (en, hi, ta)
            extracted_data: Extracted data from the query (amount, date, etc)
            intent: The detected intent (income, expense, market, mentor, scheme, etc)
            
        Returns:
            Voice-friendly response or None if Gemini unavailable
        """
        if not GEMINI_ENABLED:
            logger.debug("Gemini not available for voice response")
            return None

        try:
            model = genai.GenerativeModel('gemini-pro')
            
            # ULTRA-STRICT Language-specific instructions for voice (NO MIXING)
            lang_instructions = {
                'en': """CRITICAL: You MUST respond ONLY in English. 
- Do NOT mix Hindi, Tamil, or any other language
- Do NOT use any words from other languages
- Write ONLY in pure English
- Keep sentences short and simple for voice
- Be helpful and direct
- STRICT: ONLY answer the specific question asked. Do NOT add unnecessary information or unrelated advice.""",
                'hi': """गंभीर चेतावनी: आप केवल हिंदी में जवाब दें। 
- अंग्रेजी, तमिल या अन्य भाषा मिक्स न करें
- कोई अन्य भाषा के शब्द न लिखें
- केवल शुद्ध हिंदी में लिखें
- वाक्य छोटे और सरल रखें (आवाज़ के लिए)
- सहायक और सीधे रहें
- सख्त नियम: केवल पूछे गए सवाल का जवाब दें। अनावश्यक जानकारी न जोड़ें।
[CRITICAL] सभी उत्तर पूरी तरह से हिंदी में होने चाहिए। अंग्रेजी शब्द या संकेत न लिखें।""",
                'ta': """முக்கியமான எச்சரிக்கை: நீங்கள் தமிழ் மொழியில் மட்டுமே பதிலளிக்கவும்। 
- ஆங்கிலம், இந்தி அல்லது வேறு மொழி கலக்க வேண்டாம்
- வேறு மொழியின் வார்த்தைகளை பயன்படுத்த வேண்டாம்
- தெளிவான தமிழ் மொழியை மட்டுமே பயன்படுத்தவும்
- வாக்கியங்களை குறுகியதாகவும் எளிமையாகவும் வைக்கவும் (குரல்க்கு)
- உதவிகரமாகவும் நேரடியாகவும் இருக்கவும்
- கடுமையான விதி: கேட்கப்பட்ட குறிப்பிட்ட கேள்விக்கு மட்டுமே பதிலளிக்கவும். தேவையற்ற தகவலைச் சேர்க்க வேண்டாம்।
[முக்கியம்] அனைத்து பதிலும் முழுவதுமாக தமிழ் மொழியில் இருக்க வேண்டும்। ஆங்கில வார்த்தை எழுத வேண்டாம்।""",
            }
            
            instruction = lang_instructions.get(language, 'Respond in English only. Do not mix languages. Only answer the specific question asked.')
            
            # Build context based on intent - ONLY for that specific intent
            context_parts = [
                "You are SAKHI, a helpful voice assistant for women entrepreneurs in rural India.",
                f"The user is asking about: {intent.upper()}",
                "Answer ONLY this specific question. Do NOT provide unrelated information.",
                "Do NOT suggest other topics unless directly asked.",
                "Keep response brief (2-3 sentences suitable for voice)."
            ]
            
            # Add STRICT intent-specific context that reinforces answering ONLY that question
            if intent == 'income':
                context_parts.append("STRICT: Answer ONLY about income/earnings/revenue. Do NOT mix with expense information.")
                context_parts.append("Focus on: How much was earned? When? From what source?")
                if extracted_data and extracted_data.get('amount'):
                    context_parts.append(f"Amount mentioned: ₹{extracted_data.get('amount')}")
                    
            elif intent == 'expense':
                context_parts.append("STRICT: Answer ONLY about expenses/costs/spending. Do NOT mix with income information.")
                context_parts.append("Focus on: What was spent? How much? On what?")
                if extracted_data and extracted_data.get('amount'):
                    context_parts.append(f"Amount mentioned: ₹{extracted_data.get('amount')}")
                    
            elif intent == 'market':
                context_parts.append("STRICT: Answer ONLY about market prices, trends, and selling advice for that specific product. Do NOT answer about other topics.")
                context_parts.append("Focus on: Price trends, selling recommendations, market conditions.")
                if extracted_data and extracted_data.get('product'):
                    context_parts.append(f"Product discussed: {extracted_data.get('product')}")
                if extracted_data and extracted_data.get('amount'):
                    context_parts.append(f"Price mentioned: ₹{extracted_data.get('amount')}")
                    
            elif intent == 'mentor':
                context_parts.append("STRICT: Provide ONLY business mentoring advice for their specific question. Do NOT provide general unrelated advice.")
                context_parts.append("Be encouraging and specific to their situation.")
                
            elif intent == 'scheme':
                context_parts.append("STRICT: Provide information ONLY about government schemes that match their need. Do NOT provide unrelated scheme information.")
                context_parts.append("Focus on: Eligibility, benefits, and application process for relevant schemes only.")
            
            # Build the final prompt with ULTRA-STRICT language enforcement
            context_str = "\n".join(context_parts)
            
            # Determine language name for emphasis
            lang_names = {
                'en': 'English',
                'hi': 'हिंदी (Hindi)',
                'ta': 'தமிழ் (Tamil)'
            }
            lang_name = lang_names.get(language, language)
            
            prompt = f"""LANGUAGE: {lang_name}

{instruction}

{context_str}

User Query: {user_query}

---RESPONSE RULES (ABSOLUTE)---
✓ Respond ONLY in {lang_name}
✓ Answer ONLY the {intent} question asked
✓ Do NOT add unrelated information
✓ Do NOT suggest other topics
✓ Keep response 2-3 sentences (voice-friendly)
✓ Be direct and helpful
✓ NO mixing languages
✓ NO English if responding in Hindi/Tamil
✓ NO Hindi if responding in English/Tamil  
✓ NO Tamil if responding in English/Hindi

Your response in {lang_name} only - FOCUSED ON THE {intent.upper()} QUESTION:"""
            
            logger.debug(f"Generating voice response for intent '{intent}' with strict context enforcement")
            response = model.generate_content(prompt)
            
            if response.text:
                logger.info(f"✅ Voice response generated for: {user_query[:50]}")
                return response.text
            return None
            
        except Exception as e:
            logger.error(f"❌ Error generating voice response: {str(e)}")
            return None

    @staticmethod
    def generate_mentor_advice(user_data: dict, language: str = 'en') -> Optional[str]:
        """
        Generate personalized mentor advice using Gemini
        
        Args:
            user_data: User profile and business data
            language: Language code (en, hi, ta)
            
        Returns:
            Personalized advice or None if Gemini unavailable
        """
        if not GEMINI_ENABLED:
            return None

        try:
            model = genai.GenerativeModel('gemini-pro')
            
            context = f"""
            You are a business mentor for women entrepreneurs in rural India.
            
            User Profile:
            - Business Type: {user_data.get('business_type', 'unknown')}
            - Location: {user_data.get('location', 'unknown')}
            - Monthly Income: ₹{user_data.get('monthly_income', 0)}
            - Monthly Expenses: ₹{user_data.get('monthly_expenses', 0)}
            
            Provide practical, actionable advice in {language} language.
            Be encouraging and specific to their situation.
            """
            
            query = user_data.get('question', 'How can I grow my business?')
            prompt = f"{context}\n\nQuestion: {query}"
            
            logger.debug(f"Generating mentor advice for business: {user_data.get('business_type')}")
            response = model.generate_content(prompt)
            
            if response.text:
                logger.info(f"✅ Mentor advice generated")
                return response.text
            return None
            
        except Exception as e:
            logger.error(f"❌ Error generating mentor advice: {str(e)}")
            return None

    @staticmethod
    def analyze_market_insight(product: str, price: float, language: str = 'en') -> Optional[str]:
        """
        Get market insights for a product using Gemini
        
        Args:
            product: Product name
            price: Current price
            language: Language code (en, hi, ta)
            
        Returns:
            Market insight or None if Gemini unavailable
        """
        if not GEMINI_ENABLED:
            return None

        try:
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""
            You are a market analyst for agricultural products in India.
            
            Product: {product}
            Current Price: ₹{price}
            
            Provide a brief market insight (2-3 sentences) in {language} language:
            - Is this a good price to sell now?
            - Market trend prediction
            - Selling recommendation
            
            Be practical and based on typical market behavior.
            """
            
            logger.debug(f"Analyzing market for: {product}")
            response = model.generate_content(prompt)
            
            if response.text:
                logger.info(f"✅ Market insight generated for {product}")
                return response.text
            return None
            
        except Exception as e:
            logger.error(f"❌ Error in market analysis: {str(e)}")
            return None

    @staticmethod
    def recommend_schemes(user_profile: dict, language: str = 'en') -> Optional[str]:
        """
        Recommend government schemes using Gemini
        
        Args:
            user_profile: User details
            language: Language code (en, hi, ta)
            
        Returns:
            Scheme recommendations or None if Gemini unavailable
        """
        if not GEMINI_ENABLED:
            return None

        try:
            model = genai.GenerativeModel('gemini-pro')
            
            prompt = f"""
            You are a government schemes expert for women entrepreneurs in India.
            
            Profile:
            - Business Type: {user_profile.get('business_type', 'unknown')}
            - Location: {user_profile.get('location', 'unknown')}
            - Income: ₹{user_profile.get('monthly_income', 0)}/month
            
            Recommend top 2-3 relevant government schemes in {language} language.
            For each scheme:
            1. Name
            2. Key benefits
            3. Eligibility
            4. How to apply (brief)
            
            Focus on real, active schemes only.
            """
            
            logger.debug(f"Recommending schemes for: {user_profile.get('business_type')}")
            response = model.generate_content(prompt)
            
            if response.text:
                logger.info(f"✅ Scheme recommendations generated")
                return response.text
            return None
            
        except Exception as e:
            logger.error(f"❌ Error recommending schemes: {str(e)}")
            return None
