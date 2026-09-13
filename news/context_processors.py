"""Context processors that inject shared site-wide template variables.

Provides the header/footer/branding context (language, translations, source
list, and JS UI strings) to every template that extends base.html so pages do
not need to pass them individually. View context always overrides these
defaults.
"""

import json

from news.languages import DEFAULT_SOURCES, LANGUAGE_NAMES, SOURCES, SUPPORTED_LANGUAGES, UI_STRINGS

# UI strings that the client-side JavaScript needs (share overlay, modals).
JS_UI_KEYS = (
    'share_story_title',
    'share_on_x',
    'share_facebook',
    'share_linkedin',
    'copy_link',
    'copied',
    'loading_related',
    'no_related_stories',
    'error_loading',
)


def site_globals(request):
    """Provide default site-wide context used by base.html."""
    # Match DetectLanguageMiddleware / news.views._resolve_ui_language so chrome
    # (t, language, ui_json) follows preferred_lang cookie via LANGUAGE_CODE.
    # lang=all / invalid / missing → LANGUAGE_CODE (never literal "all" for UI).
    language = request.GET.get('lang')
    if language not in SUPPORTED_LANGUAGES:
        language = getattr(request, 'LANGUAGE_CODE', 'en') or 'en'
    if language not in SOURCES:
        language = 'en'

    strings = UI_STRINGS.get(language, UI_STRINGS['en'])
    ui_json = json.dumps({key: strings.get(key, '') for key in JS_UI_KEYS})

    return {
        'language': language,
        'language_names': LANGUAGE_NAMES,
        'selected_sources': DEFAULT_SOURCES.get(language, DEFAULT_SOURCES['en']),
        't': strings,
        'ui_json': ui_json,
    }