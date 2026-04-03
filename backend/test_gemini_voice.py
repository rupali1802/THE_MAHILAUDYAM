#!/usr/bin/env python
"""
Quick test script for SAKHI voice assistant with Gemini AI
Tests the new generate_voice_response() method
"""
import os
import sys
import django

# Add backend to path
sys.path.insert(0, '/c/Users/Rupali/OneDrive/Desktop/Villupuram_Hackathon/MahilaUdyam_claude/MahilaUdyam_claude/MahilaUdyam/backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mahila_udyam_backend.settings')
django.setup()

from ml_models.voice_views import process_voice_command
from ml_models.gemini_helper import GeminiHelper

print("\n" + "="*70)
print("🎤 SAKHI VOICE ASSISTANT - GEMINI INTEGRATION TEST")
print("="*70)

print(f"\n✅ Gemini Available: {GeminiHelper.is_available()}")

# Test cases
test_cases = [
    {
        "query": "5 kg kaaikari vittren",
        "language": "ta",
        "name": "Tamil Market Query"
    },
    {
        "query": "Mere liye business growing tips de",
        "language": "hi",
        "name": "Hindi Business Advice"
    },
    {
        "query": "What schemes are available for women entrepreneurs",
        "language": "en",
        "name": "English Scheme Query"
    }
]

for i, test in enumerate(test_cases, 1):
    print(f"\n📝 Test {i}: {test['name']}")
    print(f"   Query: {test['query']}")
    print(f"   Language: {test['language']}")
    print("-" * 70)
    
    try:
        result = process_voice_command(
            text=test['query'],
            language=test['language'],
            device_id=f"test-device-{i}",
            auto_log=False
        )
        
        print(f"✅ Intent: {result['intent']}")
        print(f"🤖 Gemini Enhanced: {result.get('gemini_enhanced', False)}")
        print(f"\n📢 Response:\n{result['response'][:300]}{'...' if len(result['response']) > 300 else ''}")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

print("\n" + "="*70)
print("✅ Test Complete!")
print("="*70 + "\n")
