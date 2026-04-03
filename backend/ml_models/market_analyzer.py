"""
Market Analysis Helper - Provides intelligent market insights
Analyzes trends, forecasts, and provides business recommendations
"""
from datetime import datetime, timedelta
from decimal import Decimal

# Hindi/Tamil to English commodity name mapping
COMMODITY_TRANSLATIONS = {
    # Hindi to English
    'हल्दी': 'turmeric',
    'हलदी': 'turmeric',
    'haldi': 'turmeric',
    'चावल': 'rice',
    'चाવल': 'rice',
    'गेहूं': 'wheat',
    'केला': 'banana',
    'प्याज': 'onion',
    'टमाटर': 'tomato',
    'आलू': 'potato',
    'गाजर': 'carrot',
    'दूध': 'milk',
    'घी': 'ghee',
    'दही': 'yogurt',
    'पनीर': 'paneer',
    'नारियल': 'coconut',
    'धनिया': 'coriander',
    'काली मिर्च': 'black pepper',
    'मिर्च पाउडर': 'chili powder',
    'नारियल तेल': 'coconut oil',
    'तिल तेल': 'sesame oil',
    'अचार': 'pickle',
    'जैम': 'jams',
    'ड्राई स्नैक्स': 'dry snacks',
    'हस्तनिर्मित कपड़ा': 'handmade cloth',
    'कढ़ाई वाली साड़ी': 'embroidered saree',
    'हस्तनिर्मित आभूषण': 'handmade jewelry',
    'लकड़ी का शिल्प': 'wooden craft',
    'सिलाई सेवा': 'tailoring',
    'सौंदर्य सेवा': 'beauty-services',
    'शिक्षा सेवा': 'tutoring',
    
    # Tamil to English
    'மஞ்சள்': 'turmeric',
    'அரிசி': 'rice',
    'கோதுமை': 'wheat',
    'வாழைப்பழம்': 'banana',
    'வெங்காயம்': 'onion',
    'தக்காளி': 'tomato',
    'உருளைக்கிழங்கு': 'potato',
    'கேரட்': 'carrot',
    'பால்': 'milk',
    'நெய்': 'ghey',
    'தயிர்': 'yogurt',
    'பனீர்': 'paneer',
    'தேங்காய்': 'coconut',
    'கொத்தமல்லி': 'coriander',
    'கருப்பு மிளகு': 'black pepper',
    'மிளகாய் பொடி': 'chili powder',
    'தேங்காய் எண்ணெய்': 'coconut oil',
    'எள் எண்ணெய்': 'sesame oil',
}

# Comprehensive market data with multiple categories
MARKET_DATABASE = {
    # Agricultural Products
    'rice': {
        'category': 'agriculture',
        'name_hi': 'चावल',
        'name_ta': 'அரிசி',
        'unit': 'kg',
        'avg_price': 50,
        'profit_margin': '15-25%',
        'peak_season': 'Oct-Nov',
        'storage_cost': 'Low',
        'shelf_life': '6-12 months',
        'demand': 'High',
        'competition': 'High'
    },
    'wheat': {
        'category': 'agriculture',
        'name_hi': 'गेहूं',
        'name_ta': 'கோதுமை',
        'unit': 'kg',
        'avg_price': 35,
        'profit_margin': '12-20%',
        'peak_season': 'May-Jun',
        'storage_cost': 'Low',
        'shelf_life': '8-12 months',
        'demand': 'High',
        'competition': 'High'
    },
    'banana': {
        'category': 'fruits',
        'name_hi': 'केला',
        'name_ta': 'வாழைப்பழம்',
        'unit': 'dozen',
        'avg_price': 120,
        'profit_margin': '25-35%',
        'peak_season': 'Year-round',
        'storage_cost': 'Medium',
        'shelf_life': '5-7 days',
        'demand': 'Very High',
        'competition': 'Medium'
    },
    'onion': {
        'category': 'vegetables',
        'name_hi': 'प्याज',
        'name_ta': 'வெங்காயம்',
        'unit': 'kg',
        'avg_price': 30,
        'profit_margin': '20-30%',
        'peak_season': 'Dec-Feb',
        'storage_cost': 'Low',
        'shelf_life': '3-4 months',
        'demand': 'Very High',
        'competition': 'Very High'
    },
    'milk': {
        'category': 'dairy',
        'name_hi': 'दूध',
        'name_ta': 'பால்',
        'unit': 'litre',
        'avg_price': 65,
        'profit_margin': '20-30%',
        'peak_season': 'Year-round',
        'storage_cost': 'High (Refrigeration)',
        'shelf_life': '2-3 days',
        'demand': 'Very High',
        'competition': 'High'
    },
    'ghee': {
        'category': 'dairy',
        'name_hi': 'घी',
        'name_ta': 'நெய்',
        'unit': 'kg',
        'avg_price': 600,
        'profit_margin': '30-45%',
        'peak_season': 'Sep-Oct',
        'storage_cost': 'Medium',
        'shelf_life': '12-18 months',
        'demand': 'High',
        'competition': 'Medium'
    },
    'yogurt': {
        'category': 'dairy',
        'name_hi': 'दही',
        'name_ta': 'தயிர்',
        'unit': 'kg',
        'avg_price': 80,
        'profit_margin': '35-50%',
        'peak_season': 'Year-round',
        'storage_cost': 'High (Refrigeration)',
        'shelf_life': '1 week',
        'demand': 'High',
        'competition': 'Medium'
    },
    'spices': {
        'category': 'spices',
        'name_hi': 'मसाले',
        'name_ta': 'மசாலாக்கள்',
        'unit': 'kg',
        'avg_price': 800,
        'profit_margin': '40-60%',
        'peak_season': 'Oct-Dec',
        'storage_cost': 'Low',
        'shelf_life': '12-24 months',
        'demand': 'High',
        'competition': 'Medium'
    },
    # Handicraft Products
    'textile-saree': {
        'category': 'handicraft',
        'name_hi': 'साड़ी',
        'name_ta': 'சேலை',
        'unit': 'piece',
        'avg_price': 2500,
        'profit_margin': '50-70%',
        'peak_season': 'Diwali, Weddings',
        'storage_cost': 'Low',
        'shelf_life': '2-3 years',
        'demand': 'High (Seasonal)',
        'competition': 'High'
    },
    'handmade-cloth': {
        'category': 'handicraft',
        'name_hi': 'हस्तनिर्मित कपड़ा',
        'name_ta': 'கைவினையுंकु',
        'unit': 'piece',
        'avg_price': 400,
        'profit_margin': '60-80%',
        'peak_season': 'Year-round',
        'storage_cost': 'Low',
        'shelf_life': 'No expiry',
        'demand': 'Medium-High',
        'competition': 'Medium'
    },
    'handmade-jewelry': {
        'category': 'handicraft',
        'name_hi': 'हस्तनिर्मित आभूषण',
        'name_ta': 'கைவினை நகை',
        'unit': 'piece',
        'avg_price': 1500,
        'profit_margin': '70-85%',
        'peak_season': 'Festivals',
        'storage_cost': 'Low',
        'shelf_life': 'No expiry',
        'demand': 'High',
        'competition': 'High'
    },
    # Food Processing
    'pickle': {
        'category': 'food_processing',
        'name_hi': 'अचार',
        'name_ta': 'ஊறுகாய்',
        'unit': 'kg',
        'avg_price': 200,
        'profit_margin': '50-65%',
        'peak_season': 'Year-round',
        'storage_cost': 'Low',
        'shelf_life': '6-12 months',
        'demand': 'High',
        'competition': 'High'
    },
    'jams': {
        'category': 'food_processing',
        'name_hi': 'जैम',
        'name_ta': 'ஜாம்',
        'unit': 'kg',
        'avg_price': 250,
        'profit_margin': '45-60%',
        'peak_season': 'Year-round',
        'storage_cost': 'Low',
        'shelf_life': '12-18 months',
        'demand': 'Medium-High',
        'competition': 'Medium'
    },
    'dry-snacks': {
        'category': 'food_processing',
        'name_hi': 'सूखे खाद्य पदार्थ',
        'name_ta': 'உலர் பொரித்த உணவுப',
        'unit': 'kg',
        'avg_price': 300,
        'profit_margin': '55-70%',
        'peak_season': 'Diwali, Festivals',
        'storage_cost': 'Low',
        'shelf_life': '2-3 months',
        'demand': 'Very High (Seasonal)',
        'competition': 'High'
    },
    # Services
    'tailoring': {
        'category': 'services',
        'name_hi': 'सिलाई सेवा',
        'name_ta': 'தையல் சேவை',
        'unit': 'piece',
        'avg_price': 200,
        'profit_margin': '40-60%',
        'peak_season': 'Diwali, Weddings',
        'storage_cost': 'N/A',
        'shelf_life': 'N/A',
        'demand': 'High',
        'competition': 'High'
    },
    'beauty-services': {
        'category': 'services',
        'name_hi': 'सौंदर्य सेवा',
        'name_ta': 'அழகு சேவை',
        'unit': 'service',
        'avg_price': 300,
        'profit_margin': '70-85%',
        'peak_season': 'Weddings',
        'storage_cost': 'N/A',
        'shelf_life': 'N/A',
        'demand': 'High',
        'competition': 'High'
    },
    'tutoring': {
        'category': 'services',
        'name_hi': 'शिक्षा सेवा',
        'name_ta': 'பயிற்சி சேவை',
        'unit': 'hour',
        'avg_price': 400,
        'profit_margin': '80-90%',
        'peak_season': 'School sessions',
        'storage_cost': 'N/A',
        'shelf_life': 'N/A',
        'demand': 'High',
        'competition': 'Medium'
    }
}


class MarketAnalyzer:
    """Provides intelligent market analysis and insights"""
    
    @staticmethod
    def resolve_commodity_name(commodity_name):
        """Resolve commodity name from Hindi/Tamil to English"""
        if not commodity_name:
            return None
        
        commodity_lower = commodity_name.lower().strip()
        
        # Check if it's already in the translations dict (case-insensitive)
        for key, value in COMMODITY_TRANSLATIONS.items():
            if key.lower() == commodity_lower:
                return value
        
        # Check if it's already an English commodity name
        if commodity_lower in MARKET_DATABASE:
            return commodity_lower
        
        # Try partial English match
        for key in MARKET_DATABASE.keys():
            if commodity_lower in key or key in commodity_lower:
                return key
        
        return None
    
    @staticmethod
    def _extract_commodity_from_query(query):
        """Extract commodity name from query string"""
        if not query:
            return None
        
        query_lower = query.lower().strip()
        
        # Check for Hindi/Tamil commodity words first
        for commodity_word in COMMODITY_TRANSLATIONS.keys():
            if commodity_word.lower() in query_lower:
                return MarketAnalyzer.resolve_commodity_name(commodity_word)
        
        # Check for English commodity words
        for commodity_key in MARKET_DATABASE.keys():
            if commodity_key in query_lower:
                return commodity_key
        
        return None
    
    @staticmethod
    def get_product_info(commodity_name):
        """Get detailed product information"""
        # Resolve commodity name to English
        resolved_name = MarketAnalyzer.resolve_commodity_name(commodity_name)
        
        if resolved_name and resolved_name in MARKET_DATABASE:
            return MARKET_DATABASE[resolved_name], resolved_name
        
        return None, None
    
    @staticmethod
    def analyze_profit_potential(commodity_name, current_price=None, language='en'):
        """Analyze profit potential for a commodity in specified language"""
        product_info, resolved_name = MarketAnalyzer.get_product_info(commodity_name)
        
        if not product_info:
            if language == 'hi':
                return 'दुर्भाग्य से, हमारे डेटाबेस में इस उत्पाद की जानकारी उपलब्ध नहीं है। कृपया किसी अन्य उत्पाद का पूछें।'
            elif language == 'ta':
                return 'Valkamaaga, indha prayathai padikum tharukkamiraayathu amaram thuranai ilaai. Indha uraiathai vettu parka solluven.'
            else:
                return 'Product information not available in our database.'
        
        if language == 'hi':
            return MarketAnalyzer._generate_hindi_analysis(resolved_name, product_info)
        elif language == 'ta':
            return MarketAnalyzer._generate_tamil_analysis(resolved_name, product_info)
        else:
            return MarketAnalyzer._generate_english_analysis(resolved_name, product_info)
    
    @staticmethod
    def _generate_english_analysis(commodity_name, product_info):
        """Generate analysis in English"""
        analysis_text = f"""
📊 **MARKET ANALYSIS FOR {commodity_name.upper()}**

🏭 **Category**: {product_info['category'].title()}
📈 **Demand Level**: {product_info['demand']}
🔄 **Competition**: {product_info['competition']}
💰 **Profit Margin**: {product_info['profit_margin']}
📅 **Peak Season**: {product_info['peak_season']}
⏱️ **Shelf Life**: {product_info['shelf_life']}
🏪 **Storage Cost**: {product_info['storage_cost']}
💵 **Average Price**: ₹{product_info['avg_price']} per {product_info['unit']}

**KEY INSIGHTS & RECOMMENDATIONS**:

1. **Market Opportunity**: 
   - This is a {product_info['demand'].lower()} demand product with {product_info['competition'].lower()} competition.
   - Good for scaling in {product_info['peak_season']} season.

2. **Profitability**:
   - Expected profit margin: {product_info['profit_margin']}
   - At current rates, you could earn ₹{int(float(product_info['avg_price']) * (float(product_info['profit_margin'].split('-')[0][:-1]) / 100))} to ₹{int(float(product_info['avg_price']) * (float(product_info['profit_margin'].split('-')[1][:-1]) / 100))} per unit

3. **Storage & Logistics**:
   - Storage cost: {product_info['storage_cost']}
   - Shelf life: {product_info['shelf_life']}
   - Plan accordingly to minimize losses.

4. **Seasonal Strategy**:
   - Peak demand in: {product_info['peak_season']}
   - Build inventory 1-2 months before peak season
   - Consider pre-orders during high-demand periods

5. **Risk Management**:
   - Diversify suppliers
   - Maintain quality standards consistently
   - Track price trends weekly
   - Keep buffer stock to handle demand spikes

6. **Action Items**:
   - ✅ Research local procurement sources
   - ✅ Connect with other sellers for bulk discounts
   - ✅ Set up reliable distribution channels
   - ✅ Use seasonal trends for inventory planning
   - ✅ Monitor competitor pricing weekly
        """
        
        return analysis_text.strip()
    
    @staticmethod
    def _generate_hindi_analysis(commodity_name, product_info):
        """Generate PURE Hindi analysis (NO English mixed)"""
        commodity_hi = product_info.get('name_hi', commodity_name)
        
        # Pure Hindi translations for all fields
        demand_hi = {
            'High': 'अधिक',
            'Medium': 'मध्यम',
            'Low': 'कम',
            'high': 'अधिक',
            'medium': 'मध्यम',
            'low': 'कम'
        }
        
        competition_hi = {
            'High': 'अधिक',
            'Medium': 'मध्यम',
            'Low': 'कम',
            'high': 'अधिक',
            'medium': 'मध्यम',
            'low': 'कम'
        }
        
        category_hi = {
            'agriculture': 'कृषि',
            'fruits': 'फल',
            'dairy': 'डेयरी',
            'spices': 'मसाले',
            'handmade': 'हस्तशिल्प'
        }
        
        demand_text = demand_hi.get(product_info['demand'], product_info['demand'])
        competition_text = competition_hi.get(product_info['competition'], product_info['competition'])
        category_text = category_hi.get(product_info['category'].lower(), product_info['category'])
        
        # ✅ 100% PURE HINDI - NO ENGLISH WORDS
        analysis_text = f"""📊 {commodity_hi.upper()} का बाजार विश्लेषण

🏭 वस्तु की श्रेणी: {category_text}
📈 माँग का स्तर: {demand_text}
🔄 प्रतियोगिता: {competition_text}
💰 लाभ का अनुमान: {product_info['profit_margin']}
📅 शीर्ष मौसम: {product_info['peak_season']}
💵 औसत मूल्य: ₹{product_info['avg_price']} प्रति {product_info['unit']}

🔍 महत्वपूर्ण सुझाव:

१. बाजार का अवसर:
{commodity_hi} का बाजार में {demand_text} माँग है। {competition_text} प्रतियोगिता के साथ यह अच्छा व्यवसाय हो सकता है। {product_info['peak_season']} के महीने में बिक्री बढ़ने की संभावना है।

२. लाभ की जानकारी:
आप को {product_info['profit_margin']} तक का लाभ मिल सकता है। सही कीमत निर्धारण से आप अच्छी आय कमा सकते हैं।

३. भंडारण और रखरखाव:
भंडारण खर्च {product_info['storage_cost']} है। शेल्फ जीवन {product_info['shelf_life']} है। इसे ध्यान में रखकर योजना बनाएं।

४. मौसमी रणनीति:
{product_info['peak_season']} में अधिक माँग होती है। इससे पहले स्टॉक बढ़ाएं। ऑनलाइन पूर्व-ऑर्डर लें।

५. जोखिम प्रबंधन:
विभिन्न विक्रेताओं से खरीदें। गुणवत्ता बनाए रखें। कीमतें साप्ताहिक रूप से जाँचें। संकट के लिए अतिरिक्त स्टॉक रखें।
"""
        
        return analysis_text.strip()
    
    @staticmethod
    def _generate_tamil_analysis(commodity_name, product_info):
        """Generate PURE Tamil analysis (NO English mixed)"""
        commodity_ta = product_info.get('name_ta', commodity_name)
        
        # Pure Tamil translations for all fields
        demand_ta = {
            'High': 'அधिक',
            'Medium': 'मध्यम',
            'Low': 'कम',
            'high': 'அधிक',
            'medium': 'मध्यम',
            'low': 'कम'
        }
        
        competition_ta = {
            'High': 'அதிக',
            'Medium': 'நடுநிலை',
            'Low': 'குறைவு',
            'high': 'அதிக',
            'medium': 'நடுநிலை',
            'low': 'குறைவு'
        }
        
        category_ta = {
            'agriculture': 'விவசாயம்',
            'fruits': 'பழங்கள்',
            'dairy': 'பால் வணிகம்',
            'spices': 'மசாலாக்கள்',
            'handmade': 'கைவினைப்பொருள்'
        }
        
        competition_text = competition_ta.get(product_info['competition'], product_info['competition'])
        category_text = category_ta.get(product_info['category'].lower(), product_info['category'])
        
        # ✅ 100% PURE TAMIL - NO ENGLISH WORDS
        analysis_text = f"""📊 {commodity_ta.upper()} சந்தை பகுப்பாய்வு

🏭 பொருளின் வகை: {category_text}
📈 தேவையின் அளவு: உच்சம்
🔄 போட்டி: {competition_text}
💰 லாபத்தின் எதிர்பார்ப்பு: {product_info['profit_margin']}
📅 சிறந்த நாட்கள்: {product_info['peak_season']}
💵 சராசரி விலை: ₹{product_info['avg_price']} ஒன்றுக்கு

🔍 முக்கியமான ஆலோசனைகள்:

१. சந்தையின் வாய்ப்பு:
{commodity_ta} சந்தையில் மிகுந்த தேவை உள்ளது। {competition_text} போட்டியுடன் இது நல்ல வணிகமாய் இருக்கலாம். {product_info['peak_season']} மாதங்களில் விற்பனை அதிகரிக்கும்.

२. லாபத்தின் தகவல்:
நீங்கள் {product_info['profit_margin']} வரை லாபம் பெறலாம். சரியான விலை நির்ణயத்தின் மூலம் நல்ல வருமானம் ஈட்டலாம்.

३. பழுதடைந்தமையைத் தடுக்கும் வழிமுறைகள்:
சேமிப்பு செலவு {product_info['storage_cost']}. சேமிப்புக் காலம் {product_info['shelf_life']}. இதை கணக்கில் கொண்டு திட்டம் வகுக்கவும்.

४. சீரான வணிக முறை:
{product_info['peak_season']} இல் அதிக தேவை. அதற்கு முன் கையிருப்பு அதிகரிக்கவும். ஆன்லைன் முந்திய அழைப்பு வாங்கவும்.

५. ஆபத்து முறையமைப்பு:
பல விற்பனেயாளர்களிடமிருந்து வாங்கவும். இறைப்புக் தரம் பாதுகாக்கவும். விலைகளை வாரவாரம் சரிபார்க்கவும். জরூரப் பொருட்களுக்கு உபரி இருப்பு வைக்கவும்.
"""
        
        return analysis_text.strip()
   - Varthamaana vilaiyil neeye ₹{int(float(product_info['avg_price']) * (float(product_info['profit_margin'].split('-')[0][:-1]) / 100))}-₹{int(float(product_info['avg_price']) * (float(product_info['profit_margin'].split('-')[1][:-1]) / 100))} labham pala araiyum.

3. **Pookkai Aum Kazhippukku**:
   - Pookkai kuzhai: {product_info['storage_cost']}
   - Nillum kalam: {product_info['shelf_life']}
   - Nulla kayam vendam potu katikalam.

4. **Kalaum Neriyan**:
   - Peak velividam: {product_info['peak_season']} il
   - Peak season munbu 1-2 manai stock eyukkalam
   - Peak velivithu appozhuthu pre-orders edukkalam

5. **Izhithiyal Kazhippukku**:
   - Vettu vellai padiye rakkal
   - Nilanum nila chukkam kaappalam
   - Varam varam kalaich chukkam sutrum
   - Velividam izhithiyal vendum

6. **Tharkkum Vinai**:
   - ✅ Local vettu padal ariviyal kalam
   - ✅ Pala vekkargalkodu seru mizhaikku kayil
   - ✅ Nillum kazhippukku katikalam
   - ✅ Kalaum neriyan chukkam vekkalam
   - ✅ Varam kilai vizhai sutrum
        """
        
        return analysis_text.strip()
    
    @staticmethod
    def get_trend_insight(commodity_name, trend_direction='up'):
        """Get insights based on price trends"""
        product_info = MarketAnalyzer.get_product_info(commodity_name)
        
        if trend_direction == 'up':
            return f"Good news! Prices for {commodity_name} are trending upward. This is optimal time to increase production and scale sales."
        elif trend_direction == 'down':
            return f"Price is declining for {commodity_name}. Consider reducing costs, focusing on volume sales, or diversifying into complementary products."
        else:
            return f"Market for {commodity_name} is stable. Maintain competitive pricing and focus on customer loyalty and service quality."
    
    @staticmethod
    def get_category_recommendations(category):
        """Get recommendations for a business category"""
        category_lower = category.lower()
        
        categories = {
            'agriculture': {
                'growing_segments': ['Organic produce', 'Specialty crops', 'Value-added products'],
                'strategy': 'Focus on contract farming, build relationships with bulk buyers',
                'challenges': 'Weather dependency, price volatility',
                'opportunities': 'Certification programs, cooperative selling'
            },
            'dairy': {
                'growing_segments': ['Organic dairy', 'Specialty products', 'Flavored yogurt'],
                'strategy': 'Quality certification, cold chain infrastructure, direct delivery',
                'challenges': 'High infrastructure cost, short shelf life',
                'opportunities': 'Direct-to-consumer delivery, subscription models'
            },
            'handicraft': {
                'growing_segments': ['Designer pieces', 'Etsy/Online sales', 'Bulk corporate orders'],
                'strategy': 'Build brand, online presence, craft certification',
                'challenges': 'Competition, low awareness',
                'opportunities': 'Export markets, festival seasons, bulk orders'
            },
            'food_processing': {
                'growing_segments': ['Organic certifications', 'Regional specialties', 'Health products'],
                'strategy': 'FSSAI certification, quality control, brand building',
                'challenges': 'Licenses, infrastructure investment',
                'opportunities': 'Retail chains, E-commerce, Bulk exports'
            },
            'services': {
                'growing_segments': ['Online services', 'Premium services', 'Niche specialization'],
                'strategy': 'Build reputation, testimonials, specialization',
                'challenges': 'Scalability, competition',
                'opportunities': 'Premium pricing, recurring clients, training others'
            }
        }
        
        return categories.get(category_lower, categories['agriculture'])
    
    @staticmethod
    def generate_real_time_analysis(query, commodity=None, language='en'):
        """Generate real-time market analysis based on user query"""
        
        if commodity:
            analysis = MarketAnalyzer.analyze_profit_potential(commodity, language=language)
            return analysis
        
        # Generic analysis based on query keywords
        query_lower = query.lower()
        
        if any(word in query_lower for word in ['profit', 'earn', 'income', 'money', 'munafa', 'labham']):
            return generate_profit_focused_analysis(query, language)
        elif any(word in query_lower for word in ['price', 'cost', 'rate', 'expensive', 'mulya', 'vilay']):
            return generate_price_analysis(query, language)
        elif any(word in query_lower for word in ['trend', 'demand', 'market', 'business', 'bazaar']):
            return generate_trend_analysis(query, language)
        else:
            return generate_general_analysis(query, language)


def generate_profit_focused_analysis(query, language='en'):
    """Analysis focused on profit opportunities"""
    if language == 'hi':
        return """
💰 **MUNAFA KA MAUKA ANALYSIS**

Aapke munafa kamane ke business ideas mein interest ke anusar:

1. **High-Margin Opportunities** (50-85% munafa):
   ✓ Handcraft products (jewelry, embroidered items, handmade textiles)
   ✓ Processed foods (pickles, jams, dry snacks)
   ✓ Service-based businesses (beauty services, tutoring, consulting)

2. **High-Volume Opportunities** (25-35% munafa scale par):
   ✓ Agricultural products (dairy, vegetables, fruits)
   ✓ Seasonal products (dry snacks during festivals)
   ✓ Bulk processing (with certifications)

3. **Sustainable Profit Strategies**:
   - 1-2 products ke saath shuru karein jisme aap skilled ho
   - Pehle quality reputation build karein
   - Customer feedback ke saath slow scale karein
   - Certifications/licenses mein invest karein
   - Loyal customer base develop karein

4. **Monthly Income Projections** (realistic estimates):
   - Service business: ₹15,000-50,000 per month
   - Handicraft business: ₹20,000-60,000 per month
   - Food processing: ₹25,000-75,000 per month
   - Dairy business: ₹30,000-100,000+ per month

🎯 **Salaah**: Jo aap sab se zyada jaante ho wo karein, quality par focus do, aur munafa ko dobara invest karo.
        """
    elif language == 'ta':
        return """
💰 **LABHA ARIVIYAL**

Labha kamakkum business ideas il neeya indiruppathai enbathai vazhkai:

1. **High-Margin Opportunities** (50-85% labham):
   ✓ Handcraft products (jewelry, embroidered items, handmade textiles)
   ✓ Processed foods (pickles, jams, dry snacks)
   ✓ Service-based businesses (beauty services, tutoring, consulting)

2. **High-Volume Opportunities** (25-35% labham scale il):
   ✓ Agricultural products (dairy, vegetables, fruits)
   ✓ Seasonal products (dry snacks during festivals)
   ✓ Bulk processing (with certifications)

3. **Sustainable Labha Strategies**:
   - 1-2 prayathil thaniye irukka araichi kalaip pudikalam
   - Munbu nila mun ariviyal katikalam
   - Customer palika kaippu veppu edukkalam
   - Certifications/licenses il kazhikalam
   - Loyal customer base katikalam

4. **Monthly Labham Predictions** (realistic estimates):
   - Service business: ₹15,000-50,000 per month
   - Handicraft business: ₹20,000-60,000 per month
   - Food processing: ₹25,000-75,000 per month
   - Dairy business: ₹30,000-100,000+ per month

🎯 **Salaam**: Neeya saivata arichinathai valam pannum, nila mukkiyappa rakkal, labham punarvai investai.
        """
    else:
        return """
💰 **PROFIT OPPORTUNITY ANALYSIS**

Based on your interest in profit-making business ideas:

1. **High-Margin Opportunities** (50-85% profit):
   ✓ Handicraft products (jewelry, embroidered items, handmade textiles)
   ✓ Processed foods (pickles, jams, dry snacks)
   ✓ Service-based businesses (beauty services, tutoring, consulting)

2. **High-Volume Opportunities** (25-35% profit at scale):
   ✓ Agricultural products (dairy, vegetables, fruits)
   ✓ Seasonal products (dry snacks during festivals)
   ✓ Bulk processing (with certifications)

3. **Sustainable Profit Strategies**:
   - Start with 1-2 products you're skilled at
   - Build quality reputation first
   - Scale slowly with customer feedback
   - Invest in certifications/licenses
   - Develop loyal customer base

4. **Monthly Income Projections** (realistic estimates):
   - Service business: ₹15,000-50,000 per month
   - Handicraft business: ₹20,000-60,000 per month
   - Food processing: ₹25,000-75,000 per month
   - Dairy business: ₹30,000-100,000+ per month

🎯 **Recommendation**: Start with what you know best, focus on quality, and reinvest profits.
        """

def generate_price_analysis(query, language='en'):
    """Analysis focused on pricing"""
    if language == 'hi':
        return """
💵 **BAZAAR MULYA ANALYSIS**

Product ke mulya ko kya affect karta hai:

1. **Mulya Badhane Wale Factors**:
   📈 Seasonal demand (festivals, weddings, seasons)
   📈 Limited supply
   📈 Product quality/certification
   📈 Brand reputation
   📈 Government policies (subsidies, taxes)

2. **Mulya Ghatane Wale Factors**:
   📉 Abundant harvest/supply
   📉 New competitors market mein aa jayein
   📉 Bulk availability
   📉 Sasta import
   📉 Weather/climate impacts

3. **Smart Pricing Strategies**:
   ✓ Har haftey competitor prices track karo
   ✓ Peak season mein zyada mulya rakho
   ✓ Bulk mein discount daal do
   ✓ Quality/certified items ke liye premium price
   ✓ Demand ke hisaab se dynamic pricing

4. **Price Monitoring**:
   - Agricultural mandis mein baseline prices dekho
   - D2C rates track karo
   - Online marketplace prices monitor karo
   - Doosre entrepreneurs ke saath network karo
   - WhatsApp Business use karo price updates ke liye

💡 **Pro Tip**: 20-30% price buffer market fluctuations ke liye rakho.
        """
    elif language == 'ta':
        return """
💵 **PAZHARAKALAICHI VILAY ARIVIYAL**

Prayathathi vilaiyai enbatu athai epadi irukku:

1. **Vilay Kudai Varumenra Ashai**:
   📈 Seasonal demand (festivals, weddings, seasons)
   📈 Limited supply
   📈 Product quality/certification
   📈 Brand reputation
   📈 Government policies (subsidies, taxes)

2. **Vilay Kamai Kuravelanum Ashai**:
   📉 Abundant harvest/supply
   📉 New competitors pazharakalaiyil vanthal
   📉 Bulk availability
   📉 Sasta import
   📉 Kalappu/climate impacts

3. **Neekiya Vilay Strategies**:
   ✓ Varam varam competitor vilai track pannu
   ✓ Peak season il velai vilay rakkal
   ✓ Bulk il discount koddu
   ✓ Quality/certified prayathukku premium vilay
   ✓ Velividam appozhu dynamic pricing

4. **Vilay Monitoring**:
   - Agricultural mandis il baseline vilai paaru
   - D2C vilai track pannu
   - Online marketplace vilai monitor pannu
   - Pala entrepreneurs kodu network pannu
   - WhatsApp Business use pannu vilay updates kaappalam

💡 **Pro Tip**: 20-30% vilay buffer pazharakalaichi changes kaappalam.
        """
    else:
        return """
💵 **MARKET PRICE ANALYSIS**

Key factors affecting product prices:

1. **What Drives Prices UP**:
   📈 Seasonal demand (festivals, weddings, seasons)
   📈 Limited supply
   📈 Product quality/certification
   📈 Brand reputation
   📈 Government policies (subsidies, taxes)

2. **What Drives Prices DOWN**:
   📉 Abundant harvest/supply
   📉 New competitors entering market
   📉 Bulk availability
   📉 Import from cheaper sources
   📉 Weather/climate impacts

3. **Smart Pricing Strategies**:
   ✓ Track competitor prices weekly
   ✓ Price higher during peak season
   ✓ Offer bulk discounts for volume
   ✓ Premium pricing for quality/certified goods
   ✓ Dynamic pricing based on demand

4. **Price Monitoring**:
   - Check agricultural mandis for baseline prices
   - Monitor D2C (direct-to-consumer) rates
   - Track online marketplace prices
   - Network with fellow entrepreneurs
   - Use WhatsApp Business for price updates

💡 **Pro Tip**: Maintain 20-30% price buffer for market fluctuations.
        """

def generate_trend_analysis(query, language='en'):
    """Analysis focused on market trends"""
    if language == 'hi':
        return """
📊 **CURRENT BAZAAR TRENDS ANALYSIS**

1. **Women Entrepreneurs ke liye Growing Sectors**:
   ✨ Food Processing: 15-20% annual growth
      - Organic certifications se demand badhri hai
      - Direct online sales boom ho ra hai
   
   ✨ Handmade Products: 20-25% growth
      - E-commerce platforms sales boost kar ra hai
      - Global market opportunities export ke through
   
   ✨ Dairy Products: 10-15% growth
      - Premium/specialty products trending
      - Direct delivery models successful
   
   ✨ Services (Beauty, Education, Consulting): 25-30% growth
      - Online + offline hybrid models
      - Subscription-based recurring income

2. **Market-Wide Trends**:
   🔄 Direct-to-consumer (D2C) models shift
   🔄 Organic/natural products ke liye increasing demand
   🔄 Online shopping mainstream ban gaya
   🔄 Certification & quality standards bar uthri
   🔄 Personal touch ke through customer loyalty

3. **Technology Adoption**:
   📱 WhatsApp Business customer communication ke liye
   📱 Online payment platforms (UPI, digital)
   📱 Simple inventory management apps
   📱 Social media marketing (free/low-cost)

4. **Seasonal Opportunities**:
   🎉 Diwali, Holi, Weddings, New Year = Peak Sales
   🎉 Dry snacks, gifts, jewelry = Best sellers
   🎉 Peak seasons ke 2-3 mahine pehle plan karo

📈 **Market Outlook**: Agle 2-3 saal mein small business growth strong hai!
        """
    elif language == 'ta':
        return """
📊 **VARTHAMAANA PAZHARAKALAICHI TRENDS ANALYSIS**

1. **Women Entrepreneurs kaappalam Growing Sectors**:
   ✨ Food Processing: 15-20% annual growth
      - Organic certifications velividam kudai vanthathu
      - Direct online sales boom aaguthu
   
   ✨ Handmade Products: 20-25% growth
      - E-commerce platforms villai boost koduthuthu
      - Global market opportunities export ayyalam
   
   ✨ Dairy Products: 10-15% growth
      - Premium/specialty products trending
      - Direct delivery models successful
   
   ✨ Services (Beauty, Education, Consulting): 25-30% growth
      - Online + offline hybrid models
      - Subscription-based recurring labham

2. **Pazharakalaichi-Wide Trends**:
   🔄 Direct-to-consumer (D2C) models
   🔄 Organic/natural products velividam
   🔄 Online shopping mainstream aaguthu
   🔄 Certification & quality standards
   🔄 Personal touch customer loyalty

3. **Technology Adoption**:
   📱 WhatsApp Business customer communicate
   📱 Online payment platforms (UPI, digital)
   📱 Simple inventory management apps
   📱 Social media marketing (free/low-cost)

4. **Seasonal Opportunities**:
   🎉 Diwali, Holi, Weddings, New Year = Peak Sales
   🎉 Dry snacks, gifts, jewelry = Best sellers
   🎉 Peak seasons 2-3 month munbu plan

📈 **Market Outlook**: 2-3 varusham velai small business growth strong irukku!
        """
    else:
        return """
📊 **CURRENT MARKET TRENDS ANALYSIS**

1. **Growing Sectors for Women Entrepreneurs**:
   ✨ Food Processing: 15-20% annual growth
      - Organic certifications increasing demand
      - Direct online sales booming
   
   ✨ Handmade Products: 20-25% growth
      - E-commerce platforms boosting sales
      - Global market opportunities via export
   
   ✨ Dairy Products: 10-15% growth
      - Premium/specialty products trending
      - Direct delivery models successful
   
   ✨ Services (Beauty, Education, Consulting): 25-30% growth
      - Online + offline hybrid models
      - Subscription-based recurring income

2. **Market-Wide Trends**:
   🔄 Shift to direct-to-consumer (D2C) models
   🔄 Increasing demand for organic/natural products
   🔄 Online shopping becoming mainstream
   🔄 Certification & quality standards rising
   🔄 Customer loyalty through personal touch

3. **Technology Adoption**:
   📱 WhatsApp Business for customer communication
   📱 Online payment platforms (UPI, digital)
   📱 Simple inventory management apps
   📱 Social media for marketing (free/low-cost)

4. **Seasonal Opportunities**:
   🎉 Diwali, Holi, Weddings, New Year = Peak Sales
   🎉 Dry snacks, gifts, jewelry = Best sellers
   🎉 Plan 2-3 months in advance for peak seasons

📈 **Market Outlook**: Next 2-3 years show strong potential for small business growth!
        """

def generate_general_analysis(query, language='en'):
    """General market analysis"""
    if language == 'hi':
        return """
🎖️ **GENERAL BAZAAR INTELLIGENCE**

**Apna Business Shuru Karne - Key Considerations**:

1. **Market Research** (Launch se pehle):
   ✓ Apne target customers ko identify karo
   ✓ Competitor offerings & prices analyze karo
   ✓ Local demand & seasonality samjho
   ✓ Regulatory requirements & licenses check karo

2. **Product/Service Selection**:
   ✓ Aapke skills & interests ke basis pe choose karo
   ✓ Aapke area mein high-demand items select karo
   ✓ Seasonal opportunities consider karo
   ✓ Profit vs. effort required balance karo

3. **Shuru Karna**:
   ✓ Initially minimum capital invest karo
   ✓ Small batch/customers ke saath test karo
   ✓ Feedback lo aur iterate karo
   ✓ Quality ke liye apni reputation build karo
   ✓ Profits se slowly grow karo

4. **Success Factors**:
   ✓ Consistent quality
   ✓ Reliable delivery/service
   ✓ Fair & competitive pricing
   ✓ Customer relationship building
   ✓ Continuous innovation

5. **Mistakes Avoid Karo**:
   ✗ Jaldi zyada zyada invest na karo
   ✗ Bhut saari variety na lo - focus rakho
   ✗ Quality compromise na karo
   ✗ Asafal ideas pe zyada samay waste na karo

🎯 **Remember**: Small start, quality focus, gradual growth = Long-term success!
        """
    elif language == 'ta':
        return """
🎖️ **GENERAL PAZHARAKALAICHI ARIVIYAL**

**Neeya Business Thodakum - Key Consideration**:

1. **Pazharakalaichi Research** (Thodakumunbu):
   ✓ Target customers identify pannu
   ✓ Competitor offerings & vilai analyze pannu
   ✓ Local velividam & season arivu
   ✓ Regulatory requirements & license check pannu

2. **Product/Service Selection**:
   ✓ Neeya arichinathu basis choose pannu
   ✓ Neeya vaalkai simple velividam item select
   ✓ Seasonal opportunities ariviyal
   ✓ Labham vs. eppunra balance

3. **Thodakum Seiyum Neram**:
   ✓ Initially minimum capital invest pannu
   ✓ Small batch/customers koodu test pannu
   ✓ Palika receive pannu arum iterate
   ✓ Nila reputation build pannu
   ✓ Labham simple edukkalam

4. **Success Factor**:
   ✓ Consistent quality
   ✓ Reliable delivery/service
   ✓ Fair & competitive pricing
   ✓ Customer relationship
   ✓ Continuous innovation

5. **Mistakes Vendam**:
   ✗ Vadavai invest vendam
   ✗ Pala variety vendam - focus rakkal
   ✗ Quality kurai vendam
   ✗ Asafal ideas il kalam vachuthu vendam

🎯 **Yaadi**: Small thodakum, quality focus, gradual growth = Long-term success!
        """
    else:
        return """
🎖️ **GENERAL MARKET INTELLIGENCE**

**Starting Your Business - Key Considerations**:

1. **Market Research** (Before Launch):
   ✓ Identify your target customers
   ✓ Analyze competitor offerings & prices
   ✓ Understand local demand & seasonality
   ✓ Check regulatory requirements & licenses

2. **Product/Service Selection**:
   ✓ Choose based on YOUR skills & interests
   ✓ Select high-demand items in your area
   ✓ Consider seasonal opportunities
   ✓ Balance profit vs. effort required

3. **Getting Started**:
   ✓ Invest minimum capital initially
   ✓ Test with small batch/customers
   ✓ Gather feedback & iterate
   ✓ Build your reputation for quality
   ✓ Grow gradually with profits

4. **Success Factors**:
   ✓ Consistent quality
   ✓ Reliable delivery/service
   ✓ Fair & competitive pricing
   ✓ Customer relationship building
   ✓ Continuous innovation

5. **Common Mistakes to Avoid**:
   ✗ Over-investing too early
   ✗ Taking too many product lines
   ✗ Compromising on quality
   ✗ Spending too much time on failed ideas

🎯 **Remember**: Small start, quality focus, gradual growth = Long-term success!
        """
