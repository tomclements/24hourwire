from django.shortcuts import render, redirect
from django.core import signing
from django.http import Http404
from django.utils import timezone
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
    
    if not url:
        raise Http404("Invalid link")
    
    return render(request, 'branded_redirect.html', {
        'url': url,
        'title': title,
        'source': source,
        'token': token,
    })


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
