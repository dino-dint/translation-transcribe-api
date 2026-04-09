from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    WHISPER_MODEL: str = "base"
    
     # These are now language codes, not HuggingFace model names
    TRANSLATION_MODEL: str = "en→km"
    TRANSLATION_MODEL_KM_EN: str = "km→en"

    class Config:
        env_file = ".env"

settings = Settings()

