"""
Mahila Udyam - ML Model Training from CSV Dataset
Trains intent classification model using provided dataset
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
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import re

def preprocess_text(text):
    """Preprocess text: lowercase, remove special chars, normalize"""
    text = str(text).lower()
    text = re.sub(r'[^\w\s₹]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def train_model_from_csv(csv_path):
    """Train the intent classification model from CSV dataset"""
    print("=" * 70)
    print("MAHILA UDYAM - ML Model Training from CSV Dataset")
    print("=" * 70)

    # Load dataset
    if not os.path.exists(csv_path):
        print(f"❌ Error: Dataset file not found at {csv_path}")
        return False

    try:
        df = pd.read_csv(csv_path)
        print(f"✅ Dataset loaded successfully")
        print(f"   Rows: {len(df)}")
        print(f"   Columns: {list(df.columns)}")
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return False

    # Validate data
    if 'text' not in df.columns or 'intent' not in df.columns:
        print(f"❌ Error: CSV must have 'text' and 'intent' columns")
        return False

    # Remove empty rows
    df = df.dropna()
    df = df[df['text'].str.strip() != '']
    print(f"\n📊 Dataset Info:")
    print(f"   Total samples after cleanup: {len(df)}")

    # Get intent statistics
    intent_counts = df['intent'].value_counts()
    print(f"\n   Intent distribution:")
    for intent, count in intent_counts.items():
        percentage = (count / len(df)) * 100
        print(f"      {intent:15s}: {count:4d} ({percentage:5.1f}%)")

    # Prepare data
    texts = df['text'].values
    labels = df['intent'].values

    # Preprocess texts
    print(f"\n🔄 Preprocessing texts...")
    texts = [preprocess_text(t) for t in texts]

    print(f"   Unique intents: {len(set(labels))}")
    print(f"   Intents: {sorted(set(labels))}")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=0.2, random_state=42, stratify=labels
    )

    print(f"\n📈 Data Split:")
    print(f"   Training samples: {len(X_train)}")
    print(f"   Test samples: {len(X_test)}")

    # Create TF-IDF vectorizer
    print(f"\n🔨 Creating TF-IDF Vectorizer...")
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
    print("🔨 Fitting TF-IDF vectorizer...")
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    print("🔨 Training Logistic Regression classifier...")
    classifier.fit(X_train_vec, y_train)

    # Evaluate
    train_pred = classifier.predict(X_train_vec)
    test_pred = classifier.predict(X_test_vec)

    train_accuracy = accuracy_score(y_train, train_pred)
    test_accuracy = accuracy_score(y_test, test_pred)

    print(f"\n{'=' * 70}")
    print(f"📊 MODEL PERFORMANCE")
    print(f"{'=' * 70}")
    print(f"Training Accuracy:  {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
    print(f"Test Accuracy:      {test_accuracy:.4f} ({test_accuracy*100:.2f}%)")
    print(f"{'=' * 70}")

    print(f"\n📋 Classification Report:")
    print(classification_report(y_test, test_pred))

    # Save model
    save_dir = os.path.join(os.path.dirname(__file__), 'saved_models')
    os.makedirs(save_dir, exist_ok=True)

    model_path = os.path.join(save_dir, 'mahila_intent_model.pkl')
    vectorizer_path = os.path.join(save_dir, 'mahila_intent_model_vectorizer.pkl')

    print(f"\n💾 Saving model files...")
    with open(model_path, 'wb') as f:
        pickle.dump(classifier, f)
    print(f"   ✅ Model saved: {model_path}")

    with open(vectorizer_path, 'wb') as f:
        pickle.dump(vectorizer, f)
    print(f"   ✅ Vectorizer saved: {vectorizer_path}")

    # Save model info
    model_info = {
        'train_accuracy': float(train_accuracy),
        'test_accuracy': float(test_accuracy),
        'total_examples': int(len(df)),
        'training_examples': int(len(X_train)),
        'test_examples': int(len(X_test)),
        'intents': sorted(list(set(labels))),
        'vectorizer_features': int(vectorizer.max_features),
        'ngram_range': list(vectorizer.ngram_range),
        'intent_distribution': {k: int(v) for k, v in intent_counts.items()},
    }

    info_path = os.path.join(save_dir, 'model_info.json')
    with open(info_path, 'w') as f:
        json.dump(model_info, f, indent=2)
    print(f"   ✅ Model info saved: {info_path}")

    print(f"\n✅ Model training completed successfully!")
    return True

if __name__ == '__main__':
    # Get CSV path - default to mahila_dataset.csv in parent directory
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'mahila_dataset.csv')

    success = train_model_from_csv(csv_path)
    sys.exit(0 if success else 1)
