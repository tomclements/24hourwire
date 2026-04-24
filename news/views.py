from django.shortcuts import render, redirect
from django.core import signing
from django.http import Http404, HttpResponse
from django.utils import timezone
from django.views.decorators.cache import cache_page
from datetime import timedelta
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Story, StoryCluster
from .sources_config import (
    LANGUAGE_SOURCE_INFO, DEFAULT_SOURCES, SOURCES, LANGUAGE_NAMES,
    PAYWALLED_SOURCES, CATEGORY_KEYWORDS, CATEGORY_NAMES, UI_STRINGS, LANGUAGE_NAMES,
)
from .categorization import categorize_story, get_story_categories, check_exclusion


def is_staff_or_superuser(user):
    """Check if user is staff or superuser."""
    return user.is_staff or user.is_superuser


@cache_page(60)  # Cache home page for 1 minute
def home(request):
    cutoff = timezone.now() - timedelta(hours=24)
    
    # Get language from request - URL param overrides detected language
    language = request.GET.get('lang', getattr(request, 'detected_language', 'en'))
    if language not in SOURCES:
        language = 'en'
    
    # Get sources for this language
    lang_sources = SOURCES.get(language, SOURCES['en'])
    lang_default_sources = DEFAULT_SOURCES.get(language, DEFAULT_SOURCES['en'])
    lang_source_info = LANGUAGE_SOURCE_INFO.get(language, LANGUAGE_SOURCE_INFO['en'])
    category_names = CATEGORY_NAMES.get(language, CATEGORY_NAMES['en'])
    
    selected_sources_param = request.GET.get('sources')
    
    if selected_sources_param == 'all':
        selected_sources = [s[0] for s in lang_sources]
    elif selected_sources_param == 'center':
        selected_sources = [s[0] for s in lang_sources if s[1] == 'Center']
    elif selected_sources_param == 'left-center':
        selected_sources = [s[0] for s in lang_sources if s[1] == 'Left-Center']
    elif selected_sources_param == 'left':
        selected_sources = [s[0] for s in lang_sources if s[1] == 'Left']
    elif selected_sources_param == 'right':
        selected_sources = [s[0] for s in lang_sources if s[1] == 'Right']
    elif selected_sources_param == 'clear' or selected_sources_param == '':
        selected_sources = []
    elif selected_sources_param:
        # Check if the param contains bias categories (left, center, right, etc.)
        bias_categories = ['left', 'left-center', 'center', 'right-center', 'right']
        requested_values = [v.strip().lower() for v in selected_sources_param.split(',')]
        
        # If any requested value is a bias category, convert to source names
        if any(v in bias_categories for v in requested_values):
            selected_sources = []
            for val in requested_values:
                if val == 'left':
                    selected_sources.extend([s[0] for s in lang_sources if s[1] == 'Left'])
                elif val == 'left-center':
                    selected_sources.extend([s[0] for s in lang_sources if s[1] == 'Left-Center'])
                elif val == 'center':
                    selected_sources.extend([s[0] for s in lang_sources if s[1] == 'Center'])
                elif val == 'right-center':
                    selected_sources.extend([s[0] for s in lang_sources if s[1] == 'Right-Center'])
                elif val == 'right':
                    selected_sources.extend([s[0] for s in lang_sources if s[1] == 'Right'])
        else:
            # Treat as source names
            selected_sources = requested_values
    else:
        selected_sources = lang_default_sources
    
    all_stories = list(Story.objects.filter(published__gte=cutoff, language=language).order_by('-published'))
    
    for story in all_stories:
        story.story_categories = get_story_categories(story.title, language)
        bias_info = lang_source_info.get(story.source, ('Unknown', '#999', 'https://mediabiasfactcheck.com/'))
        story.bias_label = bias_info[0]
        story.bias_color = bias_info[1]
        story.bias_link = bias_info[2]
        story.is_paywalled = story.source in PAYWALLED_SOURCES
    
    stories = [s for s in all_stories if s.source in selected_sources]

    # Load pre-computed clusters for "Most Covered" tab
    most_covered_stories = []
    clusters = StoryCluster.objects.filter(
        language=language,
        source_count__gte=2,
    ).prefetch_related('stories')[:20]

    for cluster in clusters:
        rep = cluster.representative_story
        # Apply bias info to the representative story
        bias_info = lang_source_info.get(rep.source, ('Unknown', '#999', 'https://mediabiasfactcheck.com/'))
        rep.bias_label = bias_info[0]
        rep.bias_color = bias_info[1]
        rep.bias_link = bias_info[2]
        rep.is_paywalled = rep.source in PAYWALLED_SOURCES
        rep.story_categories = get_story_categories(rep.title, language)
        rep.covered_by_count = cluster.source_count
        rep.covered_by_sources = cluster.sources
        most_covered_stories.append(rep)

    grouped = {}
    for cat_id, cat_name in category_names.items():
        if cat_id == 'all':
            cat_stories = list(stories)
        elif cat_id == 'most_covered':
            cat_stories = most_covered_stories
        else:
            cat_stories = [s for s in stories if cat_id in s.story_categories]
        grouped[cat_id] = {
            'name': cat_name,
            'stories': cat_stories
        }
    
    return render(request, 'home.html', {
        'grouped': grouped,
        'sources': lang_sources,
        'selected_sources': selected_sources,
        'default_sources': lang_default_sources,
        'language': language,
        'language_names': LANGUAGE_NAMES,
        't': UI_STRINGS.get(language, UI_STRINGS['en']),
        'source_filter': selected_sources_param or 'default',
    })


@cache_page(3600)  # Cache static pages for 1 hour
def about_view(request):
    language = request.GET.get('lang', getattr(request, 'detected_language', 'en'))
    if language not in SOURCES:
        language = 'en'

    lang_sources = SOURCES.get(language, SOURCES['en'])
    lang_source_info = LANGUAGE_SOURCE_INFO.get(language, LANGUAGE_SOURCE_INFO['en'])

    # Group sources by bias for display
    bias_groups = {}
    for source_name, bias in lang_sources:
        if bias not in bias_groups:
            bias_groups[bias] = []
        bias_groups[bias].append(source_name)

    template = 'about_es.html' if language == 'es' else 'about.html'
    return render(request, template, {
        'language': language,
        'sources': lang_sources,
        'source_info': lang_source_info,
        'bias_groups': bias_groups,
    })


def terms_view(request):
    language = request.GET.get('lang', getattr(request, 'detected_language', 'en'))
    if language == 'es':
        return render(request, 'terms_es.html')
    return render(request, 'terms.html')


def privacy_view(request):
    language = request.GET.get('lang', getattr(request, 'detected_language', 'en'))
    if language == 'es':
        return render(request, 'privacy_es.html')
    return render(request, 'privacy.html')


def copyright_view(request):
    return render(request, 'copyright.html')


def login_view(request):
    if request.user.is_authenticated:
        if is_staff_or_superuser(request.user):
            return redirect('dashboard')
        else:
            logout(request)
            messages.error(request, 'Access restricted to administrators only.')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if is_staff_or_superuser(user):
                login(request, user)
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, 'Access restricted to administrators only.')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@cache_page(3600)  # Cache story share pages for 1 hour
def story_share(request, story_id):
    """Display a story sharing page with proper OG/Twitter Card meta tags.
    
    This page is designed to be shared on social media. It shows the story
    preview with full Open Graph and Twitter Card metadata, then redirects
    to the original article.
    """
    from django.http import Http404
    
    try:
        story = Story.objects.get(id=story_id)
    except Story.DoesNotExist:
        raise Http404("Story not found")
    
    # Get language and bias info
    language = story.language
    lang_source_info = LANGUAGE_SOURCE_INFO.get(language, LANGUAGE_SOURCE_INFO['en'])
    bias_info = lang_source_info.get(story.source, ('Unknown', '#999', ''))
    story.bias_label = bias_info[0]
    story.bias_color = bias_info[1]
    story.is_paywalled = story.source in PAYWALLED_SOURCES
    
    # Get UI strings
    ui_strings = UI_STRINGS.get(language, UI_STRINGS['en'])
    
    return render(request, 'story_share.html', {
        'story': story,
        'language': language,
        't': ui_strings,
    })


def branded_redirect(request, token):
    """Stateless branded redirect using signed tokens.
    
    Verifies a signed token containing story metadata, renders a branded
    landing page with OG/Twitter Card tags, then redirects to the
    original article. No database storage required.
    """
    signer = signing.Signer()
    try:
        # Verify the signed token
        payload = signer.unsign(token)
        data = signing.loads(payload)
    except (signing.BadSignature, signing.SignatureExpired):
        raise Http404("Invalid or expired link")
    
    url = data.get('url', '')
    title = data.get('title', '')
    source = data.get('source', '')
    image_url = data.get('image_url', '')
    
    if not url:
        raise Http404("Invalid link")
    
    return render(request, 'branded_redirect.html', {
        'url': url,
        'title': title,
        'source': source,
        'image_url': image_url,
        'token': token,
    })


@cache_page(600)  # Cache sitemaps for 10 minutes
def sitemap(request):
    """Generate standard XML sitemap for static pages."""
    from django.utils.xmlutils import SimplerXMLGenerator
    from io import StringIO

    urls = [
        {'loc': 'https://24hourwire.news/', 'priority': '1.0', 'changefreq': 'hourly'},
        {'loc': 'https://24hourwire.news/feeds/', 'priority': '0.8', 'changefreq': 'daily'},
        {'loc': 'https://24hourwire.news/about/', 'priority': '0.5', 'changefreq': 'weekly'},
        {'loc': 'https://24hourwire.news/terms/', 'priority': '0.3', 'changefreq': 'monthly'},
        {'loc': 'https://24hourwire.news/privacy/', 'priority': '0.3', 'changefreq': 'monthly'},
    ]

    output = StringIO()
    xml = SimplerXMLGenerator(output, 'utf-8')
    xml.startDocument()
    xml.startElement('urlset', {
        'xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9'
    })

    now = timezone.now().strftime('%Y-%m-%d')
    for url in urls:
        xml.startElement('url', {})
        xml.addQuickElement('loc', url['loc'])
        xml.addQuickElement('lastmod', now)
        xml.addQuickElement('changefreq', url['changefreq'])
        xml.addQuickElement('priority', url['priority'])
        xml.endElement('url')

    xml.endElement('urlset')
    xml.endDocument()

    return HttpResponse(output.getvalue(), content_type='application/xml')


@cache_page(600)  # Cache news sitemap for 10 minutes
def news_sitemap(request):
    """Generate Google News sitemap with recent stories.
    
    Google News requires:
    - Only articles from last 48 hours
    - <news:publication> with name and language
    - <news:publication_date> in W3C format
    - <news:title> matching the article headline
    """
    cutoff = timezone.now() - timedelta(hours=48)
    stories = Story.objects.filter(
        published__gte=cutoff
    ).order_by('-published')[:1000]

    output = []
    output.append('<?xml version="1.0" encoding="UTF-8"?>')
    output.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    output.append('        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">')

    for story in stories:
        output.append('  <url>')
        output.append(f'    <loc>https://24hourwire.news/story/{story.id}/</loc>')
        output.append('    <news:news>')
        output.append('      <news:publication>')
        output.append('        <news:name>24HourWire</news:name>')
        output.append(f'        <news:language>{story.language}</news:language>')
        output.append('      </news:publication>')
        output.append(f'      <news:publication_date>{story.published.strftime("%Y-%m-%dT%H:%M:%SZ")}</news:publication_date>')
        # Escape XML special characters in title
        title = story.title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        output.append(f'      <news:title>{title}</news:title>')
        output.append('    </news:news>')
        output.append('  </url>')

    output.append('</urlset>')

    return HttpResponse('\n'.join(output), content_type='application/xml')


def different_angle(request, story_id):
    """Show related stories with different bias for a given story.
    
    Uses StoryCluster to find stories covering the same event from different sources,
    then presents up to one story from each different bias category.
    """
    from django.http import JsonResponse
    import json
    import logging
    
    logger = logging.getLogger('news.different_angle')
    
    try:
        story = Story.objects.get(id=story_id)
        logger.info(f"Different Angle requested for story {story_id}: '{story.title}' from {story.source}")
    except Story.DoesNotExist:
        logger.error(f"Story {story_id} not found")
        return JsonResponse({'error': 'Story not found'}, status=404)
    
    # Get story's bias
    language = story.language
    lang_source_info = LANGUAGE_SOURCE_INFO.get(language, LANGUAGE_SOURCE_INFO['en'])
    story_bias = lang_source_info.get(story.source, ('Unknown', '#999', ''))[0]
    
    # Find clusters this story belongs to
    clusters = story.clusters.filter(language=language)
    cluster_count = clusters.count()
    logger.info(f"Story {story_id} belongs to {cluster_count} cluster(s)")
    
    # Collect all stories from these clusters (stories covering the same event)
    related_stories = []
    seen_biases = set()
    
    for cluster in clusters:
        # Get all stories in this cluster except the current one
        cluster_stories = cluster.stories.exclude(id=story_id)
        
        for related in cluster_stories:
            related_bias = lang_source_info.get(related.source, ('Unknown', '#999', ''))[0]
            
            # Skip if same bias as original story or already have a story from this bias
            if related_bias == story_bias or related_bias in seen_biases:
                continue
            
            bias_info = lang_source_info.get(related.source, ('Unknown', '#999', ''))
            related.bias_label = bias_info[0]
            related.bias_color = bias_info[1]
            related.is_paywalled = related.source in PAYWALLED_SOURCES
            # Note: skip get_story_categories() here for performance - not needed for JSON response
            related_stories.append(related)
            seen_biases.add(related_bias)
    
    # Sort by bias (Left to Right) for consistent presentation
    bias_order = {'Left': 0, 'Left-Center': 1, 'Center': 2, 'Right-Center': 3, 'Right': 4, 'Unknown': 5}
    related_stories.sort(key=lambda x: bias_order.get(x.bias_label, 5))
    
    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        stories_data = []
        for s in related_stories:
            stories_data.append({
                'id': s.id,
                'title': s.title,
                'source': s.source,
                'url': s.url,
                'bias_label': s.bias_label,
                'bias_color': s.bias_color,
                'published': s.published.strftime('%Y-%m-%d %H:%M'),
                'is_paywalled': s.is_paywalled,
                'excerpt': s.get_clean_excerpt()[:200] if s.get_clean_excerpt() else '',
            })
        logger.info(f"Returning {len(stories_data)} related stories for story {story_id}")
        return JsonResponse({
            'original_story': {
                'id': story.id,
                'title': story.title,
                'source': story.source,
                'bias_label': story_bias,
            },
            'related_stories': stories_data,
        })
    
    # Return HTML for direct browser requests
    return render(request, 'different_angle.html', {
        'original_story': story,
        'original_bias': story_bias,
        'related_stories': related_stories,
        'language': language,
        'language_names': LANGUAGE_NAMES,
        't': UI_STRINGS.get(language, UI_STRINGS['en']),
    })


@cache_page(300)  # Cache feeds page for 5 minutes
def feeds_view(request):
    """Display available RSS and JSON feeds for the selected language."""
    language = request.GET.get('lang', getattr(request, 'detected_language', 'en'))
    t = UI_STRINGS.get(language, UI_STRINGS['en'])
    
    # Get categories for the selected language only
    cutoff = timezone.now() - timedelta(hours=24)
    categories = Story.objects.filter(
        language=language,
        published__gte=cutoff,
        category__isnull=False
    ).values('category').distinct().order_by('category')
    
    # Build category feeds list
    category_feeds = []
    for item in categories:
        cat = item['category']
        if cat:
            category_feeds.append({
                'category': cat,
                'name': cat.replace('-', ' ').title(),
                'rss_url': f'/feed/{language}/{cat}/',
                'json_url': f'/feed/{language}/{cat}.json',
            })
    
    context = {
        't': t,
        'language': language,
        'language_name': LANGUAGE_NAMES.get(language, language.upper()),
        'category_feeds': category_feeds,
        'language_rss': f'/feed/{language}/',
        'language_json': f'/feed/{language}.json',
    }
    
    return render(request, 'feeds.html', context)


def widget_js(request):
    """Generate an embeddable JavaScript widget for external sites.
    
    Usage:
        <script src="https://24hourwire.news/widget.js?lang=en&limit=5&category=world"></script>
    
    Parameters:
        lang: Language code (default: en)
        limit: Number of stories to show (default: 5, max: 20)
        category: Filter by category (optional)
        theme: 'light' or 'dark' (default: light)
        target: CSS selector for container (default: #hourwire-widget)
    """
    from django.http import JsonResponse
    
    language = request.GET.get('lang', 'en')
    if language not in SOURCES:
        language = 'en'
    
    try:
        limit = min(int(request.GET.get('limit', 5)), 20)
    except ValueError:
        limit = 5
    
    category = request.GET.get('category', '')
    theme = request.GET.get('theme', 'light')
    target = request.GET.get('target', '#hourwire-widget')
    
    # Fetch stories
    cutoff = timezone.now() - timedelta(hours=24)
    stories = Story.objects.filter(language=language, published__gte=cutoff)
    
    if category:
        stories = stories.filter(category=category)
    
    stories = stories.order_by('-published')[:limit]
    
    # Get source bias info for each story
    lang_source_info = LANGUAGE_SOURCE_INFO.get(language, LANGUAGE_SOURCE_INFO['en'])
    story_data = []
    for story in stories:
        bias_info = lang_source_info.get(story.source, ('Unknown', '#999', ''))
        story_data.append({
            'title': story.title,
            'url': story.url,
            'source': story.source,
            'bias_label': bias_info[0],
            'published': story.published.isoformat(),
            'image_url': story.image_url or '',
        })
    
    response = render(request, 'widget.js', {
        'stories': story_data,
        'theme': theme,
        'target': target,
        'language': language,
    })
    
    response['Content-Type'] = 'application/javascript; charset=utf-8'
    response['Access-Control-Allow-Origin'] = '*'
    return response
