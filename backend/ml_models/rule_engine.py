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
        """
        Comprehensive scheme handler with detailed information for farmers and women entrepreneurs
        """
        text_lower = text.lower()
        
        # Detect specific scheme interests
        scheme_type = 'general'
        
        # Loan schemes
        if any(w in text_lower for w in ['loan', 'karz', 'kadhan', 'udhar', 'capital']):
            scheme_type = 'loan'
        # Subsidy schemes
        elif any(w in text_lower for w in ['subsidy', 'anudan', 'aanudhan', 'grant']):
            scheme_type = 'subsidy'
        # Training schemes
        elif any(w in text_lower for w in ['training', 'skill', 'learn', 'siksha', 'payirchi']):
            scheme_type = 'training'
        # Women-specific
        elif any(w in text_lower for w in ['women', 'mahila', 'stree', 'pen', 'female']):
            scheme_type = 'women'
        # Farmer-specific
        elif any(w in text_lower for w in ['farmer', 'kisaan', 'krishi', 'kisan', 'agriculture']):
            scheme_type = 'farmer'
        
        # Get appropriate detailed response
        if self.language == 'en':
            responses = {
                'loan': "Great question! Here are the main loan schemes for women entrepreneurs like you:\n\n1. **Pradhan Mantri Mudra Yojana (PMMY)** - Up to ₹10 lakh loan for business, interest rates around 8-10%, easy approval, no collateral needed. Repayment over 5 years.\n\n2. **Stree Shakti Package by SBI** - Special for women with 50%+ ownership, lower interest rates (around 7-9%), priority processing, flexible repayment terms.\n\n3. **Mahila Udyam Nidhi** - Up to ₹1 crore for women-led businesses, interest rates competitive, GST benefits available.\n\n4. **Stand Up India Scheme** - SC/ST and women entrepreneurs can get up to ₹10 lakh with minimal paperwork.\n\nAll these require basic documents like Aadhaar, business plan, and income proof. Which one interests you most? I can guide you through the application process.",
                'subsidy': "Excellent! Here are key subsidy programs for women entrepreneurs in your sector:\n\n1. **Pradhan Mantri Rojgar Srijan Yojana** - Provides subsidy on loan interest and EPFO contributions for new businesses. Coverage up to ₹1 crore loan.\n\n2. **Scheme for Promotion of Innovation, Rural Industry & Entrepreneurship (ASPIRE)** - Grants and subsidy support up to 30-50% of project cost.\n\n3. **PMKVY Skill Development** - Free vocational training worth ₹8,000-15,000, 100% subsidy by government.\n\n4. **Tool Kit Subsidy** - Governments state-wise provide tool kits for women entrepreneurs at subsidized rates (40-50% subsidy).\n\nWhich sector are you in? I can find the exact subsidy available for your business type!",
                'training': "Perfect! Here are comprehensive training programs:\n\n1. **Pradhan Mantri Kaushal Vikas Yojana (PMKVY)** - Completely FREE skill training in 40+ courses. Digital marketing, accounting, handicrafts, food processing - whatever you want. Certification included!\n\n2. **NABARD Rural Entrepreneurship Program** - Free 6-month intensive training in business management, especially for rural women.\n\n3. **Udyam Sakhi Platform** - Online training modules, business mentorship, completely free. 40+ hours of video content.\n\n4. **NIESBUD Programs** - Government-run training in business planning, GST compliance, digital skills.\n\n5. **SHG Linkage Programs** - Government supports SHGs (Self Help Groups) with regular free training sessions.\n\nWhich skill would help your business grow the most? I can connect you with the right training program today!",
                'women': "Wonderful! Government has amazing programs just for women like you! Here's what's available:\n\n**FINANCIAL SUPPORT:**\n- Mahila Samman Saving Scheme: Safe savings with good returns\n- Sukanya Samriddhi Yojana: For girls' future\n- Mahila Udyam Nidhi: Up to ₹1 crore for business\n\n**LOANS (Women-Specific):**\n- PMMY for women: ₹10 lakh, 8-10% interest, no collateral\n- Stree Shakti SBI Loan: Special rates 7-9%\n- Stand Up India: ₹10 lakh for SC/ST/Women\n\n**BUSINESS SUPPORT:**\n- Free registration guidance\n- GST and compliance support\n- Market linkage programs\n- Insurance subsidies\n\n**TRAINING & MENTORSHIP:**\n- Free skill training (PMKVY)\n- Business mentor connection\n- Peer learning groups\n\nEverything is designed with women entrepreneurs in mind. What specific help do you need most right now - funding, training, or business mentorship?",
                'farmer': "Perfect! Here are agricultural and farming schemes tailored for farmer women:\n\n**FARMING SUPPORT:**\n1. **Pradhan Mantri Fasal Bima Yojana** - Crop insurance at just ₹300-700 per acre depending on crop. Complete loss coverage.\n\n2. **Soil Health Card Scheme** - Free soil testing and personalized fertilizer recommendations to increase yield by 10-20%.\n\n3. **National Horticulture Mission** - Subsidy up to 50% for horticulture/vegetable cultivation equipment.\n\n**INCOME SUPPORT:**\n1. **PM-Kisan Yojana** - ₹6,000 per year direct to your account (₹2,000 every 4 months) just for being a farmer.\n\n2. **Agricultural Loan** - Up to ₹3 lakh at subsidized rates, especially for women farmers.\n\n**VALUE ADDITION:**\n1. **PMEGP Agro-Processing** - Up to ₹25 lakh loan to start food processing, vegetable preservation, dairy units.\n\n2. **Kisan Vikas Patra** - Invest and get guaranteed returns on farming capital.\n\nAre you looking to expand farming, start food processing, or increase your current yield? Let me guide you!",
                'general': "Great! I help you find relevant government schemes. Here's a quick overview:\n\n**FINANCIAL SCHEMES:**\n- Loans up to ₹10 lakh with 0% processing fee\n- Interest subsidies available\n- No collateral needed for smaller loans\n\n**BUSINESS SCHEMES:**\n- Registration support\n- Business mentor connections  \n- Digital tools and software\n- Market linkage programs\n\n**SKILL SCHEMES:**\n- Free training programs (PMKVY)\n- Certification courses\n- Digital marketing training\n- Financial literacy programs\n\n**INSURANCE & SECURITY:**\n- Subsidized insurance\n- Pension schemes\n- Health coverage\n\nNow, tell me - what's your main challenge right now? Do you need:\n1. Money for starting or expanding?\n2. Skills or business training?\n3. Help with payments and finances?\n4. Or something else?\n\nI'll point you to the exact scheme that fits your situation!"
            }
        elif self.language == 'hi':
            responses = {
                'loan': "Bilkul! Mahila entrepreneurs ke liye ye loan schemes hain:\n\n1. **Pradhan Mantri Mudra Yojana** - 10 lakh tak loan, interest 8-10%, koi collateral nahi chahiye!\n\n2. **Stree Shakti SBI** - Women ke liye special, interest 7-9%, approval jaldi, flexible terms.\n\n3. **Mahila Udyam Nidhi** - 1 crore tak, competitive interest, GST benefits.\n\n4. **Stand Up India** - 10 lakh, SC/ST aur women ke liye special.\n\nSab mein sirf Aadhaar, business plan, aur income proof chahiye. Kaun sa loan lena chahti ho?",
                'subsidy': "Fantastic! Women entrepreneurs ke liye ye subsidy schemes hain:\n\n1. **Pradhan Mantri Rojgar Srijan** - Interest subsidy aur EPF contribution subsidy.\n\n2. **ASPIRE Scheme** - 30-50% project cost ka grants.\n\n3. **PMKVY Training** - Free training worth 8,000-15,000, bilkul free!\n\n4. **Tool Kit Subsidy** - 40-50% subsidy on tools and equipment.\n\nAapka business kaunse sector mein hai?",
                'women': "Bilkul! Mahila entrepreneurs ke liye government ka bohot support hai!\n\n**PAISA SUPPORT:**\n- Mahila Samman Saving Scheme\n- Mahila Udyam Nidhi: 1 crore tak\n- PMMY Loans: 10 lakh, 8-10% interest\n\n**FREE TRAINING:**\n- PMKVY: Bilkul Free\n- Business mentor connection\n- Skill courses\n\n**BUSINESS SUPPORT:**\n- GST help\n- Insurance subsidy\n- Market connect\n\nAapko kya chahiye - paisa, training, ya mentor? Mujhe batao!",
                'farmer': "Bilkul! Kisaan aur farming women ke liye:\n\n**FARMING HELP:**\n1. **Fasal Bima** - Crop insurance sirf 300-700 rupaye\n2. **Soil Health Card** - Free soil test aur advice\n3. **Horticulture Mission** - 50% subsidy on tools\n\n**INCOME SUPPORT:**\n1. **PM-Kisan** - 6,000 per year directly\n2. **Agricultural Loan** - 3 lakh subsidized rate par\n\n**PROCESSING:**\n- PMEGP: 25 lakh loan for food processing\n- Vegetable preservation equipment subsidy\n\nAp kya karna chahti ho - farming badhani hai ya processing start karni hai?",
                'general': "Bilkul! Schemes mein ye available hai:\n\n**PAISA SCHEMES:**\n- Loans 10 lakh tak\n- Interest subsidy\n- Koi collateral nahi\n\n**TRAINING:**\n- PMKVY bilkul free\n- Digital marketing\n- Business skills\n\n**BUSINESS:**\n- Mentor connection\n- GST support\n- Market linkage\n\nBatao - aapko kya chahiye? Paisa, training, ya kuch aur?"
            }
        else:  # Tamil
            responses = {
                'loan': "Sari! Penmani yathai indha kadhan thittagal ullathu:\n\n1. **Pradhan Mantri Mudra** - 10 laksham varai, interest 8-10%, saippukkanam vendaathu\n2. **Stree Shakti SBI** - Penmanirgalrkku special, interest 7-9%\n3. **Mahila Udyam Nidhi** - 1 crore varai\n4. **Stand Up India** - 10 laksham, penmanirgalrkku\n\nEtha kadhan patigal?",
                'women': "Puriyum! Penmani yathairgalrkku arasu thittagal ennam ullathu!\n\n**PANAM THITTAGAL:**\n- Mahila Udyam Nidhi\n- PMMY: 10 laksham\n- Interest subsidy\n\n**FREE PAYIRCHI:**\n- PMKVY: Saippukkanam vendaathu\n- Mentor connection\n\n**THOZHIL THITTAGAL:**\n- GST help\n- Insurance subsidy\n\nEnnai vendum?",
                'farmer': "Sari! Vellaikkaigalrkku:\n\n1. **Fasal Bima** - Crop insurance 300-700 mathumai\n2. **Soil Health** - Free soil test\n3. **Horticulture** - 50% subsidy\n\n**PANAM:**\n1. **PM-Kisan** - 6000 varushamh\n2. **Kadhan** - 3 laksham\n\nEtha pannuvey?",
                'general': "Sari! Tharavum thittagal:\n\n**PANAM:**\n- Kadhain 10 laksham\n- Interest subsidy\n\n**PAYIRCHI:**\n- PMKVY free\n- Digital marketing\n\n**THOZHIL:**\n- Mentor connection\n- GST help\n\nEnnai vendum?"
            }
        
        response = responses.get(scheme_type, responses['general'])
        
        return {
            'status': 'success',
            'message': response,
            'action': 'show_schemes',
            'scheme_type': scheme_type,
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
        """
        Comprehensive general question handler.
        Answers questions about the app, features, how to use, troubleshooting, business advice, etc.
        """
        text_lower = text.lower()
        
        # Detect what the user is asking about
        question_type = 'general'
        
        # About the app
        if any(w in text_lower for w in ['what is mahila', 'what is sakhi', 'about app', 'what do you do', 'who are you', 'kya ho', 'kaun ho', 'enna', 'yenna']):
            question_type = 'about_app'
        # How to use features
        elif any(w in text_lower for w in ['how to', 'kaise', 'eppadi', 'tips', 'guide', 'use', 'record']):
            question_type = 'how_to'
        # Features overview
        elif any(w in text_lower for w in ['feature', 'what can', 'do what', 'naa', 'facilities', 'tools']):
            question_type = 'features'
        # Business suggestions and advice
        elif any(w in text_lower for w in ['suggest', 'advice', 'suggestion', 'improve', 'increase', 'grow', 'business', 'strategy', 'how can', 'how should', 'tips for', 'sudha', 'sujhav', 'vyapar', 'salah', 'alochana']):
            question_type = 'business_advice'
        # Benefits and advantages
        elif any(w in text_lower for w in ['benefit', 'advantage', 'fayda', 'labh']):
            question_type = 'benefits'
        # Technical help
        elif any(w in text_lower for w in ['not working', 'error', 'bug', 'problem', 'issue', 'crash', 'samasya']):
            question_type = 'help'
        
        # Prepare response based on question type
        if self.language == 'en':
            responses = {
                'about_app': "Hello! I'm Sakhi, your AI business mentor! 🤖\n\nMahila Udyam is a complete business platform designed just for women entrepreneurs like you. I'm here to:\n\n✨ **Record Your Business** - Track income, expenses, sales, and calculate profits automatically\n✨ **Market Information** - Get real-time market prices for commodities you sell\n✨ **Government Schemes** - Find and understand all financial schemes, loans, subsidies for women\n✨ **Business Mentorship** - Connect with experienced mentors in your field\n✨ **Smart Analytics** - See your business growth with detailed reports\n✨ **Multi-Language Support** - Talk to me in English, Hindi, or Tamil\n\nEverything is voice-enabled, so you can just speak and I'll listen! No typing needed. What would you like help with today?",
                
                'business_advice': "Great! I'd love to help you grow your business! Here are my proven strategies:\n\n🎯 **SALES GROWTH:**\n- Track which products sell best using my analytics\n- Compare prices with market rates to set competitive pricing\n- Repeat successful sales patterns\n- Expand to nearby markets once you master local selling\n\n💰 **PROFIT MAXIMIZATION:**\n- Monitor your profit margin (healthy: 20-30%)\n- Reduce waste and loss - track every rupee spent\n- Negotiate better prices with suppliers\n- Bundle products to increase average sale value\n\n📈 **CUSTOMER RETENTION:**\n- Build loyalty by consistent quality\n- Remember regular customers and their preferences\n- Offer discounts on bulk purchases\n- Provide excellent service - word-of-mouth is your best marketing\n\n🤝 **NETWORK GROWTH:**\n- Join women entrepreneur groups\n- Share experiences with other businesses\n- Form buying cooperatives for bulk discounts\n- Help others - they'll help you back\n\n💡 **BUSINESS EXPANSION:**\n- Start with what you know - master single product first\n- Expand to related products once profitable\n- Look for government schemes to fund expansion\n- Connect with mentors before major decisions\n\n📱 **DIGITAL PRESENCE:**\n- Use WhatsApp to reach more customers\n- Show product photos to customers online\n- Keep a simple price list\n- Online marketing helps you sell 50% more!\n\n✅ **QUICK WINS - Do This This Week:**\n1. Track today's sales and profit exactly\n2. Compare your prices to market rates\n3. List 5 loyal customers and contact them\n4. Learn about 1 government scheme available to you\n\nWhat specific area do you want to focus on first?",
                
                'features': "Great! Here's what I can help you with:\n\n📊 **BUSINESS TRACKING:**\n- Record income from your sales\n- Track expenses and where your money goes\n- Record individual sales with products and prices\n- Automatically calculate your profit\n\n💰 **FINANCIAL INSIGHTS:**\n- See your profit/loss for today, week, or month\n- Track which products sell the most\n- Monitor your business growth\n\n🌾 **MARKET KNOWLEDGE:**\n- Check real-time market prices\n- Know when to buy and sell\n- Get commodity rates from across India\n\n💡 **GOVERNMENT SUPPORT:**\n- Find loans, subsidies, grants\n- Understand eligibility criteria\n- Get step-by-step guidance for applications\n\n👩‍🏫 **MENTORSHIP:**\n- Connect with business experts\n- Get personalized advice\n- Learn from successful entrepreneurs\n\n📚 **FREE TRAINING:**\n- Skill development programs\n- Business management courses\n- Digital marketing guidance\n\nWhich feature interests you most? I can guide you step-by-step!",
                
                'how_to': "Absolutely! Here's how to use the app:\n\n**RECORDING INCOME:**\nSay: \"I earned 500 rupees from vegetable sales\"\nI'll record it and ask for more details if needed.\n\n**TRACKING EXPENSES:**\nSay: \"I spent 200 rupees on supplies\"\nI'll categorize it and track it for you.\n\n**RECORDING SALES:**\nSay: \"I sold 10 tomato bundles for 300 rupees each\"\nI'll calculate total and store the transaction.\n\n**CHECKING PROFIT:**\nSay: \"What's my profit this month?\"\nI'll show you income minus expenses automatically.\n\n**MARKET PRICES:**\nSay: \"What's the current price of tomatoes?\"\nI'll check the official market prices for you.\n\n**FINDING SCHEMES:**\nSay: \"What loans are available for me?\"\nI'll explain all government schemes you qualify for.\n\n**GETTING MENTOR:**\nSay: \"I need business advice\"\nI'll connect you with the right mentor.\n\n**EVERYTHING IS IN YOUR LANGUAGE:**\nYou can speak English, Hindi, or Tamil - I understand all three!\n\nWhat would you like to do now?",
                
                'benefits': "Wonderful question! Here's how Mahila Udyam helps your business:\n\n💪 **BUSINESS CLARITY:**\n- Know exactly where your money comes from and goes\n- Track profit automatically\n- Make data-driven decisions\n\n⚡ **SAVE TIME:**\n- Voice-based recording takes just 10 seconds\n- No manual calculations needed\n- Automated reports\n\n💰 **MORE MONEY:**\n- Find schemes providing ₹10-100 lakh loans\n- Get subsidies up to 50%\n- Access government financial support\n\n📈 **GROW FASTER:**\n- Learn market trends\n- Compare prices and profit margins\n- Get expert mentorship for strategy\n\n😊 **STRESS-FREE:**\n- No complex software to learn\n- Simple voice commands\n- I explain everything in your language\n\n🎓 **SKILL UP:**\n- Free training programs\n- Digital marketing courses\n- Business planning guidance\n\n👥 **NOT ALONE:**\n- Connect with mentors\n- Learn from other entrepreneurs\n- Community support\n\nMost women using Mahila Udyam grow their business by 30-40% in the first year! Would you like to start tracking your business today?",
                
                'help': "No problem! I'm here to help! 🤝\n\n**COMMON ISSUES & SOLUTIONS:**\n\n❌ \"App is slow\"\n→ Try closing other apps and refresh the page\n\n❌ \"Voice is not working\"\n→ Check if your microphone permission is enabled\n→ Try a different browser (Chrome works best)\n\n❌ \"Language not working\"\n→ Select your language from the home screen first\n\n❌ \"Data not saved\"\n→ Make sure you're connected to internet\n→ Check if you have storage space\n\n❌ \"Can't find my transaction\"\n→ It's saved in your Dashboard - check there\n\n**QUICK TIPS:**\n✓ Speak clearly and slowly for best results\n✓ Use exact numbers like \"five hundred\" not \"5 hundred\"\n✓ Internet connection is needed for some features\n✓ Always confirm when I ask you to verify\n\n**STILL HAVING ISSUES?**\nTell me exactly what's happening - I'll guide you step by step!\n\nOr contact our support team at the bottom of the app.",
                
                'general': "Hi there! 👋\n\nI'm Sakhi, your AI business mentor in Mahila Udyam!\n\nI can help you with:\n💼 Recording income, expenses, and sales\n📊 Checking your profit and business analytics  \n🌾 Market prices for what you sell\n💰 Finding government loans and schemes\n👩‍🏫 Connecting with business mentors\n📚 Skill training and development\n💡 Business growth strategies\n\nWhat would you like to do? Just tell me - say something like:\n\n\"I earned 500 rupees\"\n\"What's my profit this month?\"\n\"Show me vegetable prices\"\n\"Give me business tips\"\n\"Find me a loan scheme\"\n\"Connect me with a mentor\"\n\nI understand English, Hindi, and Tamil! Which one do you prefer?"
            }
        elif self.language == 'hi':
            responses = {
                'about_app': "Namaste! Main Sakhi hoon, aapka AI business mentor! 🤖\n\nMahila Udyam ek complete business platform hai jo sirf aapjaise women entrepreneurs ke liye banaya gaya hai. Main aapko:\n\n✨ **Business Track** - Income, expense, sales record karein aur profit automatically calculate ho\n✨ **Market Jankari** - Real-time mandi ke bhav dekhein\n✨ **Sarkari Schemes** - Loans, subsidies, grants samjhne mein madad\n✨ **Mentor Connection** - Experienced mentors se sujhav lein\n✨ **Business Analytics** - Aapke business ki growth dekhein\n✨ **Bhasha Support** - English, Hindi, ya Tamil mein baat karein\n\nSab kuch voice se ho sakta hai! Typing ki zaroorat nahi. Aaj aapko kya madad chahiye?",
                
                'business_advice': "Bahut badhiya! Main aapke business ko grow karne mein madad kar sakti hoon! Ye mera salaah:\n\n🎯 **BIKRI BADHANE KE LIYE:**\n- Mera analytics dekhen - kaun sa product zyada bik raha hai\n- Market se apne rate compare karein\n- Jo products best bik rahe ho un ko repeat karein\n- Apne area mein success milo to naaye area mein expand karein\n\n💰 **PROFIT BADHANE KE LIYE:**\n- Apna profit margin check karein (20-30% achha hota hai)\n- Har paisa waste na ho iska dekh-bhaal karein\n- Suppliers se sasta rate negotiate karein\n- Products ko bundle karke becho - zyada paisa milega\n\n📈 **CUSTOMER LOYAL RAKNE KE LIYE:**\n- Hamesha quality achhi rakhen\n- Regular customers ko yaad rakhen\n- Bulk mein khareedne par discount do\n- Service achhi rakho - log aapke bare mein bolenge\n\n🤝 **NETWORK BADHANE KE LIYE:**\n- Women entrepreneur groups mein join karein\n- Doosre businesses se baat karein\n- Saath mein bulk mein khareedne ka group banao\n- Doosron ki madad karo to aapki bhi hogi\n\n💡 **BUSINESS EXPAND KARNE KE LIYE:**\n- Ek product par achche se focus karein pehle\n- Ek successful ban gaya to doosri add karein\n- Government schemes se funding lo expansion ke liye\n- Mentor se sujhav lo badi decisions se pehle\n\n📱 **ONLINE PRESENCE BADHANE KE LIYE:**\n- WhatsApp se customers ko reach karein\n- Products ki photos dikhaein\n- Price list ready rakhen\n- Online marketing se 50% zyada sale ho sakta hai!\n\n✅ **IS HAFTE KI PRIORITY:**\n1. Aaj ka sale aur profit exactly track karein\n2. Apna rate market ke saath compare karein\n3. 5 loyal customers ko call karke pucho kaisa chal raha hai\n4. 1 sarkari scheme ke bare mein seekhen\n\nKaun sa area par focus karna chahte ho pehle?",
                
                'features': "Bilkul! Main aapko isme madad kar sakti hoon:\n\n📊 **BUSINESS TRACKING:**\n- Income record karein\n- Expense track karein\n- Sales likhen\n- Profit automatically calculate ho\n\n💰 **FINANCIAL REPORT:**\n- Today, week, ya month ka profit dekhein\n- Kaun sa product zyada bik raha hai\n- Business kitni grow kar raha hai\n\n🌾 **MARKET BHAV:**\n- Real-time market prices\n- Pura India se current rates\n\n💡 **SARKARI SCHEMES:**\n- Loans, subsidies, grants\n- Kaise apply karein guide\n\n👩‍🏫 **MENTORSHIP:**\n- Business experts se connect karein\n- Personal advice lein\n\n📚 **FREE TRAINING:**\n- Skills seekhne ke courses\n- Business management training\n\nKaun sa feature use karna hai? Main guide kar dunga!",
                
                'how_to': "Bilkul! Iska use kaise karein:\n\n**INCOME RECORD KAREIN:**\nKahen: \"Mne 500 rupaye kamaye sabji se\"\nMain record kar dunga.\n\n**EXPENSE TRACK KAREIN:**\nKahen: \"200 rupaye supplies par lagaye\"\nMain categorize kar dunga.\n\n**SALES LIKHEN:**\nKahen: \"10 bundel tamatar 300 rupaye mein becha\"\nMain total calculate kar dunga.\n\n**PROFIT DEKHEIN:**\nKahen: \"Is mahine mera profit kya hai?\"\nMain calculate kar ke dikhaunga.\n\n**MARKET BHAV:**\nKahen: \"Tamatar ka price kya hai?\"\nMain official rates dekhaunga.\n\n**SCHEME DHUNDHEN:**\nKahen: \"Mujhe loan chahiye\"\nMain sari schemes samjhaunga.\n\n**MENTOR CONNECT KAREIN:**\nKahen: \"Mujhe business advice chahiye\"\nMain right mentor find kar dunga.\n\nAji kya karna hai?",
                
                'benefits': "Bahut badhiya! Mahila Udyam se ye fayde hote hain:\n\n💪 **CLARITY:**\n- Pata chalega paise kahan se aate-jate hain\n- Profit track ho sakta hai\n\n⚡ **TIME BACHAYE:**\n- Sirf 10 second mein record ho jaye\n- Calculation automatic\n\n💰 **ZYADA PAISA:**\n- 10-100 lakh till loan mil sakte hain\n- 50% subsidy available\n\n📈 **BUSINESS GROW KARE:**\n- Market trends samjhein\n- Expert advice lein\n\n😊 **STRESS NAHI:**\n- Simple voice commands\n- Aapki language mein samjhaunga\n\n🎓 **SKILL DEVELOP:**\n- Free training programs\n- Digital marketing seekhein\n\n👥 **AKELE NAHI:**\n- Mentors hain\n- Customer community hai\n\nJyadatar women ke business 30-40% grow ho jayat! Aaj hi start karoge?",
                
                'help': "Koi problem nahi! Main madad kar dunga! 🤝\n\n**COMMON ISSUES:**\n\n❌ \"App slow hai\"\n→ Doosri apps band karein\n\n❌ \"Voice nahi sunai de raha\"\n→ Microphone permission check karein\n→ Chrome use karein\n\n❌ \"Language nahi change ho raha\"\n→ Home se language select karein\n\n❌ \"Data save nahi ho raha\"\n→ Internet check karein\n\n❌ \"Transaction nahi mila\"\n→ Dashboard mein dekhein\n\n**TIPS:**\n✓ Clearly aur slowly bolein\n✓ Numbers clear bolein\n✓ Internet connection zaroori hai\n\n**AJAIB ISSUE HAI?**\nMain guide kar dunga! Batao kya problem hai.",
                
                'general': "Namaste! 👋\n\nMain Sakhi hoon, aapka AI business mentor!\n\nMain maadadh kar sakti hoon:\n💼 Income, expense, aur sales record mein\n📊 Profit calculate karne mein\n🌾 Market prices batane mein\n💰 Government schemes dhundne mein\n👩‍🏫 Mentors connect karne mein\n📚 Free training provide karne mein\n💡 Business growth ke ideas dene mein\n\nAaj kya karna hai? Bolien:\n\n\"Mne 500 rupaye kamaye\"\n\"Mera profit kya hai?\"\n\"Tamatar ka price batao\"\n\"Business tips do\"\n\"Mujhe loan chahiye\"\n\nMain Hindi, English, ya Tamil samjhti hoon!"
            }
        else:  # Tamil
            responses = {
                'about_app': "Vanakkam! Naan Sakhi, ungal AI business mentor! 🤖\n\nMahila Udyam - penmanikalkkum business platform!\n\n✨ **Thozhil Track** - Income, expense, sales padhivu pannu, profit automatic kalkulat\n✨ **Santhai Vilai** - Real-time price parunga\n✨ **Arasu Thittam** - Loan, subsidy guide\n✨ **Mentor Connect** - Business expert salah\n✨ **Analytics** - Business grow parunga\n✨ **Moli Support** - Tamil, Hindi, English\n\nEllaith voice-la! Ethukkalam shettuvaikal vendaathu. Indru ennai vendum?",
                
                'business_advice': "Mika! Ungal thozhil velikai karikka udavi pannren! Indha sujhavugal:\n\n🎯 **VIKKAI ADIGAPPATTUNGA:**\n- Yeth poruli mika vikkukkirathu athiya parunga\n- Ungal vilai aum santhai vilai compare pannunga\n- Best vikkai repeat pannunga\n- Puram areas-la vikkai adigappaduthunga\n\n💰 **LAABHAM ADIGAPPATTUNGA:**\n- Profit percentage check pannunga (20-30% sari)\n- Panam waste aagavendum illa\n- Suppliers-la vilai negotiate pannunga\n- Poruli bundle pannunga - miga vikrai karum\n\n📈 **CUSTOMER LOYAL VAIKUNGA:**\n- Quality nalla vaikunga\n- Regular customers mukkavey yaadil vaikunga\n- Bulk vikkai-la discount pannum\n- Service nalla vaikunga - kathanum pantuvargal\n\n🤝 **VEDHANAI ADIGAPPADUTHUNGA:**\n- Women entrepreneur groups-la join pannum\n- Other businesses-l nilaikuravanargal-u inaicen\n- Bulk vikkai groupu panunga\n- Others-ai madatai pannuma to ungaik-um madatai pannuvargal\n\n💡 **THOZHIL VELIKAI:**\n- Oru poruli nalla understand pannum puthakku\n- Vaalka velikai paya doosri porul add pannum\n- Government schemes irunthu funding vaangum\n- Mentor-u sujhav patukkum\n\n📱 **ONLINE PRESENCE:**\n- WhatsApp-la customers-ai reach pannunga\n- Poruli photos kaattunga\n- Price list prepare pannunga\n- Online marketing-la 50% velikai adigappaduthum!\n\n✅ **INDHA VAARAM PRIORITIES:**\n1. Indru vikkai aiyum laabham track pannunga\n2. Ungal vilai santhai-u compare pannunga\n3. 5 loyal customers-ai sollunga\n4. 1 government scheme about seekhunga\n\nYeth area-la focus pannuvey?",
                
                'features': "Sari! Main atha madatai pannren:\n\n📊 **THOZHIL TRACK:**\n- Income padhivu\n- Expense track\n- Sales store\n- Profit auto\n\n💰 **REPORT:**\n- Profit parunga\n- Best products parunga\n\n🌾 **SANTHAI BHAV:**\n- Real-time price\n- Pura India rate\n\n💡 **ARASU THITTAM:**\n- Loans, subsidy\n\n👩‍🏫 **MENTOR:**\n- Expert advice\n\n📚 **FREE TRAINING:**\n- Skill courses\n\nEnnai pannunga?",
                
                'how_to': "Sari! Eppadi use pannunga:\n\n**INCOME PADHIVU:**\nSollunga: \"Naan 500 rupai kaaikari vittirkkiil pannigal\"\nNaans padhivu pannren.\n\n**EXPENSE TRACK:**\nSollunga: \"200 rupai supplies vittey\"\nTrackkik pannren.\n\n**SALES LIKHEN:**\nSollunga: \"10 mozhakku 300 vitey\"\nTotal kalkulat pannren.\n\n**PROFIT PARUNGA:**\nSollunga: \"Indha maadham profit enna?\"\nKalkulat pannutuy.\n\n**PRICE CHECK:**\nSollunga: \"Kaaikari vilai enna?\"\nOfficial rate kaattukkalum.\n\n**SCHEME:**\nSollunga: \"Enakku kadhan vendum\"\nEllaith explain pannren.\n\n**MENTOR:**\nSollunga: \"Advice vendum\"\nMentor connect pannren.\n\nIndru enna pannunga?",
                
                'benefits': "Mika! Magdala irukkum:\n\n💪 **CLARITY:**\n- Panam engirunthu varukkirathu atiaya parunga\n- Profit track\n\n⚡ **KALAM RAKKAI:**\n- 10 second mein padhivu\n- Auto kalkulat\n\n💰 **MIGATHUM PANAM:**\n- 10-100 laksham kadhan\n- 50% subsidy\n\n📈 **THOZHIL VELIKAI:\n- Market trends parunga\n- Expert salah\n\n😊 **ADHIGARAM ILLA:**\n- Simple voice\n- Tamil-la sozhuvikal\n\n🎓 **SKILL:**\n- Free training\n- Digital marketing\n\n👥 **THANIKAL ILLA:**\n- Mentors un\n- Community un\n\nIndru start pannuvey?",
                
                'help': "Problem illa! Main madatai pannren! 🤝\n\n**COMMON ISSUES:**\n\n❌ \"App slow\"\n→ Other apps close pannunga\n\n❌ \"Voice illa\"\n→ Microphone check pannunga\n→ Chrome use pannunga\n\n❌ \"Language nai change\"\n→ Home-la select pannunga\n\n❌ \"Data save illa\"\n→ Internet check pannunga\n\n**TIPS:**\n✓ Clear sollunga\n✓ Internet vendum\n\nEnnai madatai pannren!",
                
                'general': "Vanakkam! 👋\n\nNaan Sakhi, ungal AI mentor!\n\nMain madatai pannren:\n💼 Income, expense padhivu\n📊 Profit kalkulat\n🌾 Price parunga\n💰 Scheme dhundhunga\n👩‍🏫 Mentor connect pannum\n📚 Training\n💡 Business sujhavugal\n\nSollunga:\n\"Naan 500 panigal\"\n\"Profit enna?\"\n\"Vilai enna?\"\n\"Business tips sol\"\n\"Kadhan vendum\"\n\nTamil, Hindi, English! Enna moli?"
            }
        
        response = responses.get(question_type, responses['general'])
        
        return {
            'status': 'success',
            'message': response,
            'action': 'info',
            'extracted_data': {},
        }
