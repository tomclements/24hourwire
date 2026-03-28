from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from news.models import Story, StoryCluster
from news.sources_config import LANGUAGE_FEEDS, LANGUAGE_NAMES, SOURCES
import feedparser
import urllib.request
import ssl


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

    # Feed health — refresh if requested or cache expired
    cache_key = 'feed_health'
    cache_time_key = 'feed_health_time'
    cached_time = request.session.get(cache_time_key)
    force_refresh = request.method == 'POST' and request.GET.get('refresh')

    if force_refresh or not cached_time or (timezone.now().timestamp() - cached_time) > 3600:
        feed_health = _check_all_feeds()
        request.session[cache_key] = feed_health
        request.session[cache_time_key] = timezone.now().timestamp()
    else:
        feed_health = request.session[cache_key]

    # Summary
    total_feeds = sum(len(feeds) for feeds in LANGUAGE_FEEDS.values())
    healthy = sum(1 for f in feed_health if f['status'] == 'ok')
    empty = sum(1 for f in feed_health if f['status'] == 'empty')
    errors = sum(1 for f in feed_health if f['status'] not in ('ok', 'empty'))

    broken_feeds = [f for f in feed_health if f['status'] != 'ok']

    return render(request, 'dashboard.html', {
        'story_counts': story_counts,
        'feed_health': feed_health,
        'broken_feeds': broken_feeds,
        'total_stories': Story.objects.count(),
        'total_clusters': StoryCluster.objects.count(),
        'total_feeds': total_feeds,
        'healthy': healthy,
        'empty': empty,
        'errors': errors,
        'now': timezone.now(),
    })


def _check_all_feeds():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    results = []
    for language, feeds in sorted(LANGUAGE_FEEDS.items()):
        for source_name, feed_url in feeds:
            try:
                req = urllib.request.Request(feed_url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                with urllib.request.urlopen(req, context=ctx, timeout=10) as response:
                    try:
                        feed = feedparser.parse(response.read())
                        if feed.entries:
                            results.append({
                                'language': language,
                                'source': source_name,
                                'status': 'ok',
                                'entries': len(feed.entries),
                            })
                        else:
                            results.append({
                                'language': language,
                                'source': source_name,
                                'status': 'empty',
                                'entries': 0,
                            })
                    except Exception as parse_error:
                        results.append({
                            'language': language,
                            'source': source_name,
                            'status': f'parse_error',
                            'entries': 0,
                        })
            except Exception as e:
                results.append({
                    'language': language,
                    'source': source_name,
                    'status': 'error',
                    'entries': 0,
                })

    return results
