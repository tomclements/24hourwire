from django.shortcuts import render, redirect
from django.core import signing
from django.http import Http404, HttpResponse
from django.utils import timezone
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.views.decorators.http import condition
from datetime import timedelta
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Story, StoryCluster, AnalyticsEvent, Topic, Poll, PollGenerationConfig
from .sources_config import (
    LANGUAGE_SOURCE_INFO, DEFAULT_SOURCES, SOURCES, LANGUAGE_NAMES,
    PAYWALLED_SOURCES, CATEGORY_KEYWORDS, CATEGORY_NAMES, UI_STRINGS, LANGUAGE_NAMES,
)
from .categorization import categorize_story, get_story_categories, check_exclusion


def _latest_story_timestamp(request):
    """Return the timestamp of the most recently published story for conditional GET."""
    cutoff = timezone.now() - timedelta(hours=24)
    latest = Story.objects.filter(published__gte=cutoff).order_by('-published').values_list('published', flat=True).first()
    return latest


def get_related_topics(story, active_topics=None):
    """Find active topics that match a story's title or categories.
    
    Returns a list of Topic objects (max 2) for display on story cards.
    
    NOTE: Does NOT verify topic has matching stories in DB (avoids N+1 queries).
    Topics are assumed to be relevant if keywords/categories match.
    """
    title_lower = story.title.lower()
    categories = getattr(story, 'story_categories', [story.category])
    
    related = []
    topics = active_topics or Topic.objects.filter(is_active=True)
    
    for topic in topics:
        # Check keyword match
        for kw in topic.keywords:
            if kw.lower() in title_lower:
                related.append(topic)
                break
        else:
            # Check category match if no keyword matched
            for cat in topic.categories:
                if cat in categories:
                    related.append(topic)
                    break
        
        if len(related) >= 2:
            break
    
    return related


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
        # Default to ALL sources (same as sources=all) so "All" bias filter shows everything
        selected_sources = [s[0] for s in lang_sources]
    
    # PERFORMANCE: Filter by source in DB, use only() to reduce data transfer,
    # then process in Python. Index: language + published + source covers this.
    stories = list(Story.objects.filter(
        published__gte=cutoff,
        language=language,
        source__in=selected_sources
    ).only(
        'id', 'title', 'excerpt', 'url', 'source', 'published',
        'language', 'category', 'image_url', 'url_hash', 'title_fingerprint'
    ).order_by('-published'))
    
    # Pre-fetch active topics once to avoid N+1 queries in get_related_topics
    active_topics = list(Topic.objects.filter(is_active=True))
    
    # Apply metadata to displayed stories only
    for story in stories:
        story.story_categories = get_story_categories(story.title, language, story.source)
        bias_info = lang_source_info.get(story.source, ('Unknown', '#999', 'https://mediabiasfactcheck.com/'))
        story.bias_label = bias_info[0]
        story.bias_color = bias_info[1]
        story.related_topics = get_related_topics(story, active_topics=active_topics)
        story.bias_link = bias_info[2]
        story.bias_class = bias_info[0].lower().replace(' ', '-').replace('/', '-') if bias_info[0] else 'unknown'
        story.is_paywalled = story.source in PAYWALLED_SOURCES

    # Load pre-computed clusters for "Most Covered" tab
    most_covered_stories = []
    clusters = StoryCluster.objects.filter(
        language=language,
        source_count__gte=2,
    ).select_related('representative_story')[:20]

    for cluster in clusters:
        rep = cluster.representative_story
        bias_info = lang_source_info.get(rep.source, ('Unknown', '#999', 'https://mediabiasfactcheck.com/'))
        rep.bias_label = bias_info[0]
        rep.bias_color = bias_info[1]
        rep.bias_link = bias_info[2]
        rep.is_paywalled = rep.source in PAYWALLED_SOURCES
        rep.story_categories = get_story_categories(rep.title, language, rep.source)
        rep.covered_by_count = cluster.source_count
        rep.covered_by_sources = cluster.sources
        most_covered_stories.append(rep)

    # Fetch active book recommendations for English categories
    recommended_books = {}
    all_books = []
    if language == 'en':
        from .models import RecommendedBook
        books = RecommendedBook.objects.filter(language='en', is_active=True)
        for book in books:
            if book.category not in recommended_books:
                recommended_books[book.category] = []
            recommended_books[book.category].append(book)
            all_books.append(book)
    
    # Fetch active poll for this language (at most 1, light presence)
    now = timezone.now()
    active_poll = Poll.objects.filter(
        language=language,
        is_active=True,
        status='active',
        ends_at__gt=now,
    ).order_by('?').first()
    
    grouped = {}
    for cat_id, cat_name in category_names.items():
        if cat_id == 'all':
            cat_stories = list(stories)
        elif cat_id == 'most_covered':
            cat_stories = most_covered_stories
        else:
            cat_stories = [s for s in stories if cat_id in s.story_categories]
        
        import random
        if cat_id == 'all' and all_books:
            cat_books = list(all_books)
            random.shuffle(cat_books)
            cat_books = cat_books[:2]  # Max 2 books for "All" tab
        else:
            cat_books = recommended_books.get(cat_id, [])
            if cat_books:
                random.shuffle(cat_books)
                cat_books = cat_books[:2]  # Max 2 books per category
        
        # Send first 20 for initial render, include metadata for "load more"
        grouped[cat_id] = {
            'name': cat_name,
            'stories': cat_stories[:20],
            'total_stories': len(cat_stories),
            'loaded': min(20, len(cat_stories)),
            'has_more': len(cat_stories) > 20,
            'books': cat_books,
            'poll': active_poll if cat_id == 'all' else None,
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
        'active_topics': active_topics,
        'active_poll': active_poll,
        'most_covered': most_covered_stories[:8],  # Top 8 for dedicated homepage section
    })


@cache_page(86400)  # 24 hours — robots.txt rarely changes
def robots_txt(request):
    """Serve robots.txt dynamically.
    
    Strategy:
    - Block ephemeral pages (/go/, /story/) from Google indexing to avoid
      'Crawled - currently not indexed' and 404 issues
    - Allow social media crawlers (Twitter, Facebook, LinkedIn) to access
      /go/ pages for generating preview cards
    - Sitemap only includes stable pages and recent 24h stories
    """
    content = """User-agent: *
Allow: /
Allow: /topic/
Disallow: /dashboard/
Disallow: /login/
Disallow: /go/
Disallow: /story/
Disallow: /different-angle/
Crawl-delay: 1

# Allow social media crawlers to access share pages for card generation
User-agent: Twitterbot
Allow: /go/
Allow: /story/

User-agent: facebookexternalhit
Allow: /go/
Allow: /story/

User-agent: LinkedInBot
Allow: /go/
Allow: /story/

Sitemap: https://24hourwire.news/sitemap.xml
Sitemap: https://24hourwire.news/news-sitemap.xml
"""
    return HttpResponse(content, content_type='text/plain')


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


@cache_page(3600)
def terms_view(request):
    language = request.GET.get('lang', getattr(request, 'detected_language', 'en'))
    if language == 'es':
        return render(request, 'terms_es.html')
    return render(request, 'terms.html')


@cache_page(3600)
def privacy_view(request):
    language = request.GET.get('lang', getattr(request, 'detected_language', 'en'))
    if language == 'es':
        return render(request, 'privacy_es.html')
    return render(request, 'privacy.html')


@cache_page(3600)
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

    Verifies a signed token containing story or poll metadata, renders a branded
    landing page with OG/Twitter Card tags, then redirects to the
    original article or poll page. No database storage required.
    """
    signer = signing.Signer()
    try:
        # Verify the signed token
        payload = signer.unsign(token)
        data = signing.loads(payload)
    except (signing.BadSignature, signing.SignatureExpired):
        raise Http404("Invalid or expired link")

    token_type = data.get('type', 'story')

    if token_type == 'poll':
        # Poll token: redirect to poll detail page
        poll_id = data.get('poll_id')
        if not poll_id:
            raise Http404("Invalid poll link")
        url = f"/poll/{poll_id}/"
        title = data.get('question', 'Poll')
        source = '24HourWire Poll'
        image_url = ''
        options = data.get('options', [])
        language = data.get('language', 'en')
        return render(request, 'branded_redirect.html', {
            'url': url,
            'title': title,
            'source': source,
            'image_url': image_url,
            'token': token,
            'is_poll': True,
            'options': options,
            'language': language,
        })

    # Story token: redirect to original article
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
        'is_poll': False,
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
    
    # Add active topic hub pages (indexable evergreen content)
    for topic in Topic.objects.filter(is_active=True):
        urls.append({
            'loc': f'https://24hourwire.news{topic.get_absolute_url()}',
            'priority': '0.7',
            'changefreq': 'hourly',
        })

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
    - Only articles from last 48 hours (but we use 24h to avoid 404s)
    - <news:publication> with name and language
    - <news:publication_date> in W3C format
    - <news:title> matching the article headline
    
    NOTE: We only include stories from last 24 hours (not 48) because
    stories expire and are deleted after 24h. Including 48h-old stories
    would cause Google to crawl URLs that return 404.
    """
    cutoff = timezone.now() - timedelta(hours=24)
    stories = Story.objects.filter(
        published__gte=cutoff
    ).order_by('-published')[:500]

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


def search_stories(request):
    """Search recent stories by keyword in title or excerpt.
    
    Searches only the last 24 hours of stories. No user tracking.
    """
    query = request.GET.get('q', '').strip()
    language = request.GET.get('lang', getattr(request, 'detected_language', 'en'))
    if language not in SOURCES:
        language = 'en'
    
    t = UI_STRINGS.get(language, UI_STRINGS['en'])
    lang_source_info = LANGUAGE_SOURCE_INFO.get(language, LANGUAGE_SOURCE_INFO['en'])
    
    results = []
    if query and len(query) >= 2:
        cutoff = timezone.now() - timedelta(hours=24)
        from django.db.models import Q
        results = list(Story.objects.filter(
            Q(title__icontains=query) | Q(excerpt__icontains=query),
            published__gte=cutoff,
            language=language,
        ).only('id', 'title', 'excerpt', 'url', 'source', 'published', 'image_url').order_by('-published')[:50])
        
        for story in results:
            bias_info = lang_source_info.get(story.source, ('Unknown', '#999', ''))
            story.bias_label = bias_info[0]
            story.bias_color = bias_info[1]
            story.bias_class = bias_info[0].lower().replace(' ', '-').replace('/', '-') if bias_info[0] else 'unknown'
            story.is_paywalled = story.source in PAYWALLED_SOURCES
    
    return render(request, 'search_results.html', {
        'query': query,
        'results': results,
        'language': language,
        't': t,
        'language_names': LANGUAGE_NAMES,
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


@condition(last_modified_func=_latest_story_timestamp)
@cache_page(60)  # Cache AJAX endpoint for 1 minute
def load_more_stories(request):
    """API endpoint for loading more stories via AJAX.
    
    Parameters:
        lang: Language code
        category: Category ID or 'all'
        offset: Number of stories already loaded
        sources: Source filter (optional)
    """
    from django.http import JsonResponse
    
    language = request.GET.get('lang', 'en')
    if language not in SOURCES:
        language = 'en'
    
    category_id = request.GET.get('category', 'all')
    try:
        offset = int(request.GET.get('offset', 20))
    except ValueError:
        offset = 20
    
    selected_sources_param = request.GET.get('sources', '')
    lang_sources = SOURCES.get(language, SOURCES['en'])
    lang_default_sources = DEFAULT_SOURCES.get(language, DEFAULT_SOURCES['en'])
    lang_source_info = LANGUAGE_SOURCE_INFO.get(language, LANGUAGE_SOURCE_INFO['en'])
    
    if selected_sources_param == 'all':
        selected_sources = [s[0] for s in lang_sources]
    elif selected_sources_param in ['left', 'left-center', 'center', 'right-center', 'right']:
        selected_sources = [s[0] for s in lang_sources if s[1].lower() == selected_sources_param.lower()]
    elif selected_sources_param:
        selected_sources = selected_sources_param.split(',')
    else:
        # Default to ALL sources (same as sources=all)
        selected_sources = [s[0] for s in lang_sources]
    
    cutoff = timezone.now() - timedelta(hours=24)
    stories = list(Story.objects.filter(
        published__gte=cutoff,
        language=language,
        source__in=selected_sources
    ).only(
        'id', 'title', 'excerpt', 'url', 'source', 'published',
        'language', 'category', 'image_url', 'url_hash', 'title_fingerprint'
    ).order_by('-published'))
    
    # Filter by category
    if category_id != 'all' and category_id != 'most_covered':
        stories = [s for s in stories if category_id in get_story_categories(s.title, language, s.source)]
    
    total = len(stories)
    batch = stories[offset:offset + 50]
    
    story_data = []
    for story in batch:
        bias_info = lang_source_info.get(story.source, ('Unknown', '#999', ''))
        excerpt = story.get_clean_excerpt()
        story_data.append({
            'id': story.id,
            'title': story.title,
            'url': story.url,
            'source': story.source,
            'bias_label': bias_info[0],
            'bias_class': bias_info[0].lower().replace(' ', '-').replace('/', '-') if bias_info[0] else 'unknown',
            'is_paywalled': story.source in PAYWALLED_SOURCES,
            'covered_by_count': getattr(story, 'covered_by_count', None),
            'time_ago': f"{story.published.strftime('%H:%M')}",
            'excerpt': excerpt[:200] if excerpt else '',
            'image_url': story.image_url or '',
            'search_terms': story.get_search_terms(),
            'share_token': '',  # Will be generated in template if needed
        })
    
    # Fetch book recommendations for English categories
    book_data = []
    if language == 'en' and category_id != 'most_covered':
        from .models import RecommendedBook
        import random
        if category_id == 'all':
            cat_books = list(RecommendedBook.objects.filter(
                language='en', is_active=True
            ))
        else:
            cat_books = list(RecommendedBook.objects.filter(
                language='en', is_active=True, category=category_id
            ))
        if cat_books:
            random.shuffle(cat_books)
            for book in cat_books[:2]:
                book_data.append({
                    'title': book.title,
                    'author': book.author,
                    'description': book.description or '',
                    'image_url': book.image_url or '',
                    'amazon_url': book.amazon_url(),
                    'asin': book.asin,
                })
    
    # Include active poll for 'all' tab (at most one per loaded batch)
    poll_data = None
    if category_id == 'all':
        now = timezone.now()
        active_poll = Poll.objects.filter(
            language=language,
            is_active=True,
            status='active',
            ends_at__gt=now,
        ).order_by('?').first()
        if active_poll:
            poll_data = {
                'id': active_poll.id,
                'question': active_poll.question,
                'options': active_poll.options,
                'poll_type': active_poll.get_poll_type_display(),
                'vote_count': active_poll.vote_count,
            }
    
    return JsonResponse({
        'stories': story_data,
        'books': book_data,
        'poll': poll_data,
        'total': total,
        'has_more': offset + len(batch) < total,
    })


@condition(last_modified_func=_latest_story_timestamp)
@cache_page(300)  # 5 minutes — widget content changes with stories
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


def track_book_click(request):
    """Track book recommendation clicks via beacon API.
    
    Accepts POST requests with JSON body containing book ASIN.
    Records as an analytics event for aggregated reporting.
    """
    from django.http import JsonResponse
    if request.method == 'POST':
        try:
            import json
            body = json.loads(request.body.decode('utf-8'))
            asin = body.get('asin', '')
            if asin:
                country_code = request.META.get('HTTP_CF_IPCOUNTRY') or ''
                user_agent = request.META.get('HTTP_USER_AGENT', '')[:200]
                AnalyticsEvent.objects.create(
                    event_type='book_click',
                    path=f'/book/{asin}',
                    language=request.GET.get('lang', 'en')[:5],
                    country_code=country_code[:5],
                    user_agent=user_agent,
                    is_bot=False,  # Beacon API calls are always from real users
                )
        except Exception:
            pass
    return JsonResponse({'status': 'ok'})


@user_passes_test(is_staff_or_superuser, login_url='/login/')
def analytics_dashboard(request):
    """Analytics dashboard showing aggregated visitor data.
    
    No personal data displayed. Only aggregated counts and trends.
    """
    from django.db.models import Count
    from django.db import OperationalError, ProgrammingError
    
    # Check if AnalyticsEvent table exists
    try:
        AnalyticsEvent.objects.count()
    except (OperationalError, ProgrammingError) as e:
        return render(request, 'analytics_dashboard.html', {
            'error': f"Database table missing: {e}. Run: python manage.py migrate",
            'summary': {},
            'top_pages': [],
            'countries': [],
            'event_types': [],
            'languages': [],
            'hourly': [],
            'recent_events': [],
            'feed_access': 0,
            'widget_loads': 0,
            'shares': 0,
        })
    
    # Time ranges
    now = timezone.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday = today - timedelta(days=1)
    last_7_days = today - timedelta(days=7)
    last_30_days = today - timedelta(days=30)
    
    # Base queryset: exclude admin/dashboard/analytics pages
    base_qs = AnalyticsEvent.objects.exclude(
        path__startswith='/dashboard/'
    ).exclude(
        path__startswith='/analytics/'
    )
    
    # Summary stats (human only, excluding bots)
    human_qs = base_qs.filter(is_bot=False)
    summary = {
        'today': human_qs.filter(timestamp__gte=today).count(),
        'yesterday': human_qs.filter(timestamp__gte=yesterday, timestamp__lt=today).count(),
        'last_7_days': human_qs.filter(timestamp__gte=last_7_days).count(),
        'last_30_days': human_qs.filter(timestamp__gte=last_30_days).count(),
        'total': human_qs.count(),
    }
    
    # Bot detection stats
    bot_stats = {
        'today_bots': base_qs.filter(timestamp__gte=today, is_bot=True).count(),
        'today_human': summary['today'],
        'last_7_bots': base_qs.filter(timestamp__gte=last_7_days, is_bot=True).count(),
        'last_7_human': summary['last_7_days'],
    }
    
    # Top pages (last 7 days, human only)
    top_pages = human_qs.filter(
        timestamp__gte=last_7_days,
        event_type='page_view'
    ).values('path').annotate(
        count=Count('id')
    ).order_by('-count')[:20]
    
    # Geographic distribution (last 7 days, human only) with daily counts
    countries_7d = human_qs.filter(
        timestamp__gte=last_7_days,
        country_code__isnull=False
    ).exclude(country_code='').values('country_code').annotate(
        count_7d=Count('id')
    ).order_by('-count_7d')[:20]
    
    # Add today's count for each country
    countries = []
    for country in countries_7d:
        today_count = human_qs.filter(
            timestamp__gte=today,
            country_code=country['country_code']
        ).count()
        countries.append({
            'country_code': country['country_code'],
            'count_7d': country['count_7d'],
            'count_today': today_count,
        })
    
    # Event type breakdown (last 7 days, human only)
    event_types = human_qs.filter(
        timestamp__gte=last_7_days
    ).values('event_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Language distribution (last 7 days, human only)
    languages = human_qs.filter(
        timestamp__gte=last_7_days,
        language__isnull=False
    ).exclude(language='').values('language').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Hourly activity (last 24 hours, human only)
    hourly = []
    for i in range(24):
        hour_start = now - timedelta(hours=i+1)
        hour_end = now - timedelta(hours=i)
        count = human_qs.filter(
            timestamp__gte=hour_start,
            timestamp__lt=hour_end
        ).count()
        hourly.append({
            'hour': hour_end.strftime('%H:00'),
            'count': count
        })
    hourly.reverse()
    
    # Calculate bar heights as percentages
    max_hourly = max(h['count'] for h in hourly) if hourly else 0
    for h in hourly:
        h['percent'] = round((h['count'] / max_hourly * 100), 1) if max_hourly > 0 else 0
    
    # Recent events (last 50, human only, excluding admin)
    recent_events = human_qs[:50]
    
    # Feed access stats (last 7 days, all - bots can access feeds too)
    feed_access = base_qs.filter(
        timestamp__gte=last_7_days,
        event_type='feed_access'
    ).count()
    
    # Widget loads (last 7 days)
    widget_loads = base_qs.filter(
        timestamp__gte=last_7_days,
        event_type='widget_load'
    ).count()
    
    # Shares (last 7 days)
    shares = base_qs.filter(
        timestamp__gte=last_7_days,
        event_type='share'
    ).count()
    
    context = {
        'summary': summary,
        'bot_stats': bot_stats,
        'top_pages': top_pages,
        'countries': countries,
        'event_types': event_types,
        'languages': languages,
        'hourly': hourly,
        'recent_events': recent_events,
        'feed_access': feed_access,
        'widget_loads': widget_loads,
        'shares': shares,
    }
    
    return render(request, 'analytics_dashboard.html', context)


@cache_page(300)  # 5 minutes — topic content changes with new stories
def topic_detail(request, slug):
    """Display an evergreen topic hub page with live matching stories.
    
    Topic pages are indexable by search engines and aggregate stories
    from the last 24 hours that match the topic's keywords and categories.
    """
    from django.db.models import Count
    
    try:
        topic = Topic.objects.get(slug=slug, is_active=True)
    except Topic.DoesNotExist:
        raise Http404("Topic not found")
    
    # Get language filter from query param
    language = request.GET.get('lang')
    if language and language not in [s[0] for s in Story._meta.get_field('language').choices]:
        language = None
    
    # Fetch matching stories with metadata
    stories = topic.get_stories(language=language, limit=50)
    
    # Apply metadata
    lang_source_info = LANGUAGE_SOURCE_INFO.get('en', LANGUAGE_SOURCE_INFO.get('en', {}))
    for story in stories:
        story.story_categories = get_story_categories(story.title, story.language, story.source)
        bias_info = lang_source_info.get(story.source, ('Unknown', '#999', ''))
        story.bias_label = bias_info[0]
        story.bias_color = bias_info[1]
        story.bias_class = bias_info[0].lower().replace(' ', '-').replace('/', '-') if bias_info[0] else 'unknown'
        story.is_paywalled = story.source in PAYWALLED_SOURCES
    
    # Get languages with stories for filter pills
    languages_with_stories = topic.get_languages_with_stories()
    
    # Bias spectrum: count stories by bias
    # Keys normalized to use underscores (Django templates can't handle hyphens in variable names)
    bias_counts = {}
    for story in stories:
        bias = getattr(story, 'bias_label', 'Unknown')
        normalized_bias = bias.replace('-', '_').replace(' ', '_').lower()
        bias_counts[normalized_bias] = bias_counts.get(normalized_bias, 0) + 1
    
    # Total story count (uncapped for display)
    total_stories = topic.get_story_count(language=language)
    
    # Get translated headline/description for the selected language
    topic_translation = topic.get_translation(language or 'en')
    
    # Get UI strings
    ui_strings = UI_STRINGS.get('en', UI_STRINGS.get('en', {}))
    
    context = {
        'topic': topic,
        'topic_translation': topic_translation,
        'stories': stories,
        'language': language or 'all',
        'languages_with_stories': languages_with_stories,
        'bias_counts': bias_counts,
        'total_stories': total_stories,
        't': ui_strings,
        'language_names': LANGUAGE_NAMES,
    }
    
    return render(request, 'topic_detail.html', context)


@cache_page(60)  # 1 minute — votes change frequently
def poll_detail(request, poll_id):
    """Public poll page — works even for expired polls."""
    from django.http import JsonResponse
    
    poll = Poll.objects.filter(id=poll_id).first()
    if not poll:
        raise Http404("Poll not found")
    
    # Determine if voting is open
    now = timezone.now()
    can_vote = (
        poll.is_active and
        poll.status == 'active' and
        (poll.ends_at is None or poll.ends_at > now)
    )
    
    has_voted = poll.has_voted(request) if can_vote else False
    results = poll.get_results_display()
    
    # Track poll view analytics
    if request.method == 'GET' and not request.headers.get('X-Requested-With'):
        AnalyticsEvent.objects.create(
            event_type='poll_view',
            path=f'/poll/{poll.id}/',
            language=poll.language,
        )
    
    # Handle AJAX vote
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if not can_vote:
            return JsonResponse({'error': 'Poll is closed'}, status=403)
        
        try:
            option_index = int(request.POST.get('option'))
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid option'}, status=400)
        
        if option_index < 0 or option_index >= len(poll.options):
            return JsonResponse({'error': 'Invalid option'}, status=400)
        
        success = poll.record_vote(option_index, request)
        if not success:
            return JsonResponse({'error': 'Already voted'}, status=409)
        
        # Also track in AnalyticsEvent
        AnalyticsEvent.objects.create(
            event_type='poll_vote',
            path=f'/poll/{poll.id}/',
            language=poll.language,
        )
        
        return JsonResponse({
            'success': True,
            'results': poll.get_results_display(),
            'vote_count': poll.vote_count,
        })
    
    # Get user's preferred language for navigation links
    language = request.GET.get('lang', getattr(request, 'detected_language', 'en'))
    if language not in SOURCES:
        language = 'en'
    
    context = {
        'poll': poll,
        'can_vote': can_vote,
        'has_voted': has_voted,
        'results': results,
        'is_expired': poll.ends_at and poll.ends_at <= now,
        'language': language,
    }
    return render(request, 'poll_detail.html', context)


@cache_page(60)  # 1 minute — poll list changes when new polls activate
def polls_list(request):
    """Public polls listing page — current active polls only."""
    now = timezone.now()
    language = request.GET.get('lang', getattr(request, 'detected_language', 'en'))
    if language not in SOURCES:
        language = 'en'
    language_filter = request.GET.get('lang', '')
    
    # Active polls (current)
    active_polls = Poll.objects.filter(
        is_active=True,
        status='active',
        ends_at__gt=now,
    ).order_by('-created_at')
    
    if language_filter:
        active_polls = active_polls.filter(language=language_filter)
    
    # For each active poll, check if user has voted
    for poll in active_polls:
        poll.user_has_voted = poll.has_voted(request)
        poll.results_display = poll.get_results_display()
    
    context = {
        'active_polls': active_polls,
        'language_filter': language_filter,
        'languages': LANGUAGE_NAMES,
        'language': language,
    }
    return render(request, 'polls_list.html', context)


@cache_page(600)  # 10 minutes — archive rarely changes
def polls_archive(request):
    """Archive page for closed polls (expired only, not rejected)."""
    now = timezone.now()
    language = request.GET.get('lang', getattr(request, 'detected_language', 'en'))
    if language not in SOURCES:
        language = 'en'
    language_filter = request.GET.get('lang', '')
    
    # Expired polls only (not rejected)
    closed_polls = Poll.objects.filter(
        status='expired',
    ).order_by('-ends_at')
    
    if language_filter:
        closed_polls = closed_polls.filter(language=language_filter)
    
    for poll in closed_polls:
        poll.results_display = poll.get_results_display()
    
    context = {
        'closed_polls': closed_polls,
        'language_filter': language_filter,
        'languages': LANGUAGE_NAMES,
        'language': language,
    }
    return render(request, 'polls_archive.html', context)


@user_passes_test(is_staff_or_superuser, login_url='/login/')
def polls_manage(request):
    """Staff-only poll review and management page."""
    status_filter = request.GET.get('status', 'pending_review')
    language_filter = request.GET.get('language', '')
    language = request.GET.get('lang', getattr(request, 'detected_language', 'en'))
    if language not in SOURCES:
        language = 'en'
    
    polls = Poll.objects.all().order_by('-created_at')
    
    if status_filter:
        polls = polls.filter(status=status_filter)
    if language_filter:
        polls = polls.filter(language=language_filter)
    
    # Handle actions
    if request.method == 'POST':
        action = request.POST.get('action')
        poll_id = request.POST.get('poll_id')
        
        if action == 'create_manual':
            # Manual poll creation by staff
            q = request.POST.get('question', '').strip()
            options_raw = request.POST.get('options', '').strip()
            poll_lang = request.POST.get('language', 'en')
            poll_type = request.POST.get('poll_type', 'topical')
            english_translation = request.POST.get('english_translation', '').strip()
            ends_at_str = request.POST.get('ends_at', '')
            
            if not q or not options_raw:
                messages.error(request, 'Question and options are required.')
            else:
                options = [opt.strip() for opt in options_raw.split('\n') if opt.strip()]
                if len(options) < 2:
                    messages.error(request, 'At least 2 options are required.')
                else:
                    ends_at = timezone.now() + timedelta(days=14)
                    if ends_at_str:
                        from datetime import datetime
                        ends_at = datetime.fromisoformat(ends_at_str.replace('Z', '+00:00'))
                    
                    if poll_lang == 'en':
                        english_translation = q
                    
                    Poll.objects.create(
                        language=poll_lang,
                        question=q,
                        options=options,
                        poll_type=poll_type,
                        english_translation=english_translation or q,
                        status='pending_review',
                        is_active=False,
                        ends_at=ends_at,
                        source='manual',
                    )
                    messages.success(request, f'Created poll: {q[:50]}...')
        
        elif action == 'generate_now':
            # Trigger OpenAI generation immediately
            import os
            from io import StringIO
            from django.core.management import call_command
            
            out = StringIO()
            try:
                call_command('generate_polls', '--language', language, '--num', '3', stdout=out, stderr=out)
                output = out.getvalue()
                if 'Created' in output:
                    created = output.count('Created:')
                    messages.success(request, f'OpenAI generation complete. {created} polls created. Check pending review.')
                elif 'DRY RUN' in output:
                    messages.warning(request, 'Dry run detected — no polls created.')
                elif 'disabled' in output.lower():
                    messages.warning(request, 'Auto-generation is disabled in config.')
                elif 'OPENAI_API_KEY' in output:
                    messages.error(request, 'OPENAI_API_KEY is not set. Add it in Render environment variables.')
                else:
                    messages.info(request, f'Generation output: {output[:200]}')
            except Exception as e:
                messages.error(request, f'Generation failed: {e}')
        
        elif poll_id and action:
            poll = Poll.objects.filter(id=poll_id).first()
            if poll:
                if action == 'activate':
                    poll.status = 'active'
                    poll.is_active = True
                    if not poll.starts_at:
                        poll.starts_at = timezone.now()
                    poll.save()
                    messages.success(request, f'Activated: {poll.question[:50]}')
                elif action == 'reject':
                    poll.status = 'rejected'
                    poll.is_active = False
                    poll.save()
                    messages.success(request, f'Rejected: {poll.question[:50]}')
                elif action == 'expire':
                    poll.status = 'expired'
                    poll.is_active = False
                    poll.ends_at = timezone.now()
                    poll.save()
                    messages.success(request, f'Expired: {poll.question[:50]}')
                elif action == 'update':
                    poll.question = request.POST.get('question', poll.question)
                    poll.english_translation = request.POST.get('english_translation', poll.english_translation)
                    poll.poll_type = request.POST.get('poll_type', poll.poll_type)
                    # Parse options from textarea (one per line)
                    options_raw = request.POST.get('options', '')
                    if options_raw:
                        poll.options = [opt.strip() for opt in options_raw.split('\n') if opt.strip()]
                    # Parse ends_at
                    ends_at_str = request.POST.get('ends_at', '')
                    if ends_at_str:
                        from datetime import datetime
                        poll.ends_at = datetime.fromisoformat(ends_at_str.replace('Z', '+00:00'))
                    poll.save()
                    messages.success(request, f'Updated: {poll.question[:50]}')
                elif action == 'update_config':
                    config = PollGenerationConfig.get_active_config()
                    try:
                        config.frequency_hours = int(request.POST.get('frequency_hours', config.frequency_hours))
                        config.polls_per_language = int(request.POST.get('polls_per_language', config.polls_per_language))
                        config.is_enabled = request.POST.get('is_enabled') == 'on'
                        config.save()
                        messages.success(request, 'Generation config updated.')
                    except (ValueError, TypeError):
                        messages.error(request, 'Invalid config values.')
        
        return redirect(f'/polls/manage/?status={status_filter}&language={language_filter}')
    
    # Pagination
    from django.core.paginator import Paginator
    paginator = Paginator(polls, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    # Generation config
    gen_config = PollGenerationConfig.get_active_config()
    
    context = {
        'polls': page_obj,
        'page_obj': page_obj,
        'paginator': paginator,
        'status_filter': status_filter,
        'language_filter': language_filter,
        'languages': LANGUAGE_NAMES,
        'poll_types': Poll.POLL_TYPE_CHOICES,
        'statuses': Poll.STATUS_CHOICES,
        'gen_config': gen_config,
        'language': language,
    }
    return render(request, 'polls_manage.html', context)


def poll_vote_api(request, poll_id):
    """Standalone API endpoint for voting (used by feed inline polls)."""
    from django.http import JsonResponse
    
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    poll = Poll.objects.filter(id=poll_id).first()
    if not poll:
        return JsonResponse({'error': 'Poll not found'}, status=404)
    
    now = timezone.now()
    can_vote = (
        poll.is_active and
        poll.status == 'active' and
        (poll.ends_at is None or poll.ends_at > now)
    )
    
    if not can_vote:
        return JsonResponse({'error': 'Poll is closed'}, status=403)
    
    try:
        option_index = int(request.POST.get('option'))
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid option'}, status=400)
    
    if option_index < 0 or option_index >= len(poll.options):
        return JsonResponse({'error': 'Invalid option'}, status=400)
    
    success = poll.record_vote(option_index, request)
    if not success:
        return JsonResponse({'error': 'Already voted'}, status=409)
    
    AnalyticsEvent.objects.create(
        event_type='poll_vote',
        path=f'/poll/{poll.id}/',
        language=poll.language,
    )
    
    return JsonResponse({
        'success': True,
        'results': poll.get_results_display(),
        'vote_count': poll.vote_count,
    })
