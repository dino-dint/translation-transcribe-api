from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from app.services.transcription_service import transcribe_audio
from app.models import TranscribeResponse


router = APIRouter(prefix="/transcribe", tags=["Transcription"])

@router.post("/", response_model=TranscribeResponse)
async def transcribe(
    file: UploadFile = File(..., description="Audio file (mp3, wav, m4a, etc.)"),
    model: Optional[str] = Form(None, description="Override Whisper model (tiny/base/small/medium/large)")
):
    """
    Upload an audio file. Whisper auto-detects the language (Khmer or English)
    and returns the transcript.
    """
    file_bytes = await file.read()
    result = await transcribe_audio(file_bytes, file.filename, model_name=model)
    return TranscribeResponse(**result)


