from fastapi import APIRouter, HTTPException
from app.models import (
    TranslateRequest, TranslateResponse,
    ModelUpdateRequest, ModelStatusResponse
)
from app.services.translation_service import translate_text
from app.config import settings

router = APIRouter(tags=["Translation & Config"])

@router.post("/translate", response_model=TranslateResponse)
def translate(req: TranslateRequest):
    if req.direction not in ("en_to_km", "km_to_en"):
        raise HTTPException(status_code=400, detail="direction must be 'en_to_km' or 'km_to_en'")
    translated = translate_text(req.text, req.direction)
    return TranslateResponse(original=req.text, translated=translated, direction=req.direction)

# New combined endpoint: auto-translate based on detected language
@router.post("/transcribe-and-translate")
def transcribe_and_translate(req: dict):
    """
    Input: { "transcript": "...", "detected_language": "en" or "km" }
    Output: { "transcript": "...", "detected_language": "...", "translation": "..." }
    Automatically translates to the opposite language based on detected language.
    """
    transcript = req.get("transcript", "").strip()
    detected_lang = req.get("detected_language", "unknown").lower()
    
    if not transcript:
        raise HTTPException(status_code=400, detail="transcript cannot be empty")
    
    # Determine translation direction based on detected language
    if detected_lang == "en":
        direction = "en_to_km"  # English -> Khmer
    elif detected_lang == "km":
        direction = "km_to_en"  # Khmer -> English
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported language: {detected_lang}")
    
    translated = translate_text(transcript, direction)
    
    return {
        "transcript": transcript,
        "detected_language": detected_lang,
        "translation": translated,
        "translation_direction": direction
    }

@router.get("/models", response_model=ModelStatusResponse)
def get_models():
    return ModelStatusResponse(
        whisper_model=settings.WHISPER_MODEL,
        translation_provider=settings.TRANSLATION_PROVIDER,
        openai_model=settings.OPENAI_MODEL,
        gemini_model=settings.GEMINI_MODEL, 
    )
                                            


@router.patch("/models", response_model=ModelStatusResponse)
def update_models(req: ModelUpdateRequest):
    """
    Whisper options: tiny | base | small | medium | large
    """
    if req.whisper_model:
        settings.WHISPER_MODEL = req.whisper_model
    if req.translation_provider:
        settings.TRANSLATION_PROVIDER = req.translation_provider
    if req.openai_model:
        settings.OPENAI_MODEL = req.openai_model
    if req.gemini_model:                      
        settings.GEMINI_MODEL = req.gemini_model
    return ModelStatusResponse(
        whisper_model=settings.WHISPER_MODEL,
        translation_provider=settings.TRANSLATION_PROVIDER,
        openai_model=settings.OPENAI_MODEL,
        gemini_model=settings.GEMINI_MODEL,
    )