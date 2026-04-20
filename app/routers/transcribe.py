# from fastapi import APIRouter, UploadFile, File, Form
# from typing import Optional
# from app.services.transcription_service import transcribe_audio
# from app.models import TranscribeResponse


# router = APIRouter(prefix="/transcribe", tags=["Transcription"])

# @router.post("/", response_model=TranscribeResponse)
# async def transcribe(
#     file: UploadFile = File(..., description="Audio file (mp3, wav, m4a, etc.)"),
#     model: Optional[str] = Form(None, description="Override Whisper model (tiny/base/small/medium/large)")
# ):
#     """
#     Upload an audio file. Whisper auto-detects the language (Khmer or English)
#     and returns the transcript.
#     """
#     file_bytes = await file.read()
#     result = await transcribe_audio(file_bytes, file.filename, model_name=model)
#     return TranscribeResponse(**result)

from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from app.services.transcription_service import transcribe_audio, get_transcription_models
from app.models import TranscribeResponse, ModelStatusResponse, ModelUpdateRequest
from app.config import settings

router = APIRouter(prefix="/transcribe", tags=["Transcription"])

@router.post("/", response_model=TranscribeResponse)
async def transcribe(
    file: UploadFile = File(...),
    model: Optional[str] = Form(None)
):
    """
    Transcribe Khmer audio using paid API (OpenAI or Gemini)
    
    The provider and model are selected in .env or via /models PATCH endpoint
    """
    file_bytes = await file.read()
    result = await transcribe_audio(file_bytes, file.filename, language="km")
    return TranscribeResponse(**result)

@router.get("/models")
def get_models():
    """Get current transcription configuration"""
    return get_transcription_models()

@router.patch("/models", response_model=ModelStatusResponse)
def update_transcription_models(req: ModelUpdateRequest):
    """Update transcription provider and model"""
    
    if req.transcription_provider:
        settings.transcription_provider = req.transcription_provider
    
    if req.openai_whisper_model:
        settings.openai_whisper_model = req.openai_whisper_model
    
    if req.gemini_model:
        settings.gemini_model = req.gemini_model
    
    return ModelStatusResponse(
        transcription_provider=settings.transcription_provider,
        transcription_model=settings.openai_whisper_model 
            if settings.transcription_provider == "openai" 
            else settings.gemini_model
    )