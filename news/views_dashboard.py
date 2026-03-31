from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from news.models import Story, StoryCluster
from news.sources_config import LANGUAGE_FEEDS, LANGUAGE_NAMES, SOURCES


def dashboard_view(request):
    cutoff = timezone.now() - timedelta(hours=24)

    # Story counts per language
    story_counts = {}
    for lang in sorted(LANGUAGE_FEEDS.keys()):
        story_counts[lang] = {
            'name': LANGUAGE_NAMES.get(lang, lang),
            'total': Story.objects.filter(language=lang).count(),
            'recent': Story.objects.filter(language=lang, published__gte=cutoff).count(),
            'clusters': StoryCluster.objects.filter(language=lang).count(),
            'sources': len(SOURCES.get(lang, [])),
            'feeds': len(LANGUAGE_FEEDS.get(lang, [])),
        }

    # Summary
    total_feeds = sum(len(feeds) for feeds in LANGUAGE_FEEDS.values())
    
    # Get latest story info
    last_import = Story.objects.order_by('-fetched_at').first()
    newest_story = Story.objects.order_by('-published').first()
    
    # Time since last import
    if last_import:
        time_since_import = timezone.now() - last_import.fetched_at
        hours_since_import = time_since_import.total_seconds() / 3600
    else:
        hours_since_import = None

    return render(request, 'dashboard.html', {
        'story_counts': story_counts,
        'total_stories': Story.objects.count(),
        'total_clusters': StoryCluster.objects.count(),
        'total_feeds': total_feeds,
        'now': timezone.now(),
        'last_import': last_import,
        'newest_story': newest_story,
        'hours_since_import': hours_since_import,
    })