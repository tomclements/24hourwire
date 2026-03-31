from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from news.models import Story, StoryCluster, build_clusters
from news.sources_config import LANGUAGE_FEEDS, LANGUAGE_NAMES, SOURCES


def dashboard_view(request):
    cutoff = timezone.now() - timedelta(hours=24)

    # Handle rebuild clusters request
    if request.method == 'POST' and request.POST.get('action') == 'rebuild_clusters':
        if request.user.is_staff:
            total_clusters = 0
            for lang in LANGUAGE_FEEDS.keys():
                try:
                    count = build_clusters(lang)
                    total_clusters += count
                except Exception as e:
                    messages.error(request, f'Error building clusters for {lang}: {e}')
            messages.success(request, f'Rebuilt {total_clusters} clusters')
            return redirect('/dashboard/')
    
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
    
    # Get latest cluster info
    latest_cluster = StoryCluster.objects.order_by('-created_at').first()
    recent_clusters = StoryCluster.objects.filter(
        created_at__gte=timezone.now() - timedelta(hours=24)
    ).count()

    return render(request, 'dashboard.html', {
        'story_counts': story_counts,
        'total_stories': Story.objects.count(),
        'total_clusters': StoryCluster.objects.count(),
        'total_feeds': total_feeds,
        'now': timezone.now(),
        'last_import': last_import,
        'newest_story': newest_story,
        'hours_since_import': hours_since_import,
        'latest_cluster': latest_cluster,
        'recent_clusters': recent_clusters,
        'user': request.user,
    })