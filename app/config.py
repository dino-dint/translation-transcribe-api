from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
   
    # API KEYS (from .env file)
   
    
    openai_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    
    
    # SERVER CONFIGURATION
   
    
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    
    # TRANSCRIPTION CONFIGURATION
    
    
    # Provider: "openai" or "gemini"
    transcription_provider: str = "openai"
    
    # OpenAI model for transcription
    openai_whisper_model: str = "whisper-1"
    
    # Gemini model for transcription
    gemini_model: str = "gemini-1.5-pro"
    
  
    # TRANSLATION CONFIGURATION
    
    
    # Provider: "openai" or "gemini"
    translation_provider: str = "openai"
    
    # OpenAI model for translation
    openai_gpt_model: str = "gpt-4o"
    
    # Gemini model for translation (same as transcription)
    # gemini_model already defined above
    
    
    # OTHER SETTINGS
   
    
    pythonunbuffered: Optional[str] = None
    pythondontwritebytecode: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"

settings = Settings()