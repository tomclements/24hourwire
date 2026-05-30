from django import template
from django.core import signing
from news.sources_config import LANGUAGE_NAMES

register = template.Library()


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
