"""
RSS Feeds for 24HourWire news aggregator.

Feed URLs:
- /feed/ - Global feed (all languages)
- /feed/<language>/ - Language-specific feed
- /feed/<language>/<category>/ - Category-specific feed
"""

from django.contrib.syndication.views import Feed
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed

from .models import Story
from .languages import LANGUAGE_NAMES


class ExtendedRSSFeed(Rss201rev2Feed):
    """Extended RSS feed with additional elements."""
    
    def add_item_elements(self, handler, item):
        super().add_item_elements(handler, item)
        # Add source as category
        if item.get('source'):
            handler.addQuickElement('category', item['source'])
        # Add language
        if item.get('language'):
            handler.addQuickElement('language', item['language'])


class GlobalFeed(Feed):
    """Global RSS feed - all stories from all languages."""
    feed_type = ExtendedRSSFeed
    title = "24HourWire - Global News Feed"
    link = "/"
    description = "News from all angles, all languages. Updated every 15 minutes with fresh perspectives from around the world."
    
    def items(self):
        """Return stories from last 24 hours."""
        cutoff = timezone.now() - timedelta(hours=24)
        return Story.objects.filter(
            published__gte=cutoff
        ).order_by('-published')[:100]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        excerpt = item.get_clean_excerpt()
        if excerpt:
            return f"{excerpt}\n\nSource: {item.source} | Curated by 24HourWire"
        return f"Source: {item.source} | Curated by 24HourWire"
    
    def item_link(self, item):
        # Link to original article
        return item.url
    
    def item_pubdate(self, item):
        return item.published
    
    def item_guid(self, item):
        # Use URL as unique identifier
        return item.url
    
    def item_extra_kwargs(self, item):
        return {
            'source': item.source,
            'language': item.language,
        }
    
    def item_categories(self, item):
        """Return story category and source as categories."""
        cats = [item.source]
        if item.category:
            cats.append(item.category.replace('-', ' ').title())
        return cats


class LanguageFeed(Feed):
    """Language-specific RSS feed."""
    feed_type = ExtendedRSSFeed
    
    def get_object(self, request, language):
        """Validate language parameter."""
        if language not in dict(Story.LANGUAGE_CHOICES):
            from django.http import Http404
            raise Http404(f"Language '{language}' not supported")
        return language
    
    def title(self, obj):
        lang_name = LANGUAGE_NAMES.get(obj, obj.upper())
        return f"24HourWire - {lang_name} News Feed"
    
    def link(self, obj):
        return f"/?lang={obj}"
    
    def description(self, obj):
        lang_name = LANGUAGE_NAMES.get(obj, obj.upper())
        return f"News from all angles in {lang_name}. Updated every 15 minutes."
    
    def items(self, obj):
        """Return stories for specific language from last 24 hours."""
        cutoff = timezone.now() - timedelta(hours=24)
        return Story.objects.filter(
            language=obj,
            published__gte=cutoff
        ).order_by('-published')[:100]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        excerpt = item.get_clean_excerpt()
        if excerpt:
            return f"{excerpt}\n\nSource: {item.source} | Curated by 24HourWire"
        return f"Source: {item.source} | Curated by 24HourWire"
    
    def item_link(self, item):
        return item.url
    
    def item_pubdate(self, item):
        return item.published
    
    def item_guid(self, item):
        return item.url
    
    def item_extra_kwargs(self, item):
        return {
            'source': item.source,
            'language': item.language,
        }
    
    def item_categories(self, item):
        cats = [item.source]
        if item.category:
            cats.append(item.category.replace('-', ' ').title())
        return cats


class CategoryFeed(Feed):
    """Category-specific RSS feed (within a language)."""
    feed_type = ExtendedRSSFeed
    
    def get_object(self, request, language, category):
        """Validate language and category."""
        if language not in dict(Story.LANGUAGE_CHOICES):
            from django.http import Http404
            raise Http404(f"Language '{language}' not supported")
        return {'language': language, 'category': category}
    
    def title(self, obj):
        lang_name = LANGUAGE_NAMES.get(obj['language'], obj['language'].upper())
        cat_name = obj['category'].replace('-', ' ').title()
        return f"24HourWire - {lang_name} {cat_name} News"
    
    def link(self, obj):
        return f"/?lang={obj['language']}"
    
    def description(self, obj):
        lang_name = LANGUAGE_NAMES.get(obj['language'], obj['language'].upper())
        cat_name = obj['category'].replace('-', ' ').title()
        return f"{cat_name} news from all angles in {lang_name}."
    
    def items(self, obj):
        """Return stories for specific language and category."""
        cutoff = timezone.now() - timedelta(hours=24)
        return Story.objects.filter(
            language=obj['language'],
            category=obj['category'],
            published__gte=cutoff
        ).order_by('-published')[:50]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        excerpt = item.get_clean_excerpt()
        if excerpt:
            return f"{excerpt}\n\nSource: {item.source} | Curated by 24HourWire"
        return f"Source: {item.source} | Curated by 24HourWire"
    
    def item_link(self, item):
        return item.url
    
    def item_pubdate(self, item):
        return item.published
    
    def item_guid(self, item):
        return item.url
    
    def item_extra_kwargs(self, item):
        return {
            'source': item.source,
            'language': item.language,
        }
    
    def item_categories(self, item):
        return [item.source]


# JSON Feed support for modern readers
from django.http import JsonResponse
from django.views import View


class JSONFeedView(View):
    """JSON Feed (https://jsonfeed.org/) for modern RSS readers."""
    
    def get(self, request, language=None, category=None):
        """Generate JSON feed."""
        cutoff = timezone.now() - timedelta(hours=24)
        stories = Story.objects.filter(published__gte=cutoff)
        
        if language:
            stories = stories.filter(language=language)
        if category:
            stories = stories.filter(category=category)
        
        stories = stories.order_by('-published')[:100]
        
        items = []
        for story in stories:
            excerpt = story.get_clean_excerpt()
            items.append({
                'id': story.url,
                'url': story.url,
                'title': story.title,
                'content_text': excerpt if excerpt else story.title,
                'date_published': story.published.isoformat(),
                'author': {
                    'name': story.source,
                },
                'tags': [story.category] if story.category else [],
                'language': story.language,
            })
        
        feed = {
            'version': 'https://jsonfeed.org/version/1.1',
            'title': '24HourWire News Feed',
            'home_page_url': 'https://24hourwire.com',
            'feed_url': request.build_absolute_uri(),
            'description': 'News from all angles',
            'items': items,
        }
        
        return JsonResponse(feed)
