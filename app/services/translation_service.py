from deep_translator import GoogleTranslator

DIRECTION_MAP = {
    "en_to_km": ("en", "km"),
    "km_to_en": ("km", "en"),
}

def translate_text(text: str, direction: str) -> str:
    if direction not in DIRECTION_MAP:
        raise ValueError("direction must be 'en_to_km' or 'km_to_en'")

    source_lang, target_lang = DIRECTION_MAP[direction]
    translator = GoogleTranslator(source=source_lang, target=target_lang)
    return translator.translate(text)



  