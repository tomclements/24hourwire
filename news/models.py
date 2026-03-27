import hashlib
import re
from urllib.parse import urlparse, parse_qs, urlencode

from django.db import models


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

    class Meta:
        ordering = ['-published']
        indexes = [
            models.Index(fields=['language', 'published']),
            models.Index(fields=['source', 'language']),
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
        text = re.sub(r'<[^>]+>', ' ', self.excerpt)
        # Remove source attribution at end
        attribution = SOURCE_ATTRIBUTION.get(self.language, SOURCE_ATTRIBUTION['en'])
        text = re.sub(attribution, '', text, flags=re.IGNORECASE)
        # Remove common artifacts
        text = re.sub(r'&nbsp;', ' ', text)
        text = re.sub(r'&amp;', '&', text)
        text = re.sub(r'&lt;', '<', text)
        text = re.sub(r'&gt;', '>', text)
        text = re.sub(r'&#39;', "'", text)
        text = re.sub(r'&[a-z]+;', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
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


def build_clusters(language):
    """Build StoryClusters for a language by grouping stories with similar titles."""
    from django.utils import timezone
    from datetime import timedelta
    from collections import OrderedDict
    from news.sources_config import LANGUAGE_STOP_WORDS

    cutoff = timezone.now() - timedelta(hours=24)
    stories = list(Story.objects.filter(published__gte=cutoff, language=language))

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
