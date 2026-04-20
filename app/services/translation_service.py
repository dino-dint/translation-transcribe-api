from app.config import settings
from openai import OpenAI
import google.generativeai as genai


# Initialize API Clients


if settings.openai_api_key:
    openai_client = OpenAI(api_key=settings.openai_api_key)
else:
    openai_client = None

if settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)
else:
    gemini_client = None


# Translation Functions


DIRECTION_MAP = {
    "en_to_km": ("English", "Khmer"),
    "km_to_en": ("Khmer", "English"),
}

def translate_text(text: str, direction: str) -> dict:
    """
    Translate Khmer ↔ English using configured paid API
    
    Provider is selected via settings.translation_provider
    """
    
    if direction not in DIRECTION_MAP:
        return {
            "original": text,
            "translated": "",
            "direction": direction,
            "error": "direction must be 'en_to_km' or 'km_to_en'"
        }
    
    provider = settings.translation_provider.lower()
    
    print(f"[Translation] Using {provider} | Direction: {direction}")
    
    if provider == "openai":
        return translate_openai(text, direction)
    elif provider == "gemini":
        return translate_gemini(text, direction)
    else:
        return {
            "original": text,
            "translated": "",
            "direction": direction,
            "error": f"Unknown provider: {provider}"
        }

def translate_openai(text: str, direction: str) -> dict:
    """Translate using OpenAI GPT"""
    
    if not openai_client:
        return {
            "original": text,
            "translated": "",
            "direction": direction,
            "error": "OpenAI API key not configured in .env"
        }
    
    source_lang, target_lang = DIRECTION_MAP[direction]
    
    try:
        print("[OpenAI GPT] Translating...")
        
        model = settings.openai_gpt_model or "gpt-4o"
        
        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": f"You are an expert Khmer-English translator. Translate accurately from {source_lang} to {target_lang}."
                },
                {
                    "role": "user",
                    "content": f"Translate this text from {source_lang} to {target_lang}. Return ONLY the translation:\n\n{text}"
                }
            ],
            temperature=0.3,
            max_tokens=1000
        )
        
        translated = response.choices[0].message.content.strip()
        
        return {
            "original": text,
            "translated": translated,
            "direction": direction,
            "model": model,
            "provider": "openai"
        }
    
    except Exception as e:
        return {
            "original": text,
            "translated": "",
            "direction": direction,
            "error": f"OpenAI translation failed: {str(e)}"
        }

def translate_gemini(text: str, direction: str) -> dict:
    """Translate using Google Gemini"""
    
    if not settings.gemini_api_key:
        return {
            "original": text,
            "translated": "",
            "direction": direction,
            "error": "Gemini API key not configured in .env"
        }
    
    source_lang, target_lang = DIRECTION_MAP[direction]
    
    try:
        print("[Gemini] Translating...")
        
        model_name = settings.gemini_model or "gemini-1.5-pro"
        gemini_model = genai.GenerativeModel(model_name)
        
        prompt = f"""You are an expert Khmer-English translator.
Translate this text from {source_lang} to {target_lang}.
Return ONLY the translation, nothing else:

{text}"""
        
        response = gemini_model.generate_content(prompt)
        translated = response.text.strip()
        
        return {
            "original": text,
            "translated": translated,
            "direction": direction,
            "model": model_name,
            "provider": "gemini"
        }
    
    except Exception as e:
        return {
            "original": text,
            "translated": "",
            "direction": direction,
            "error": f"Gemini translation failed: {str(e)}"
        }


# Model Info


def get_translation_models() -> dict:
    """Get current translation configuration"""
    
    return {
        "current_provider": settings.translation_provider,
        "current_model": (
            settings.openai_gpt_model 
            if settings.translation_provider == "openai" 
            else settings.gemini_model
        ),
        "available_providers": [
            {
                "name": "openai",
                "model": "gpt-4o",
                "status": "active" if settings.openai_api_key else "not_configured"
            },
            {
                "name": "gemini",
                "models": ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash"],
                "status": "active" if settings.gemini_api_key else "not_configured"
            }
        ]
    }
