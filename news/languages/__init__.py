"""
Language registry for 24HourWire.

Each language module exports:
- CODE: str - language code (e.g. 'en')
- NAME: str - display name
- FEEDS: list - (name, url) tuples
- SOURCE_INFO: dict - {name: (bias_label, color, link)}
- DEFAULT_SOURCES: list - default selected sources
- SOURCES: list - (name, bias) tuples
- CATEGORY_KEYWORDS: dict - {category: [keywords]}
- STOP_WORDS: set - stop words for dedup/clustering
- SOURCE_ATTRIBUTION: str - regex for excerpt cleaning
- GENERIC_TEXT: list - generic text to filter
- CATEGORY_NAMES: OrderedDict - {id: display_name}
- UI_STRINGS: dict - {key: translated_string}
- PAYWALLED_SOURCES: set - paywalled source names
"""

from news.languages import en, es, fr, de, pt, it, ar, ru, ja, zh, ko, tr, hi

LANGUAGE_MODULES = {m.CODE: m for m in [en, es, fr, de, pt, it, ar, ru, ja, zh, ko, tr, hi]}

SUPPORTED_LANGUAGES = set(LANGUAGE_MODULES.keys())

# Convenience dicts for backward compatibility and easy access
LANGUAGE_FEEDS = {code: mod.FEEDS for code, mod in LANGUAGE_MODULES.items()}
LANGUAGE_SOURCE_INFO = {code: mod.SOURCE_INFO for code, mod in LANGUAGE_MODULES.items()}
DEFAULT_SOURCES = {code: mod.DEFAULT_SOURCES for code, mod in LANGUAGE_MODULES.items()}
SOURCES = {code: mod.SOURCES for code, mod in LANGUAGE_MODULES.items()}
CATEGORY_KEYWORDS = {code: mod.CATEGORY_KEYWORDS for code, mod in LANGUAGE_MODULES.items()}
LANGUAGE_STOP_WORDS = {code: mod.STOP_WORDS for code, mod in LANGUAGE_MODULES.items()}
SOURCE_ATTRIBUTION = {code: mod.SOURCE_ATTRIBUTION for code, mod in LANGUAGE_MODULES.items()}
GENERIC_TEXT = {code: mod.GENERIC_TEXT for code, mod in LANGUAGE_MODULES.items()}
CATEGORY_NAMES = {code: mod.CATEGORY_NAMES for code, mod in LANGUAGE_MODULES.items()}
UI_STRINGS = {code: mod.UI_STRINGS for code, mod in LANGUAGE_MODULES.items()}
LANGUAGE_NAMES = {code: mod.NAME for code, mod in LANGUAGE_MODULES.items()}

# Combined paywalled sources across all languages
PAYWALLED_SOURCES = set()
for mod in LANGUAGE_MODULES.values():
    PAYWALLED_SOURCES |= mod.PAYWALLED_SOURCES
