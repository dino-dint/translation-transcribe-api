import os
import tempfile
from typing import Optional
from app.config import settings

from openai import OpenAI
import google.generativeai as genai


# Initialize API Clients


# OpenAI (Whisper)
if settings.openai_api_key:
    openai_client = OpenAI(api_key=settings.openai_api_key)
else:
    openai_client = None

# Gemini
if settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)
else:
    gemini_client = None


# Transcription Functions
async def transcribe_audio(
    file_bytes: bytes,
    filename: str,
    language: str = "km"
) -> dict:
    """
    Transcribe Khmer audio using configured paid API
    
    Provider is selected via settings.transcription_provider
    """
    
    provider = settings.transcription_provider.lower()
    
    print(f"[Transcription] Using {provider} | Language: {language}")
    
    if provider == "openai":
        return await transcribe_openai(file_bytes, filename, language)
    elif provider == "gemini":
        return await transcribe_gemini(file_bytes, filename, language)
    else:
        return {
            "error": f"Unknown provider: {provider}. Use: openai or gemini",
            "detected_language": "km",
            "transcript": ""
        }

async def transcribe_openai(
    file_bytes: bytes,
    filename: str,
    language: str = "km"
) -> dict:
    """Transcribe using OpenAI Whisper API"""
    
    if not openai_client:
        return {
            "error": "OpenAI API key not configured in .env",
            "detected_language": "km",
            "transcript": ""
        }
    
    suffix = os.path.splitext(filename)[-1] or ".mp3"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    
    try:
        print("[OpenAI Whisper] Transcribing...")
        
        model = settings.openai_whisper_model or "whisper-1"
        
        with open(tmp_path, "rb") as audio_file:
            transcript = openai_client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                language=language,
                prompt="This is a Khmer language audio. Transcribe accurately."
            )
        
        return {
            "transcript": transcript.text,
            "detected_language": "km",
            "model": model,
            "provider": "openai"
        }
    
    except Exception as e:
        return {
            "error": f"OpenAI transcription failed: {str(e)}",
            "detected_language": "km",
            "transcript": ""
        }
    
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

async def transcribe_gemini(
    file_bytes: bytes,
    filename: str,
    language: str = "km"
) -> dict:
    """Transcribe using Google Gemini API"""
    
    if not settings.gemini_api_key:
        return {
            "error": "Gemini API key not configured in .env",
            "detected_language": "km",
            "transcript": ""
        }
    
    suffix = os.path.splitext(filename)[-1] or ".mp3"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name
    
    try:
        print("[Gemini] Transcribing...")
        
        model_name = settings.gemini_model or "gemini-1.5-pro"
        gemini_model = genai.GenerativeModel(model_name)
        
        audio_file = genai.upload_file(tmp_path)
        
        response = gemini_model.generate_content([
            "Transcribe this Khmer audio to text accurately. Return ONLY the transcript, nothing else.",
            audio_file
        ])
        
        return {
            "transcript": response.text.strip(),
            "detected_language": "km",
            "model": model_name,
            "provider": "gemini"
        }
    
    except Exception as e:
        return {
            "error": f"Gemini transcription failed: {str(e)}",
            "detected_language": "km",
            "transcript": ""
        }
    
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


# Model Info
def get_transcription_models() -> dict:
    """Get current transcription configuration"""
    
    return {
        "current_provider": settings.transcription_provider,
        "current_model": (
            settings.openai_whisper_model 
            if settings.transcription_provider == "openai" 
            else settings.gemini_model
        ),
        "available_providers": [
            {
                "name": "openai",
                "model": "whisper-1",
                "status": "active" if settings.openai_api_key else "not_configured"
            },
            {
                "name": "gemini",
                "models": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash"],
                "status": "active" if settings.gemini_api_key else "not_configured"
            }
        ]
    }

