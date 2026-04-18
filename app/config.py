# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    WHISPER_MODEL: str = "base"

    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"

    # Gemini
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-1.5-flash"

    # Active provider: "google" | "openai" | "gemini"
    TRANSLATION_PROVIDER: str = "google"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()