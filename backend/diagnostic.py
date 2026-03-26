#!/usr/bin/env python
"""
Voice Assistant API Diagnostic Tool
Tests the complete voice → backend → response flow
Run this to verify the API is working correctly before testing from frontend
"""
import os
import sys
import json
import requests
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_step(num, text):
    """Print numbered step"""
    print(f"\n📍 STEP {num}: {text}")
    print("-" * 70)

def test_audio_file(audio_path, language='en'):
    """Test with audio file"""
    print_step(1, "Audio File Test")
    
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        return False
    
    try:
        from ml_models.recognize_speech import recognize_speech
        text = recognize_speech(audio_path, language=f'{language}-IN')
        print(f"✅ Recognized text: '{text}'")
        return text
    except Exception as e:
        print(f"❌ Speech recognition failed: {e}")
        return None

def test_api_endpoint(text, language='en'):
    """Test API endpoint"""
    print_step(2, "API Endpoint Test")
    
    # Configuration
    backend_url = 'http://localhost:8000'
    api_endpoint = f'{backend_url}/api/predict-intent/'
    
    print(f"🔗 API URL: {api_endpoint}")
    print(f"📝 Text: '{text}'")
    print(f"🔤 Language: {language}")
    
    # Prepare request
    payload = {
        'text': text,
        'language': language,
        'device_id': 'diagnostic-test-device'
    }
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }
    
    print(f"\n📤 Sending request...")
    print(f"   Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(api_endpoint, json=payload, headers=headers, timeout=10)
        
        print(f"\n✅ Response received!")
        print(f"   Status Code: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ SUCCESS! Backend response:")
            print(json.dumps(data, indent=2))
            return data
        else:
            print(f"\n❌ ERROR! Status: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError as e:
        print(f"❌ Connection Error: {e}")
        print("   → Is the backend running on port 8000?")
        print("   → Run: python manage.py runserver 0.0.0.0:8000")
        return None
    except requests.exceptions.Timeout as e:
        print(f"❌ Timeout Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_cors_headers():
    """Test CORS headers"""
    print_step(3, "CORS Headers Test")
    
    backend_url = 'http://localhost:8000'
    api_endpoint = f'{backend_url}/api/predict-intent/'
    
    print(f"🔗 API URL: {api_endpoint}")
    print(f"📤 Sending OPTIONS preflight request...")
    
    headers = {
        'Origin': 'http://localhost:3000',
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'content-type',
    }
    
    try:
        response = requests.options(api_endpoint, headers=headers, timeout=10)
        
        print(f"\n✅ OPTIONS response received!")
        print(f"   Status Code: {response.status_code}")
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
        }
        
        print(f"\n✅ CORS Headers:")
        for key, value in cors_headers.items():
            print(f"   {key}: {value}")
        
        if cors_headers['Access-Control-Allow-Origin'] == 'http://localhost:3000':
            print(f"\n✅ CORS properly configured for localhost:3000")
            return True
        else:
            print(f"\n⚠️  WARNING: Origin might not be properly configured")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Main diagnostic"""
    print_header("🔍 VOICE ASSISTANT API DIAGNOSTIC")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test cases
    test_texts = [
        ('income 500', 'en'),
        ('खर्च 200', 'hi'),
        ('விற்பனை 5 kg', 'ta'),
    ]
    
    print("\n" + "=" * 70)
    print("CONFIGURATION")
    print("=" * 70)
    print(f"Frontend URL: http://localhost:3000")
    print(f"Backend URL: http://localhost:8000")
    print(f"API Endpoint: http://localhost:8000/api/predict-intent/")
    
    # Test backend connectivity
    print_step(0, "Backend Connectivity Check")
    try:
        response = requests.get('http://localhost:8000/api/diagnostics/', timeout=5)
        print(f"✅ Backend is running and reachable!")
        print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot reach backend: {e}")
        print("❌ Start the backend first:")
        print("   cd backend")
        print("   python manage.py runserver 0.0.0.0:8000")
        return
    
    # Test CORS
    test_cors_headers()
    
    # Test API with different languages
    for text, lang in test_texts:
        test_api_endpoint(text, lang)
        print()
    
    print_header("✅ DIAGNOSTIC COMPLETE")
    print("\nIf you see errors above:")
    print("1. Check that backend is running: python manage.py runserver 0.0.0.0:8000")
    print("2. Check CORS is configured in mahila_udyam_backend/settings.py")
    print("3. Check firewall allows connections to port 8000")
    print("4. Check frontend is trying to connect to correct URL")

if __name__ == '__main__':
    main()
