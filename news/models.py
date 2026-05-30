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
        ('poll_view', 'Poll View'),
        ('poll_vote', 'Poll Vote'),
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


# Common entity synonyms and acronym expansions for clustering
# Maps alternative names to a canonical form
ENTITY_SYNONYMS = {
    # Political figures
    'biden': 'us_president',
    'trump': 'us_president',
    'obama': 'us_president',
    'us president': 'us_president',
    'president of the united states': 'us_president',
    'putin': 'russia_leader',
    'russian president': 'russia_leader',
    'zelensky': 'ukraine_leader',
    'zelenskyy': 'ukraine_leader',
    'netanyahu': 'israel_leader',
    'xi jinping': 'china_leader',
    'xi': 'china_leader',
    'macron': 'france_leader',
    'scholz': 'germany_leader',
    'starmer': 'uk_leader',
    'sunak': 'uk_leader',
    'meloni': 'italy_leader',
    # Countries / geopolitical entities
    'uk': 'britain',
    'united kingdom': 'britain',
    'british': 'britain',
    'england': 'britain',
    'usa': 'america',
    'us': 'america',
    'united states': 'america',
    'america': 'america',
    'russia': 'russia',
    'russian': 'russia',
    'moscow': 'russia',
    'ukraine': 'ukraine',
    'ukrainian': 'ukraine',
    'kyiv': 'ukraine',
    'kiev': 'ukraine',
    'china': 'china',
    'chinese': 'china',
    'chinese leader': 'china_leader',
    'beijing': 'china',
    'israel': 'israel',
    'israeli': 'israel',
    'gaza': 'gaza',
    'palestine': 'gaza',
    'palestinian': 'gaza',
    'iran': 'iran',
    'iranian': 'iran',
    'tehran': 'iran',
    'north korea': 'north_korea',
    'dprk': 'north_korea',
    'eu': 'european_union',
    'european union': 'european_union',
    'nato': 'nato',
    'un': 'united_nations',
    'united nations': 'united_nations',
    # Organizations
    'fed': 'federal_reserve',
    'federal reserve': 'federal_reserve',
    'ecb': 'ecb',
    'european central bank': 'ecb',
    'imf': 'imf',
    'who': 'who',
    'cdc': 'cdc',
    # Events / generic
    'covid': 'covid',
    'coronavirus': 'covid',
    'pandemic': 'covid',
    'climate change': 'climate',
    'global warming': 'climate',
}

# Acronyms to expand in titles
ACRONYM_EXPANSIONS = {
    'u.s.': 'united states',
    'u.s': 'united states',
    'u.k.': 'united kingdom',
    'u.k': 'united kingdom',
    'e.u.': 'european union',
    'eu': 'european union',
    'nato': 'nato',
    'n.h.s.': 'national health service',
    'nhs': 'national health service',
    'n.y.': 'new york',
    'ny': 'new york',
    'l.a.': 'los angeles',
    'la': 'los angeles',
    'g.d.p.': 'gross domestic product',
    'gdp': 'gross domestic product',
    'a.i.': 'artificial intelligence',
    'ai': 'artificial intelligence',
    'i.p.o.': 'initial public offering',
    'ipo': 'initial public offering',
}


def _normalize_title(title, stop_words):
    """Normalize a title for clustering: lowercase, strip punctuation, expand acronyms."""
    text = title.lower()
    # Expand acronyms (whole word only)
    for acr, expansion in ACRONYM_EXPANSIONS.items():
        text = re.sub(rf'\b{re.escape(acr)}\b', expansion, text)
    # Remove possessive 's and trailing punctuation
    text = re.sub(r"'s\b", '', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    words = text.split()
    # Filter stop words and very short tokens
    words = [w for w in words if w not in stop_words and len(w) > 1]
    return words


def _extract_entities(words):
    """Extract canonical entity tokens from a word list."""
    entities = set()
    # Single-word entities
    for w in words:
        if w in ENTITY_SYNONYMS:
            entities.add(ENTITY_SYNONYMS[w])
    # Multi-word entities (bigrams and trigrams)
    for i in range(len(words) - 1):
        bigram = f"{words[i]} {words[i + 1]}"
        if bigram in ENTITY_SYNONYMS:
            entities.add(ENTITY_SYNONYMS[bigram])
    for i in range(len(words) - 2):
        trigram = f"{words[i]} {words[i + 1]} {words[i + 2]}"
        if trigram in ENTITY_SYNONYMS:
            entities.add(ENTITY_SYNONYMS[trigram])
    return entities


def _compute_similarity(words_a, words_b, entities_a, entities_b):
    """Compute similarity between two title word lists.

    Returns a score from 0.0 to 1.0. Uses multiple signals:
    - Entity overlap (strong signal)
    - Jaccard similarity on content words
    - Bigram overlap boost
    """
    if not words_a or not words_b:
        return 0.0

    set_a = set(words_a)
    set_b = set(words_b)

    # 1. Entity overlap: if they share any major entity, high similarity
    if entities_a and entities_b:
        shared_entities = entities_a & entities_b
        if shared_entities:
            # Boost based on how many content words also overlap
            jaccard = len(set_a & set_b) / max(len(set_a), len(set_b))
            return max(0.55, min(0.95, 0.55 + jaccard * 0.4))

    # 2. Bigram overlap (adjacent word pairs matter)
    bigrams_a = {f"{words_a[i]} {words_a[i + 1]}" for i in range(len(words_a) - 1)}
    bigrams_b = {f"{words_b[i]} {words_b[i + 1]}" for i in range(len(words_b) - 1)}
    if bigrams_a and bigrams_b:
        bigram_overlap = len(bigrams_a & bigrams_b) / max(len(bigrams_a), len(bigrams_b))
        if bigram_overlap >= 0.5:
            return 0.55  # Enough to cluster

    # 3. Standard Jaccard on content words
    intersection = len(set_a & set_b)
    union_size = max(len(set_a), len(set_b))
    if union_size == 0:
        return 0.0
    jaccard = intersection / union_size

    # 4. Short-title bonus: if both are short and share >=1 key word, boost
    if len(words_a) <= 4 and len(words_b) <= 4:
        if intersection >= 1:
            jaccard = max(jaccard, 0.45)

    return jaccard


def build_clusters(language, max_stories=500):
    """Build StoryClusters for a language by grouping stories with similar titles.

    Improved algorithm with entity matching, acronym expansion, synonym
    detection, and two-tier similarity scoring.

    Args:
        language: Language code
        max_stories: Maximum stories to process (to prevent memory issues)
    """
    from django.utils import timezone
    from datetime import timedelta
    from collections import OrderedDict
    from news.sources_config import LANGUAGE_STOP_WORDS

    cutoff = timezone.now() - timedelta(hours=24)
    stories = list(Story.objects.filter(
        published__gte=cutoff,
        language=language
    ).order_by('-published')[:max_stories])

    stop_words = LANGUAGE_STOP_WORDS.get(language, LANGUAGE_STOP_WORDS['en'])

    # Pre-normalize every story
    normalized_stories = []
    for story in stories:
        words = _normalize_title(story.title, stop_words)
        entities = _extract_entities(words)
        normalized_stories.append({
            'story': story,
            'words': words,
            'entities': entities,
            'key': ' '.join(sorted(set(words))),
        })

    # Greedy grouping by similarity
    SIMILARITY_THRESHOLD = 0.45
    story_groups = OrderedDict()
    group_keys = []  # parallel list of representative keys

    for ns in normalized_stories:
        matched_idx = None
        for idx, gk in enumerate(group_keys):
            # Fast path: exact key match
            if ns['key'] == gk:
                matched_idx = idx
                break
            # Compute similarity against representative story (first in group)
            rep = story_groups[gk][0]
            rep_words = rep['words']
            rep_entities = rep['entities']
            score = _compute_similarity(ns['words'], rep_words, ns['entities'], rep_entities)
            if score >= SIMILARITY_THRESHOLD:
                matched_idx = idx
                break

        if matched_idx is not None:
            gk = group_keys[matched_idx]
            story_groups[gk].append(ns)
        else:
            story_groups[ns['key']] = [ns]
            group_keys.append(ns['key'])

    # Clear existing clusters for this language
    StoryCluster.objects.filter(language=language).delete()

    # Create clusters for groups with 2+ stories from different sources
    clusters_to_create = []
    cluster_stories = []

    for group in story_groups.values():
        group_stories = [ns['story'] for ns in group]
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
    
    # Translations for headline and description by language code
    translations = models.JSONField(
        default=dict,
        help_text="Translations by language: {'es': {'headline': '...', 'description': '...'}, ...}"
    )
    
    # Affiliate merchandise links
    merchandise = models.JSONField(
        default=dict,
        help_text="Merchandise links: {'title': '...', 'items': [{'name': '...', 'url': '...', 'image': '...'}]}"
    )
    
    class Meta:
        ordering = ['-priority', '-created_at']
        indexes = [
            models.Index(fields=['is_active', 'priority']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_translation(self, language='en'):
        """Get translated headline/description for a language.
        
        Falls back to English if no translation exists.
        Returns dict with headline and description.
        """
        if language == 'en' or not self.translations:
            return {
                'headline': self.headline,
                'description': self.description,
            }
        
        lang_data = self.translations.get(language, {})
        return {
            'headline': lang_data.get('headline', self.headline),
            'description': lang_data.get('description', self.description),
        }
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('topic_detail', kwargs={'slug': self.slug})
    
    def get_stories(self, language=None, limit=50):
        """Fetch matching stories from last 24 hours.
        
        Matches are based strictly on keywords in the story title.
        Category matching is NOT used here to avoid broad, off-topic
        results (e.g. a generic NBA story matching the World Cup topic
        just because both have category='sports').
        """
        from django.utils import timezone
        from datetime import timedelta
        from django.db.models import Q
        
        cutoff = timezone.now() - timedelta(hours=24)
        
        # Build keyword Q objects — strict title matching only
        keyword_q = Q()
        for kw in self.keywords:
            keyword_q |= Q(title__icontains=kw)
        
        # Require keyword match within last 24h
        base_q = Q(published__gte=cutoff) & keyword_q
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
        
        # Keyword-only matching (same logic as get_stories)
        base_q = Q(published__gte=cutoff) & keyword_q
        qs = Story.objects.filter(base_q).distinct().values_list('language', flat=True)
        
        return sorted(set(qs))


class Poll(models.Model):
    """Community polls for engagement — news-related and fun."""
    
    STATUS_CHOICES = [
        ('pending_review', 'Pending Review'),
        ('active', 'Active'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]
    
    POLL_TYPE_CHOICES = [
        ('topical', 'Topical'),
        ('fun', 'Fun'),
        ('lifestyle', 'Lifestyle'),
        ('opinion', 'Opinion'),
        ('sports', 'Sports'),
        ('culture', 'Culture'),
    ]
    
    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('es', 'Español'),
        ('fr', 'Français'),
        ('de', 'Deutsch'),
        ('pt', 'Português'),
        ('it', 'Italiano'),
        ('ar', 'العربية'),
        ('ru', 'Русский'),
        ('ja', '日本語'),
        ('zh', '中文'),
        ('ko', '한국어'),
        ('tr', 'Türkçe'),
        ('hi', 'हिन्दी'),
    ]
    
    language = models.CharField(max_length=5, choices=LANGUAGE_CHOICES, default='en', db_index=True)
    question = models.CharField(max_length=300)
    options = models.JSONField(default=list, help_text="List of option strings")
    poll_type = models.CharField(max_length=20, choices=POLL_TYPE_CHOICES, default='topical', db_index=True)
    english_translation = models.CharField(max_length=300, blank=True, help_text="For review of non-English polls")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_review', db_index=True)
    is_active = models.BooleanField(default=False, db_index=True)
    starts_at = models.DateTimeField(null=True, blank=True)
    ends_at = models.DateTimeField(null=True, blank=True)
    vote_count = models.IntegerField(default=0)
    results = models.JSONField(default=dict, help_text="{option_index: count}")
    source = models.CharField(max_length=20, default='auto', help_text="auto or manual")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'language']),
            models.Index(fields=['is_active', 'language', 'ends_at']),
            models.Index(fields=['poll_type', 'created_at']),
        ]
    
    def __str__(self):
        return f"[{self.language}] {self.question[:50]}"
    
    def get_results_display(self):
        """Return list of {option, count, percentage} for each option."""
        total = self.vote_count
        display = []
        for idx, option in enumerate(self.options):
            # Support both integer and string keys for backward compatibility
            count = self.results.get(idx, self.results.get(str(idx), 0))
            pct = round((count / total) * 100, 1) if total > 0 else 0
            display.append({
                'index': idx,
                'option': option,
                'count': count,
                'percentage': pct,
            })
        return display
    
    def has_voted(self, request):
        """Check if this request (IP+UA hash) has already voted."""
        vote_hash = self._make_vote_hash(request)
        return PollVote.objects.filter(poll=self, vote_hash=vote_hash).exists()
    
    def record_vote(self, option_index, request):
        """Record a vote with light anti-abuse."""
        vote_hash = self._make_vote_hash(request)
        
        # Idempotent: ignore duplicate votes from same hash
        if PollVote.objects.filter(poll=self, vote_hash=vote_hash).exists():
            return False
        
        PollVote.objects.create(
            poll=self,
            option_index=option_index,
            vote_hash=vote_hash,
        )
        
        # Update results counter atomically-ish (safe for our scale)
        # Normalize keys to integers for consistency
        key = option_index
        self.results[key] = self.results.get(key, self.results.get(str(key), 0)) + 1
        self.vote_count += 1
        self.save(update_fields=['results', 'vote_count'])
        return True
    
    def _make_vote_hash(self, request):
        """Create a hash from IP + User-Agent + poll ID.
        
        Note: In production (Render + Cloudflare), HTTP_X_FORWARDED_FOR
        may contain multiple IPs (client, Cloudflare, Render). We take the
        first (leftmost) IP which is the original client address.
        """
        ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')).split(',')[0].strip()
        ua = request.META.get('HTTP_USER_AGENT', '')
        raw = f"{ip}:{ua}:{self.id}"
        return hashlib.sha256(raw.encode()).hexdigest()[:32]


class PollVote(models.Model):
    """Individual vote record for analytics and anti-abuse."""
    
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name='votes')
    option_index = models.IntegerField()
    vote_hash = models.CharField(max_length=32, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['poll', 'vote_hash']),
        ]
    
    def __str__(self):
        return f"Vote on Poll {self.poll_id}: option {self.option_index}"


class PollGenerationConfig(models.Model):
    """Simple configuration for poll generation frequency and volume."""
    
    frequency_hours = models.PositiveIntegerField(
        default=24,
        help_text="Hours between automatic poll generation runs"
    )
    polls_per_language = models.PositiveIntegerField(
        default=3,
        help_text="Polls to generate per language per run"
    )
    is_enabled = models.BooleanField(
        default=True,
        help_text="Whether automatic generation is enabled"
    )
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Poll Generation Config"
        verbose_name_plural = "Poll Generation Configs"
    
    def __str__(self):
        return f"Every {self.frequency_hours}h, {self.polls_per_language}/lang"
    
    @classmethod
    def get_active_config(cls):
        """Get the current active config (singleton pattern)."""
        config = cls.objects.first()
        if not config:
            config = cls.objects.create()
        return config
