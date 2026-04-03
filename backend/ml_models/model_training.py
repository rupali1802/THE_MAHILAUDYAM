"""
Mahila Udyam - ML Model Training
TF-IDF + Logistic Regression for voice intent classification
Target accuracy: 92.31% test, 94.87% training
"""
import os
import sys
import json
import pickle
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
import re

# ==================== TRAINING DATA ====================

TRAINING_DATA = [
    # INCOME
    ("I received 500 rupees today", "income"),
    ("Got income of one thousand rupees", "income"),
    ("Earned 2000 from vegetable sale", "income"),
    ("Income received 300 rupees", "income"),
    ("Add income 1500", "income"),
    ("Record my earning of 800", "income"),
    ("Got payment of 5000", "income"),
    ("Received money 2500 from milk sale", "income"),
    ("Aaj 500 rupaye ki aay hui", "income"),
    ("Mujhe 1000 rupaye mile", "income"),
    ("Aay hua 750 rupaye", "income"),
    ("Paanch sau rupaye ki kamai", "income"),
    ("Meri aay ek hazaar hai", "income"),
    ("Indru 500 roopaay varumanam kittiyathu", "income"),
    ("Aayiram roopaay varumanam kidaitthathu", "income"),
    ("Varumanam 2000 roopaay", "income"),
    ("Maadu paalaai vittirnthu 800 roopaay", "income"),
    ("Thinai vittirnthu 1500 roopaay varumanam", "income"),
    ("Income 400 rupees agriculture", "income"),
    ("Received salary payment 3000", "income"),
    ("money received from customer 600", "income"),
    ("daily income record 250", "income"),
    ("Aaj grahak se 700 rupaye mile", "income"),
    ("Varumanam padhivu 900", "income"),

    # EXPENSE
    ("I spent 200 rupees on raw material", "expense"),
    ("Expense of 500 for transport", "expense"),
    ("Paid 150 for electricity", "expense"),
    ("Spent 1000 on labor", "expense"),
    ("Add expense 300 rent", "expense"),
    ("Record spending 800 raw material", "expense"),
    ("paid 600 for equipment", "expense"),
    ("marketing expense 400 rupees", "expense"),
    ("Mera kharcha 300 rupaye hua", "expense"),
    ("Bijli ka bill 150 diya", "expense"),
    ("Transport mein 200 kharch hua", "expense"),
    ("Mazdoori ke liye 500 diya", "expense"),
    ("Kiraya 800 rupaye", "expense"),
    ("Kachcha maal 600 rupaye mein liya", "expense"),
    ("Selavu 300 roopaay", "expense"),
    ("Minu bill 150 kattinen", "expense"),
    ("Payanam 200 roopaay selavu", "expense"),
    ("Koolikal 500 roopaay", "expense"),
    ("Vaadagai 800 roopaay", "expense"),
    ("paid 250 for supplies", "expense"),
    ("spent money on packaging 180", "expense"),
    ("office expense 350 rupees", "expense"),
    ("purchase raw material 750", "expense"),
    ("delivery charge 100", "expense"),

    # SALES
    ("I sold 5 kg vegetables for 100 rupees", "sales"),
    ("Sale of saree for 800 rupees", "sales"),
    ("Sold 10 pieces of handicraft", "sales"),
    ("Record sale 500 rupees", "sales"),
    ("Sold products worth 2000", "sales"),
    ("Today's sales 1500 rupees", "sales"),
    ("Bikri 500 rupaye ki", "sales"),
    ("Aaj 10 kg doodh becha", "sales"),
    ("Saree becha 800 rupaye mein", "sales"),
    ("Khilona becha 200 rupaye", "sales"),
    ("Aaj ki bikri 1500 rupaye", "sales"),
    ("Vittirkai 500 roopaay", "sales"),
    ("Indru 10 kg kaaikari vittren", "sales"),
    ("Pottu vittirnthu 200 roopaay", "sales"),
    ("Aaj vikri 800 rupaye", "sales"),
    ("sold 3 dozen eggs 150 rupees", "sales"),
    ("sale record product 450", "sales"),
    ("sold milk today 300", "sales"),
    ("customer bought 5 pieces 1000", "sales"),
    ("product sold 600 rupees", "sales"),

    # PROFIT
    ("What is my profit this month", "profit"),
    ("Show me profit report", "profit"),
    ("How much did I earn this week", "profit"),
    ("Calculate my profit today", "profit"),
    ("Profit and loss statement", "profit"),
    ("Is mein laabh hui ya nuksan", "profit"),
    ("Mera laabh kitna hua", "profit"),
    ("Mahine ka laabh batao", "profit"),
    ("Ungal laabham ethanai", "profit"),
    ("Indha maadham laabham parunga", "profit"),
    ("Laabham loss report", "profit"),
    ("Net profit this year", "profit"),
    ("monthly earnings summary", "profit"),
    ("business profit analysis", "profit"),
    ("income vs expense report", "profit"),
    ("how much profit did I make", "profit"),
    ("kul laabh kitna hua", "profit"),
    ("Varumanam selavu kanakaadu", "profit"),

    # MARKET PRICES
    ("What is the price of tomato today", "market"),
    ("Check market price for rice", "market"),
    ("Onion price in market", "market"),
    ("Current rate of wheat", "market"),
    ("Mandi bhav batao", "market"),
    ("Aaj tamatar ka bhav kya hai", "market"),
    ("Chawal ka mandi bhav", "market"),
    ("Pyaaz kitne ka hai", "market"),
    ("Santhai vilai parunga", "market"),
    ("Indru thaakkali santhai vilai", "market"),
    ("Arisi santhai vilai ethanai", "market"),
    ("commodity price check", "market"),
    ("vegetable market rates today", "market"),
    ("what is the rate of pulses", "market"),
    ("grain price today", "market"),
    ("check price of dal", "market"),

    # SCHEMES
    ("Tell me about government schemes", "schemes"),
    ("What loans are available for women", "schemes"),
    ("Mudra yojana kya hai", "schemes"),
    ("Mahila loan scheme", "schemes"),
    ("Subsidy for small business", "schemes"),
    ("Women entrepreneur scheme", "schemes"),
    ("Sarkaari yojana batao", "schemes"),
    ("Loan scheme ki jaankari", "schemes"),
    ("Mahila udyam loan", "schemes"),
    ("Arasin thittagal parunga", "schemes"),
    ("Penmanikal loan thittam", "schemes"),
    ("Subsidy thittam ethanai", "schemes"),
    ("financial assistance government", "schemes"),
    ("what schemes am I eligible for", "schemes"),
    ("business grant for women", "schemes"),
    ("Stand up India scheme", "schemes"),

    # MENTOR
    ("I need a business mentor", "mentor"),
    ("Connect me with an expert", "mentor"),
    ("Business advice needed", "mentor"),
    ("Who can help me with my business", "mentor"),
    ("Mentor se milna hai", "mentor"),
    ("Business mein madad chahiye", "mentor"),
    ("Expert ki salah chahiye", "mentor"),
    ("Aalochanai vendumen", "mentor"),
    ("Mentor kitta pesanum", "mentor"),
    ("Thozhil aalosakaru", "mentor"),
    ("get business guidance", "mentor"),
    ("need expert help for business", "mentor"),
    ("find a mentor for me", "mentor"),
    ("connect with business advisor", "mentor"),

    # PAYMENT
    ("Record UPI payment of 500", "payment"),
    ("Cash payment received 200", "payment"),
    ("Track payment 1000 rupees", "payment"),
    ("Bank transfer 5000 done", "payment"),
    ("UPI payment 300 bheja", "payment"),
    ("Cash mein 500 mila", "payment"),
    ("Payment record karo 800", "payment"),
    ("UPI thilam 300 parivarthanai", "payment"),
    ("Cash 500 roopaay paniyaatram", "payment"),
    ("Bank transfer padhivu", "payment"),
    ("show my QR code", "payment"),
    ("UPI id share karo", "payment"),
    ("received payment today", "payment"),
    ("payment done 750", "payment"),
    ("track transactions", "payment"),

    # TRAINING
    ("I want to learn business skills", "training"),
    ("Show me training videos", "training"),
    ("How to improve my business", "training"),
    ("Digital marketing training", "training"),
    ("Kaise apna business badhao", "training"),
    ("Training chahiye business ke liye", "training"),
    ("Seekhna hai", "training"),
    ("Payirchi vendumen", "training"),
    ("Thozhil kalvi parunga", "training"),
    ("Business improve seiya payirchi", "training"),
    ("accounting training", "training"),
    ("learn financial management", "training"),
    ("skill development program", "training"),
    ("entrepreneurship training", "training"),

    # ========== ADDITIONAL TRAINING DATA FOR ROBUSTNESS ==========
    # More INCOME variations (real-world phrasing)
    ("Aaj subah 300 rupaye ki aay hui", "income"),
    ("I just received payment 500 rupees from customer", "income"),
    ("Customer paid mujhe 800 for the order", "income"),
    ("Kul 1200 rupaye ki kamai aaj", "income"),
    ("Sapte 2000 ki varumanam", "income"),
    ("Liquid cash received, amount 600", "income"),
    ("Made some money, 750 rupees", "income"),
    ("Indru 500 roopaay padhivu kittiyathu", "income"),
    ("Selling items earned me 400 rupees", "income"),
    ("Commission received 350", "income"),

    # More EXPENSE variations (realistic phrasing)
    ("Bijli ka bill 200 rupaye dena tha", "expense"),
    ("Spent 150 rupees on packaging materials", "expense"),
    ("Mazdoor ko 600 bonus diya aaj", "expense"),
    ("Transport expenses came to 250", "expense"),
    ("Purchased raw materials, bill 800", "expense"),
    ("Marketing banners cost 300", "expense"),
    ("Rent payment 1500 rupees due", "expense"),
    ("Bought equipment, 500 rupees", "expense"),
    ("Office supplies kharche, 180 rupees", "expense"),
    ("Sapte 400 transport kharcha", "expense"),

    # More SALES variations (different structures)
    ("Sold 5 kg vegetables for 100 rupees total", "sales"),
    ("Aaj 10 kg doodh 500 rupaye mein becha", "sales"),
    ("Saree bik gaya 800 rupaye mein", "sales"),
    ("Sold items worth 2000 rupees today", "sales"),
    ("Customer bought 3 items for 450 rupees", "sales"),
    ("Made a sale, amount 1200", "sales"),
    ("Vittirkai 500 roopaay kittiyathu", "sales"),
    ("Kapda vittirnthu 600 roopaay", "sales"),
    ("Today's transaction 800 rupees sale", "sales"),
    ("Goods sold for 350 rupees", "sales"),

    # More PROFIT variations
    ("Mujhe profit kitna mila is month", "profit"),
    ("Profit batao is quarter ke liye", "profit"),
    ("Kul laabh minus nuksan batao", "profit"),
    ("Monthly income minus expense kya hua", "profit"),
    ("Earning minus spending calculate karo", "profit"),
    ("Indha maadham laabham loss report", "profit"),
    ("Varumanam minus selavu ethanai", "profit"),
    ("Net earnings check karo", "profit"),
    ("Profit loss statement month end", "profit"),
    ("Calculate net profit today", "profit"),

    # More MARKET variations
    ("Aaj tamatar ka Current rate kya hai", "market"),
    ("Pyaaz market mein aaj kitne ka", "market"),
    ("Rice price check kar de", "market"),
    ("Current wheat rate in mandi", "market"),
    ("Indru kaaikari santhai vilai", "market"),
    ("Thaakkali vithai parunga mandi", "market"),
    ("Commodity prices today check", "market"),
    ("What's the going rate for chickpeas", "market"),
    ("Pulses price in market today", "market"),
    ("Dal rate check karao", "market"),

    # More SCHEMES variations
    ("Loan lena hai, scheme bata", "schemes"),
    ("MUDRA yojana details", "schemes"),
    ("Women entrepreneur benefit scheme", "schemes"),
    ("Subsidy milega mujhe kya", "schemes"),
    ("Aaj government catering scheme apply kaise karen", "schemes"),
    ("Prime Minister scheme for women", "schemes"),
    ("Stand Up India check karao", "schemes"),
    ("Mahila udyam ni loan scheme", "schemes"),
    ("Arasin thittam details parungal", "schemes"),
    ("Business grant apply kaise hota", "schemes"),

    # More MENTOR variations
    ("Mentor connect kar do please", "mentor"),
    ("Business expert chahiye", "mentor"),
    ("Guidance chahiye business growth ke liye", "mentor"),
    ("Aalochanai vendumen expert kooda", "mentor"),
    ("Kise aitbar kar sakte hain guidance ke liye", "mentor"),
    ("Business advice chahiye urgent", "mentor"),
    ("Find someone to help my business", "mentor"),
    ("Thozhil alasukarudan pesanam", "mentor"),
    ("Expert consultation needed", "mentor"),
    ("Mentor service available", "mentor"),

    # More PAYMENT variations
    ("Received payment via UPI", "payment"),
    ("Cash payment 300 received", "payment"),
    ("Bank transfer record 5000 rupees", "payment"),
    ("UPI se 600 payment mila", "payment"),
    ("Online payment record karo 1500", "payment"),
    ("Check payment tracking 800", "payment"),
    ("Payment method UPI 400 rupees", "payment"),
    ("Padhivu cash 250 poorayiya", "payment"),
    ("Payment thilam 500 rupaye", "payment"),
    ("Track my UPI transaction", "payment"),

    # Edge cases and error scenarios (real user mistakes)
    ("Aaj 500 rupaye ka", "income"),  # Incomplete
    ("Becha rupaye 200 mein", "sales"),  # Wrong word order
    ("Money 300 spend kar di", "expense"),  # Mixed structure
    ("Kamai likshm rupaye", "income"),  # Incomplete word
    ("Santhai bhav", "market"),  # Very short
    ("Scheme ki jaankari", "schemes"),  # General
    ("Profit dekho", "profit"),  # Minimal
    ("Payment track", "payment"),  # Minimal
    ("Training chahiye", "training"),  # Minimal
    ("Mentor help", "mentor"),  # Minimal

    # Mixed language variations (English + Hindi/Tamil)
    ("I sold 5 kg sabjiyaan for 100 rupaye", "sales"),
    ("Aaj 500 rupaye ki kamai from business", "income"),
    ("Business mein 200 rupaye kharcha", "expense"),
    ("Profit kitna hua is time period", "profit"),
    ("Scheme mein apply kar sakte hain", "schemes"),
    ("Market price check karao for tomatoes", "market"),
    ("Mentor se business advice chahiye", "mentor"),
    ("Payment record via UPI 400 rupaye", "payment"),
    ("Training chahiye digital marketing", "training"),
]


def preprocess_text(text):
    """Preprocess text: lowercase, remove special chars, normalize"""
    text = text.lower()
    text = re.sub(r'[^\w\s₹]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def train_model():
    """Train the intent classification model"""
    print("=" * 60)
    print("MAHILA UDYAM - ML Model Training")
    print("=" * 60)

    # Prepare data
    texts, labels = zip(*TRAINING_DATA)
    texts = [preprocess_text(t) for t in texts]

    print(f"Total training examples: {len(texts)}")
    print(f"Unique intents: {len(set(labels))}")
    print(f"Intents: {sorted(set(labels))}")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    print(f"\nTraining samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")

    # Create TF-IDF vectorizer
    vectorizer = TfidfVectorizer(
        max_features=500,
        ngram_range=(1, 2),
        analyzer='word',
        min_df=1,
        sublinear_tf=True,
    )

    # Create classifier
    classifier = LogisticRegression(
        max_iter=1000,
        C=1.0,
        solver='lbfgs',
        random_state=42,
    )

    # Fit
    print("\nTraining TF-IDF vectorizer...")
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("Training Logistic Regression classifier...")
    classifier.fit(X_train_vec, y_train)

    # Evaluate
    train_pred = classifier.predict(X_train_vec)
    test_pred = classifier.predict(X_test_vec)

    train_accuracy = accuracy_score(y_train, train_pred)
    test_accuracy = accuracy_score(y_test, test_pred)

    print(f"\n{'=' * 40}")
    print(f"Training Accuracy: {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
    print(f"Test Accuracy:     {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    print(f"{'=' * 40}")

    print("\nClassification Report:")
    print(classification_report(y_test, test_pred))

    # Save model
    save_dir = os.path.join(os.path.dirname(__file__), 'saved_models')
    os.makedirs(save_dir, exist_ok=True)

    model_path = os.path.join(save_dir, 'mahila_intent_model.pkl')
    vectorizer_path = os.path.join(save_dir, 'mahila_intent_model_vectorizer.pkl')

    with open(model_path, 'wb') as f:
        pickle.dump(classifier, f)

    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)

    # Save model info
    model_info = {
        'train_accuracy': float(train_accuracy),
        'test_accuracy': float(test_accuracy),
        'total_examples': len(texts),
        'intents': sorted(list(set(labels))),
        'vectorizer_features': vectorizer.max_features,
        'ngram_range': list(vectorizer.ngram_range),
    }

    info_path = os.path.join(save_dir, 'model_info.json')
    with open(info_path, 'w') as f:
        json.dump(model_info, f, indent=2)

    print(f"\nModels saved to: {save_dir}")
    print(f"  - {model_path}")
    print(f"  - {vectorizer_path}")
    print(f"  - {info_path}")
    print("\nTraining complete!")

    return classifier, vectorizer, train_accuracy, test_accuracy


if __name__ == '__main__':
    train_model()
