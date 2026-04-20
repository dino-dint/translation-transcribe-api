# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware
# from app.routers import transcribe, translate
# import os


# app = FastAPI(
#     title="🇰🇭 Khmer ↔ English Transcription & Translation API",
#     description="""
# ## Features
# -  **Transcribe** audio files (Khmer or English) using OpenAI Whisper (free, local)
# -  **Translate** text: English → Khmer or Khmer → English using googletranslate
# -  **Swap models** at runtime — no restart needed
# -  Docker-ready, runs on `0.0.0.0`
#     """,
#     version="1.0.0"
# )

# # Enable CORS for external requests (needed for Docker/network access)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Allow all origins (you can restrict this to specific domains)
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Routers
# app.include_router(transcribe.router)
# app.include_router(translate.router)

# # Serve custom UI
# static_dir = os.path.join(os.path.dirname(__file__), "static")
# app.mount("/static", StaticFiles(directory=static_dir), name="static")


# @app.get("/", include_in_schema=False)
# def root():
#     return FileResponse(os.path.join(static_dir, "index.html"))

# @app.get("/health")
# def health():
#     return {"status": "ok"}

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from app.routers import transcribe, translate
import os

app = FastAPI(
    title="🇰🇭 Khmer Transcription & Translation API",
    description="""
## Features
- **Transcribe** Khmer audio using paid APIs (OpenAI Whisper, Google Gemini)
- **Translate** Khmer ↔ English using paid APIs
- **Switch models** at runtime — no restart needed
- **Secure** API keys stored in .env file only
    """,
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transcribe.router)
app.include_router(translate.router)

# Serve UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
def root():
    return FileResponse(os.path.join(static_dir, "index.html"))

@app.get("/health")
def health():
    return {"status": "ok"}