"""Shared metadata for reader-facing languages.

Registry membership is not publication. Callers must derive availability from
actual published destinations before rendering a language to readers.
"""

LANGUAGES = {
    "nb": {"label": "Norsk", "english_name": "Norwegian", "direction": "ltr"},
    "en": {"label": "English", "english_name": "English", "direction": "ltr"},
    "fr": {"label": "Français", "english_name": "French", "direction": "ltr"},
    "de": {"label": "Deutsch", "english_name": "German", "direction": "ltr"},
    "ja": {"label": "日本語", "english_name": "Japanese", "direction": "ltr"},
    "ko": {"label": "한국어", "english_name": "Korean", "direction": "ltr"},
    "zh-Hans": {"label": "简体中文", "english_name": "Simplified Chinese", "direction": "ltr"},
    "es-AR": {"label": "Español (Argentina)", "english_name": "Spanish (Argentina)", "direction": "ltr"},
    "es": {"label": "Español", "english_name": "Spanish", "direction": "ltr"},
    "zh-Hant": {"label": "繁體中文", "english_name": "Traditional Chinese", "direction": "ltr"},
    "pt": {"label": "Português", "english_name": "Portuguese", "direction": "ltr"},
    "pt-BR": {"label": "Português (Brasil)", "english_name": "Portuguese (Brazil)", "direction": "ltr"},
    "ar": {"label": "العربية", "english_name": "Arabic", "direction": "rtl"},
    "hi": {"label": "हिन्दी", "english_name": "Hindi", "direction": "ltr"},
    "he": {"label": "עברית", "english_name": "Hebrew", "direction": "rtl"},
}

RTL_BASE_LANGUAGES = {"ar", "fa", "he", "ur"}


def metadata(code):
    known = LANGUAGES.get(code)
    if known:
        return known
    base = code.split("-", 1)[0].lower()
    return {
        "label": code,
        "english_name": code,
        "direction": "rtl" if base in RTL_BASE_LANGUAGES else "ltr",
    }


def label(code):
    return metadata(code)["label"]


def english_name(code):
    return metadata(code)["english_name"]


def direction(code):
    return metadata(code)["direction"]


def ordered_published(codes):
    """Return only observed publication languages in stable display order."""
    published = set(codes)
    ordered = [code for code in LANGUAGES if code in published]
    return ordered + sorted(published.difference(ordered))
