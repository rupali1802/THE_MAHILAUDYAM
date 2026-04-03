"""
Mahila Udyam - Speech Recognition Module
Converts audio files or audio bytes to text using Google Speech Recognition API
Supports multiple audio formats and handles errors gracefully
"""
import speech_recognition as sr
import os
from pydub import AudioSegment
import io


def recognize_speech(audio_source, language='en-IN'):
    """
    Convert speech audio to text using Google Speech Recognition API.
    
    Args:
        audio_source: Either a file path (str) or audio bytes (bytes)
        language: Language code for recognition (default: 'en-IN' for English India)
                 Supported: 'en-IN', 'hi-IN', 'ta-IN', etc.
    
    Returns:
        text (str): Recognized text from the audio
    
    Raises:
        sr.UnknownValueError: If speech could not be understood
        sr.RequestError: If API request fails
        FileNotFoundError: If audio file not found
        ValueError: If invalid audio source provided
    
    Examples:
        # From file path
        text = recognize_speech('/path/to/audio.wav')
        
        # From audio bytes
        with open('audio.wav', 'rb') as f:
            audio_bytes = f.read()
        text = recognize_speech(audio_bytes, language='hi-IN')
    """
    recognizer = sr.Recognizer()
    
    try:
        # Handle file path input
        if isinstance(audio_source, str):
            if not os.path.exists(audio_source):
                raise FileNotFoundError(f"Audio file not found: {audio_source}")
            
            print(f"📁 Loading audio file: {audio_source}")
            
            # Determine audio format and convert to WAV if needed
            with sr.AudioFile(audio_source) as source:
                audio = recognizer.record(source)
        
        # Handle audio bytes input
        elif isinstance(audio_source, bytes):
            print(f"🔊 Processing audio bytes ({len(audio_source)} bytes)")
            
            # Try to detect format and convert to WAV
            try:
                audio_segment = AudioSegment.from_file(io.BytesIO(audio_source))
                wav_buffer = io.BytesIO()
                audio_segment.export(wav_buffer, format='wav')
                wav_buffer.seek(0)
                
                with sr.AudioFile(wav_buffer) as source:
                    audio = recognizer.record(source)
            except Exception as e:
                print(f"⚠️  Could not parse audio bytes, trying direct WAV: {str(e)}")
                with sr.AudioFile(io.BytesIO(audio_source)) as source:
                    audio = recognizer.record(source)
        
        else:
            raise ValueError(f"Invalid audio_source type: {type(audio_source)}. Expected str or bytes.")
        
        # Recognize speech using Google Speech Recognition API
        print(f"🎤 Recognizing speech in language: {language}")
        text = recognizer.recognize_google(audio, language=language)
        
        print(f"✅ Speech recognized: '{text}'")
        return text
    
    except sr.UnknownValueError:
        error_msg = "❌ Could not understand the audio. Please speak clearly."
        print(error_msg)
        raise sr.UnknownValueError(error_msg)
    
    except sr.RequestError as e:
        error_msg = f"❌ API request failed: {str(e)}"
        print(error_msg)
        raise sr.RequestError(error_msg)
    
    except FileNotFoundError as e:
        error_msg = f"❌ File error: {str(e)}"
        print(error_msg)
        raise
    
    except ValueError as e:
        error_msg = f"❌ Invalid input: {str(e)}"
        print(error_msg)
        raise
    
    except Exception as e:
        error_msg = f"❌ Unexpected error during speech recognition: {str(e)}"
        print(error_msg)
        raise


def recognize_speech_from_microphone(timeout=10, language='en-IN'):
    """
    Capture and recognize speech directly from microphone.
    
    Args:
        timeout: Maximum seconds to listen (default: 10)
        language: Language code for recognition (default: 'en-IN')
    
    Returns:
        text (str): Recognized text from microphone input
    
    Raises:
        sr.UnknownValueError: If speech could not be understood
        sr.RequestError: If API request fails
        sr.MicrophoneError: If microphone not available
    """
    recognizer = sr.Recognizer()
    
    try:
        print("🎤 Listening from microphone...")
        
        with sr.Microphone() as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("📢 Listening... (speak now)")
            
            # Listen with timeout
            audio = recognizer.listen(source, timeout=timeout)
        
        print("🎤 Processing audio...")
        text = recognizer.recognize_google(audio, language=language)
        
        print(f"✅ Speech recognized: '{text}'")
        return text
    
    except sr.UnknownValueError:
        error_msg = "❌ Could not understand the audio. Please speak clearly."
        print(error_msg)
        raise sr.UnknownValueError(error_msg)
    
    except sr.RequestError as e:
        error_msg = f"❌ API request failed: {str(e)}"
        print(error_msg)
        raise sr.RequestError(error_msg)
    
    except sr.MicrophoneError as e:
        error_msg = f"❌ Microphone error: {str(e)}"
        print(error_msg)
        raise sr.MicrophoneError(error_msg)
    
    except Exception as e:
        error_msg = f"❌ Unexpected error: {str(e)}"
        print(error_msg)
        raise


# Supported languages mapping
SUPPORTED_LANGUAGES = {
    'en': 'en-IN',      # English (India)
    'hi': 'hi-IN',      # Hindi (India)
    'ta': 'ta-IN',      # Tamil (India)
    'en-US': 'en-US',   # English (US)
    'en-GB': 'en-GB',   # English (UK)
    'es': 'es-ES',      # Spanish
    'fr': 'fr-FR',      # French
    'de': 'de-DE',      # German
    'it': 'it-IT',      # Italian
    'pt': 'pt-BR',      # Portuguese (Brazil)
    'zh': 'zh-CN',      # Chinese (Simplified)
    'ja': 'ja-JP',      # Japanese
}


def get_supported_languages():
    """Get list of supported language codes"""
    return SUPPORTED_LANGUAGES


def recognize_speech_auto_detect(audio_source, available_languages=None):
    """
    Try to recognize speech with automatic language fallback.
    
    Args:
        audio_source: File path or audio bytes
        available_languages: List of language codes to try (default: ['en', 'hi', 'ta'])
    
    Returns:
        dict with keys: 'text', 'language', 'confidence'
    """
    if available_languages is None:
        available_languages = ['en', 'hi', 'ta']
    
    print(f"🔍 Attempting speech recognition with {len(available_languages)} languages...")
    
    for lang_code in available_languages:
        try:
            lang_full = SUPPORTED_LANGUAGES.get(lang_code, lang_code)
            print(f"  Trying: {lang_code} ({lang_full})")
            
            text = recognize_speech(audio_source, language=lang_full)
            
            return {
                'text': text,
                'language': lang_code,
                'confidence': 'high',  # Google API doesn't return confidence
            }
        except Exception as e:
            print(f"  ⚠️  Failed for {lang_code}: {str(e)}")
            continue
    
    raise ValueError(f"Could not recognize speech in any of the {len(available_languages)} attempted languages")
