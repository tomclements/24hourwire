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
- CATEGORY_KEYWORDS_WEIGHTED: dict - {category: {high: [], medium: [], low: []}}
- EXCLUSION_RULES: dict - {category: {keyword: [exclusions]}}
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

# Per-language weighted keywords for categorization
# Falls back to English for languages without weighted keywords
LANGUAGE_CATEGORY_KEYWORDS_WEIGHTED = {}
for code, mod in LANGUAGE_MODULES.items():
    if hasattr(mod, 'CATEGORY_KEYWORDS_WEIGHTED'):
        LANGUAGE_CATEGORY_KEYWORDS_WEIGHTED[code] = mod.CATEGORY_KEYWORDS_WEIGHTED
    else:
        # Fallback to English weighted keywords if not defined
        LANGUAGE_CATEGORY_KEYWORDS_WEIGHTED[code] = getattr(en, 'CATEGORY_KEYWORDS_WEIGHTED', en.CATEGORY_KEYWORDS)

# Per-language exclusion rules for categorization
# Falls back to English for languages without exclusion rules
LANGUAGE_EXCLUSION_RULES = {}
for code, mod in LANGUAGE_MODULES.items():
    if hasattr(mod, 'EXCLUSION_RULES'):
        LANGUAGE_EXCLUSION_RULES[code] = mod.EXCLUSION_RULES
    else:
        # Fallback to English exclusion rules if not defined
        LANGUAGE_EXCLUSION_RULES[code] = getattr(en, 'EXCLUSION_RULES', {})

# Backward compatibility: English weighted keywords as default
CATEGORY_KEYWORDS_WEIGHTED = LANGUAGE_CATEGORY_KEYWORDS_WEIGHTED.get('en', {})

# Backward compatibility: English exclusion rules as default
EXCLUSION_RULES = LANGUAGE_EXCLUSION_RULES.get('en', {})
