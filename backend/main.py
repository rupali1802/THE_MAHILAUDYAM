#!/usr/bin/env python
"""
Mahila Udyam - Main Entry Point for Voice Pipeline
Demonstrates complete speech → intent → response → speech flow
Usage: python main.py <audio_file_path> [language]
       python main.py --debug [audio_file]
"""
import sys
import os
import argparse

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))


def debug_pipeline(audio_file=None, language='en'):
    """
    DEBUG MODE: Step-by-step pipeline with explicit print statements.
    Helps identify exactly which step fails.
    """
    print("\n" + "=" * 60)
    print("🐛 DEBUG MODE: STEP-BY-STEP PIPELINE")
    print("=" * 60)
    
    try:
        # ==================== STEP 1: SPEECH RECOGNITION ====================
        print("\n📍 STEP 1: SPEECH RECOGNITION")
        print("-" * 60)
        print("DEBUG START")
        
        from ml_models.recognize_speech import recognize_speech, recognize_speech_from_microphone
        
        if audio_file and os.path.exists(audio_file):
            print(f"📁 Loading audio file: {audio_file}")
            text = recognize_speech(audio_file, language=f'{language}-IN')
        else:
            print("🎤 Using microphone input (10 seconds)...")
            text = recognize_speech_from_microphone(timeout=10, language=f'{language}-IN')
        
        print(f"✅ Recognized Text: '{text}'")
        print(f"   Type: {type(text)}")
        print(f"   Length: {len(text)} chars")
        
        if not text:
            print("❌ ERROR: Text is empty!")
            return 1
        
        # ==================== STEP 2: INTENT PREDICTION ====================
        print("\n📍 STEP 2: INTENT PREDICTION")
        print("-" * 60)
        
        from ml_models.model_predict import predict_intent
        
        print(f"🧠 Predicting intent for: '{text}'")
        prediction_result = predict_intent(text)
        
        print(f"✅ Prediction Result:")
        print(f"   Intent: {prediction_result.get('intent')}")
        print(f"   Confidence: {prediction_result.get('confidence'):.2%}")
        print(f"   Model Used: {prediction_result.get('model_used')}")
        print(f"   Full Result: {prediction_result}")
        
        intent = prediction_result.get('intent')
        if not intent:
            print("❌ ERROR: Intent is empty!")
            return 1
        
        # ==================== STEP 3: RESPONSE GENERATION ====================
        print("\n📍 STEP 3: RESPONSE GENERATION")
        print("-" * 60)
        
        from ml_models.voice_views import process_voice_command
        
        print(f"🔄 Processing voice command with full context...")
        response_result = process_voice_command(
            text,
            language=language,
            device_id='debug_device',
            auto_log=False
        )
        
        response = response_result.get('response')
        print(f"✅ Generated Response:")
        print(f"   Response Text: '{response}'")
        print(f"   Action: {response_result.get('action')}")
        print(f"   Intent: {response_result.get('intent')}")
        print(f"   Language: {response_result.get('detected_language')}")
        
        if not response:
            print("❌ ERROR: Response is empty!")
            return 1
        
        # ==================== STEP 4: TEXT-TO-SPEECH ====================
        print("\n📍 STEP 4: TEXT-TO-SPEECH")
        print("-" * 60)
        
        output_lang = response_result.get('detected_language', language)
        print(f"🔊 Would speak: '{response}'")
        print(f"   Language: {output_lang}")
        print(f"   Note: TTS requires browser context (skipping)")
        
        # ==================== DEBUG COMPLETE ====================
        print("\n" + "=" * 60)
        print("✅ DEBUG COMPLETE - All steps executed successfully!")
        print("=" * 60)
        print(f"""
FINAL RESULT:
  Text Input:    "{text}"
  Intent:        {intent}
  Response:      "{response}"
  Output Lang:   {output_lang}
        """)
        
        print("DEBUG END\n")
        return 0
        
    except Exception as e:
        print(f"\n❌ DEBUG FAILED AT THIS STEP")
        print(f"Error: {str(e)}")
        import traceback
        print(f"\nFull Traceback:")
        print(traceback.format_exc())
        return 1


def main():
    """Main voice processing pipeline"""
    parser = argparse.ArgumentParser(
        description='MahilaUdyam Voice Assistant - Process audio and respond',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py audio.wav                    # Process audio file
  python main.py --mic                        # Use microphone input  
  python main.py --debug audio.wav            # DEBUG MODE (shows each step)
  python main.py --debug --mic                # DEBUG MODE with microphone
        """,
    )
    parser.add_argument(
        'audio_file',
        nargs='?',
        help='Path to audio file (WAV, MP3, etc.) or leave empty for microphone input'
    )
    parser.add_argument(
        '--language',
        default='en',
        choices=['en', 'hi', 'ta'],
        help='Language code (default: en)'
    )
    parser.add_argument(
        '--mic',
        action='store_true',
        help='Use microphone input instead of file'
    )
    parser.add_argument(
        '--device-id',
        default='demo_device',
        help='Device ID for logging (default: demo_device)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable DEBUG MODE - shows each step with detailed output'
    )
    
    args = parser.parse_args()
    
    # DEBUG MODE
    if args.debug:
        audio_input = None
        if args.audio_file and os.path.exists(args.audio_file):
            audio_input = args.audio_file
        return debug_pipeline(audio_file=audio_input, language=args.language)
    
    try:
        print("\n🚀 Mahila Udyam Voice Assistant Pipeline")
        print("=" * 50)
        
        # Step 1: Speech Recognition
        print("\n📍 STEP 1: SPEECH RECOGNITION")
        print("-" * 50)
        
        from ml_models.recognize_speech import recognize_speech, recognize_speech_from_microphone
        from ml_models.voice_views import process_voice_command
        from frontend.src.utils.voiceOutput import speak  # Would work if configured
        
        if args.mic or not args.audio_file:
            # Microphone input
            print("🎤 Listening from microphone for 10 seconds...")
            text = recognize_speech_from_microphone(timeout=10, language=f'{args.language}-IN')
        else:
            # Audio file input
            if not os.path.exists(args.audio_file):
                print(f"❌ Error: File not found: {args.audio_file}")
                sys.exit(1)
            
            print(f"📁 Processing audio file: {args.audio_file}")
            text = recognize_speech(args.audio_file, language=f'{args.language}-IN')
        
        print(f"\n✅ RECOGNIZED TEXT: '{text}'")
        print(f"🔤 Length: {len(text)} characters")
        
        # Step 2: Intent Processing
        print("\n📍 STEP 2: INTENT & LANGUAGE DETECTION + RESPONSE")
        print("-" * 50)
        
        print(f"🧠 Processing command with language detection...")
        result = process_voice_command(
            text,
            language=args.language,
            device_id=args.device_id,
            auto_log=True
        )
        
        print(f"✅ Intent: {result.get('intent')}")
        print(f"✅ Confidence: {result.get('confidence'):.2%}")
        print(f"✅ Detected Language: {result.get('detected_language')} ({result.get('language_name')})")
        print(f"✅ Response: '{result.get('response')}'")
        print(f"✅ Action: {result.get('action')}")
        
        # Step 3: Text-to-Speech (Optional - requires browser context)
        print("\n📍 STEP 3: TEXT-TO-SPEECH OUTPUT")
        print("-" * 50)
        
        response_text = result.get('response', '')
        output_lang = result.get('detected_language', args.language)
        
        print(f"🔊 Would speak: '{response_text}'")
        print(f"🎵 Language: {output_lang}")
        
        try:
            # Note: speak() is for browser only, would need web server to test
            print("ℹ️  (TTS requires browser context - skipping)")
            # Uncomment below if running in browser context:
            # from frontend.src.utils.voiceOutput import speak
            # await speak(response_text, output_lang)
        except ImportError:
            print("ℹ️  TTS not available in server context")
        
        # Final Summary
        print("\n" + "=" * 50)
        print("✅ PIPELINE COMPLETE")
        print("=" * 50)
        print(f"""
Pipeline Summary:
  1️⃣  Audio Input → Text: "{text[:50]}..."
  2️⃣  Text → Intent: {result.get('intent')} (confidence: {result.get('confidence'):.1%})
  3️⃣  Intent → Response: "{response_text[:50]}..."
  4️⃣  Response → Speech: (browser TTS)

Device ID: {args.device_id}
Language: {output_lang}
Logged: {'Yes' if result.get('logging_id') else 'No'}
        """)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        print(f"\n📋 Traceback:\n{traceback.format_exc()}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
