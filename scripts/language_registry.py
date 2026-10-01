"""Shared reader-language metadata.

Adding metadata here does not publish a language. Reader-facing availability is
derived from actual article translations and registered static destinations.
"""

LANGUAGES = {
    "nb": {"label": "Norsk", "direction": "ltr"},
    "en": {"label": "English", "direction": "ltr"},
    "fr": {"label": "Français", "direction": "ltr"},
    "de": {"label": "Deutsch", "direction": "ltr"},
    "ja": {"label": "日本語", "direction": "ltr"},
    "ko": {"label": "한국어", "direction": "ltr"},
    "hi": {"label": "हिन्दी", "direction": "ltr"},
    "he": {"label": "עברית", "direction": "rtl"},
    "zh-Hans": {"label": "简体中文", "direction": "ltr"},
    "zh-Hant": {"label": "繁體中文", "direction": "ltr"},
}

RTL_BASE_LANGUAGES = {"ar", "fa", "he", "ur"}


def metadata(code):
    known = LANGUAGES.get(code)
    if known:
        return known
    base = code.split("-", 1)[0].lower()
    return {
        "label": code,
        "direction": "rtl" if base in RTL_BASE_LANGUAGES else "ltr",
    }


def label(code):
    return metadata(code)["label"]


def direction(code):
    return metadata(code)["direction"]
