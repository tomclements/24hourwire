from django import template
from django.core import signing

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
