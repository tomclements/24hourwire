from django.shortcuts import render, redirect
from django.core import signing
from django.http import Http404, HttpResponse
from django.utils import timezone
from django.views.decorators.cache import cache_page
from datetime import timedelta
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Story, StoryCluster, AnalyticsEvent
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
    
    # PERFORMANCE: Filter by source in DB, then process in Python
    stories = list(Story.objects.filter(
        published__gte=cutoff,
        language=language,
        source__in=selected_sources
    ).order_by('-published'))
    
    # Apply metadata to displayed stories only
    for story in stories:
        story.story_categories = get_story_categories(story.title, language)
        bias_info = lang_source_info.get(story.source, ('Unknown', '#999', 'https://mediabiasfactcheck.com/'))
        story.bias_label = bias_info[0]
        story.bias_color = bias_info[1]
        story.bias_link = bias_info[2]
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
        rep.story_categories = get_story_categories(rep.title, language)
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
    
    grouped = {}
    for cat_id, cat_name in category_names.items():
        if cat_id == 'all':
            cat_stories = list(stories)
        elif cat_id == 'most_covered':
            cat_stories = most_covered_stories
        else:
            cat_stories = [s for s in stories if cat_id in s.story_categories]
        
        # Get books for this category (randomize order)
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


def robots_txt(request):
    """Serve robots.txt dynamically."""
    content = """User-agent: *
Allow: /
Disallow: /dashboard/
Disallow: /login/

# Allow social media crawlers to access share pages for card generation
User-agent: Twitterbot
Allow: /go/

User-agent: facebookexternalhit
Allow: /go/

User-agent: LinkedInBot
Allow: /go/

Sitemap: https://24hourwire.news/sitemap.xml
Sitemap: https://24hourwire.news/news-sitemap.xml

Crawl-delay: 1
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
        selected_sources = lang_default_sources
    
    cutoff = timezone.now() - timedelta(hours=24)
    stories = list(Story.objects.filter(
        published__gte=cutoff,
        language=language,
        source__in=selected_sources
    ).order_by('-published'))
    
    # Filter by category
    if category_id != 'all' and category_id != 'most_covered':
        stories = [s for s in stories if category_id in get_story_categories(s.title, language)]
    
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
    
    return JsonResponse({
        'stories': story_data,
        'books': book_data,
        'total': total,
        'has_more': offset + len(batch) < total,
    })


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
    
    # Summary stats
    summary = {
        'today': AnalyticsEvent.objects.filter(timestamp__gte=today).count(),
        'yesterday': AnalyticsEvent.objects.filter(timestamp__gte=yesterday, timestamp__lt=today).count(),
        'last_7_days': AnalyticsEvent.objects.filter(timestamp__gte=last_7_days).count(),
        'last_30_days': AnalyticsEvent.objects.filter(timestamp__gte=last_30_days).count(),
        'total': AnalyticsEvent.objects.count(),
    }
    
    # Top pages (last 7 days)
    top_pages = AnalyticsEvent.objects.filter(
        timestamp__gte=last_7_days,
        event_type='page_view'
    ).values('path').annotate(
        count=Count('id')
    ).order_by('-count')[:20]
    
    # Geographic distribution (last 7 days)
    countries = AnalyticsEvent.objects.filter(
        timestamp__gte=last_7_days,
        country_code__isnull=False
    ).exclude(country_code='').values('country_code').annotate(
        count=Count('id')
    ).order_by('-count')[:20]
    
    # Event type breakdown (last 7 days)
    event_types = AnalyticsEvent.objects.filter(
        timestamp__gte=last_7_days
    ).values('event_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Language distribution (last 7 days)
    languages = AnalyticsEvent.objects.filter(
        timestamp__gte=last_7_days,
        language__isnull=False
    ).exclude(language='').values('language').annotate(
        count=Count('id')
    ).order_by('-count')[:10]
    
    # Hourly activity (last 24 hours)
    hourly = []
    for i in range(24):
        hour_start = now - timedelta(hours=i+1)
        hour_end = now - timedelta(hours=i)
        count = AnalyticsEvent.objects.filter(
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
    
    # Recent events (last 50)
    recent_events = AnalyticsEvent.objects.all()[:50]
    
    # Feed access stats (last 7 days)
    feed_access = AnalyticsEvent.objects.filter(
        timestamp__gte=last_7_days,
        event_type='feed_access'
    ).count()
    
    # Widget loads (last 7 days)
    widget_loads = AnalyticsEvent.objects.filter(
        timestamp__gte=last_7_days,
        event_type='widget_load'
    ).count()
    
    # Shares (last 7 days)
    shares = AnalyticsEvent.objects.filter(
        timestamp__gte=last_7_days,
        event_type='share'
    ).count()
    
    context = {
        'summary': summary,
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
