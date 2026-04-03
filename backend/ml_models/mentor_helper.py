"""
Mahila Udyam - Mentor AI Helper
Generate personalized mentor responses using Gemini AI
"""
import logging
from typing import Optional, Dict
from .gemini_helper import GeminiHelper

logger = logging.getLogger(__name__)


class MentorAIHelper:
    """
    Helper class for AI-powered mentor responses
    Generates personalized business advice using Gemini
    """

    # Mentor specializations for context
    MENTOR_SPECIALIZATIONS = {
        'organic': 'Organic Farming',
        'dairy': 'Dairy Business',
        'food': 'Food Processing',
        'digital': 'Digital Marketing & E-commerce',
        'handicraft': 'Handicraft & Artisan Work',
    }

    MENTOR_EXPERTISE = {
        'organic': 'Organic farming techniques',
        'dairy': 'Dairy farming and milk production',
        'foodProcessing': 'Food processing and preservation',
        'handicraft': 'Handicraft and artisan products',
        'digitalMarketing': 'Digital marketing and online sales',
    }

    @staticmethod
    def get_mentor_context(mentor_data: dict) -> str:
        """Build mentor context for better responses"""
        name = mentor_data.get('name', 'Mentor')
        specialization_key = mentor_data.get('specializationKey', 'organic')
        expertise_key = mentor_data.get('expertiseKey', 'organic')
        experience = mentor_data.get('experience_years', 10)
        
        specialization = MentorAIHelper.MENTOR_SPECIALIZATIONS.get(specialization_key, 'Business')
        expertise = MentorAIHelper.MENTOR_EXPERTISE.get(expertise_key, 'Business')
        
        context = f"""
You are {name}, an experienced business mentor with {experience} years in {specialization}.
Your expertise: {expertise}

You are helping a woman entrepreneur in rural India with her business.
Provide practical, actionable advice that is:
- Specific to her business context
- Culturally sensitive
- Focused on sustainable growth
- Practical with limited resources
- Encouraging and supportive

Keep responses concise (2-3 paragraphs) and directly address her question.
"""
        return context

    @staticmethod
    def generate_mentor_response(
        question: str,
        mentor_data: dict,
        language: str = 'en',
        conversation_history: list = None
    ) -> Optional[str]:
        """
        Generate a mentor response using Gemini AI
        
        Args:
            question: User's question
            mentor_data: Mentor profile information
            language: Language code (en, hi, ta)
            conversation_history: Previous messages for context
            
        Returns:
            Generated response or None if Gemini unavailable
        """
        if not GeminiHelper.is_available():
            logger.debug("Gemini not available for mentor response")
            return None

        try:
            mentor_context = MentorAIHelper.get_mentor_context(mentor_data)
            
            # Build conversation context
            history_text = ""
            if conversation_history and len(conversation_history) > 0:
                # Include last 3-5 messages for context
                recent_messages = conversation_history[-5:]
                history_text = "\nPrevious conversation:\n"
                for msg in recent_messages:
                    msg_type = msg.get('message_type', 'response')
                    content = msg.get('message', '')
                    role = "User" if msg_type == 'query' else "You"
                    history_text += f"\n{role}: {content}"

            # Language-specific instructions
            lang_instructions = {
                'en': 'Respond in clear, simple English',
                'hi': 'हिंदी में जवाब दें। सरल और व्यावहारिक सुझाव दें।',
                'ta': 'தமிழ் மொழியில் பதிலளிக்கவும். எளிய மற்றும் நடைமுறை பরामர்சை கொடுக்கவும்.',
            }
            
            instruction = lang_instructions.get(language, 'Respond in English')
            
            # Build the final prompt
            prompt = f"""{mentor_context}

{instruction}

{history_text}

User's Current Question: {question}

Provide helpful, specific advice based on your expertise."""
            
            logger.debug(f"Generating mentor response for: {question[:50]}")
            response = GeminiHelper.enhance_response(question, language, prompt)
            
            if response:
                logger.info(f"✅ Mentor response generated")
                return response
            return None
            
        except Exception as e:
            logger.error(f"❌ Error generating mentor response: {str(e)}")
            return None

    @staticmethod
    def get_mentor_tips(
        business_type: str,
        language: str = 'en'
    ) -> Optional[str]:
        """
        Generate quick tips for a business type
        
        Args:
            business_type: Type of business (dairy, organic, food, etc.)
            language: Language code (en, hi, ta)
            
        Returns:
            Tips or None if Gemini unavailable
        """
        if not GeminiHelper.is_available():
            return None

        try:
            prompt = f"""
You are a business mentor for women entrepreneurs in India.
Provide 3-4 quick, actionable tips for someone starting/running a {business_type} business.
Focus on:
1. Cost-effective solutions
2. Local market advantages
3. Sustainable practices
4. Profit maximization

Keep it concise and practical. Respond in {language} language.
"""
            
            logger.debug(f"Generating tips for {business_type}")
            response = GeminiHelper.enhance_response("", language, prompt)
            
            if response:
                logger.info(f"✅ Business tips generated for {business_type}")
                return response
            return None
            
        except Exception as e:
            logger.error(f"❌ Error generating tips: {str(e)}")
            return None

    @staticmethod
    def create_fallback_response(question: str, mentor_data: dict) -> str:
        """
        Create a fallback response when Gemini is unavailable
        This is a basic rule-based response
        
        Args:
            question: User's question
            mentor_data: Mentor information
            
        Returns:
            Fallback response string
        """
        mentor_name = mentor_data.get('name', 'Mentor')
        specialization = MentorAIHelper.MENTOR_SPECIALIZATIONS.get(
            mentor_data.get('specializationKey', 'organic'),
            'Business'
        )
        experience = mentor_data.get('experience_years', 10)
        
        fallback_responses = {
            'income': f"Based on my {experience} years in {specialization}, here are proven ways to increase income:\n1. Focus on quality products - better quality commands premium prices\n2. Build customer loyalty through consistent service\n3. Explore multiple channels - direct sales, local markets, wholesale\n4. Calculate profit margins to identify high-margin products\n5. Consider seasonal products that complement your main business",
            
            'cost': f"To reduce operational costs in {specialization}:\n1. Buy directly from producers/suppliers to cut middlemen costs\n2. Join cooperatives for bulk purchasing discounts\n3. Minimize waste - plan production based on demand\n4. Use local resources and traditional methods where possible\n5. Track all expenses to identify unnecessary spending",
            
            'market': f"Market insights for {specialization}:\n1. The {specialization} market is growing - consumers want quality and authenticity\n2. Check local mandis and market rates regularly - timing matters\n3. Build relationships with established buyers and traders\n4. Weather and seasons affect prices - plan your production accordingly\n5. Digital platforms are opening new sales channels - explore them",
            
            'growth': f"For sustainable growth in {specialization}:\n1. Start with what you know and do well - perfect your craft first\n2. Reinvest 20-30% of profits back into your business\n3. Gradually expand - add new products or customers carefully\n4. Keep learning - attend trainings and workshops\n5. Document your processes - this helps in scaling",
            
            'technology': f"Technology in {specialization}:\n1. WhatsApp Business for customer communication\n2. Simple apps to track inventory and sales\n3. Online platforms like JioMart, Amazon for reaching more customers\n4. Digital payment options increase customer convenience\n5. Start simple - use tools you understand before expanding",
            
            'skill': f"Skill development in {specialization}:\n1. Learn from experienced practitioners in your field\n2. Government and NGO programs offer free trainings\n3. Certifications (like FSSAI for food) add credibility\n4. Quality improvement translates to better prices\n5. Invest in developing specialized skills for differentiation",
            
            'loan': "Government schemes and loans for women entrepreneurs:\n1. Pradhan Mantri Mudra Yojana offers loans up to ₹10 lakhs\n2. State-specific schemes vary - check your state government website\n3. Banks now have dedicated women entrepreneur programs\n4. Online application makes getting loans easier\n5. Have your business plan and financial records ready",
            
            'default': f"Thank you for your question! I'm {mentor_name} with {experience} years of experience in {specialization}. To give you better advice, could you be more specific about:\n- What aspect of your business are you asking about?\n- Are you facing challenges or looking to grow?\n- What resources or constraints do you have?\n\nWith more details, I can provide personalized guidance for your specific situation."
        }
        
        # Try to match question to response type
        question_lower = question.lower()
        for key in ['income', 'cost', 'market', 'growth', 'technology', 'skill', 'loan']:
            if key in question_lower:
                return fallback_responses[key]
        
        return fallback_responses['default']
