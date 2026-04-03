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
            'query': 'Great! Tell me - how much income did you make, and what was the source? For example, vegetable sales, handicraft, or dairy products?',
            'today': 'Your total income today is ₹{amount}.',
            'error': 'I want to help you record this, but I need the amount clearly. Could you say it again?',
            'success': '✓ Excellent! Income of ₹{amount} from {source} is now recorded in your account.',
        },
        'hi': {
            'confirm': '{date} ko {source} se ₹{amount} ki aay record ho gayi.',
            'query': 'Bahut achcha! Batayein - aapko kitni aay hui aur kahan se? Jaise sabji bikri, handicraft, ya dairy ka byapar?',
            'today': 'Aaj aapki kul aay ₹{amount} hai.',
            'error': 'Main aapki madad karna chahti hoon, lekin mujhe amount clearly chahiye. Dobara bolein?',
            'success': '✓ Waah! ₹{amount} {source} se aay aapke account mein record ho gayi.',
        },
        'ta': {
            'confirm': '{date} anil {source} irunthu ₹{amount} varumanam padhivu seyyappattathu.',
            'query': 'Mika nalla! Sollunga - ethanai varumanam adum aachu, engkirunthu? Udhaaranam: kaaikari vittirkai, handicraft, dairy?',
            'today': 'Indru ungal motta varumanam ₹{amount}.',
            'error': 'Naan ungai udavi seya viruppan, aanaal thokkam theliva trevai. Punppu sollunga?',
            'success': '✓ Waah! ₹{amount} {source} irunthu varumanam ungal accountil padhivu aaylathu.',
        },
    },
    'expense': {
        'en': {
            'confirm': 'Expense of ₹{amount} for {category} recorded.',
            'query': 'I see you spent money! Could you tell me - what did you buy and how much did it cost? For example, raw materials, transport, or supplies?',
            'today': 'Your total expenses today are ₹{amount}.',
            'error': 'I understand you had an expense, but I need more details. What did you spend on, and how much?',
            'success': '✓ Perfect! Your expense of ₹{amount} for {category} has been recorded.',
        },
        'hi': {
            'confirm': '{category} ke liye ₹{amount} kharcha record hua.',
            'query': 'Dekh rahi hoon aapne paisa kharch kiya! Batayein - kya liya aur kitna kharch hua? Jaise raw material, transport, ya samaan?',
            'today': 'Aaj aapka kul kharcha ₹{amount} hai.',
            'error': 'Samajh rahi hoon kharcha hua, lekin mujhe aur detail chahiye. Kisliye kharch aur kitna?',
            'success': '✓ Bilkul! Aapka ₹{amount} kharcha {category} ke liye record ho gaya.',
        },
        'ta': {
            'confirm': '{category} selavu ₹{amount} padhivu seyyappattathu.',
            'query': 'Panam kharchettirukkireenga! Sollunga - enna vittirukkal aum ettanai kharch? Udhaaranam: kacha porul, payanam, samaan?',
            'today': 'Indru ungal motta selavu ₹{amount}.',
            'error': 'Puriyum selavu aachu, aanaal ennum detail kariam. Enna vittirukkal, ethanai?',
            'success': '✓ Sari! Ungal ₹{amount} selavu {category}kkaaga padhivu seyyappattlathu.',
        },
    },
    'sales': {
        'en': {
            'confirm': 'Sale recorded: {quantity} {product} sold for ₹{total}.',
            'query': 'Wonderful! You made a sale! Help me record this - what did you sell, how many units, and what was the price?',
            'today': 'Your total sales today are ₹{amount}.',
            'error': 'Great that you made a sale! I just need clarity on what you sold, quantity, and price.',
            'success': '✓ Fantastic! Your sale of {product} for ₹{total} has been recorded successfully!',
        },
        'hi': {
            'confirm': 'Bikri record: {quantity} {product} ₹{total} mein bika.',
            'query': 'Bailkul! Aapne bikri ki! Mujhe record karne mein madad karein - kya becha, kitne unit, aur kitne mein?',
            'today': 'Aaj aapki kul bikri ₹{amount} hai.',
            'error': 'Bahut badiya bikri hui! Mujhe sirf samajhna hai kya becha, kitna, aur kitne mein.',
            'success': '✓ Bahut badhiya! Aapki {product} ki bikri ₹{total} mein record ho gayi!',
        },
        'ta': {
            'confirm': 'Vittirkai padhivu: {quantity} {product} ₹{total}ku vittirukkireenga.',
            'query': 'Vaazhkai! Neer vittirukkireenga! Padhivu seya udavi seyyunga - enna vittir, ethanai, ethanai vilai?',
            'today': 'Indru ungal motta vittirkai ₹{amount}.',
            'error': 'Mika nalla vittirkai! Tholaikkai, alavai, vilai puriya trevai.',
            'success': '✓ Vaazhkai! Ungal {product} vittirkai ₹{total}ku padhivu seyyappattlathu!',
        },
    },
    'profit': {
        'en': {
            'confirm': 'Profit for {period}: Income ₹{income} - Expense ₹{expense} = Net ₹{profit}.',
            'query': 'Let me calculate your profit! For which period would you like to check - today, this week, or this month?',
            'today': 'Today\'s profit: ₹{profit}.',
            'error': 'I want to help you see your profit, but I need your income and expense data. Please record some transactions first.',
            'positive': '🎉 Fantastic work! You\'ve made a net profit of ₹{profit} this {period}. Keep it up!',
            'negative': 'I see a loss of ₹{loss} this {period}. Let\'s focus on increasing sales and managing costs better.',
        },
        'hi': {
            'confirm': '{period} laabh: Aay ₹{income} - Kharcha ₹{expense} = Net ₹{profit}.',
            'query': 'Aapka laabh calculate karti hoon! Kaunse period ka - Aaj, is hafte, ya is mahine ka?',
            'today': 'Aaj ka laabh: ₹{profit}.',
            'error': 'Laabh dikhana chahti hoon par mujhe aay aur kharcha ka data chahiye. Pehle kuch transaction record karein.',
            'positive': '🎉 Bahut badhiya! Is {period} ₹{profit} ka net laabh earn kiya. Aage bhi yaisi hi kamyabi!',
            'negative': 'Is {period} ₹{loss} ka nuksan hai. Bikri badhane aur kharche par niyantran rakhne par dhyan dein.',
        },
        'ta': {
            'confirm': '{period} laabham: Varumanam ₹{income} - Selavu ₹{expense} = Net ₹{profit}.',
            'query': 'Ungal laabham calculate pannipen! Enna period: Indru, indha vaaram, athavaa indha maadham?',
            'today': 'Indru laabham: ₹{profit}.',
            'error': 'Laabham kaattukka viruppan, aanaal varumanam aum selavu data trevai. Mudal kuraichal padhivu seyyunga.',
            'positive': '🎉 Mika vaazhkai! Indha {period} ₹{profit} net laabham seitteergal. Miga ninaithukollunga!',
            'negative': 'Indha {period} ₹{loss} nattam ullathu. Vittirkai adigappaduthunga matrum selavu kontrolil vettunga.',
        },
    },
    'market': {
        'en': {
            'confirm': 'Market price: {commodity} is ₹{price} per {unit} (Trend: {trend}).',
            'query': 'Smart choice! Which commodity would you like me to check the current market price for?',
            'today': 'Today\'s market prices have been updated. You can check any commodity in the Market section.',
            'error': 'I couldn\'t find that commodity in the market. Try checking the Market section for all available options.',
        },
        'hi': {
            'confirm': 'Mandi bhav: {commodity} ₹{price} prati {unit} (Trend: {trend}).',
            'query': 'Samjhdar faislaa! Kaunsi chiz ka mandi bhav dekhna hai?',
            'today': 'Aaj ke mandi ke bhav update ho gaye. Market section mein koi bhi chiz dekhein.',
            'error': 'Woh chiz market mein nahi mili. Market section mein sabhi options dekhein.',
        },
        'ta': {
            'confirm': 'Santhai vilai: {commodity} ₹{price} oru {unit}ku (Nilaimai: {trend}).',
            'query': 'Perumaan thavanamudal! Enna porulin sandipaavai paarkka viruppireergal?',
            'today': 'Indru santhai vilaikal pudhuppikkappattu. Market pattiilula ella porulinum paarkka ollathu.',
            'error': 'Andha poruli santhaiyil illaathathu. Market pakkam ella vilaigalum parunga.',
        },
    },
    'schemes': {
        'en': {
            'confirm': 'Scheme found: {name} by {agency}. Benefits: {benefits}.',
            'query': 'Excellent! I can help you find the right scheme. What are you looking for - a loan, subsidy, or training program?',
            'today': '{count} active government schemes are available for women entrepreneurs like you.',
            'error': 'Let me help you find the perfect scheme. Visit the Schemes section to explore all available options tailored for your business.',
        },
        'hi': {
            'confirm': 'Yojana mili: {name} ({agency}). Fayde: {benefits}.',
            'query': 'Bilkul! Main aapko sahi yojana dhundarne mein madad kar sakti hoon. Loan, subsidy, ya training program?',
            'today': 'Mahila udyamiyoin ke liye {count} sarkaari yojanayen available hain.',
            'error': 'Aapke liye sahi yojana dhundne mein madad kar sakti hoon. Schemes section mein explore karein.',
        },
        'ta': {
            'confirm': 'Thittam kidaitthathu: {name} ({agency}). Nanmaikal: {benefits}.',
            'query': 'Sari! Sariyaana thittam kidaika udavi seyan. Kadan, subsidy, athavaa payirchi?',
            'today': 'Penmani thozhilalgalukku {count} arasin thittagal ullathu.',
            'error': 'Ungalukku sariyaana thittam kidaika udavi seyan. Schemes pakkam explore pannunga.',
        },
    },
    'mentor': {
        'en': {
            'confirm': 'Mentor {name} ({expertise}) is {availability}. Contact: {contact}.',
            'query': 'Perfect! I can connect you with an AI-powered mentor who specializes in your field. What kind of business guidance do you need?',
            'today': '{count} expert mentors are available right now to guide your business.',
            'error': 'Don\'t worry! Visit the Mentor section to find the perfect advisor for your specific business needs.',
        },
        'hi': {
            'confirm': 'Mentor {name} ({expertise}) {availability} hain. Contact: {contact}.',
            'query': 'Bilkul! Main aapko AI mentor se connect kar sakti hoon jo aapke field mein expert ho. Kaunsi business guidance chahiye?',
            'today': 'Abhi {count} expert mentors available hain aapke business ko guide karne ke liye.',
            'error': 'Bilkul ghabraayen nahi! Mentor section mein apne business ke liye perfect advisor khojein.',
        },
        'ta': {
            'confirm': 'Mentor {name} ({expertise}) {availability} ullanar. Thodarpugal: {contact}.',
            'query': 'Sari! AI mentorodu ninaippen avanai thozhhil marunthukkol makakkum. Enna guidance trevai?',
            'today': 'Ippoathu {count} expert mentorgal ungal thozhilai guide panna kaaittirukkinranar.',
            'error': 'Bayam illa! Mentor pakkam ungal latchamukka mentor kidaika pugunga.',
        },
    },
    'payment': {
        'en': {
            'confirm': 'Payment of ₹{amount} via {method} recorded. Status: {status}.',
            'query': 'Great! Let me help track this payment. Tell me - the amount, method (UPI, Cash, or Bank), and whether you received or sent it.',
            'today': 'Your UPI ID: {upi_id}. Share this with customers to receive payments digitally.',
            'error': 'I want to record this payment accurately. Could you specify the amount and the payment method you used?',
        },
        'hi': {
            'confirm': '₹{amount} {method} payment record hua. Status: {status}.',
            'query': 'Bilkul! Payment track karne mein madad karti hoon. Batayein - amount, tarika (UPI, Cash, Bank), aur received ya sent?',
            'today': 'Aapka UPI ID: {upi_id}. Yeh customers ko share karein payment receive karne ke liye.',
            'error': 'Payment sahi track karna chahti hoon. Amount aur method clearly batayein.',
        },
        'ta': {
            'confirm': '₹{amount} {method} pana parivarthanai padhivu. Nilaimai: {status}.',
            'query': 'Sari! Pana parivarthanai kelvi panna udavi seyan. Sollunga - thokai, vazi (UPI, Cash, Bank), pethukka athavaa pattukkava?',
            'today': 'Ungal UPI ID: {upi_id}. Itu kayyetiyilai kuttunga pana pethukka.',
            'error': 'Pana parivarthanai sari padhivu pannum. Thokai mutrum vazi theliva sollunga.',
        },
    },
    'training': {
        'en': {
            'confirm': 'Training module available: {topic}.',
            'query': 'Smart thinking! What skill would you like to develop? Business management, digital marketing, or financial literacy?',
            'today': 'New training resources covering {topics} are now available for you.',
            'error': 'Visit the Training section to access free courses and resources to enhance your business skills.',
        },
        'hi': {
            'confirm': 'Training module available: {topic}.',
            'query': 'Samjhdar soch! Kaunsi skill develop karna chahti ho? Business, digital marketing, ya financial training?',
            'today': '{topics} pe nayi training resources available hain.',
            'error': 'Training section mein jaoen free courses aur resources dekhen apni skills badhane ke liye.',
        },
        'ta': {
            'confirm': 'Payirchi module kaaittirukkirathu: {topic}.',
            'query': 'Perumaan sinthanaigal! Enna thiranai kalka viruppireergal? Thozhil, digital, athavaa nidhi?',
            'today': '{topics} matrikum payirchi vidhaigal ullathu.',
            'error': 'Payirchi pakkam poi free padhikal, serikal paarkkal muthalai vidhaigal parunga.',
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
