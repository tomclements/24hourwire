from django.shortcuts import render, redirect
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


def is_staff_or_superuser(user):
    """Check if user is staff or superuser."""
    return user.is_staff or user.is_superuser


def categorize_story(title, language='en'):
    title_lower = title.lower()
    keywords = CATEGORY_KEYWORDS.get(language, CATEGORY_KEYWORDS['en'])

    for keyword in keywords['sports']:
        if keyword in title_lower:
            return 'sports'

    for keyword in keywords['health']:
        if keyword in title_lower:
            return 'health'

    for keyword in keywords['technology']:
        if keyword in title_lower:
            return 'technology'

    for keyword in keywords['science']:
        if keyword in title_lower:
            return 'science'

    for keyword in keywords['entertainment']:
        if keyword in title_lower:
            return 'entertainment'

    for keyword in keywords['business']:
        if keyword in title_lower:
            return 'business'

    for keyword in keywords['politics']:
        if keyword in title_lower:
            return 'politics'

    for keyword in keywords['us']:
        if keyword in title_lower:
            return 'us'

    for keyword in keywords['world']:
        if keyword in title_lower:
            return 'world'

    return 'world'


def get_story_categories(title, language='en'):
    title_lower = title.lower()
    categories = []
    keywords = CATEGORY_KEYWORDS.get(language, CATEGORY_KEYWORDS['en'])

    for cat in ['sports', 'health', 'technology', 'science', 'entertainment', 'business', 'politics', 'us', 'world']:
        for keyword in keywords[cat]:
            if keyword in title_lower:
                categories.append(cat)
                break

    if not categories:
        categories = ['world']

    return categories




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


def different_angle(request, story_id):
    """Show related stories with different bias for a given story."""
    from django.http import JsonResponse
    import json
    
    try:
        story = Story.objects.get(id=story_id)
    except Story.DoesNotExist:
        return JsonResponse({'error': 'Story not found'}, status=404)
    
    # Get story's bias
    language = story.language
    lang_source_info = LANGUAGE_SOURCE_INFO.get(language, LANGUAGE_SOURCE_INFO['en'])
    story_bias = lang_source_info.get(story.source, ('Unknown', '#999', ''))[0]
    
    # Find opposite biases
    bias_order = ['Left', 'Left-Center', 'Center', 'Right-Center', 'Right']
    opposite_biases = []
    if story_bias in bias_order:
        story_idx = bias_order.index(story_bias)
        # Get biases that are different (prioritize farther ones)
        for i, bias in enumerate(bias_order):
            if bias != story_bias:
                opposite_biases.append(bias)
    
    # Get search terms from story title
    search_terms = story.get_search_terms().split('+')
    
    # Find related stories from different biases
    cutoff = timezone.now() - timedelta(hours=48)  # Wider time window
    related_stories = []
    
    all_recent_stories = Story.objects.filter(
        published__gte=cutoff,
        language=language
    ).exclude(id=story_id)
    
    for related in all_recent_stories:
        related_bias = lang_source_info.get(related.source, ('Unknown', '#999', ''))[0]
        if related_bias not in opposite_biases:
            continue
            
        # Check for keyword overlap
        related_title_lower = related.title.lower()
        match_score = 0
        for term in search_terms:
            if term.lower() in related_title_lower:
                match_score += 1
        
        # Include if at least 2 keywords match or high similarity
        if match_score >= 2 or match_score >= len(search_terms) * 0.5:
            bias_info = lang_source_info.get(related.source, ('Unknown', '#999', ''))
            related.bias_label = bias_info[0]
            related.bias_color = bias_info[1]
            related.is_paywalled = related.source in PAYWALLED_SOURCES
            related.story_categories = get_story_categories(related.title, language)
            related.match_score = match_score
            related_stories.append(related)
    
    # Sort by match score (highest first) then by published date
    related_stories.sort(key=lambda x: (-x.match_score, x.published), reverse=False)
    
    # Limit to top 10
    related_stories = related_stories[:10]
    
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
