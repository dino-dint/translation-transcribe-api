# import whisper 
# import tempfile
# import os
# from app.config import settings

# _model_cache = {}



# def get_whisper_model(model_name: str = None):
#     name = model_name or settings.WHISPER_MODEL
#     if name not in _model_cache:
#         print(f"[Whisper] Loading model: {name}")
#         _model_cache[name] = whisper.load_model(name)
#     return _model_cache[name]

# async def transcribe_audio(file_bytes: bytes, filename: str, model_name: str = None) -> dict:
#     model = get_whisper_model(model_name)

#     suffix = os.path.splitext(filename)[-1] or ".wav"
#     with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
#         tmp.write(file_bytes)
#         tmp_path = tmp.name

#     try:
#         result = model.transcribe(tmp_path)
#         return {
#             "detected_language": result.get("language", "unknown"),
#             "transcript": result["text"].strip()
#         }
#     finally:
#         os.unlink(tmp_path)

from faster_whisper import WhisperModel
import tempfile
import os
from app.config import settings

_model_cache = {}


def get_whisper_model(model_name: str = None):
    """Load or get cached Whisper model"""
    name = model_name or settings.WHISPER_MODEL
    if name not in _model_cache:
        print(f"[Whisper] Loading model: {name}")
        # faster-whisper: device="cpu", compute_type="int8" for CPU processing
        _model_cache[name] = WhisperModel(name, device="cpu", compute_type="int8")
    return _model_cache[name]


async def transcribe_audio(file_bytes: bytes, filename: str, model_name: str = None) -> dict:
    """Transcribe audio file using faster-whisper"""
    model = get_whisper_model(model_name)

    suffix = os.path.splitext(filename)[-1] or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    try:
        # faster-whisper API: returns (segments, info)
        segments, info = model.transcribe(tmp_path, language=None)
        
        # Combine all segment texts
        transcript = " ".join([segment.text for segment in segments]).strip()
        
        return {
            "detected_language": info.language or "unknown",
            "transcript": transcript
        }
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)