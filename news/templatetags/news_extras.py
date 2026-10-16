import re

from django import template
from django.core import signing
from django.utils import translation
from django.utils.timesince import timesince
from news.sources_config import LANGUAGE_NAMES, UI_STRINGS

register = template.Library()

META_SUFFIX = ' | 24HourWire'

# Django's catalogs: hi lacks timesince units; de needs dative plurals after "vor".
TIMESINCE_FIXES = {
    'de': (('Tage', 'Tagen'), ('Monate', 'Monaten'), ('Jahre', 'Jahren')),
    'hi': (('minutes', 'मिनट'), ('minute', 'मिनट'), ('hours', 'घंटे'), ('hour', 'घंटा'),
           ('days', 'दिन'), ('day', 'दिन'), ('weeks', 'सप्ताह'), ('week', 'सप्ताह'),
           ('months', 'महीने'), ('month', 'महीना'), ('years', 'वर्ष'), ('year', 'वर्ष')),
}


@register.filter
def sign_share_data(story):
    """Generate a signed token for stateless branded sharing.
    
    Usage in template: {{ story|sign_share_data }}
    Returns a URL-safe signed token containing story metadata.
    """
    data = {
        'url': story.url,
        'title': story.title,
        'source': story.source,
        'image_url': story.image_url or '',
    }
    signer = signing.Signer()
    payload = signing.dumps(data)
    return signer.sign(payload)


@register.filter
def sign_poll_data(poll):
    """Generate a signed token for stateless poll sharing.
    
    Usage in template: {{ poll|sign_poll_data }}
    Returns a URL-safe signed token containing poll metadata.
    """
    data = {
        'type': 'poll',
        'poll_id': poll.id,
        'question': poll.question,
        'options': poll.options,
        'language': poll.language,
    }
    signer = signing.Signer()
    payload = signing.dumps(data)
    return signer.sign(payload)


@register.filter
def language_name(code):
    """Return the full language name for a language code.
    
    Usage: {{ lang|language_name }}
    """
    return LANGUAGE_NAMES.get(code, code)


@register.filter
def topic_translation(topic, language):
    """Return the topic's translated headline/description for language."""
    return topic.get_translation(language)


@register.filter
def topic_meta_title(topic, language):
    """Return the topic meta title with the site suffix exactly once.

    English uses the stored meta_title (already suffixed in seed data); for
    other languages we prefer a translated meta_title, then the translated
    title, then fall back to English. The suffix is stripped and re-added so
    prod rows that already contain it remain valid.
    """
    if language == 'en' or not language:
        base = topic.meta_title or topic.title
    else:
        lang_data = topic.translations.get(language, {})
        base = lang_data.get('meta_title') or lang_data.get('title') or topic.title
    base = base.rstrip().removesuffix(META_SUFFIX).strip()
    return f"{base}{META_SUFFIX}"


@register.filter
def topic_meta_description(topic, language):
    """Return the translated topic meta description for language."""
    if language == 'en' or not language:
        return topic.meta_description or topic.description
    lang_data = topic.translations.get(language, {})
    return lang_data.get('description') or lang_data.get('meta_description') or topic.description


@register.filter
def bias_label(label, language):
    """Translate a story/source bias label into the page language.

    The English class name (used for CSS) is left untouched; only the
    displayed text is localized.
    """
    strings = UI_STRINGS.get(language, UI_STRINGS['en'])
    mapping = {
        'Left': strings.get('filter_left', 'Left'),
        'Left-Center': strings.get('filter_left_center', 'Left-Center'),
        'Center': strings.get('filter_center', 'Center'),
        'Right-Center': strings.get('filter_right_center', 'Right-Center'),
        'Right': strings.get('filter_right', 'Right'),
    }
    return mapping.get(label, label)


@register.filter
def source_count_label(count, language):
    """Return a localized 'N sources' phrase with correct plural forms."""
    strings = UI_STRINGS.get(language, UI_STRINGS['en'])
    count = int(count)

    if count == 1:
        return strings.get('source_count_one', '1 source').format(count=count)

    # Arabic plural forms (Django ar formula)
    if language == 'ar':
        if count == 2:
            return strings.get('source_count_two', '{count} مصادر').format(count=count)
        if 3 <= count % 100 <= 10:
            return strings.get('source_count_few', '{count} مصادر').format(count=count)
        if count % 100 >= 11:
            return strings.get('source_count_many', '{count} مصدرًا').format(count=count)
        return strings.get('source_count_other', '{count} مصادر').format(count=count)

    # Russian plural forms
    if language == 'ru':
        last_two = count % 100
        last_one = count % 10
        if 11 <= last_two <= 19:
            return strings.get('source_count_many', '{count} источников').format(count=count)
        if last_one == 1:
            return strings.get('source_count_one', '{count} источник').format(count=count)
        if 2 <= last_one <= 4:
            return strings.get('source_count_few', '{count} источника').format(count=count)
        return strings.get('source_count_many', '{count} источников').format(count=count)

    return strings.get('source_count_other', '{count} sources').format(count=count)


@register.filter
def local_timesince(value, language):
    """Render a localized relative time phrase in the requested language."""
    django_lang = {'zh': 'zh-hans'}.get(language, language)
    with translation.override(django_lang):
        delta = timesince(value, depth=1)
    for src, dst in TIMESINCE_FIXES.get(language, ()):
        delta = re.sub(rf'\b{src}\b', dst, delta)
    strings = UI_STRINGS.get(language, UI_STRINGS['en'])
    template = strings.get('time_ago', '{delta} ago')
    return template.format(delta=delta)
