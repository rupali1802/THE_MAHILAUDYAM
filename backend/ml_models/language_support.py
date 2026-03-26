"""
Mahila Udyam - Language Support
50+ response templates for 9 intents across 3 languages
"""
import re


# ==================== RESPONSE TEMPLATES ====================

TEMPLATES = {
    'income': {
        'en': {
            'confirm': 'Income of ₹{amount} from {source} recorded for {date}.',
            'query': 'How much income did you receive? And from which source?',
            'today': 'Your total income today is ₹{amount}.',
            'error': 'Sorry, I could not understand the income amount. Please say clearly, like "five hundred rupees income from vegetable sale".',
            'success': '✓ Income recorded! ₹{amount} from {source}.',
        },
        'hi': {
            'confirm': '{date} ko {source} se ₹{amount} ki aay record ho gayi.',
            'query': 'Aapko kitni aay hui? Kahan se?',
            'today': 'Aaj aapki kul aay ₹{amount} hai.',
            'error': 'Maafi kijiye, aay samajh nahi aayi. Clearly bolein jaise "sabji bikri se paanch sau rupaye".',
            'success': '✓ Aay record ho gayi! ₹{amount} {source} se.',
        },
        'ta': {
            'confirm': '{date} anil {source} irunthu ₹{amount} varumanam padhivu seyyappattathu.',
            'query': 'Ungalukku ethanai varumanam kidaitthathu? Engirunthu?',
            'today': 'Indru ungal motta varumanam ₹{amount}.',
            'error': 'Mannikavum, varumaanatthai puriyavillai. Theliva sollunga, udhaaranam: "kaaikari vittirkaiyil ainjoothu roopaay".',
            'success': '✓ Varumanam padhivu! ₹{amount} {source} irunthu.',
        },
    },
    'expense': {
        'en': {
            'confirm': 'Expense of ₹{amount} for {category} recorded.',
            'query': 'What was the expense for? How much did you spend?',
            'today': 'Your total expenses today are ₹{amount}.',
            'error': 'Please tell me clearly - how much did you spend and for what?',
            'success': '✓ Expense recorded! ₹{amount} for {category}.',
        },
        'hi': {
            'confirm': '{category} ke liye ₹{amount} kharcha record hua.',
            'query': 'Kaunsa kharcha hua? Kitna kharch hua?',
            'today': 'Aaj aapka kul kharcha ₹{amount} hai.',
            'error': 'Clearly batayein - kitna kharch hua aur kisliye?',
            'success': '✓ Kharcha record hua! ₹{amount} {category} ke liye.',
        },
        'ta': {
            'confirm': '{category} selavu ₹{amount} padhivu seyyappattathu.',
            'query': 'Enna selavu aachu? Ethanai roopaay?',
            'today': 'Indru ungal motta selavu ₹{amount}.',
            'error': 'Theliva sollunga - ethanai selavu aachu, ennatkkaaga?',
            'success': '✓ Selavu padhivu! ₹{amount} {category}kkaga.',
        },
    },
    'sales': {
        'en': {
            'confirm': 'Sale recorded: {quantity} {product} sold for ₹{total}.',
            'query': 'What did you sell? How many units and at what price?',
            'today': 'Your total sales today are ₹{amount}.',
            'error': 'Please tell me - what did you sell, how many, and at what price?',
            'success': '✓ Sale recorded! {product} ₹{total}.',
        },
        'hi': {
            'confirm': 'Bikri record: {quantity} {product} ₹{total} mein bika.',
            'query': 'Kya becha? Kitne unit aur kitne mein?',
            'today': 'Aaj aapki kul bikri ₹{amount} hai.',
            'error': 'Batayein - kya becha, kitna, aur kitne mein?',
            'success': '✓ Bikri record! {product} ₹{total}.',
        },
        'ta': {
            'confirm': 'Vittirkai padhivu: {quantity} {product} ₹{total}ku vittirukkireenga.',
            'query': 'Enna vittirukkireenga? Ethanai alavai, ethanai vilaikku?',
            'today': 'Indru ungal motta vittirkai ₹{amount}.',
            'error': 'Sollunga - enna vittirukkireenga, ethanai, ethanai vilaikku?',
            'success': '✓ Vittirkai padhivu! {product} ₹{total}.',
        },
    },
    'profit': {
        'en': {
            'confirm': 'Profit for {period}: Income ₹{income} - Expense ₹{expense} = Net ₹{profit}.',
            'query': 'For which period do you want to see profit? Today, this week, or this month?',
            'today': 'Today\'s profit: ₹{profit}.',
            'error': 'Could not calculate profit. Please ensure you have income and expense records.',
            'positive': '🎉 Great work! Net profit of ₹{profit} this {period}.',
            'negative': 'Loss of ₹{loss} this {period}. Focus on increasing sales.',
        },
        'hi': {
            'confirm': '{period} laabh: Aay ₹{income} - Kharcha ₹{expense} = Net ₹{profit}.',
            'query': 'Kis period ka laabh dekhna hai? Aaj, is hafte, ya is mahine ka?',
            'today': 'Aaj ka laabh: ₹{profit}.',
            'error': 'Laabh calculate nahi ho saka. Income aur expense records check karein.',
            'positive': '🎉 Bahut badiya! Is {period} ₹{profit} ka net laabh hua.',
            'negative': 'Is {period} ₹{loss} ka nuksan hua. Bikri badhane par dhyan dein.',
        },
        'ta': {
            'confirm': '{period} laabham: Varumanam ₹{income} - Selavu ₹{expense} = Net ₹{profit}.',
            'query': 'Eppadikku laabham paarkka virukkireergal? Indru, indha vaaram, athavaa indha maadham?',
            'today': 'Indru laabham: ₹{profit}.',
            'error': 'Laabham kanakidiyavillai. Varumanam matrum selavu padhivugalai parunga.',
            'positive': '🎉 Mika nalla! Indha {period} ₹{profit} net laabham.',
            'negative': 'Indha {period} ₹{loss} nattam. Vittirkaiyai adigappaduthunga.',
        },
    },
    'market': {
        'en': {
            'confirm': 'Market price: {commodity} is ₹{price} per {unit} (Trend: {trend}).',
            'query': 'Which commodity price do you want to check?',
            'today': 'Today\'s market prices are updated.',
            'error': 'Could not find price for that commodity. Please check the Market section.',
        },
        'hi': {
            'confirm': 'Mandi bhav: {commodity} ₹{price} prati {unit} (Trend: {trend}).',
            'query': 'Kaun si chiz ka bhav dekhna hai?',
            'today': 'Aaj ke mandi ke bhav update hain.',
            'error': 'Woh chiz ka bhav nahi mila. Market section mein dekhein.',
        },
        'ta': {
            'confirm': 'Santhai vilai: {commodity} ₹{price} oru {unit}ku (Nilaimai: {trend}).',
            'query': 'Enna porulin vilai paarkka virukkireergal?',
            'today': 'Indru santhai vilaigal pudhuppikkappattathu.',
            'error': 'Andha porulin vilai kaanavum. Market pakkam parunga.',
        },
    },
    'schemes': {
        'en': {
            'confirm': 'Scheme found: {name} by {agency}. Benefits: {benefits}.',
            'query': 'Are you looking for a loan scheme, subsidy, or training program?',
            'today': '{count} active government schemes available for women entrepreneurs.',
            'error': 'Could not find matching schemes. Check the Schemes section for all available options.',
        },
        'hi': {
            'confirm': 'Yojana mili: {name} ({agency}). Fayde: {benefits}.',
            'query': 'Loan yojana, subsidy, ya training program chahiye?',
            'today': 'Mahila udyamiyoin ke liye {count} sarkaari yojanayen available hain.',
            'error': 'Matching yojana nahi mili. Schemes section mein sabhi options dekhein.',
        },
        'ta': {
            'confirm': 'Thittam kidaitthathu: {name} ({agency}). Nanmaikal: {benefits}.',
            'query': 'Kadhan thittam, subsidy, athavaa payirchi thittam venduma?',
            'today': 'Penmani thozhilalargalukku {count} arasin thittagal tharaippatta ullathu.',
            'error': 'Poruntha thittam illaathathu. Schemes pakkam ellaa thittagalaiyum parunga.',
        },
    },
    'mentor': {
        'en': {
            'confirm': 'Mentor {name} ({expertise}) is {availability}. Contact: {contact}.',
            'query': 'What kind of business help do you need? I can connect you with the right mentor.',
            'today': '{count} mentors are available now.',
            'error': 'Could not find a suitable mentor. Check the Mentor section.',
        },
        'hi': {
            'confirm': 'Mentor {name} ({expertise}) {availability} hain. Contact: {contact}.',
            'query': 'Kaunsi business help chahiye? Sahi mentor se connect kar sakti hoon.',
            'today': 'Abhi {count} mentors available hain.',
            'error': 'Suitable mentor nahi mila. Mentor section check karein.',
        },
        'ta': {
            'confirm': 'Mentor {name} ({expertise}) {availability} ullanar. Thodarpugal: {contact}.',
            'query': 'Enna thozhil udhavi thevai? Sariyaana mentorodu inaippen.',
            'today': 'Ippoathu {count} mentorgal kaaittirukkinranar.',
            'error': 'Thagundha mentor illaathathu. Mentor pakkam parunga.',
        },
    },
    'payment': {
        'en': {
            'confirm': 'Payment of ₹{amount} via {method} recorded. Status: {status}.',
            'query': 'Tell me about the payment - amount, method (UPI/Cash/Bank), and direction (received/sent).',
            'today': 'Your UPI ID: {upi_id}. Share this QR to receive payments.',
            'error': 'Payment details unclear. Please specify amount and payment method.',
        },
        'hi': {
            'confirm': '₹{amount} {method} payment record hua. Status: {status}.',
            'query': 'Payment ki detail batayein - amount, tarika (UPI/Cash/Bank), aur direction (mila/diya).',
            'today': 'Aapka UPI ID: {upi_id}. Payment receive karne ke liye QR share karein.',
            'error': 'Payment detail samajh nahi aayi. Amount aur tarika batayein.',
        },
        'ta': {
            'confirm': '₹{amount} {method} moolam pana parivarthanai padhivu. Nilaimai: {status}.',
            'query': 'Pana parivarthanai patrri sollunga - thokai, vazi (UPI/Cash/Bank), matrum thiccham.',
            'today': 'Ungal UPI ID: {upi_id}. Panaththa pethukka QR share pannunga.',
            'error': 'Pana parivarthanai vivarangal puriyavillai. Thokai matrum vaziyai sollunga.',
        },
    },
    'training': {
        'en': {
            'confirm': 'Training module available: {topic}.',
            'query': 'What skill would you like to learn? Business, digital, or financial skills?',
            'today': 'New training resources available: {topics}.',
            'error': 'Training resource not found. Check the Training section.',
        },
        'hi': {
            'confirm': 'Training module available: {topic}.',
            'query': 'Kaunsi skill seekhni hai? Business, digital, ya financial skills?',
            'today': 'Nayi training resources available: {topics}.',
            'error': 'Training resource nahi mila. Training section dekhein.',
        },
        'ta': {
            'confirm': 'Payirchi module kaaittirukkirathu: {topic}.',
            'query': 'Enna thiranai kalka virukkireergal? Thozhil, digital, athavaa nidhi thirangal?',
            'today': 'Pudiya payirchi valimaigal ullathu: {topics}.',
            'error': 'Payirchi vazhimurai illaathathu. Payirchi pakkam parunga.',
        },
    },
}


def get_template(intent, variant, language='en', **kwargs):
    """
    Get a response template for an intent and variant.
    Falls back to English if translation not found.
    """
    intent_templates = TEMPLATES.get(intent, {})
    lang_templates = intent_templates.get(language, intent_templates.get('en', {}))
    template = lang_templates.get(variant, '')

    if not template and language != 'en':
        # Fallback to English
        en_templates = intent_templates.get('en', {})
        template = en_templates.get(variant, '')

    if not template:
        return f'Action: {intent}'

    try:
        return template.format(**kwargs)
    except KeyError:
        return template


def extract_entities_from_text(text, language='en'):
    """
    Extract entities (amounts, dates, categories) from text.
    Returns dict with extracted values.
    """
    entities = {}

    # Extract amount - look for numbers
    amount_patterns = [
        r'₹\s*(\d+(?:,\d+)*(?:\.\d+)?)',
        r'(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:rupees?|rupaye|roopaay|rs\.?)',
        r'(\d+(?:,\d+)*(?:\.\d+)?)\s*(?:thousand|hazaar|aayiram)',
        r'(\d+(?:,\d+)*(?:\.\d+)?)',
    ]

    for pattern in amount_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            amount_str = match.group(1).replace(',', '')
            try:
                if 'thousand' in text.lower() or 'hazaar' in text.lower() or 'aayiram' in text.lower():
                    entities['amount'] = float(amount_str) * 1000
                elif 'lakh' in text.lower() or 'laakh' in text.lower() or 'latcham' in text.lower():
                    entities['amount'] = float(amount_str) * 100000
                else:
                    entities['amount'] = float(amount_str)
                break
            except ValueError:
                pass

    # Extract category for expenses
    expense_categories = {
        'raw_material': ['raw material', 'kachcha maal', 'kacha porul', 'material'],
        'transport': ['transport', 'travel', 'yatra', 'payanam'],
        'rent': ['rent', 'kiraya', 'vaadagai'],
        'electricity': ['electricity', 'bijli', 'minu'],
        'labor': ['labor', 'labour', 'mazdoori', 'koolikal'],
        'marketing': ['marketing', 'advertisement', 'vishyapan'],
        'equipment': ['equipment', 'machine', 'yantiram'],
    }

    for category, keywords in expense_categories.items():
        if any(kw in text.lower() for kw in keywords):
            entities['category'] = category
            break

    # Extract product/source
    source_patterns = [
        r'from\s+([a-zA-Z\s]+?)(?:\s+sale|\s+selling|\s+business|$)',
        r'for\s+([a-zA-Z\s]+?)(?:\s+sale|\s+selling|$)',
        r'(\w+(?:\s+\w+)?)\s+(?:becha|vikri|vittirkai)',
    ]

    for pattern in source_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            entities['source'] = match.group(1).strip()
            break

    return entities
