"""Shared metadata for reader-facing languages.

Registry membership is not publication. Callers must derive availability from
actual published destinations before rendering a language to readers.
"""

LANGUAGES = {
    "nb": {"label": "Norsk", "direction": "ltr"},
    "en": {"label": "English", "direction": "ltr"},
    "fr": {"label": "Français", "direction": "ltr"},
    "de": {"label": "Deutsch", "direction": "ltr"},
    "ja": {"label": "日本語", "direction": "ltr"},
    "ko": {"label": "한국어", "direction": "ltr"},
    "zh-Hans": {"label": "简体中文", "direction": "ltr"},
    "es": {"label": "Español", "direction": "ltr"},
    "pt": {"label": "Português", "direction": "ltr"},
    "ar": {"label": "العربية", "direction": "rtl"},
    # Prepared metadata only. These remain invisible until a real published
    # destination is present in the article/static-page registry.
    "hi": {"label": "हिन्दी", "direction": "ltr"},
    "he": {"label": "עברית", "direction": "rtl"},
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


def ordered_published(codes):
    """Return only observed publication languages in stable display order."""
    published = set(codes)
    ordered = [code for code in LANGUAGES if code in published]
    return ordered + sorted(published.difference(ordered))
