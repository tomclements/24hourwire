"""
Unit tests for 24HourWire news app.
Run with: python manage.py test
"""

import re
from datetime import datetime, timedelta
from django.test import TestCase, Client, RequestFactory
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse

from news.models import Story, StoryCluster, title_fingerprint, normalize_url
from news.views import story_share, different_angle, branded_redirect
from django.core import signing
from news.templatetags.news_extras import sign_share_data


class StoryModelTests(TestCase):
    """Tests for Story model methods."""
    
    def setUp(self):
        self.story = Story.objects.create(
            source='BBC',
            title='Test Story Title',
            excerpt='<p>This is a test excerpt with <a href="https://example.com">link</a>.</p>',
            url='https://example.com/test-story',
            language='en',
            category='world',
            published=timezone.now(),
            url_hash='abc123',
            title_fingerprint='def456'
        )
    
    def test_title_fingerprint_function(self):
        """Test title fingerprint normalization."""
        fp1 = title_fingerprint("Breaking News: Market Update")
        fp2 = title_fingerprint("Market Update: Breaking News")
        self.assertEqual(fp1, fp2, "Same words in different order should have same fingerprint")
    
    def test_normalize_url_function(self):
        """Test URL normalization."""
        url1 = "https://example.com/path?utm_source=twitter&ref=home"
        url2 = "https://example.com/path?utm_source=facebook"
        # Should normalize to same URL without tracking params
        norm1 = normalize_url(url1)
        norm2 = normalize_url(url2)
        self.assertEqual(norm1, norm2)
    
    def test_get_clean_excerpt_removes_html(self):
        """Test that HTML tags are removed from excerpts."""
        clean = self.story.get_clean_excerpt()
        self.assertNotIn('<p>', clean)
        self.assertNotIn('</p>', clean)
        self.assertNotIn('<a', clean)
        self.assertNotIn('</a>', clean)
    
    def test_get_clean_excerpt_removes_google_news_urls(self):
        """Test that Google News RSS reference URLs are removed."""
        self.story.excerpt = 'Story text <a href="https://news.google.com/rss/articles/CBMi2">Read more</a> more text'
        self.story.save()
        clean = self.story.get_clean_excerpt()
        self.assertNotIn('news.google.com', clean)
        self.assertNotIn('<a', clean)
    
    def test_get_clean_excerpt_removes_urls(self):
        """Test that bare URLs are removed from excerpts."""
        self.story.excerpt = 'Story text https://example.com/page more text'
        self.story.save()
        clean = self.story.get_clean_excerpt()
        self.assertNotIn('https://', clean)
    
    def test_get_clean_excerpt_decodes_entities(self):
        """Test HTML entities are decoded."""
        self.story.excerpt = 'Text with &amp; and &lt;tag&gt; and &quot;quote&quot;'
        self.story.save()
        clean = self.story.get_clean_excerpt()
        self.assertIn('&', clean)
        self.assertIn('<tag>', clean)
        self.assertIn('"quote"', clean)
        self.assertNotIn('&amp;', clean)
        self.assertNotIn('&lt;', clean)
        self.assertNotIn('&gt;', clean)
        self.assertNotIn('&quot;', clean)
    
    def test_get_clean_excerpt_length_requirement(self):
        """Test that short excerpts are filtered out."""
        self.story.excerpt = 'Too short'
        self.story.save()
        clean = self.story.get_clean_excerpt()
        self.assertEqual(clean, '')
    
    def test_get_clean_excerpt_filters_title_duplicates(self):
        """Test that excerpts matching title are filtered out."""
        self.story.excerpt = self.story.title
        self.story.save()
        clean = self.story.get_clean_excerpt()
        self.assertEqual(clean, '')
    
    def test_get_search_terms(self):
        """Test search term generation."""
        terms = self.story.get_search_terms()
        self.assertIn('test', terms.lower())
        self.assertIn('story', terms.lower())


class StoryShareViewTests(TestCase):
    """Tests for story_share view."""
    
    def setUp(self):
        self.client = Client()
        self.story = Story.objects.create(
            source='BBC',
            title='Test Story for Sharing',
            excerpt='This is a test excerpt.',
            url='https://example.com/share-test',
            language='en',
            category='world',
            published=timezone.now(),
            url_hash='share123',
            title_fingerprint='share456'
        )
    
    def test_story_share_view_exists(self):
        """Test that story_share URL resolves correctly."""
        url = reverse('story_share', args=[self.story.id])
        self.assertEqual(url, f'/story/{self.story.id}/')
    
    def test_story_share_view_returns_200(self):
        """Test that story_share view returns 200 for valid story."""
        response = self.client.get(f'/story/{self.story.id}/')
        self.assertEqual(response.status_code, 200)
    
    def test_story_share_view_returns_404_for_invalid_story(self):
        """Test that story_share view returns 404 for non-existent story."""
        response = self.client.get('/story/99999/')
        self.assertEqual(response.status_code, 404)
    
    def test_story_share_template_used(self):
        """Test that correct template is used."""
        response = self.client.get(f'/story/{self.story.id}/')
        self.assertTemplateUsed(response, 'story_share.html')


class HomeViewTests(TestCase):
    """Tests for home view."""
    
    def setUp(self):
        self.client = Client()
        # Create a recent story
        self.story = Story.objects.create(
            source='BBC',
            title='Recent Test Story',
            excerpt='Test excerpt content.',
            url='https://example.com/recent',
            language='en',
            category='world',
            published=timezone.now() - timedelta(hours=1),
            url_hash='recent123',
            title_fingerprint='recent456'
        )
    
    def test_home_view_returns_200(self):
        """Test that home view returns 200."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
    
    def test_home_view_uses_correct_template(self):
        """Test that home view uses home.html template."""
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ExcerptCleaningTests(TestCase):
    """Tests for excerpt cleaning functionality."""
    
    def setUp(self):
        self.story = Story.objects.create(
            source='Test Source',
            title='Test Title',
            excerpt='',
            url='https://example.com/test',
            language='hi',  # Hindi
            category='world',
            published=timezone.now(),
            url_hash='test123',
            title_fingerprint='test456'
        )
    
    def test_hindi_google_news_reference_removed(self):
        """Test that Google News RSS reference codes are removed from Hindi excerpts."""
        # Simulate real excerpt from Google News RSS with reference code
        self.story.excerpt = '''
        भारत ने एक नई अंतरिक्ष योजना की घोषणा की है। 
        <a href="https://news.google.com/rss/articles/CBMi2">Read more</a>
        यह एक महत्वपूर्ण विकास है।
        '''
        self.story.save()
        
        clean = self.story.get_clean_excerpt()
        
        # Should not contain the Google News URL
        self.assertNotIn('news.google.com', clean)
        self.assertNotIn('CBMi2', clean)
        self.assertNotIn('<a', clean)
        self.assertNotIn('</a>', clean)
        
        # Should contain the Hindi text
        self.assertIn('भारत', clean)
        self.assertIn('अंतरिक्ष', clean)


class StoryClusterModelTests(TestCase):
    """Tests for StoryCluster model."""
    
    def setUp(self):
        self.story1 = Story.objects.create(
            source='BBC',
            title='Breaking News Event',
            excerpt='First report.',
            url='https://example.com/news1',
            language='en',
            category='world',
            published=timezone.now(),
            url_hash='hash1',
            title_fingerprint='fp1'
        )
        
        self.story2 = Story.objects.create(
            source='CNN',
            title='Breaking News Event Update',
            excerpt='Second report.',
            url='https://example.com/news2',
            language='en',
            category='world',
            published=timezone.now(),
            url_hash='hash2',
            title_fingerprint='fp2'
        )
        
        # Create a cluster linking them
        self.cluster = StoryCluster.objects.create(
            language='en',
            representative_story=self.story1,
            source_count=2,
            sources=['BBC', 'CNN']
        )
        self.cluster.stories.add(self.story1, self.story2)
    
    def test_cluster_str_representation(self):
        """Test StoryCluster string representation."""
        expected = "2 sources: Breaking News Event"
        self.assertEqual(str(self.cluster), expected)
    
    def test_cluster_stories_relationship(self):
        """Test that cluster has correct stories."""
        stories = list(self.cluster.stories.all())
        self.assertEqual(len(stories), 2)
        self.assertIn(self.story1, stories)
        self.assertIn(self.story2, stories)


class BrandedRedirectTests(TestCase):
    """Tests for stateless branded share redirect."""
    
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_signing_roundtrip(self):
        """Test that signed tokens can be created and verified."""
        data = {
            'url': 'https://example.com/article',
            'title': 'Test Article',
            'source': 'Test Source',
        }
        signer = signing.Signer()
        payload = signing.dumps(data)
        token = signer.sign(payload)
        
        # Verify token
        payload = signer.unsign(token)
        result = signing.loads(payload)
        
        self.assertEqual(result['url'], data['url'])
        self.assertEqual(result['title'], data['title'])
        self.assertEqual(result['source'], data['source'])
    
    def test_tampered_token_returns_404(self):
        """Test that tampered tokens return 404."""
        from django.http import Http404
        request = self.factory.get('/go/invalid-token/')
        with self.assertRaises(Http404):
            branded_redirect(request, 'invalid-token')
    
    def test_branded_redirect_view_renders(self):
        """Test the branded redirect view renders with OG tags."""
        data = {
            'url': 'https://bbc.com/news/test-article',
            'title': 'Breaking News Test',
            'source': 'BBC',
            'image_url': 'https://example.com/image.jpg',
        }
        signer = signing.Signer()
        payload = signing.dumps(data)
        token = signer.sign(payload)
        
        request = self.factory.get(f'/go/{token}/')
        response = branded_redirect(request, token)
        
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        
        # Check branding
        self.assertIn('24HourWire', content)
        self.assertIn('Breaking News Test', content)
        self.assertIn('BBC', content)
        self.assertIn('bbc.com/news/test-article', content)
        
        # Check OG image uses story image
        self.assertIn('https://example.com/image.jpg', content)
        
        # Check JavaScript redirect (not meta refresh, so crawlers read OG tags)
        self.assertIn('window.location.href', content)
    
    def test_template_filter_generates_valid_token(self):
        """Test the sign_share_data template filter."""
        story = Story.objects.create(
            source='Test Source',
            title='Test Title',
            excerpt='Test excerpt',
            url='https://example.com/story',
            language='en',
            category='world',
            published=timezone.now(),
            url_hash='test123',
            title_fingerprint='tf123',
        )
        
        token = sign_share_data(story)
        
        # Verify it's a valid signed token
        signer = signing.Signer()
        payload = signer.unsign(token)
        data = signing.loads(payload)
        
        self.assertEqual(data['url'], story.url)
        self.assertEqual(data['title'], story.title)
        self.assertEqual(data['source'], story.source)
        self.assertEqual(data['image_url'], story.image_url)


class ShareFunctionalityTests(TestCase):
    """Tests for social sharing functionality - stateless URLs, OG tags, intent URLs."""
    
    def setUp(self):
        self.story = Story.objects.create(
            source='Test Source',
            title='Test Story Title',
            excerpt='Test excerpt',
            url='https://example.com/story',
            language='en',
            category='world',
            published=timezone.now(),
            url_hash='test123',
            title_fingerprint='tf123',
            image_url='https://example.com/image.jpg',
        )
    
    def test_branded_redirect_has_og_tags(self):
        """Branded redirect page must have Open Graph tags for Twitter cards."""
        data = {
            'url': self.story.url,
            'title': self.story.title,
            'source': self.story.source,
            'image_url': self.story.image_url,
        }
        signer = signing.Signer()
        payload = signing.dumps(data)
        token = signer.sign(payload)
        
        response = self.client.get(f'/go/{token}/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        
        # Required OG tags for Twitter cards
        self.assertIn('og:title', content, "Missing og:title")
        self.assertIn('og:description', content, "Missing og:description")
        self.assertIn('og:url', content, "Missing og:url")
        self.assertIn('og:type', content, "Missing og:type")
        self.assertIn('og:image', content, "Missing og:image")
        
        # Twitter Card tags
        self.assertIn('twitter:card', content, "Missing twitter:card")
        self.assertIn('twitter:title', content, "Missing twitter:title")
        self.assertIn('twitter:description', content, "Missing twitter:description")
        self.assertIn('twitter:image', content, "Missing twitter:image")
    
    def test_branded_redirect_og_title_contains_story_title(self):
        """OG title should contain the actual story title."""
        data = {
            'url': self.story.url,
            'title': self.story.title,
            'source': self.story.source,
            'image_url': self.story.image_url,
        }
        signer = signing.Signer()
        payload = signing.dumps(data)
        token = signer.sign(payload)
        
        response = self.client.get(f'/go/{token}/')
        content = response.content.decode()
        self.assertIn(self.story.title, content)
    
    def test_branded_redirect_og_image_uses_story_image(self):
        """OG image should use the story's image."""
        data = {
            'url': self.story.url,
            'title': self.story.title,
            'source': self.story.source,
            'image_url': self.story.image_url,
        }
        signer = signing.Signer()
        payload = signing.dumps(data)
        token = signer.sign(payload)
        
        response = self.client.get(f'/go/{token}/')
        content = response.content.decode()
        self.assertIn(self.story.image_url, content)
    
    def test_branded_redirect_works_after_story_deleted(self):
        """Branded redirect is stateless - works even after story is deleted."""
        data = {
            'url': self.story.url,
            'title': self.story.title,
            'source': self.story.source,
            'image_url': self.story.image_url,
        }
        signer = signing.Signer()
        payload = signing.dumps(data)
        token = signer.sign(payload)
        
        # Delete the story
        story_id = self.story.id
        self.story.delete()
        
        # Branded redirect should still work
        response = self.client.get(f'/go/{token}/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn(self.story.title, content)
    
    def test_twitter_intent_url_single_encoding(self):
        """Twitter intent URL must encode wireUrl exactly once."""
        from urllib.parse import quote
        title = 'Test Story'
        wire_url = 'https://24hourwire.news/go/abc123/'
        
        # Simulate the intent URL construction (same as JS shareToTwitter)
        text = 'via @24HourWire\n\n' + title
        twitter_url = ('https://twitter.com/intent/tweet?text='
                      + quote(text, safe='') + '&url='
                      + quote(wire_url, safe=''))
        
        # URL should be encoded exactly once
        self.assertIn('24hourwire.news%2Fgo%2Fabc123%2F', twitter_url)
        # Should NOT be double-encoded
        self.assertNotIn('%252F', twitter_url)
    
    def test_share_token_generation(self):
        """Template filter should generate valid signed token."""
        token = sign_share_data(self.story)
        
        # Token should be a non-empty string
        self.assertIsInstance(token, str)
        self.assertTrue(len(token) > 0)
        
        # Should be verifiable
        signer = signing.Signer()
        payload = signer.unsign(token)
        data = signing.loads(payload)
        self.assertEqual(data['title'], self.story.title)


class BiasFilterRegressionTests(TestCase):
    """Regression tests for bias filter bugs."""
    
    def test_default_homepage_uses_all_sources(self):
        """Default homepage (no sources param) should use all sources, not just defaults."""
        from .sources_config import SOURCES, DEFAULT_SOURCES
        
        # Create stories from sources that are in SOURCES but NOT in DEFAULT_SOURCES
        non_default_source = None
        lang_sources = SOURCES.get('en', SOURCES['en'])
        lang_defaults = DEFAULT_SOURCES.get('en', DEFAULT_SOURCES['en'])
        
        for source_name, _ in lang_sources:
            if source_name not in lang_defaults:
                non_default_source = source_name
                break
        
        if non_default_source:
            # Use a title that matches 'world' category keywords
            Story.objects.create(
                source=non_default_source,
                title='Global Summit Reaches Trade Agreement',
                excerpt='Test',
                url='https://example.com/test',
                language='en',
                category='world',
                published=timezone.now(),
                url_hash='nd123',
                title_fingerprint='ndfp123',
            )
            
            # Default homepage should show this story
            response = self.client.get('/')
            content = response.content.decode()
            self.assertIn('Global Summit Reaches Trade Agreement', content,
                         "Default homepage should show stories from ALL sources, not just defaults")
    
    def test_bias_class_set_on_stories(self):
        """Stories rendered on homepage should have bias_class attribute set."""
        Story.objects.create(
            source='BBC',
            title='Global Summit Reaches Trade Agreement',
            excerpt='Test',
            url='https://example.com/bbc',
            language='en',
            category='world',
            published=timezone.now(),
            url_hash='bbc123',
            title_fingerprint='bbcfp123',
        )
        
        response = self.client.get('/')
        content = response.content.decode()
        
        # Check that bias badge has a non-default class (not just 'center')
        # BBC is Left-Center in en.py, so it should have class 'left-center'
        self.assertIn('bias-badge left-center', content,
                     "BBC stories should have 'left-center' bias class, not default 'center'")
    
    def test_load_more_includes_bias_class(self):
        """AJAX load_more should include bias_class in JSON response."""
        Story.objects.create(
            source='BBC',
            title='Tech Giants Announce New AI Chips',
            excerpt='Test',
            url='https://example.com/bbc2',
            language='en',
            category='technology',
            published=timezone.now(),
            url_hash='bbc456',
            title_fingerprint='bbcfp456',
        )
        
        response = self.client.get('/api/stories/?lang=en&category=technology&offset=0')
        import json
        data = json.loads(response.content)
        
        self.assertTrue(len(data['stories']) > 0, "Should return at least one story")
        self.assertIn('bias_class', data['stories'][0],
                     "AJAX response should include 'bias_class' field")
        self.assertNotEqual(data['stories'][0]['bias_class'], 'center',
                           "bias_class should reflect actual bias, not default 'center'")


class BotDetectionTests(TestCase):
    """Tests for bot/crawler detection in analytics middleware."""
    
    def test_mozilla_user_agent_not_flagged_as_bot(self):
        """Normal browser user agents containing 'Mozilla' should NOT be bots."""
        from .middleware import AnalyticsMiddleware
        
        middleware = AnalyticsMiddleware(lambda req: None)
        
        # Common browser UAs all contain "Mozilla"
        browser_uas = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
        ]
        
        for ua in browser_uas:
            is_bot = middleware._is_bot(ua)
            self.assertFalse(is_bot, f"Browser UA should NOT be flagged as bot: {ua[:50]}...")
    
    def test_actual_bots_flagged_correctly(self):
        """Known bot user agents SHOULD be flagged as bots."""
        from .middleware import AnalyticsMiddleware
        
        middleware = AnalyticsMiddleware(lambda req: None)
        
        bot_uas = [
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Twitterbot/1.0',
            'facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)',
            'Feedly/1.0 (+http://www.feedly.com/fetcher.html; 1 subscribers; )',
            'LinkedInBot/1.0 (compatible; Mozilla/5.0; Apache-HttpClient +http://www.linkedin.com)',
        ]
        
        for ua in bot_uas:
            is_bot = middleware._is_bot(ua)
            self.assertTrue(is_bot, f"Bot UA should be flagged as bot: {ua[:50]}...")
    
    def test_headless_chrome_flagged_as_bot(self):
        """HeadlessChrome (Playwright, Puppeteer) should be flagged as bot."""
        from .middleware import AnalyticsMiddleware
        
        middleware = AnalyticsMiddleware(lambda req: None)
        
        # GitHub Actions Playwright uses this exact UA
        playwright_ua = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/147.0.7727.15 Safari/537.36'
        
        is_bot = middleware._is_bot(playwright_ua)
        self.assertTrue(is_bot, "Playwright HeadlessChrome should be flagged as bot")


class SitemapTests(TestCase):
    """Tests for XML sitemaps."""

    def test_sitemap_returns_xml(self):
        """Test that standard sitemap returns valid XML."""
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

        content = response.content.decode()
        self.assertIn('<urlset', content)
        self.assertIn('https://24hourwire.news/', content)
        self.assertIn('https://24hourwire.news/feeds/', content)
        self.assertIn('<priority>1.0</priority>', content)

    def test_news_sitemap_returns_xml(self):
        """Test that news sitemap returns valid Google News XML."""
        # Create a recent story
        story = Story.objects.create(
            source='BBC',
            title='Test News Story',
            excerpt='Test excerpt',
            url='https://example.com/test',
            language='en',
            category='world',
            published=timezone.now(),
            url_hash='hash123',
            title_fingerprint='fp123',
        )

        response = self.client.get('/news-sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/xml')

        content = response.content.decode()
        self.assertIn('<urlset', content)
        self.assertIn('xmlns:news=', content)
        self.assertIn('<news:news>', content)
        self.assertIn('<news:name>24HourWire</news:name>', content)
        self.assertIn('<news:language>en</news:language>', content)
        self.assertIn(f'https://24hourwire.news/story/{story.id}/', content)
        self.assertIn('Test News Story', content)

    def test_news_sitemap_excludes_old_stories(self):
        """Test that news sitemap only includes recent stories."""
        # Create an old story
        old_story = Story.objects.create(
            source='BBC',
            title='Old Story',
            excerpt='Old excerpt',
            url='https://example.com/old',
            language='en',
            category='world',
            published=timezone.now() - timedelta(hours=72),
            url_hash='old123',
            title_fingerprint='oldfp',
        )

        response = self.client.get('/news-sitemap.xml')
        content = response.content.decode()

        # Old story should not appear
        self.assertNotIn('Old Story', content)
        self.assertNotIn(f'https://24hourwire.news/story/{old_story.id}/', content)


class SportsCategorizationTests(TestCase):
    """Tests for sports-only category restriction."""
    
    def test_sports_story_only_in_sports_category(self):
        """Sports stories should only be categorized as sports, not world/politics/etc."""
        from news.categorization import get_story_categories
        
        # A title that could match multiple categories but is clearly sports
        categories = get_story_categories('Olympics Opening Ceremony Draws Global Crowd')
        self.assertEqual(categories, ['sports'],
                         "Sports stories should be restricted to only 'sports' category")
    
    def test_sports_with_political_terms_still_only_sports(self):
        """Even sports titles with political/world keywords should be sports-only."""
        from news.categorization import get_story_categories
        
        categories = get_story_categories('World Cup Politics: FIFA Election Controversy')
        self.assertEqual(categories, ['sports'],
                         "Sports story with political terms should still be sports-only")
    
    def test_non_sports_story_not_affected(self):
        """Non-sports stories should get their normal categories."""
        from news.categorization import get_story_categories
        
        categories = get_story_categories('Congress Passes New Budget Bill')
        self.assertNotIn('sports', categories,
                        "Non-sports stories should not be categorized as sports")
        self.assertIn('politics', categories)
    
    def test_mlb_trade_headline_is_sports_only(self):
        """MLB trade headlines should be categorized as sports only."""
        from news.categorization import get_story_categories
        
        categories = get_story_categories("Ranking the Mets' trade bait value ahead of a potential fire sale")
        self.assertEqual(categories, ['sports'],
                        "MLB trade story should be sports-only")
    
    def test_golf_pga_headline_is_sports_only(self):
        """PGA golf headlines should be categorized as sports only."""
        from news.categorization import get_story_categories
        
        categories = get_story_categories("Looking ahead to the rest of the 2026 PGA Championship")
        self.assertEqual(categories, ['sports'],
                        "PGA golf story should be sports-only")
    
    def test_nfl_player_headline_is_sports_only(self):
        """NFL player headlines should be categorized as sports only."""
        from news.categorization import get_story_categories
        
        categories = get_story_categories("Jameis Winston uses his artistic talents in hilarious Giants 2026 schedule release video")
        self.assertEqual(categories, ['sports'],
                        "NFL player story should be sports-only")
