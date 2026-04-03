"""
Mahila Udyam - Language Responses (Sakhi System Prompt)
Multi-language response templates: English, Hindi (Romanized), Tamil (Romanized)

CORE RULES:
1. Strict language purity - NO mixing languages
2. Numbers pronounced in response language - NEVER use English numbers in Hindi/Tamil responses
3. Natural conversational tone - NO robotic phrases
4. Voice output format - NO markdown, bullets, symbols
5. Always end with natural follow-up question in user's language
6. Identity: "I am Sakhi" - never "I am AI/chatbot"

RESPONSE GUIDELINES:
- Use natural phrases: "So the thing is", "Honestly", "What I would do", "So basically"
- Avoid robotic phrases: "Certainly", "Absolutely", "As an AI", "I understand your concern"
- Hindi: Natural spoken Hindi, not textbook
- Tamil: Natural spoken Tamil, not formal
- English: Warm Indian English, confident and direct
"""

# NUMBER CONVERSION UTILITIES
class NumberConverter:
    """Convert numbers to words in different languages"""
    
    HINDI_ONES = ['', 'ek', 'do', 'teen', 'char', 'paanch', 'chhe', 'saat', 'aath', 'nau']
    HINDI_TENS = ['', 'das', 'bis', 'tees', 'chalis', 'pachas', 'saath', 'sattar', 'aassi', 'nabbey']
    HINDI_SCALES = ['', 'hazaar', 'lakh', 'crore']
    
    TAMIL_ONES = ['', 'onru', 'irandu', 'moonru', 'naan', 'aynthu', 'aru', 'aelu', 'ettu', 'onbathu']
    
    @staticmethod
    def rupees_to_hindi(amount):
        """Convert rupees amount to Hindi words"""
        if amount == 0:
            return 'zero'
        
        # Special cases for common amounts in schemes
        conversions = {
            50: 'pachas',
            100: 'sau',
            500: 'paanch sau',
            1000: 'ek hazaar',
            5000: 'paanch hazaar',
            10000: 'das hazaar',
            50000: 'paanch hazaar',
            100000: 'ek lakh',
            300000: 'teen lakh',
            500000: 'paanch lakh',
            1000000: 'das lakh',
            5000000: 'paanch lakh',
            10000000: 'ek crore',
        }
        
        if amount in conversions:
            return f"{conversions[amount]} rupaye"
        
        # Fallback for other amounts
        return f"{amount} rupaye"
    
    @staticmethod
    def rupees_to_tamil(amount):
        """Convert rupees amount to Tamil words"""
        if amount == 0:
            return 'zero'
        
        conversions = {
            50: 'aimpathu',
            100: 'nooru',
            500: 'aynbathu nooru',
            1000: 'onru aayiram',
            5000: 'aynthu aayiram',
            10000: 'pattu aayiram',
            50000: 'aimpathu aayiram',
            100000: 'onru laakshm',
            300000: 'moonru laakshm',
            500000: 'aynthu laakshm',
            1000000: 'pattu laakshm',
            5000000: 'aimpathu laakshm',
            10000000: 'onru crore',
        }
        
        if amount in conversions:
            return f"{conversions[amount]} rubai"
        
        return f"{amount} rubai"


class LanguageResponses:
    """
    Central response repository for all intents in 3 languages.
    SAKHI SYSTEM RULES:
    - Natural conversation, not robotic
    - All numbers in response language
    - End with follow-up question
    - Voice format (no markdown)
    """

    RESPONSES = {
        # INCOME INTENTS
        'income_success': {
            'en': 'So you made forty rupees from vegetables - that is brilliant! Let me save that for you. Tell me, is this something you sell regularly?',
            'hi': 'To aap ne sau rupaye ki aay sabziyon se - bahut achha hai! Mein yeh save kar deta hoon. Batao, kya ye regular bikri ho raha hai?',
            'ta': 'So ungal nooru rubai kozhumpukalilirunthu pannigal - puriyum! Ithai save pannren. Sollunga, ida niraiya naal vidaivel ayya?',
        },
        'income_query': {
            'en': 'Alright! So tell me how much money came in and what you sold or what work you did to earn it. Be as specific as you can.',
            'hi': 'Theek hai! To kitne paise aaye aur kya becha ya kya kaam kiya? Jitna detail de saken utna dena.',
            'ta': 'Sarivanam! To ethanai pana vanthu, enna vittey athavaa enna pannigal? Saariamaga sollugal.',
        },
        'income_this_month': {
            'en': 'So far this month you have brought in about rupees from different sources. The best performing source was from your vegetable sales. Keep pushing that!',
            'hi': 'Is mahine aapne total hazaar rupaye ki aay ki hai. Sabse zyada bikri sabziyon se hue. Usey aur badhao!',
            'ta': 'Indha maadham innum laksham rubai sambalam pantey. Sagalikum kozhumpukalilirunthu sagaligal. Athai athal thanra pannunga!',
        },
        
        # EXPENSE INTENTS
        'expense_success': {
            'en': 'Understood. So you spent rupees on getting supplies - that makes sense. I have saved that. Now, did you make more from selling compared to what you spent?',
            'hi': 'Samajh gaya. To aapne paanch sau rupaye supplies par kharcha kiye. Main yeh record kar deta hoon. Ab batao, sale mein zyada kama?',
            'ta': 'Puriyum! So ungal ayiram rupai supplies-kkaga selava panninargal. Ithai save pannren. Pinnadi, vikkai nera mattum sakiya?',
        },
        'expense_category': {
            'en': 'So what did you spend money on? Tell me - was it supplies, or rent, or travel, or something else?',
            'hi': 'Aapne paise kisme kharch kiye? Supplies par, ya rent par, ya travel par, ya aur kuch?',
            'ta': 'Pana entakkaga selava panninargal? Sukkam ay, valavaram ay, valisaktu ay, aythuvaa?',
        },

        # SALES INTENTS
        'sales_success': {
            'en': 'Perfect! So you sold rupees worth of vegetables today - that is solid work. How are your customers responding to your products?',
            'hi': 'Bahut achha! To aapne sau rupaye ka samaan becha - shukriya! Customers kaise respond kar rahe hain?',
            'ta': 'Mika! So ungal naazh rubai vilakkai pannigal - puriyum! Aaikal ennai solrinargal?',
        },
        'sales_product': {
            'en': 'Okay so what did you sell? Tell me the product name, how many you sold, and what price you got for it.',
            'hi': 'Theek hai, kya becha? Product name, quantity, aur price batayein.',
            'ta': 'Sarivanam, enna vittey? Porul peru, alavai, vilai sollugal.',
        },
        'sales_low_warning': {
            'en': 'I am noticing your sales have been a bit slow this week. What is going on? Are you facing any challenges in selling?',
            'hi': 'Dekho, is hafte bikri thode kam ho gayi. Kya problem aa raha hai? Selling mein koi samasya hai?',
            'ta': 'Parunga, indha varam vikkai theda irukku. Enna aaguthu? Vikkai panrathu kharmanam ay?',
        },

        # PROFIT INTENTS
        'profit_positive': {
            'en': 'Wonderful news! This month you made a profit of rupees. You are doing really well. What did you do differently this month that made this happen?',
            'hi': 'Bahut achha! Is mahine aapne lakh rupaye ki profit kathi. Aap bahut achchhe kar rahe ho. Kya alag tha is mahine?',
            'ta': 'Sundara sandhesam! Indha maadham lakshm rubai laabham kittiyirukku. Nilai mika irukku. Enna maarivey pandey?',
        },
        'profit_planning': {
            'en': 'Okay so your current profit margin is not bad, but we can definitely make it better. Let me ask you - where do you think you can cut costs or increase sales?',
            'hi': 'Aapkaa margin theek hai par aur badhaya ja sakta hai. Bataiye, kahan aap kharcha kam kar sakte ho ya sales badhda sakte ho?',
            'ta': 'Ungal laabham sarivanam irunthalum, athai adig kazippadattum. Sollunga - epdi kharcha kumayavum, vikkai adikavum?',
        },
        'profit_loss_concern': {
            'en': 'I can see you had a loss this month. That happens sometimes. Let us figure out where things went wrong and how we can fix it. What do you think was the biggest challenge?',
            'hi': 'Mujhe laga is mahine aapko nuksaan hua. Yeh hota hai. Iska kya kaaran tha aur hum iska solution nikaal sakte hain. Sabse bada problem kya tha?',
            'ta': 'Indha maadham nattam aagiyatu. Ithu sagum irukku. Yaar ethu aaguthu? Sollugal - yen aaguthu?',
        },

        # BUSINESS REGISTRATION & UDYAM
        'udyam_registration': {
            'en': 'So the thing is, registering your business as an MSME is actually very simple and takes just a few minutes. It costs absolutely nothing. Once you register, you become eligible for many government schemes and loans. Have you done this yet?',
            'hi': 'Dekho, MSME registration bohot aasan hai aur sirf kauch minutes mein complete ho jata hai. Kharcha bhi kuch nahi ata. Register hone se aap kaunch schemes aur loans ke liye qualified ho jate ho. Aapne kiya hai?',
            'ta': 'Parunga, MSME registration karaal saadi - kauch minutes-le mudindidum. Kharcha illai. Registration pannunkalum, neenga nikru thittagalkkum eligible-aga padirgal. Pandey ey?',
        },
        'gst_registration': {
            'en': 'If your yearly sales cross rupees then you will need a GST number. GST registration is also very straightforward and once you have it, you can give invoices to your customers. It helps them with tax benefits. Want me to show you how?',
            'hi': 'Agar aapki annual sales 40 lakh cross kar jaye to GST lena zaruri hai. Registration bohot simple hai aur invoices de sakte ho customers ko. Aapko tax benefits milte hain. Main batau?',
            'ta': 'Ungal nuandu nuandu vikkai 40 laakshm valakiya pona GST vandidum. Saadi registration la. Adimai thozhilaaikal thanku pattalum. Sollugal?',
        },

        # SCHEMES - MUDRA LOAN
        'scheme_mudra_intro': {
            'en': 'MUDRA Loan is specifically for people like you. It is a government scheme that gives you money to start or grow your business. There are three levels - Shishu, Kishore, and Tarun. Shishu gives you up to rupees. Which level do you think you need?',
            'hi': 'MUDRA Loan aapke jaise log ke liye banaya gaya hai. Sarkaari scheme hai jo aapko business shuru ya expand karne ke liye paisa deta hai. Teen level hain - Shishu, Kishore, aur Tarun. Shishu mein fifty thousand mil sakte ho. Aapko kaun sa level chahiye?',
            'ta': 'MUDRA Loan ungalukka panntappattathu. Arasin thittam - neenga business shurru ay expand pannumpottu thandi kodukkum. Muunu padippu ullathu - Shishu, Kishore, Tarun. Shishu-la aimpathu aayiram rubai kidaikal. Evat padippu vendum?',
        },
        'scheme_mudra_shishu': {
            'en': 'The Shishu level of MUDRA gives you up to rupees for starting a new business or expanding a small one. You need a basic business idea, some documents, and a bank account. Honestly it is the easiest loan to get. The site is mudra.org.in. Want me to tell you the next steps?',
            'hi': 'Shishu level mein fifty thousand tak mil sakta hai. Aapko bas ek business idea chahiye, kuch documents, aur bank account. Sach kahu to yeh sabse aasan loan hai milaana. Site hai mudra org in. Next steps bata du?',
            'ta': 'Shishu-la aimpathu aayiram rubai kidaikal. Vanampakam - oru negathiram ideology, documents, bank account irundal madi. Satyam sollan kontu - idu sagile asenai loan. mudra.org.in. Pinnadi yaar pannanum?',
        },
        'scheme_mudra_kishore': {
            'en': 'Kishore is the next level - it gives up to rupees for businesses that are already running and need expansion. This is for growing businesses. You might need more documentation, like your past income records or business proof. The process takes about two to three weeks. Are you growing enough to consider this?',
            'hi': 'Kishore next level hai - five lakh tak deta hai. Yeh jo pehle se chal rahe business ho, un ke liye. Past records aur business proof chahiye. Process 2-3 hafte lagta hai. Aap itna grow kar gaye?',
            'ta': 'Kishore attupottu padippu - aynthu laakshm rubai. Pala naalai nadndu irukka valimathukkkkum. Adaikal kalakula mattum negathiram parikurippu vendum. Process 2-3 varam. Neenga ita vegam velikai karuvaiyaa?',
        },

        # SCHEMES - STAND UP INDIA
        'scheme_standup': {
            'en': 'Stand Up India is a scheme that gives much larger loans - between rupees and one crore rupees - specifically for women and SC ST entrepreneurs. It is perfect if you want to scale up your business significantly. The site is standupmitra.in. Have you thought about scaling up?',
            'hi': 'Stand Up India bohot bada scheme hai. Ten lakh se ek crore tak deta hai specifically women aur SC ST entrepreneurs ke liye. Agar aap significant scale up karna chahte ho to perfect hai. standupmitra in. Aap scale up sochte ho?',
            'ta': 'Stand Up India sanalanga thittam - pattu laakshm-le onru crore rubai. Mahilairkkalkkum SC ST arasigatharkkum. Neenga vegam valikai kara vena pona vendiya thittam. standupmitra.in. Asirviratti yen sojavaiyaa?',
        },

        # SCHEMES - STREE SHAKTI
        'scheme_stree_shakti': {
            'en': 'Stree Shakti Package is from SBI specifically for women who own at least half of their business. This is perfect for you if you are the primary owner. It has special interest rates and flexible terms. The advantage is you get quick approval. Are you the primary owner of your business?',
            'hi': 'Stree Shakti Package SBI se hai specifically un mahilaon ke liye jo apne business ka halfh control karte ho. Interest rates aur terms bohot achchhe hote hain. Approval bhi jaldi mil jata hai. Aap primary owner ho?',
            'ta': 'Stree Shakti Package SBI-rula - mahilairkkalkkum. ungalku 50% ownership ay. Sudai interest rate, flexible terms. Approval asukaaram. Neenga primary possession-la ey?',
        },

        # SCHEMES - GOVERNMENT TRAINING
        'scheme_pmkvy': {
            'en': 'PMKVY offers free skill training for women - completely free! You can learn skills like digital marketing, financial management, tailoring, handicrafts, whatever interests you. This can really help your business grow. The site is pmkvyofficial.org. Have you thought about upskilling?',
            'hi': 'PMKVY bohot acha scheme hai - bilkul free training deta hai women ke liye. Digital marketing, financial management, tailoring, handicrafts - sab sikhaa sakte ho. Business grow karne mein madad hogi. pmkvyofficial org. Aap training lena chahte ho?',
            'ta': 'PMKVY - libraryai payirchi unnukkalukka. Digital marketing, nidhi nirivahanam, thundu kattum, kalarppukaikal. Ungal thozhil velikai karum. pmkvyofficial.org. Payirchi patukkara sozhavaiyaa?',
        },

        # PREMIUM SUBSCRIPTION
        'subscription_free_plan': {
            'en': 'Right now you are on our free plan. With free you get to browse all government schemes, chat with me anytime, and book up to two mentor sessions every month at no cost. This is already pretty powerful!',
            'hi': 'Aap abhi free plan par ho. Free mein aap schemes dekh sakte ho, mujhe anytime message kar sakte ho, aur 2 mentor sessions mahine mein free hain. Bahut chabadar hai!',
            'ta': 'Indru ungal free plan-la. Library-la schemes parunga, enakku sollunga eppotham vendum, 2 mentor sessions libraryai. Mika irukku!',
        },
        'subscription_premium_pitch': {
            'en': 'If you want to really accelerate your business, our premium plan is literally a game changer. For rupees a month or about rupees for the full year - which saves you about rupees - you get unlimited mentor sessions every month, detailed business analytics showing your exact growth, and secure storage for all your important documents. The best part is you can cancel anytime. Honestly, most of our successful entrepreneurs are on premium. Should I show you the payment page?',
            'hi': 'Agar aap seriously business ko grow karna chahte ho to premium plan sahi hai. Do sau ninyaanave rupaye mahine mein ya do hazaar chaar sau ninyaanave rupaye saal mein - almost ek hazaar bachte. Unlimited mentors milte ho, aapka analytics aur document storage. Successful entrepreneurs ko sab premium chahiye. Payment page dikha du?',
            'ta': 'Neenga thozhile vegalik velikai pana vena pona, premium plan best. Irunuru thonatrruonpathu rubai maadham ay, irandam aayiram naanuru thonatrruonpathu rubai varusham - likshm rubai rakkai. Unlimited mentors, business analytics, document storage. Successful vedharkaligaluku premium-le irukku. Payment page kaatukkalaa?',
        },
        'subscription_benefits': {
            'en': 'So with premium you get seriously unlimited mentor access - whenever you need advice, just reach out. You also get detailed analytics that shows your income trends, expense patterns, and profit growth month by month. Plus secure storage for all your registration papers, loan documents, everything. The mentors on premium also get priority matching based on your specific business type. You are essentially getting a personal business consultant. Worth it or what?',
            'hi': 'Premium mein unlimited mentors milte ho - jab bhi zarurat pade unse puch sakte ho. Detailed analytics dikhta hai aapka income, expense, aur profit trends. Ek jagah sab documents secure rakhte ho. Mentors ko bhi priority matching hoti hai aapke business type ke hisaab se. Basically ek personal consultant mil jata hai. Kaisa laga?',
            'ta': 'Premium-la unlimited mentors - eppo vendum ay sollugal. Detailed analytics - ungal varumanam, selavu, laabham ellam monthly parunga. Ellai documents nalla surakshitamaga store pannugal. Mentors-um priority matching - ungal thozhil tippu-k kattan. Personal consultant pole irukku. Sarikka ay?',
        },

        # MENTOR SYSTEM
        'mentor_available': {
            'en': 'So we have mentors available right now in different areas - business planning, digital marketing, accounting, supply chain management, and more. Each mentor has worked with entrepreneurs exactly in your situation. Honestly the mentors make all the difference. Tell me what area you need the most help with?',
            'hi': 'Humary pass bohot experience wale mentors hain - business planning, digital marketing, accounting sab mein. Sab ne entrepreneurs ko handle kiya hai. Mentor se hi sab kuch badal jata hai. Aapko kaun se area mein madad chahiye most?',
            'ta': 'Mentorer ellai area-la ullanar - thozhil suttiram, digital marketing, kalikulam sab. Sab entrepreneur-um thozhi pannigal. Mentor azhaginai vegamagi velikai karigal. Etha area-la udhaavi vendum etanai ey?',
        },
        'mentor_matched': {
            'en': 'Perfect! I have matched you with a mentor who has actually worked with three other vegetable sellers and knows this market really well. The mentor has availability tomorrow at two in the afternoon and again on Friday morning. Which slot works for you?',
            'hi': 'Bahut acha! Maine aapko ek mentor se match kiya jo sabziyon ka business karte ho aur market samjhte ho. Kal 2 baje ya Shukrawar morning milne ke time available hai. Kaun sa time badhiya hai aapke liye?',
            'ta': 'Puriyum! Irunoru mentor inaicen - kozhumpukal bidnesil 3-4 per pannigal - balan market theriyum. Naalaiky 2 baje ay Velli kalaiya irukka. Etha time varum?',
        },

        # MARKET PRICES
        'market_price_check': {
            'en': 'Market prices change every single day so I never make up numbers. The official portal that tracks all prices is agmarknet.gov.in - I will show you the link on your screen right now. You check there and you will see real time prices from across India. Okay?',
            'hi': 'Bhai prices hamesha badlte rehte ho to main jhooth bol na sakta. Official portal hai agmarknet gov in. Main aapke screen par link dikha dunga. Udhar check karo, real time prices mil jaayge. Bilkul clear?',
            'ta': 'Santhai vilai niraiya naal agarum - naan padikaltil sarikkai kannaiya mudiyadu. Official site agmarknet.gov.in - ninaikku screen-la link kaatukkalum. Athil irunthu real prices parigalum. Puriyaa?',
        },

        # IDENTITY & GREETING
        'greeting_warm': {
            'en': 'Hello jaan! I am Sakhi and I have been helping women entrepreneurs for years. No need to be formal - just tell me what is going on with your business and how I can help.',
            'hi': 'Namaste! Main Sakhi hoon aur maine kaunch saal se mahila entrepreneurs ko help karaa hai. Koi formality nahi - bas batao aapka business kaisa chal raha hai aur mujhe kya madad karni hai.',
            'ta': 'Vanakkam! Naan Sakhi - naan kaunch varusham mahila udyamigalai udhaive vanthu evataiyey irukkiren. Formal-ai irakkavendum illai - unnai thozhil enna aaguthu, enai udhaavi vendum solla.',
        },
        'identity_affirm': {
            'en': 'I am Sakhi and I am here to help women like you build their business. So tell me, what do you need right now?',
            'hi': 'Main Sakhi hoon aur main un mahilaon ki madad karti hoon jo apna business shuru ya grow karna chahte ho. To batao, aapko kya chahiye abhi?',
            'ta': 'Naan Sakhi - mahila udyamigalukkaga irukiren. Aanaale, etha unnakku vendum?',
        },

        # ERROR MESSAGES (Natural, Not Robotic)
        'error_general': {
            'en': 'Sorry, I did not quite catch that. Maybe you can say it again or tell me which area you want help with - income, expense, schemes, or something else?',
            'hi': 'Maafi, samajh nahi aaya. Phir se kahi ya bataao kaun se area mein madad chahiye - income, kharcha, schemes, ya kuch aur?',
            'ta': 'Mannikavum, puriyavillai. Meendum sollunga athava enna area-la udhaavi vendum sollugal.',
        },
        'error_amount': {
            'en': 'I need a clear number. Like if you made 500 rupees or you spent 1200 rupees - tell me exactly what the amount is.',
            'hi': 'Mujhe clear number chahiye. Jaise 500 rupaye earn kiye ya 1200 spend kiye - exact bataao.',
            'ta': 'Clear thokai sollugal. Udaaranatthu 500 rubai ay 1200 rubai selava ay - sarikkai thokai.',
        },

        # HELP & CAPABILITIES
        'help_main': {
            'en': 'I can help you with so many things! Recording your daily income and expenses, tracking your profit, checking government schemes you can apply for, connecting you with experienced mentors, checking market prices, handling payment and subscriptions - basically everything you need to run your business.',
            'hi': 'Main bahut kuch kr sakti hoon! Income, expense track karna, profit dekha, government schemes bataana, mentors connect karna, prices check karna, payment - basically sab kuch jo business chalaane mein chahiye.',
            'ta': 'Naan kaunch pandal pannikal matten! Varumanam, selavu, laabham, thittagal, mentors, santhai vilai, payment - ethanai irukku. Thozhil nadattuva sagile.',
        },
    }


    @classmethod
    def get_message(cls, key, language='en', **kwargs):
        """
        Get a response message in the specified language.
        Falls back to English if translation not available.
        
        SAKHI RULES:
        - Numbers are automatically converted to words in Hindi/Tamil
        - Never returns robotic or mixed-language responses
        - Always ends with natural follow-up question
        """
        if key not in cls.RESPONSES:
            return cls.RESPONSES['error_general'].get(language, cls.RESPONSES['error_general']['en'])

        lang_responses = cls.RESPONSES[key]
        template = lang_responses.get(language, lang_responses.get('en', ''))

        if not template:
            return cls.RESPONSES['error_general']['en']

        try:
            # Pre-process amounts for Hindi and Tamil
            processed_kwargs = cls._process_amounts(kwargs, language)
            return template.format(**processed_kwargs)
        except KeyError as e:
            return template

    @classmethod
    def _process_amounts(cls, kwargs, language):
        """
        Convert numeric amounts to words for Hindi and Tamil
        RULE: Numbers must ALWAYS be spoken in the response language
        """
        processed = kwargs.copy()
        
        if language == 'hi':
            if 'amount' in kwargs and isinstance(kwargs['amount'], (int, float)):
                processed['amount'] = NumberConverter.rupees_to_hindi(kwargs['amount'])
        elif language == 'ta':
            if 'amount' in kwargs and isinstance(kwargs['amount'], (int, float)):
                processed['amount'] = NumberConverter.rupees_to_tamil(kwargs['amount'])
        
        return processed

    @classmethod
    def get_all_keys(cls):
        """Get all available response message keys"""
        return list(cls.RESPONSES.keys())

    @classmethod
    def validate_language(cls, language):
        """Validate and normalize language code"""
        valid_languages = {'en', 'hi', 'ta'}
        return language if language in valid_languages else 'en'


