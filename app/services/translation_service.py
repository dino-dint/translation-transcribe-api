
from deep_translator import GoogleTranslator
from app.config import settings
import openai

DIRECTION_MAP = {
    "en_to_km": ("en", "km"),
    "km_to_en": ("km", "en"),
}

def translate_text(text: str, direction: str) -> str:
    if direction not in DIRECTION_MAP:
        raise ValueError("direction must be 'en_to_km' or 'km_to_en'")

    source_lang, target_lang = DIRECTION_MAP[direction]
    provider = settings.TRANSLATION_PROVIDER.lower()

    if provider == "openai":
        return _translate_openai(text, source_lang, target_lang)
    elif provider == "gemini":
        return _translate_gemini(text, source_lang, target_lang)
    else:  # default: google
        return _translate_google(text, source_lang, target_lang)


def _translate_google(text: str, source: str, target: str) -> str:
    return GoogleTranslator(source=source, target=target).translate(text)


def _translate_openai(text: str, source: str, target: str) -> str:
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
    lang_map = {"en": "English", "km": "Khmer"}
    prompt = (
        f"Translate this from {lang_map[source]} to {lang_map[target]}. "
        f"Return only the translation, nothing else:\n\n{text}"
    )
    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def _translate_gemini(text: str, source: str, target: str) -> str:
    import google.generativeai as genai
    genai.configure(api_key=settings.GEMINI_API_KEY)
    lang_map = {"en": "English", "km": "Khmer"}
    model = genai.GenerativeModel(settings.GEMINI_MODEL)
    prompt = (
        f"Translate this from {lang_map[source]} to {lang_map[target]}. "
        f"Return only the translation, nothing else:\n\n{text}"
    )
    response = model.generate_content(prompt)
    return response.text.strip()