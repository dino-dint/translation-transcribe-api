# # app/models.py
# from pydantic import BaseModel
# from typing import Optional

# class TranscribeResponse(BaseModel):
#     detected_language: str
#     transcript: str

# class TranslateRequest(BaseModel):
#     text: str
#     direction: str  # "en_to_km" or "km_to_en"

# class TranslateResponse(BaseModel):
#     original: str
#     translated: str
#     direction: str

# class ModelUpdateRequest(BaseModel):
#     whisper_model: Optional[str] = None
#     translation_provider: Optional[str] = None
#     openai_model: Optional[str] = None
#     gemini_model: Optional[str] = None      

# class ModelStatusResponse(BaseModel):
#     whisper_model: str
#     translation_provider: str
#     openai_model: str
#     gemini_model: str       
                 
from pydantic import BaseModel
from typing import Optional

class TranscribeResponse(BaseModel):
    transcript: str
    detected_language: str
    model: Optional[str] = None
    provider: Optional[str] = None

class TranslateRequest(BaseModel):
    text: str
    direction: str  # "en_to_km" or "km_to_en"

class TranslateResponse(BaseModel):
    original: str
    translated: str
    direction: str
    model: Optional[str] = None
    provider: Optional[str] = None

class ModelStatusResponse(BaseModel):
    transcription_provider: Optional[str] = None
    transcription_model: Optional[str] = None
    translation_provider: Optional[str] = None
    translation_model: Optional[str] = None

class ModelUpdateRequest(BaseModel):
    transcription_provider: Optional[str] = None
    openai_whisper_model: Optional[str] = None
    gemini_model: Optional[str] = None
    translation_provider: Optional[str] = None
    openai_gpt_model: Optional[str] = None
