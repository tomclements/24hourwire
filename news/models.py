import hashlib
import re
from urllib.parse import urlparse, parse_qs, urlencode

from django.db import models


# Pre-compile regex patterns for excerpt cleaning
GOOGLE_NEWS_URL_PATTERN = re.compile(r'<a\s+href="https?://news\.google\.com/rss/articles/[^"]*"[^>]*>.*?</a>', re.IGNORECASE | re.DOTALL)
HTML_TAG_PATTERN = re.compile(r'<[^>]+>')
URL_PATTERN = re.compile(r'https?://\S+')
WHITESPACE_PATTERN = re.compile(r'\s+')


def normalize_url(url):
    """Normalize URL for dedup comparison - strips tracking params, normalizes scheme."""
    parsed = urlparse(url)
    drop_params = {'utm_source', 'utm_medium', 'utm_campaign', 'ref', 'source'}
    params = {k: v for k, v in parse_qs(parsed.query).items()
              if k.lower() not in drop_params}
    normalized = parsed._replace(
        scheme='https',
        netloc=parsed.netloc.lower(),
        query=urlencode(params, doseq=True),
        fragment='',
        path=parsed.path.rstrip('/') or '/',
    )
    return normalized.geturl()


def title_fingerprint(title):
    """Create a normalized fingerprint for same-source duplicate detection."""
    normalized = re.sub(r'[^\w\s]', '', title.lower())
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    words = sorted(normalized.split())
    return hashlib.md5(' '.join(words).encode()).hexdigest()


class Story(models.Model):
    CATEGORY_CHOICES = [
        ('world', 'World'),
        ('us', 'US'),
        ('politics', 'Politics'),
        ('business', 'Business'),
        ('technology', 'Technology'),
        ('science', 'Science'),
        ('health', 'Health'),
        ('sports', 'Sports'),
        ('entertainment', 'Entertainment'),
    ]

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Español'),
    ]

    source = models.CharField(max_length=50)
    title = models.CharField(max_length=500)
    excerpt = models.TextField(blank=True)
    url = models.URLField(unique=True, max_length=2000)
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='world')
    published = models.DateTimeField()
    fetched_at = models.DateTimeField(auto_now_add=True)
    url_hash = models.CharField(max_length=64, db_index=True, default='')
    title_fingerprint = models.CharField(max_length=32, db_index=True, default='')
    tweeted = models.BooleanField(default=False, db_index=True)
    image_url = models.URLField(max_length=2000, blank=True)

    class Meta:
        ordering = ['-published']
        indexes = [
            models.Index(fields=['language', 'published']),
            models.Index(fields=['source', 'language']),
            models.Index(fields=['language', 'published', 'source']),
            models.Index(fields=['language', 'published', 'category']),
        ]

    def __str__(self):
        return f"{self.source}: {self.title[:50]}"

    def get_search_terms(self):
        from news.sources_config import LANGUAGE_STOP_WORDS
        stop_words = LANGUAGE_STOP_WORDS.get(self.language, LANGUAGE_STOP_WORDS['en'])
        words = self.title.lower().split()
        clean = [w for w in words if w not in stop_words and len(w) > 2][:5]
        return "+".join(clean)

    def get_clean_excerpt(self):
        from news.sources_config import SOURCE_ATTRIBUTION, GENERIC_TEXT
        if not self.excerpt:
            return ''
        
        text = self.excerpt
        
        # Remove Google News RSS reference URLs (e.g., <a href="https://news.google.com/rss/articles/CBMi2...")
        text = GOOGLE_NEWS_URL_PATTERN.sub(' ', text)
        
        # Remove all HTML tags more aggressively
        text = HTML_TAG_PATTERN.sub(' ', text)
        
        # Remove URLs that might be left over
        text = URL_PATTERN.sub(' ', text)
        
        # Remove source attribution at end
        attribution = SOURCE_ATTRIBUTION.get(self.language, SOURCE_ATTRIBUTION['en'])
        text = re.sub(attribution, '', text, flags=re.IGNORECASE)
        
        # Decode HTML entities
        text = re.sub(r'&nbsp;', ' ', text)
        text = re.sub(r'&amp;', '&', text)
        text = re.sub(r'&lt;', '<', text)
        text = re.sub(r'&gt;', '>', text)
        text = re.sub(r'&#39;', "'", text)
        text = re.sub(r'&#8217;', "'", text)  # Right single quotation mark
        text = re.sub(r'&#8216;', "'", text)  # Left single quotation mark
        text = re.sub(r'&#8220;', '"', text)  # Left double quotation mark
        text = re.sub(r'&#8221;', '"', text)  # Right double quotation mark
        text = re.sub(r'&#8230;', '...', text)  # Ellipsis
        text = re.sub(r'&#8211;', '-', text)  # En dash
        text = re.sub(r'&#8212;', '--', text)  # Em dash
        text = re.sub(r'&quot;', '"', text)
        text = re.sub(r'&#[0-9]+;', '', text)  # Remove any remaining numeric entities
        text = re.sub(r'&[a-zA-Z0-9]+;', '', text)  # Remove any remaining named entities
        
        # Clean up whitespace
        text = WHITESPACE_PATTERN.sub(' ', text).strip()
        
        # Filter out generic text
        generic = GENERIC_TEXT.get(self.language, GENERIC_TEXT['en'])
        if any(g in text.lower() for g in generic):
            return ''
        
        # Filter out if too similar to title
        title_lower = self.title.lower()
        text_lower = text.lower()
        if text_lower == title_lower:
            return ''
        if len(text) > 10 and text_lower in title_lower:
            return ''
        if len(title_lower) > 10 and title_lower in text_lower:
            return ''
        if len(text) > 30:
            return text
        return ''


class StoryCluster(models.Model):
    """Pre-computed group of stories covering the same event from different sources."""
    language = models.CharField(max_length=5, db_index=True)
    representative_story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='representing_clusters')
    stories = models.ManyToManyField(Story, related_name='clusters')
    source_count = models.IntegerField(default=0)
    sources = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-source_count']

    def __str__(self):
        return f"{self.source_count} sources: {self.representative_story.title[:50]}"


class AnalyticsEvent(models.Model):
    """Lightweight analytics event tracking. No personal data stored."""
    
    EVENT_TYPES = [
        ('page_view', 'Page View'),
        ('share', 'Share'),
        ('feed_access', 'Feed Access'),
        ('widget_load', 'Widget Load'),
    ]
    
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, db_index=True)
    path = models.CharField(max_length=500, db_index=True)
    language = models.CharField(max_length=5, blank=True, db_index=True)
    category = models.CharField(max_length=20, blank=True)
    country_code = models.CharField(max_length=5, blank=True, db_index=True)
    user_agent = models.CharField(max_length=200, blank=True)
    is_bot = models.BooleanField(default=False, db_index=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['event_type', 'timestamp']),
            models.Index(fields=['country_code', 'timestamp']),
        ]
    
    def __str__(self):
        return f"{self.event_type}: {self.path} ({self.country_code})"


def build_clusters(language, max_stories=500):
    """Build StoryClusters for a language by grouping stories with similar titles.
    
    Args:
        language: Language code
        max_stories: Maximum stories to process (to prevent memory issues)
    """
    from django.utils import timezone
    from datetime import timedelta
    from collections import OrderedDict
    from news.sources_config import LANGUAGE_STOP_WORDS

    cutoff = timezone.now() - timedelta(hours=24)
    # Limit stories to prevent memory issues
    stories = list(Story.objects.filter(
        published__gte=cutoff, 
        language=language
    ).order_by('-published')[:max_stories])

    stop_words = LANGUAGE_STOP_WORDS.get(language, LANGUAGE_STOP_WORDS['en'])

    # Group stories by word overlap
    story_groups = OrderedDict()
    for story in stories:
        normalized = re.sub(r'[^\w\s]', '', story.title.lower())
        normalized_words = set(normalized.split()) - stop_words
        normalized_key = ' '.join(sorted(normalized_words))

        matched_key = None
        for existing_key in story_groups:
            existing_words = set(existing_key.split())
            if not existing_words or not normalized_words:
                continue
            overlap = len(existing_words & normalized_words) / max(len(existing_words), len(normalized_words))
            if overlap >= 0.6:
                matched_key = existing_key
                break

        if matched_key:
            story_groups[matched_key].append(story)
        else:
            story_groups[normalized_key] = [story]

    # Clear existing clusters for this language
    StoryCluster.objects.filter(language=language).delete()

    # Create clusters for groups with 2+ stories from different sources
    clusters_to_create = []
    cluster_stories = []

    for group_stories in story_groups.values():
        unique_sources = set(s.source for s in group_stories)
        if len(unique_sources) >= 2:
            clusters_to_create.append(StoryCluster(
                language=language,
                representative_story=group_stories[0],
                source_count=len(unique_sources),
                sources=sorted(unique_sources),
            ))
            cluster_stories.append(group_stories)

    created = StoryCluster.objects.bulk_create(clusters_to_create)

    # Set M2M relationships
    for cluster, stories_list in zip(created, cluster_stories):
        cluster.stories.set(stories_list)

    return len(created)


class RecommendedBook(models.Model):
    """Curated book recommendations shown alongside news stories."""
    
    CATEGORY_CHOICES = [
        ('world', 'World'),
        ('us', 'US'),
        ('politics', 'Politics'),
        ('business', 'Business'),
        ('technology', 'Technology'),
        ('science', 'Science'),
        ('health', 'Health'),
        ('sports', 'Sports'),
        ('entertainment', 'Entertainment'),
    ]
    
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    asin = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    language = models.CharField(max_length=5, default='en')
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    click_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['category', '-created_at']
        indexes = [
            models.Index(fields=['category', 'language', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def amazon_url(self):
        """Generate Amazon affiliate link."""
        return f"https://www.amazon.com/dp/{self.asin}?tag=24hourwire-20"


class Topic(models.Model):
    """Evergreen topic hub that aggregates live stories by keywords.
    
    Topics are permanent landing pages that auto-populate with matching
    stories from the last 24 hours. They are indexable by Google and
    serve as stable URLs for social sharing.
    """
    
    slug = models.SlugField(unique=True, db_index=True)
    title = models.CharField(max_length=200)
    headline = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    keywords = models.JSONField(default=list, help_text="Keywords for matching stories by title")
    categories = models.JSONField(default=list, help_text="Categories to match (e.g., ['sports', 'world'])")
    languages = models.JSONField(default=list, help_text="Language codes to include")
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    priority = models.IntegerField(default=0, help_text="Sort order on homepage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO fields
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['is_active', 'priority']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('topic_detail', kwargs={'slug': self.slug})
    
    def get_stories(self, language=None, limit=50):
        """Fetch matching stories from last 24 hours."""
        from django.utils import timezone
        from datetime import timedelta
        from django.db.models import Q
        
        cutoff = timezone.now() - timedelta(hours=24)
        
        # Build keyword Q objects
        keyword_q = Q()
        for kw in self.keywords:
            keyword_q |= Q(title__icontains=kw)
        
        # Build category Q objects (use actual DB category field)
        category_q = Q(category__in=self.categories) if self.categories else Q()
        
        # Combine: keyword match OR category match, within last 24h
        base_q = Q(published__gte=cutoff) & (keyword_q | category_q)
        stories = Story.objects.filter(base_q).distinct()
        
        # Language filter
        if language:
            stories = stories.filter(language=language)
        elif self.languages:
            stories = stories.filter(language__in=self.languages)
        
        return stories.order_by('-published')[:limit]
    
    def get_story_count(self, language=None):
        """Get count of matching stories."""
        return self.get_stories(language=language, limit=1000).count()
    
    def get_languages_with_stories(self):
        """Return language codes that have matching stories."""
        from django.utils import timezone
        from datetime import timedelta
        from django.db.models import Q
        
        cutoff = timezone.now() - timedelta(hours=24)
        keyword_q = Q()
        for kw in self.keywords:
            keyword_q |= Q(title__icontains=kw)
        
        category_q = Q(category__in=self.categories) if self.categories else Q()
        
        base_q = Q(published__gte=cutoff) & (keyword_q | category_q)
        qs = Story.objects.filter(base_q).distinct().values_list('language', flat=True)
        
        return sorted(set(qs))
