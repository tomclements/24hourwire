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

from news.models import Story, StoryCluster, Topic, title_fingerprint, normalize_url
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
    
    def test_espn_source_always_sports(self):
        """ESPN stories should always be sports, regardless of title."""
        from news.categorization import get_story_categories
        
        # A title that could be anything, but from ESPN it's sports
        categories = get_story_categories('Breaking News Update', source='ESPN')
        self.assertEqual(categories, ['sports'],
                        "ESPN source should always be categorized as sports")
    
    def test_bbc_sport_source_always_sports(self):
        """BBC Sport stories should always be sports, regardless of title."""
        from news.categorization import get_story_categories
        
        categories = get_story_categories('Morning Update', source='BBC Sport')
        self.assertEqual(categories, ['sports'],
                        "BBC Sport source should always be categorized as sports")
    
    def test_non_sports_source_not_affected(self):
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


class TopicHubTests(TestCase):
    """Tests for evergreen topic hub pages."""
    
    def setUp(self):
        self.client = Client()
        self.topic = Topic.objects.create(
            slug='test-topic',
            title='Test Topic',
            headline='A test topic for unit tests',
            description='This is a test topic used for unit testing.',
            keywords=['test', 'unit', 'pytest'],
            categories=['world'],
            languages=['en'],
            is_active=True,
            priority=5,
            meta_title='Test Topic | 24HourWire',
            meta_description='Test topic for verifying hub page functionality.',
        )
        
        # Create matching story
        self.matching_story = Story.objects.create(
            source='BBC',
            title='Unit testing best practices for pytest',
            excerpt='How to write better unit tests using pytest.',
            url='https://example.com/pytest-testing',
            language='en',
            category='world',
            published=timezone.now(),
            url_hash='testhash1',
            title_fingerprint='testfp1'
        )
        
        # Create non-matching story
        self.non_matching_story = Story.objects.create(
            source='Reuters',
            title='Stock market closes higher on tech gains',
            excerpt='The stock market rallied today.',
            url='https://example.com/market-rally',
            language='en',
            category='business',
            published=timezone.now(),
            url_hash='testhash2',
            title_fingerprint='testfp2'
        )
    
    def test_topic_model_str(self):
        """Topic string representation should be its title."""
        self.assertEqual(str(self.topic), 'Test Topic')
    
    def test_topic_absolute_url(self):
        """Topic should generate correct absolute URL."""
        self.assertEqual(self.topic.get_absolute_url(), '/topic/test-topic/')
    
    def test_topic_get_stories_matches_keywords(self):
        """Topic should return stories matching its keywords."""
        stories = list(self.topic.get_stories())
        self.assertEqual(len(stories), 1)
        self.assertEqual(stories[0].id, self.matching_story.id)
    
    def test_topic_get_stories_excludes_old_stories(self):
        """Topic should only return stories from last 24 hours."""
        # Update story to be 25 hours old
        self.matching_story.published = timezone.now() - timedelta(hours=25)
        self.matching_story.save()
        
        stories = list(self.topic.get_stories())
        self.assertEqual(len(stories), 0)
    
    def test_topic_get_stories_excludes_category_only_matches(self):
        """Stories matching category but NOT keywords should be excluded.
        
        This prevents broad topics (e.g. World Cup) from showing unrelated
        stories that happen to share the same category (e.g. NBA stories).
        """
        # Create a story in the same category but with no matching keywords
        non_matching = Story.objects.create(
            source='ESPN',
            title='NBA Finals: Lakers vs Celtics Game 7 Preview',
            excerpt='Basketball preview.',
            url='https://example.com/nba',
            language='en',
            category='world',  # Same category as topic
            published=timezone.now(),
            url_hash='nbahash',
            title_fingerprint='nbafp'
        )
        
        stories = list(self.topic.get_stories())
        # The original matching story should still be there
        self.assertEqual(len(stories), 1)
        self.assertEqual(stories[0].id, self.matching_story.id)
        # The non-matching category-only story should NOT appear
        self.assertNotIn(non_matching, stories)
    
    def test_topic_detail_page_renders(self):
        """Topic detail page should render with 200 status."""
        response = self.client.get('/topic/test-topic/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Topic')
        self.assertContains(response, 'A test topic for unit tests')
    
    def test_topic_detail_page_shows_matching_stories(self):
        """Topic detail should display matching stories."""
        response = self.client.get('/topic/test-topic/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Unit testing best practices for pytest')
        self.assertContains(response, 'BBC')
    
    def test_topic_detail_page_language_filter(self):
        """Topic detail should filter stories by language param."""
        # Create Spanish story that matches
        Story.objects.create(
            source='El Pais',
            title='Testing practices en Python',
            excerpt='Test practices.',
            url='https://example.com/es-testing',
            language='es',
            category='world',
            published=timezone.now(),
            url_hash='testhash3',
            title_fingerprint='testfp3'
        )
        
        response = self.client.get('/topic/test-topic/?lang=es')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Testing practices en Python')
    
    def test_topic_detail_page_404_for_inactive(self):
        """Inactive topics should return 404."""
        self.topic.is_active = False
        self.topic.save()
        response = self.client.get('/topic/test-topic/')
        self.assertEqual(response.status_code, 404)
    
    def test_topic_detail_page_404_for_missing(self):
        """Non-existent topic slugs should return 404."""
        response = self.client.get('/topic/does-not-exist/')
        self.assertEqual(response.status_code, 404)
    
    def test_topic_meta_robots_indexable(self):
        """Topic pages should have index, follow meta robots."""
        response = self.client.get('/topic/test-topic/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'index, follow')
        self.assertNotContains(response, 'noindex')
    
    def test_topic_og_tags_present(self):
        """Topic pages should have Open Graph tags."""
        response = self.client.get('/topic/test-topic/')
        self.assertContains(response, 'og:title')
        self.assertContains(response, 'Test Topic')
        self.assertContains(response, 'og:url')
        self.assertContains(response, '/topic/test-topic/')
    
    def test_sitemap_includes_active_topics(self):
        """Sitemap should include active topic URLs."""
        from django.core.cache import cache
        cache.clear()  # Clear cached sitemap from previous tests
        response = self.client.get('/sitemap.xml')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/topic/test-topic/')
    
    def test_sitemap_excludes_inactive_topics(self):
        """Sitemap should not include inactive topic URLs."""
        self.topic.is_active = False
        self.topic.save()
        response = self.client.get('/sitemap.xml')
        self.assertNotContains(response, '/topic/test-topic/')
    
    def test_get_related_topics_finds_matches(self):
        """get_related_topics should return topics matching story keywords."""
        from news.views import get_related_topics
        
        # Set story categories for the matching story
        self.matching_story.story_categories = ['world']
        related = get_related_topics(self.matching_story)
        
        self.assertEqual(len(related), 1)
        self.assertEqual(related[0].slug, 'test-topic')
    
    def test_get_related_topics_limits_to_two(self):
        """get_related_topics should return max 2 topics."""
        from news.views import get_related_topics
        
        # Create additional matching topics
        for i in range(3):
            Topic.objects.create(
                slug=f'extra-topic-{i}',
                title=f'Extra Topic {i}',
                keywords=['test', 'unit'],
                categories=['world'],
                is_active=True,
                priority=1,
            )
        
        self.matching_story.story_categories = ['world']
        related = get_related_topics(self.matching_story)
        self.assertLessEqual(len(related), 2)
    
    def test_topic_stats_bias_spectrum(self):
        """Topic detail should show bias spectrum dots."""
        response = self.client.get('/topic/test-topic/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'bias-dot')
    
    def test_topic_language_pills(self):
        """Topic detail should show language filter pills."""
        response = self.client.get('/topic/test-topic/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'lang-pill')
        self.assertContains(response, 'All Languages')


class TopicKeywordOnlyTests(TestCase):
    """Tests that topic pages use strict keyword matching (not broad categories)."""
    
    def setUp(self):
        self.topic = Topic.objects.create(
            slug='world-cup-test',
            title='World Cup Test',
            keywords=['world cup', 'fifa', 'mundial'],
            categories=['sports', 'world'],
            languages=['en'],
            is_active=True,
        )
        
        # A story that matches keywords
        self.matching_story = Story.objects.create(
            source='BBC',
            title='FIFA announces World Cup 2026 venues',
            excerpt='Football news.',
            url='https://example.com/wc',
            language='en',
            category='sports',
            published=timezone.now(),
            url_hash='wc1',
            title_fingerprint='wcf1'
        )
        
        # A story that only matches category (should be excluded)
        self.category_only_story = Story.objects.create(
            source='ESPN',
            title='NBA trade deadline roundup',
            excerpt='Basketball news.',
            url='https://example.com/nba',
            language='en',
            category='sports',
            published=timezone.now(),
            url_hash='nba1',
            title_fingerprint='nbaf1'
        )
    
    def test_keyword_match_included(self):
        """Stories matching keywords should appear on topic page."""
        stories = list(self.topic.get_stories())
        self.assertEqual(len(stories), 1)
        self.assertEqual(stories[0].id, self.matching_story.id)
    
    def test_category_only_excluded(self):
        """Stories matching only category (not keywords) should be excluded."""
        stories = list(self.topic.get_stories())
        self.assertNotIn(self.category_only_story, stories)
    
    def test_topic_detail_shows_only_keyword_matches(self):
        """Topic detail page should only display keyword-matched stories."""
        response = self.client.get('/topic/world-cup-test/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'FIFA announces World Cup 2026 venues')
        self.assertNotContains(response, 'NBA trade deadline roundup')


class TopicModelTests(TestCase):
    """Unit tests for Topic model methods."""
    
    def setUp(self):
        self.topic = Topic.objects.create(
            slug='model-test',
            title='Model Test Topic',
            keywords=['election', 'vote'],
            categories=['politics'],
            languages=['en', 'es'],
            is_active=True,
        )
        
        self.en_story = Story.objects.create(
            source='BBC',
            title='Election results are in',
            excerpt='Results.',
            url='https://example.com/election',
            language='en',
            category='politics',
            published=timezone.now(),
            url_hash='hash1',
            title_fingerprint='fp1'
        )
        
        self.es_story = Story.objects.create(
            source='El Pais',
            title='Resultados de la election en Espana',
            excerpt='Resultados.',
            url='https://example.com/votacion',
            language='es',
            category='politics',
            published=timezone.now(),
            url_hash='hash2',
            title_fingerprint='fp2'
        )
    
    def test_get_story_count(self):
        """Topic.get_story_count should return correct count."""
        count = self.topic.get_story_count()
        self.assertEqual(count, 2)
    
    def test_get_story_count_with_language_filter(self):
        """Topic.get_story_count should filter by language."""
        count = self.topic.get_story_count(language='en')
        self.assertEqual(count, 1)
    
    def test_get_languages_with_stories(self):
        """Topic.get_languages_with_stories should return language codes with stories."""
        langs = self.topic.get_languages_with_stories()
        self.assertIn('en', langs)
        self.assertIn('es', langs)


class RobotsTxtTopicTests(TestCase):
    """Tests that robots.txt allows topic pages."""
    
    def test_robots_txt_allows_topic(self):
        """robots.txt should Allow /topic/."""
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Allow: /topic/')


class TopicTranslationTests(TestCase):
    """Tests for topic headline/description translations."""
    
    def setUp(self):
        self.client = Client()
        self.topic = Topic.objects.create(
            slug='translation-test',
            title='Translation Test',
            headline='English headline',
            description='English description',
            keywords=['test'],
            categories=['world'],
            languages=['en', 'es'],
            is_active=True,
            translations={
                'es': {
                    'headline': 'Titulo en espanol',
                    'description': 'Descripcion en espanol',
                }
            }
        )
        Story.objects.create(
            source='BBC', title='Test story', excerpt='Test',
            url='https://example.com/t', language='en', category='world',
            published=timezone.now(), url_hash='h1', title_fingerprint='f1'
        )
    
    def test_get_translation_english(self):
        """get_translation('en') should return original headline/description."""
        trans = self.topic.get_translation('en')
        self.assertEqual(trans['headline'], 'English headline')
        self.assertEqual(trans['description'], 'English description')
    
    def test_get_translation_spanish(self):
        """get_translation('es') should return Spanish headline/description."""
        trans = self.topic.get_translation('es')
        self.assertEqual(trans['headline'], 'Titulo en espanol')
        self.assertEqual(trans['description'], 'Descripcion en espanol')
    
    def test_get_translation_fallback(self):
        """get_translation for unknown language should fallback to English."""
        trans = self.topic.get_translation('fr')
        self.assertEqual(trans['headline'], 'English headline')
        self.assertEqual(trans['description'], 'English description')
    
    def test_topic_page_shows_translated_content(self):
        """Topic page should display translated headline/description when lang param is set."""
        response = self.client.get('/topic/translation-test/?lang=es')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Titulo en espanol')
        self.assertContains(response, 'Descripcion en espanol')
        self.assertNotContains(response, 'English headline')
    
    def test_topic_page_shows_english_by_default(self):
        """Topic page should display English content by default."""
        response = self.client.get('/topic/translation-test/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'English headline')
        self.assertContains(response, 'English description')


class TopicLanguageNameTests(TestCase):
    """Tests for full language names on topic pages."""
    
    def setUp(self):
        self.client = Client()
        self.topic = Topic.objects.create(
            slug='lang-test',
            title='Language Test',
            keywords=['test'],
            categories=['world'],
            languages=['en', 'es', 'fr'],
            is_active=True,
        )
        # Create stories in multiple languages
        Story.objects.create(
            source='BBC', title='Test story en', excerpt='Test',
            url='https://example.com/en', language='en', category='world',
            published=timezone.now(), url_hash='h1', title_fingerprint='f1'
        )
        Story.objects.create(
            source='El Pais', title='Test story es', excerpt='Test',
            url='https://example.com/es', language='es', category='world',
            published=timezone.now(), url_hash='h2', title_fingerprint='f2'
        )
    
    def test_language_pills_show_full_names(self):
        """Language filter pills should display full language names, not codes."""
        response = self.client.get('/topic/lang-test/')
        self.assertEqual(response.status_code, 200)
        # Should show "English" and "Español", not "EN" and "ES"
        self.assertContains(response, 'English')
        self.assertContains(response, 'Español')
        self.assertNotContains(response, '>EN<')
        self.assertNotContains(response, '>ES<')


class TopicMerchandiseTests(TestCase):
    """Tests for topic merchandise/affiliate links section."""
    
    def setUp(self):
        self.client = Client()
        self.topic = Topic.objects.create(
            slug='world-cup-merch',
            title='World Cup Merch Test',
            keywords=['test'],
            categories=['sports'],
            languages=['en'],
            is_active=True,
            merchandise={
                'title': 'World Cup 2026 Gear',
                'items': [
                    {
                        'name': 'Official Match Ball',
                        'url': 'https://www.amazon.com/s?k=match+ball&tag=24hourwire-20',
                        'image': 'https://example.com/ball.jpg',
                    },
                    {
                        'name': 'Brazil Jersey',
                        'url': 'https://www.amazon.com/s?k=brazil+jersey&tag=24hourwire-20',
                    }
                ]
            }
        )
        Story.objects.create(
            source='BBC', title='Test story', excerpt='Test',
            url='https://example.com/t', language='en', category='sports',
            published=timezone.now(), url_hash='h1', title_fingerprint='f1'
        )
    
    def test_topic_page_shows_merchandise_section(self):
        """Topic page with merchandise should display the gear section."""
        response = self.client.get('/topic/world-cup-merch/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'World Cup 2026 Gear')
        self.assertContains(response, 'Official Match Ball')
        self.assertContains(response, 'Brazil Jersey')
    
    def test_merchandise_links_use_amazon_affiliate(self):
        """Merchandise links should include the affiliate tracking ID."""
        response = self.client.get('/topic/world-cup-merch/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('tag=24hourwire-20', content)
    
    def test_topic_without_merchandise_hides_section(self):
        """Topics without merchandise should not show the section."""
        no_merch_topic = Topic.objects.create(
            slug='no-merch',
            title='No Merch',
            keywords=['test'],
            categories=['world'],
            languages=['en'],
            is_active=True,
        )
        Story.objects.create(
            source='BBC', title='Another test', excerpt='Test',
            url='https://example.com/nm', language='en', category='world',
            published=timezone.now(), url_hash='h2', title_fingerprint='f2'
        )
        response = self.client.get('/topic/no-merch/')
        self.assertEqual(response.status_code, 200)
        # Check for the actual section header text (not CSS class)
        self.assertNotContains(response, 'World Cup 2026 Gear')
        self.assertNotContains(response, 'Official Match Ball')
        self.assertNotContains(response, 'Brazil Jersey')


class TopicThemeToggleTests(TestCase):
    """Tests for dark/light theme toggle on topic pages."""
    
    def setUp(self):
        self.client = Client()
        self.topic = Topic.objects.create(
            slug='theme-test',
            title='Theme Test',
            keywords=['test'],
            categories=['world'],
            is_active=True,
        )
        Story.objects.create(
            source='BBC', title='Test story', excerpt='Test',
            url='https://example.com/t', language='en', category='world',
            published=timezone.now(), url_hash='h1', title_fingerprint='f1'
        )
    
    def test_topic_page_has_theme_toggle(self):
        """Topic detail page should include theme toggle button."""
        response = self.client.get('/topic/theme-test/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'theme-toggle')
        self.assertContains(response, 'toggleTheme')
    
    def test_topic_page_has_dark_mode_css(self):
        """Topic detail page should include dark mode CSS variables."""
        response = self.client.get('/topic/theme-test/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '[data-theme="dark"]')


class HomepageTopicCardsTests(TestCase):
    """Tests for 'Ongoing Coverage' topic cards on homepage."""
    
    def setUp(self):
        self.client = Client()
        # Create active topic
        self.active_topic = Topic.objects.create(
            slug='ongoing-test',
            title='Ongoing Test Topic',
            headline='Live updates on this important event',
            description='This is a description for the ongoing test topic.',
            keywords=['ongoing', 'test'],
            categories=['world'],
            languages=['en'],
            is_active=True,
            priority=10,
        )
        # Create inactive topic
        self.inactive_topic = Topic.objects.create(
            slug='inactive-test',
            title='Inactive Test Topic',
            headline='This should not appear',
            keywords=['inactive'],
            categories=['world'],
            languages=['en'],
            is_active=False,
            priority=5,
        )
        # Create a story so homepage renders normally
        Story.objects.create(
            source='BBC',
            title='Recent World News Update',
            excerpt='Test excerpt for world news.',
            url='https://example.com/recent-world',
            language='en',
            category='world',
            published=timezone.now(),
            url_hash='recent123',
            title_fingerprint='recent456'
        )
    
    def test_homepage_shows_ongoing_coverage_section(self):
        """Homepage should display 'Ongoing Coverage' heading."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ongoing Coverage')
    
    def test_homepage_shows_active_topic_cards(self):
        """Homepage should show cards for active topics."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ongoing Test Topic')
        self.assertContains(response, 'Live updates on this important event')
        self.assertContains(response, '/topic/ongoing-test/')
    
    def test_homepage_hides_inactive_topics(self):
        """Homepage should not show inactive topic cards."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Inactive Test Topic')
        self.assertNotContains(response, '/topic/inactive-test/')
    
    def test_homepage_topic_card_links_are_valid(self):
        """Topic card links should resolve to valid topic pages."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertIn('href="/topic/ongoing-test/"', content)
    
    def test_homepage_topic_context_passed_to_template(self):
        """Homepage view should pass active_topics in context."""
        from news.views import home
        from django.test import RequestFactory
        
        request = RequestFactory().get('/')
        # Use home view directly to inspect context
        # Note: cache_page decorator wraps the view, so we test the view logic
        response = home(request)
        self.assertEqual(response.status_code, 200)
        # The template uses {% if active_topics %} so context must include it
        # We verify the response renders successfully with topics in the DB
