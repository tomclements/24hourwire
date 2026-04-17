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
from news.views import story_share, different_angle


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
