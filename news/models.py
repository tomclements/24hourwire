from django.db import models


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

    source = models.CharField(max_length=50)
    title = models.CharField(max_length=500)
    excerpt = models.TextField(blank=True)
    url = models.URLField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='world')
    published = models.DateTimeField()
    fetched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return f"{self.source}: {self.title[:50]}"

    def get_search_terms(self):
        stop_words = {'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'be', 'been', 'has', 'have', 'had', 'this', 'that', 'from', 'as', 'it', 'its', 'new', 'says', 'after', 'before', 'about', 'more', 'most', 'some', 'than', 'what', 'when', 'where', 'which', 'while', 'who', 'how', 'will', 'would', 'could', 'should', 'their', 'they', 'them', 'you', 'your', 'his', 'her', 'our', 'out', 'over', 'into', 'up', 'down', 'off', 'just', 'now', 'then'}
        words = self.title.lower().split()
        clean = [w for w in words if w not in stop_words and len(w) > 2][:5]
        return "+".join(clean)

    def get_clean_excerpt(self):
        import re
        if not self.excerpt:
            return ''
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', ' ', self.excerpt)
        # Remove source attribution at end
        text = re.sub(r'\s*(Reuters|AP News|AP|BBC|CBS|ABC|NBC|CNN|Bloomberg|Forbes|NPR|Al Jazeera|Deutsche Welle|France 24|Sky News|Yahoo|Newsweek|Time|Free Press)\s*$', '', text, flags=re.IGNORECASE)
        # Remove common artifacts
        text = re.sub(r'&nbsp;', ' ', text)
        text = re.sub(r'&amp;', '&', text)
        text = re.sub(r'&lt;', '<', text)
        text = re.sub(r'&gt;', '>', text)
        text = re.sub(r'&#39;', "'", text)
        text = re.sub(r'&[a-z]+;', '', text)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        # Filter out generic text
        generic = ['comprehensive up-to-date news coverage', 'aggregated from', 'click here for more']
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
        # Only return if meaningful content
        if len(text) > 30:
            return text
        return ''
