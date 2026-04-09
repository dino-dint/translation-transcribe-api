from pydantic import BaseModel
from typing import Optional

class TranscribeResponse(BaseModel):
    detected_language: str
    transcript: str

class TranslateRequest(BaseModel):
    text: str
    direction: str  # "en_to_km" or "km_to_en"

class TranslateResponse(BaseModel):
    original: str
    translated: str
    direction: str

class ModelUpdateRequest(BaseModel):
    whisper_model: Optional[str] = None  # tiny | base | small | medium | large

class ModelStatusResponse(BaseModel):
    whisper_model: str