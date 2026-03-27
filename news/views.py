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
        selected_sources = selected_sources_param.split(',')
    else:
        selected_sources = lang_default_sources
    
    all_stories = list(Story.objects.filter(published__gte=cutoff, language=language))
    
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
