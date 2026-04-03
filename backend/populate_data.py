#!/usr/bin/env python
"""
Populate Market Prices and Schemes data
Run: python populate_data.py
"""
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mahila_udyam_backend.settings')
django.setup()

from api.models import MarketPrice, Scheme

# Clear existing data
print("🗑️  Clearing existing data...")
MarketPrice.objects.all().delete()
Scheme.objects.all().delete()

# ==================== MARKET PRICES ====================
print("\n📊 Adding Market Prices...")

market_prices_data = [
    # Vegetables
    ('Tomato', 25, 'kg', 'Chennai Fruit Market', 'up', {'en': 'Rising', 'hi': 'बढ़ रहा है', 'ta': 'ஏறுகிறது'}),
    ('Onion', 35, 'kg', 'Delhi Mandi', 'stable', {'en': 'Stable', 'hi': 'स्थिर', 'ta': 'நிலையான'}),
    ('Potato', 18, 'kg', 'Rajasthan Mandi', 'down', {'en': 'Falling', 'hi': 'गिर रहा है', 'ta': 'குறைகிறது'}),
    ('Carrot', 30, 'kg', 'Chennai Fruit Market', 'up', {'en': 'Rising', 'hi': 'बढ़ रहा है', 'ta': 'ஏறுகிறது'}),
    
    # Fruits
    ('Banana', 40, 'piece', 'Chennai Fruit Market', 'stable', {'en': 'Stable', 'hi': 'स्थिर', 'ta': 'நிலையான'}),
    ('Mango', 60, 'kg', 'Chennai Fruit Market', 'up', {'en': 'Rising', 'hi': 'बढ़ रहा है', 'ta': 'ஏறுகிறது'}),
    ('Orange', 45, 'kg', 'Delhi Mandi', 'stable', {'en': 'Stable', 'hi': 'स्थिर', 'ta': 'நிலையான'}),
    ('Apple', 80, 'kg', 'Delhi Mandi', 'down', {'en': 'Falling', 'hi': 'गिर रहा है', 'ta': 'குறைகிறது'}),
    
    # Dairy
    ('Milk', 55, 'liter', 'Tamil Nadu Dairy', 'stable', {'en': 'Stable', 'hi': 'स्थिर', 'ta': 'நிலையான'}),
    ('Yogurt', 65, 'liter', 'Delhi Dairy', 'up', {'en': 'Rising', 'hi': 'बढ़ रहा है', 'ta': 'ஏறுகிறது'}),
    ('Paneer', 350, 'kg', 'Tamil Nadu Dairy', 'stable', {'en': 'Stable', 'hi': 'स्थिर', 'ta': 'நிலையான'}),
    ('Ghee', 800, 'kg', 'Tamil Nadu Dairy', 'up', {'en': 'Rising', 'hi': 'बढ़ रहा है', 'ta': 'ஏறுகிறது'}),
    
    # Grains & Spices
    ('Rice', 50, 'kg', 'Delhi Mandi', 'stable', {'en': 'Stable', 'hi': 'स्थिर', 'ta': 'நிலையான'}),
    ('Wheat', 28, 'kg', 'Rajasthan Mandi', 'down', {'en': 'Falling', 'hi': 'गिर रहा है', 'ta': 'குறைகிறது'}),
    ('Turmeric', 250, 'kg', 'Chennai Fruit Market', 'up', {'en': 'Rising', 'hi': 'बढ़ रहा है', 'ta': 'ஏறுகிறது'}),
    ('Chili Powder', 200, 'kg', 'Guntur Mandi', 'up', {'en': 'Rising', 'hi': 'बढ़ रहा है', 'ta': 'ஏறுகிறது'}),
    ('Coriander', 180, 'kg', 'Guntur Mandi', 'stable', {'en': 'Stable', 'hi': 'स्थिर', 'ta': 'நிலையான'}),
    ('Black Pepper', 400, 'kg', 'Kerala Mandi', 'up', {'en': 'Rising', 'hi': 'बढ़ रहा है', 'ta': 'ஏறுகிறது'}),
    
    # Oils
    ('Coconut Oil', 180, 'liter', 'Kerala Mandi', 'stable', {'en': 'Stable', 'hi': 'स्थिर', 'ta': 'நிலையான'}),
    ('Sesame Oil', 220, 'liter', 'Chennai Fruit Market', 'up', {'en': 'Rising', 'hi': 'बढ़ रहा है', 'ta': 'ஏறுகிறது'}),
    
    # Processed Foods
    ('Pickle', 150, 'kg', 'Tamil Nadu Dairy', 'stable', {'en': 'Stable', 'hi': 'स्थिर', 'ta': 'நிலையான'}),
    ('Jams', 200, 'kg', 'Delhi Mandi', 'down', {'en': 'Falling', 'hi': 'गिर रहा है', 'ta': 'குறைகிறது'}),
    ('Dry Snacks', 300, 'kg', 'Delhi Mandi', 'stable', {'en': 'Stable', 'hi': 'स्थिर', 'ta': 'நிலையான'}),
    
    # Handmade
    ('Handmade Cloth', 500, 'piece', 'Chennai Fruit Market', 'up', {'en': 'Rising', 'hi': 'बढ़ रहा है', 'ta': 'ஏறுகிறது'}),
    ('Embroidered Saree', 2000, 'piece', 'Chennai Fruit Market', 'stable', {'en': 'Stable', 'hi': 'स्थिर', 'ta': 'நிலையான'}),
    ('Handmade Jewelry', 800, 'piece', 'Delhi Mandi', 'up', {'en': 'Rising', 'hi': 'बढ़ रहा है', 'ta': 'ஏறुगिரड़'}),
    ('Wooden Craft', 1500, 'piece', 'Rajasthan Mandi', 'stable', {'en': 'Stable', 'hi': 'स्थिर', 'ta': 'நிலையான'}),
]

for commodity, price, unit, market, trend, _ in market_prices_data:
    MarketPrice.objects.create(
        commodity_name=commodity,
        price=price,
        unit=unit,
        trend=trend,
        market_location=market,
        market_date=date.today(),
        is_active=True
    )
    print(f"  ✓ {commodity}: ₹{price}/{unit} ({trend}) @ {market}")

# ==================== GOVERNMENT SCHEMES ====================
print("\n📋 Adding Government Schemes...")

schemes_data = [
    # Loan Schemes
    {
        'en': {
            'name': 'Prime Minister MUDRA Yojana',
            'description': 'Non-collateral MUDRA loan for entrepreneurs to start/expand business',
            'eligibility': 'Indian citizens aged 18-65, conducting small business',
            'benefits': 'Up to ₹10 lakhs loan without collateral, low interest rates',
            'how_to_apply': 'Visit nearest bank or apply online at pmmy.gov.in',
        },
        'hi': {
            'name': 'प्रधानमंत्री मुद्रा योजना',
            'description': 'उद्यमियों के लिए गैर-संपार्श्विक ऋण',
            'eligibility': '18-65 वर्ष के भारतीय नागरिक, छोटा व्यवसाय करने वाले',
            'benefits': '₹10 लाख तक का ऋण बिना संपार्श्विक के, कम ब्याज दर',
            'how_to_apply': 'निकटतम बैंक में जाएं या pmmy.gov.in पर ऑनलाइन आवेदन करें',
        },
        'ta': {
            'name': 'பிரதமர் முத்ரா யோஜனா',
            'description': 'பெண் உद்யோகிகளுக்கான담保 இல்லாத கடன்',
            'eligibility': '18-65 வயது இந்திய குடிமக்கள், சிறு வணிகத்தில் உள்ளவர்கள்',
            'benefits': '₹10 லட்சம் வரை담保 இல்லாத கடன், குறைந்த வட்டி விகிதம்',
            'how_to_apply': 'அருகிலுள்ள வங்கியுக்குச் செல்லவும் அல்லது pmmy.gov.in-ல் ஆன்லைனில் விண்ணப்பிக்கவும்',
        },
        'category': 'loan',
        'agency': 'Ministry of Finance & Ministry of MSME',
        'max_amount': 1000000,
        'deadline': '2025-12-31',
        'status': 'active',
        'url': 'https://www.pmmy.gov.in'
    },
    # Subsidy Schemes
    {
        'en': {
            'name': 'Interest Subsidy Scheme for Women Entrepreneurs',
            'description': 'Government subsidizes interest for women-led businesses',
            'eligibility': 'Women entrepreneurs (30% ownership for partnership), farmers',
            'benefits': 'Interest subsidy up to 5%, subsidized training programs',
            'how_to_apply': 'Apply through District Industries Centre or nearest SIDBI office',
        },
        'hi': {
            'name': 'महिला उद्यमियों के लिए ब्याज सब्सिडी योजना',
            'description': 'महिला-नेतृत्व वाले व्यवसायों के लिए सरकार ब्याज घटाती है',
            'eligibility': 'महिला उद्यमी, किसान (साझेदारी में 30% स्वामित्व)',
            'benefits': '5% तक ब्याज सब्सिडी, सब्सिडीकृत प्रशिक्षण कार्यक्रम',
            'how_to_apply': 'जिला उद्योग केंद्र या निकटतम SIDBI कार्यालय में आवेदन करें',
        },
        'ta': {
            'name': 'பெண் உத்யோகிகளுக்கான வட்டி மானியத் திட்டம்',
            'description': 'పெண் தலைமையிலான ব్యवसాయాలకు வட్టి మానియ',
            'eligibility': 'பெண் உத்யோகிகள், விவசாயிகள் (கூட்টாக 30%소유)',
            'benefits': '5% வரை வட்டி மானியம், சப்సிடி செய்யப்பட்ட பயிற்சி நிரல்கள்',
            'how_to_apply': 'மாவட்ட தொழிற்சாலை மையத்தில் அல்லது அருகிலுள்ள SIDBI அலுவலகத்திற்கு விண்ணப்பிக்கவும்',
        },
        'category': 'subsidy',
        'agency': 'Small Industries Development Bank of India (SIDBI)',
        'max_amount': 2500000,
        'deadline': '2025-06-30',
        'status': 'active',
        'url': 'https://www.sidbi.in'
    },
    # Training Scheme
    {
        'en': {
            'name': 'National Programme for Food Processing Industries (PMFME)',
            'description': 'Scheme for setting up food processing units',
            'eligibility': 'Women entrepreneurs, SHGs, producer organizations',
            'benefits': 'Up to ₹25 lakhs loan with 35% subsidy, training support',
            'how_to_apply': 'Contact Ministry of Food Processing Industries or apply online',
        },
        'hi': {
            'name': 'खाद्य प्रसंस्करण उद्योग के लिए राष्ट्रीय कार्यक्रम (PMFME)',
            'description': 'खाद्य प्रसंस्करण इकाइयां स्थापित करने की योजना',
            'eligibility': 'महिला उद्यमी, एसएचजी, उत्पादक संगठन',
            'benefits': '₹25 लाख तक ऋण 35% सब्सिडी के साथ, प्रशिक्षण समर्थन',
            'how_to_apply': 'खाद्य प्रसंस्करण उद्योग मंत्रालय से संपर्क करें या ऑनलाइन आवेदन करें',
        },
        'ta': {
            'name': 'உணவு பதப்படுத்தல் தொழிற்சாலைக்கான தேசிய திட்டம் (PMFME)',
            'description': 'உணவு பதப்படுத்தல் அலகுகளை நிறுவுவதற்கான திட்டம்',
            'eligibility': 'பெண் உத்யோகிகள், சுயஉதவி குழுக்கள், உற்பादক அமைப்புகள்',
            'benefits': '₹25 லட்சம் வரை கடன் 35% மானியத்துடன், பயிற்சி ஆதரவு',
            'how_to_apply': 'உணவு பதப்படுத்தல் தொழிற்சாலை அமைச்சரிடம் தொடர்புகொள்ளவும் அல்லது ஆன்லைனில் விண்ணப்பிக்கவும்',
        },
        'category': 'training',
        'agency': 'Ministry of Food Processing Industries',
        'max_amount': 2500000,
        'deadline': '2025-12-31',
        'status': 'active',
        'url': 'https://mofpi.gov.in/pmfme'
    },
    # Insurance Scheme
    {
        'en': {
            'name': 'Pradhan Mantri Suraksha Bima Yojana (PMSBY)',
            'description': 'Personal accident insurance for workers & business owner',
            'eligibility': 'Laborers, self-employed, business owners (18-70 years)',
            'benefits': '₹2 lakh accident insurance, ₹1 lakh disability coverage, premium ₹12/year',
            'how_to_apply': 'Register with any bank or post office',
        },
        'hi': {
            'name': 'प्रधानमंत्री सुरक्षा बीमा योजना (PMSBY)',
            'description': 'कार्मिकों और व्यवसाय मालिकों के लिए व्यक्तिगत दुर्घटना बीमा',
            'eligibility': 'मजदूर, स्व-नियोजित, व्यवसाय मालिक (18-70 वर्ष)',
            'benefits': '₹2 लाख दुर्घटना बीमा, ₹1 लाख विकलांगता कवरेज, प्रीमियम ₹12/वर्ष',
            'how_to_apply': 'किसी भी बैंक या पोस्ट ऑफिस में पंजीकरण करें',
        },
        'ta': {
            'name': 'பிரதமர் சித்திரை பாதுகாப்பு பீமா योजना (PMSBY)',
            'description': 'உழைப்பாளிகள் மற்றும் ব్యवసାయ உதयோகி களுக்குচ் தனிப்பட்ட விபத்து பீமா',
            'eligibility': 'உழைப்பாளிகள், சுய-பணிபுரிபவர்கள், வணிக உதயோகிகள் (18-70 வயது)',
            'benefits': '₹2 லட்சம் விபத்து பீமா, ₹1 லட்சம் குறைவு கவர், பிரீமியம் ₹12/வருடம்',
            'how_to_apply': 'எந்த வங்கியிலோ அல்லது தபாल் அலுவலகத்திலோ பதிவு செய்யவும்',
        },
        'category': 'insurance',
        'agency': 'Ministry of Labour & Employment',
        'max_amount': 200000,
        'deadline': '2025-12-31',
        'status': 'active',
        'url': 'https://pmsby.gov.in'
    },
    # Market Linkage
    {
        'en': {
            'name': 'National Horticulture Mission (NHM)',
            'description': 'Government support for horticulture business development',
            'eligibility': 'Farmers, women groups, entrepreneurs in horticulture',
            'benefits': 'Subsidy up to 50%, market linkage, training facilities',
            'how_to_apply': 'Contact State Horticulture Department or ICAR office',
        },
        'hi': {
            'name': 'राष्ट्रीय बागवानी मिशन (NHM)',
            'description': 'बागवानी व्यवसाय विकास के लिए सरकारी समर्थन',
            'eligibility': 'किसान, महिला समूह, बागवानी में उद्यमी',
            'benefits': '50% तक सब्सिडी, बाजार संबंध, प्रशिक्षण सुविधाएं',
            'how_to_apply': 'राज्य बागवानी विभाग या ICAR कार्यालय से संपर्क करें',
        },
        'ta': {
            'name': 'தேசிய தோட்ட இயக்குமறை (NHM)',
            'description': 'தோட்ட வணிக வளர்ச்சிக்கான அரசு ஆதரவு',
            'eligibility': 'விவசாயிகள், பெண் குழுக்கள், தோட்ட உத்யோகிகள்',
            'benefits': '50% வரை மானியம், சந்தை இணைப்பு, பயிற்சி வசதிகள்',
            'how_to_apply': 'மாநில தோட்ட கசாப அல்லது ICAR அலுவலகத்தைத் தொடர்பு கொள்ளவும்',
        },
        'category': 'market_linkage',
        'agency': 'Ministry of Agriculture & Horticulture',
        'max_amount': 1500000,
        'deadline': '2025-09-30',
        'status': 'active',
        'url': 'https://nhm.gov.in'
    },
    # Technology Scheme
    {
        'en': {
            'name': 'Technology Upgradation Fund Scheme (TUFS)',
            'description': 'Support for adopting modern technology in business',
            'eligibility': 'SMEs, women entrepreneurs, textile/agro businesses',
            'benefits': 'Subsidy up to 20% for equipment, technology training',
            'how_to_apply': 'Register with Industrial Ministry and approved TUFS nodal agency',
        },
        'hi': {
            'name': 'प्रौद्योगिकी उन्नयन निधि योजना (TUFS)',
            'description': 'व्यवसाय में आधुनिक तकनीक अपनाने के लिए समर्थन',
            'eligibility': 'एसएमई, महिला उद्यमी, वस्त्र/कृषि व्यवसाय',
            'benefits': 'उपकरण के लिए 20% तक सब्सिडी, तकनीकी प्रशिक्षण',
            'how_to_apply': 'औद्योगिक मंत्रालय और मंजूर TUFS नोडल एजेंसी के साथ पंजीकरण करें',
        },
        'ta': {
            'name': 'தொழில்நுட்ப மேம்பாட்டு நிதி அமුற்று (TUFS)',
            'description': 'வணிகத்தில் நவீன தொழில்நுட்பத்தைத் தியக்குவதற்கான ஆதரவு',
            'eligibility': 'SME கள், பெண் உத்யோகிகள், நூல்/விவசாய வணிகம்',
            'benefits': 'உபகரணங்களுக்கு 20% வரை மானியம், தொழில்நுட்ப பயிற்சி',
            'how_to_apply': 'தொழிற்சாலை அமைச்சரிடமும் मंजूर TUFS nodal agency யிடமும் பதிவு செய்யவும்',
        },
        'category': 'technology',
        'agency': 'Ministry of Textiles / Industrial Policy',
        'max_amount': 5000000,
        'deadline': '2025-11-30',
        'status': 'active',
        'url': 'https://tufs.nic.in'
    },
    # Stree Shakti Package (Women-specific)
    {
        'en': {
            'name': 'Stree Shakti Package - Women Entrepreneur Loan',
            'description': 'Special banking package exclusively for women entrepreneurs',
            'eligibility': 'Women who own at least 50% of the business',
            'benefits': 'Preferential interest rate, reduced processing fees, ₹25 to ₹50 lakhs loan',
            'how_to_apply': 'Visit your bank branch with business plan and documents',
        },
        'hi': {
            'name': 'स्त्री शक्ति पैकेज - महिला उद्यमी ऋण',
            'description': 'महिला उद्यमियों के लिए विशेष बैंकिंग पैकेज',
            'eligibility': 'जो महिलाएं व्यवसाय का कम से कम 50% स्वामित्व रखती हैं',
            'benefits': 'अनुकूल ब्याज दर, कम प्रसंस्करण शुल्क, ₹25 से ₹50 लाख ऋण',
            'how_to_apply': 'व्यवसायिक योजना और दस्तावेजों के साथ अपनी बैंक शाखा में जाएं',
        },
        'ta': {
            'name': 'பெண் சக்தி பயன்பாற் - பெண் உத்யோகி கடன்',
            'description': 'பெண் உத்யோகிகளுக்கான சிறப்பு வங்கி தொகுப்பு',
            'eligibility': 'வணிகத்தில் குறைந்தது 50%소유 கொண்ட பெண்கள்',
            'benefits': 'சாதகமான வட்டி வீதம், குறைந்த செயல்முறை கட்டணம், ₹25 முதல் ₹50 லட்சம் கடன்',
            'how_to_apply': 'வணிक योजனை மற்றும் ஆவணங்களுடன் உங்கள் வங்கி கிளையைப் பார்வையிடவும்',
        },
        'category': 'loan',
        'agency': 'Public Sector Banks',
        'max_amount': 5000000,
        'deadline': '2025-12-31',
        'status': 'active',
        'url': 'https://www.sbi.co.in/web/personal/loans/business-loans/stree-shakti'
    },
    # Udyogini Scheme
    {
        'en': {
            'name': 'Udyogini Scheme for Women',
            'description': 'Government scheme providing financial assistance for women entrepreneurs',
            'eligibility': 'Women between 18-45 years, family income below ₹1.5 lakhs/year',
            'benefits': 'Loan up to ₹3 lakhs, Government subsidy covers half the interest',
            'how_to_apply': 'Apply through District Industries Centre with documents',
        },
        'hi': {
            'name': 'महिलाओं के लिए उद्योगिनी योजना',
            'description': 'महिला उद्यमियों को वित्तीय सहायता प्रदान करने वाली सरकारी योजना',
            'eligibility': '18-45 वर्ष की महिलाएं, पारिवारिक आय ₹1.5 लाख/वर्ष से कम',
            'benefits': '₹3 लाख तक ऋण, सरकार आधी ब्याज को सब्सिडी देती है',
            'how_to_apply': 'दस्तावेजों के साथ जिला उद्योग केंद्र के माध्यम से आवेदन करें',
        },
        'ta': {
            'name': 'பெண்களுக்கான உத்யோகிनி திட்டம்',
            'description': 'பெண் உத்யோகிகளுக்கு நிதி உதவி வழங்கும் அரசு திட்டம்',
            'eligibility': '18-45 வயது பெண்கள், குடும்ப வருமானம் ₹1.5 லட்சம்/ஆண்டுக்கு கீழே',
            'benefits': '₹3 லட்சம் வரை கடன், அரசு பாதி வட்டியை மானியமாக வழங்குகிறது',
            'how_to_apply': 'ஆவணங்களுடன் மாவட்ட தொழிற்சாலை மையத்தின் மூலம் விண்ணப்பிக்கவும்',
        },
        'category': 'loan',
        'agency': 'Ministry of Rural Development',
        'max_amount': 300000,
        'deadline': '2025-12-31',
        'status': 'active',
        'url': 'https://rural.nic.in'
    },
    # National Rural Livelihood Mission (NRLM)
    {
        'en': {
            'name': 'National Rural Livelihood Mission (NRLM Aajeevika)',
            'description': 'Women self-help groups get bank-linked loans for livelihood',
            'eligibility': 'Women self-help groups, minimum 10 members, savings for 3 months',
            'benefits': 'Bank-linked loans up to ₹15 lakhs, interest subsidy, training',
            'how_to_apply': 'Form or join SHG, register, then apply for bank linkage',
        },
        'hi': {
            'name': 'राष्ट्रीय ग्रामीण आजीविका मिशन (NRLM आजीविका)',
            'description': 'महिला स्व-सहायता समूहों को जीविका के लिए बैंक-लिंक्ड ऋण',
            'eligibility': 'महिला स्व-सहायता समूह, न्यूनतम 10 सदस्य, 3 महीने बचत',
            'benefits': 'बैंक से लिंक्ड ऋण ₹15 लाख तक, ब्याज सब्सिडी, प्रशिक्षण',
            'how_to_apply': 'SHG बनाएं या जॉइन करें, पंजीकरण करें, फिर बैंक लिंकेज के लिए आवेदन करें',
        },
        'ta': {
            'name': 'தேசிய கிராம இயาபु நிலைமை (NRLM ஆசீவிக)',
            'description': 'பெண் சுய-உதவி குழுக்கள் வாழ்வாதாரத்திற்கு வங்கி-இணைக்கப்பட்ட கடன்',
            'eligibility': 'பெண் சுய-உதவி குழुவு, குறைந்தது 10 உறுப்பினர், 3 மாத சேமிப்பு',
            'benefits': 'வங்கி-இணைக்கப்பட்ட கடன் ₹15 லட்சம் வரை, வட்டி மானியம், பயிற்சி',
            'how_to_apply': 'SHG உருவாக்கவும் அல்லது சேரவும், பதிவு செய்யவும், பின்னர் வங்கி இணைப்பிற்கு விண்ணப்பிக்கவும்',
        },
        'category': 'market_linkage',
        'agency': 'Ministry of Rural Development (NRLM)',
        'max_amount': 1500000,
        'deadline': '2025-12-31',
        'status': 'active',
        'url': 'https://aajeevika.gov.in'
    },
    # PM Vishwakarma Yojana
    {
        'en': {
            'name': 'PM Vishwakarma Yojana - Artisans Scheme',
            'description': 'Support traditional artisans and craftspeople with loans and training',
            'eligibility': 'Artisans, craftspeople, traditional business owners',
            'benefits': 'Loan up to ₹3 lakhs at 5% interest, free skill training, certification',
            'how_to_apply': 'Register on pmvishwakarma.gov.in with Aadhar and bank account',
        },
        'hi': {
            'name': 'PM विश्वकर्मा योजना - कारीगर योजना',
            'description': 'पारंपरिक कारीगरों और शिल्पकारों को ऋण और प्रशिक्षण के साथ समर्थन',
            'eligibility': 'कारीगर, शिल्पकार, पारंपरिक व्यवसायी',
            'benefits': '5% ब्याज पर ₹3 लाख तक ऋण, मुफ्त कौशल प्रशिक्षण, प्रमाणन',
            'how_to_apply': 'Aadhar और बैंक खाते के साथ pmvishwakarma.gov.in पर पंजीकरण करें',
        },
        'ta': {
            'name': 'PM விஸ்வகர்மா யோஜனை - கலைஞர் திட்டம்',
            'description': 'பாரம்பரிய கலைஞர்களை கடன் மற்றும் பயிற்சி மூலம் ஆதரிக்கவும்',
            'eligibility': 'கலைஞர்கள், கைவினையாளர்கள், பாரம்பரிய ব్यवसा உதயோகிகள்',
            'benefits': '5% வட்டিக்கு ₹3 லட்சம் வரை கடன், இராஜ்ய பயிற்சி, சான்றிதழ்',
            'how_to_apply': 'Aadhaar மற்றும் வங்கி கணக்குடன் pmvishwakarma.gov.in-ல் பதிவு செய்யவும்',
        },
        'category': 'technology',
        'agency': 'Ministry of MSME',
        'max_amount': 300000,
        'deadline': '2025-12-31',
        'status': 'active',
        'url': 'https://pmvishwakarma.gov.in'
    },
]

for scheme in schemes_data:
    Scheme.objects.create(
        name=scheme['en']['name'],
        name_hi=scheme['hi']['name'],
        name_ta=scheme['ta']['name'],
        description=scheme['en']['description'],
        description_hi=scheme['hi']['description'],
        description_ta=scheme['ta']['description'],
        eligibility=scheme['en']['eligibility'],
        eligibility_hi=scheme['hi']['eligibility'],
        eligibility_ta=scheme['ta']['eligibility'],
        benefits=scheme['en']['benefits'],
        benefits_hi=scheme['hi']['benefits'],
        benefits_ta=scheme['ta']['benefits'],
        how_to_apply=scheme['en']['how_to_apply'],
        how_to_apply_hi=scheme['hi']['how_to_apply'],
        how_to_apply_ta=scheme['ta']['how_to_apply'],
        category=scheme['category'],
        agency=scheme['agency'],
        max_amount=scheme['max_amount'],
        deadline=scheme['deadline'],
        status=scheme['status'],
        url=scheme['url']
    )
    print(f"  ✓ {scheme['en']['name']} ({scheme['category']})")

print("\n✅ Data population complete!")
print(f"   Market Prices: {MarketPrice.objects.count()}")
print(f"   Schemes: {Scheme.objects.count()}")
