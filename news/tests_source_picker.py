"""Tests for the per-user source picker feature."""

import re
from datetime import timedelta
from pathlib import Path

from django.test import TestCase, Client, override_settings
from django.utils import timezone
from django.core.cache import cache
from django.urls import reverse

from news.models import Story, StoryCategory, StoryCluster
from news.languages import SOURCES
from news.source_prefs import (
    parse_excluded_sources,
    compute_effective_sources,
    encode_excluded_sources,
)


class ParseExcludedSourcesTests(TestCase):
    """Unit tests for parse_excluded_sources."""

    def _sources(self):
        return [('Reuters', 'Center'), ('AP', 'Center'), ('Deutsche Welle', 'Center')]

    def test_empty_and_none_return_empty_set(self):
        self.assertEqual(parse_excluded_sources('', self._sources()), set())
        self.assertEqual(parse_excluded_sources(None, self._sources()), set())

    def test_encoded_name_with_space_decoded(self):
        raw = 'Deutsche%20Welle'
        self.assertEqual(parse_excluded_sources(raw, self._sources()), {'Deutsche Welle'})

    def test_unknown_or_removed_names_dropped(self):
        raw = 'Reuters,Old Source,AP'
        self.assertEqual(parse_excluded_sources(raw, self._sources()), {'Reuters', 'AP'})

    def test_duplicates_whitespace_and_empty_segments(self):
        raw = '  Reuters  ,,Reuters, AP ,'
        self.assertEqual(parse_excluded_sources(raw, self._sources()), {'Reuters', 'AP'})

    def test_garbage_does_not_raise(self):
        # Invalid percent-encoding
        self.assertEqual(parse_excluded_sources('%%%', self._sources()), set())
        # Very long string
        self.assertEqual(parse_excluded_sources('a' * 10000, self._sources()), set())


class EffectiveSourcesTests(TestCase):
    """Unit tests for compute_effective_sources."""

    def test_excludes_names(self):
        selected = ['A', 'B', 'C']
        excluded = {'B'}
        self.assertEqual(compute_effective_sources(selected, excluded), ['A', 'C'])

    def test_empty_excluded_returns_selected(self):
        selected = ['A', 'B', 'C']
        self.assertEqual(compute_effective_sources(selected, set()), selected)


class EncodeExcludedSourcesTests(TestCase):
    """Unit tests for encode_excluded_sources."""

    def test_encodes_names_with_spaces(self):
        encoded = encode_excluded_sources({'Deutsche Welle', 'AP'})
        self.assertIn('Deutsche%20Welle', encoded)
        self.assertIn('AP', encoded)
        self.assertEqual(len(encoded.split(',')), 2)


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class SourcePickerHomeTests(TestCase):
    """Integration tests for source picker filtering on the homepage."""

    def setUp(self):
        cache.clear()
        self.client = Client()
        self.now = timezone.now()
        self.en_sources = SOURCES['en']
        self.source_names = [s[0] for s in self.en_sources]

    def _create_story(self, source, title, categories=None, language='en'):
        story = Story.objects.create(
            source=source,
            title=title,
            excerpt='Excerpt for ' + title,
            url=f'https://example.com/{language}/{source}/{title.replace(" ", "-")}',
            language=language,
            category='world',
            published=self.now,
            url_hash=f'{language}-{source}-{title}',
            title_fingerprint=f'{language}-{source}-{title}',
        )
        if categories:
            for slug in categories:
                StoryCategory.objects.create(story=story, slug=slug)
        return story

    def _home(self, **cookies):
        if cookies:
            for name, value in cookies.items():
                self.client.cookies[name] = value
        return self.client.get('/?lang=en')

    def test_no_cookie_no_exclusion(self):
        self._create_story('Reuters', 'Reuters story', ['all'])
        self._create_story('AP', 'AP story', ['all'])
        response = self._home()
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reuters story')
        self.assertContains(response, 'AP story')

    def test_exclude_one_source(self):
        self._create_story('Reuters', 'Reuters story', ['all'])
        self._create_story('AP', 'AP story', ['all'])
        self._create_story('BBC', 'BBC story', ['all'])
        response = self._home(excluded_sources='AP')
        self.assertContains(response, 'Reuters story')
        self.assertContains(response, 'BBC story')
        self.assertNotContains(response, 'AP story')

    def test_category_tab_respects_exclusion(self):
        self._create_story('Reuters', 'Reuters tech', ['technology'])
        self._create_story('AP', 'AP tech', ['technology'])
        response = self._home(excluded_sources='Reuters')
        self.assertContains(response, 'AP tech')
        self.assertNotContains(response, 'Reuters tech')

    def test_all_selected_same_as_no_cookie(self):
        self._create_story('Reuters', 'Reuters story', ['all'])
        self._create_story('AP', 'AP story', ['all'])
        no_cookie = self._home()
        with_cookie = self._home(excluded_sources='UnknownSource')
        self.assertEqual(no_cookie.status_code, 200)
        self.assertContains(no_cookie, 'Reuters story')
        self.assertContains(with_cookie, 'Reuters story')

    def test_empty_selection_shows_message_and_select_all(self):
        self._create_story('Reuters', 'Reuters story', ['all'])
        all_names = ','.join(self.source_names)
        response = self._home(excluded_sources=all_names)
        self.assertContains(response, 'No sources selected')
        self.assertContains(response, 'data-action="select-all-sources-apply"')
        self.assertNotContains(response, 'data-action="load-more"')

    def test_intersection_with_sources_param(self):
        self._create_story('Reuters', 'Reuters story', ['all'])
        self._create_story('AP', 'AP story', ['all'])
        self._create_story('BBC', 'BBC story', ['all'])
        # ?sources=center selects Reuters, AP (both Center). Cookie excludes AP.
        response = self.client.get('/?lang=en&sources=center', HTTP_COOKIE='excluded_sources=AP')
        self.assertContains(response, 'Reuters story')
        self.assertNotContains(response, 'AP story')
        self.assertNotContains(response, 'BBC story')

    def test_cluster_shown_with_allowed_source(self):
        story_a = self._create_story('Reuters', 'Cluster story Reuters', ['all'])
        story_b = self._create_story('AP', 'Cluster story AP', ['all'])
        cluster = StoryCluster.objects.create(
            language='en',
            representative_story=story_a,
            source_count=2,
            sources=['Reuters', 'AP'],
        )
        cluster.stories.add(story_a, story_b)
        response = self._home(excluded_sources='Reuters')
        self.assertContains(response, 'Cluster story AP')
        self.assertNotContains(response, 'Cluster story Reuters')

    def test_cluster_hidden_when_all_sources_excluded(self):
        story_a = self._create_story('Reuters', 'Cluster story Reuters', ['all'])
        story_b = self._create_story('AP', 'Cluster story AP', ['all'])
        cluster = StoryCluster.objects.create(
            language='en',
            representative_story=story_a,
            source_count=2,
            sources=['Reuters', 'AP'],
        )
        cluster.stories.add(story_a, story_b)
        response = self._home(excluded_sources='Reuters,AP')
        self.assertNotContains(response, 'Cluster story Reuters')
        self.assertNotContains(response, 'Cluster story AP')

    def test_cache_bypassed_with_exclusion_cookie(self):
        self._create_story('Reuters', 'Reuters story', ['all'])
        self._create_story('AP', 'AP story', ['all'])

        # First anonymous request caches the page with both stories.
        anon = self._home()
        self.assertContains(anon, 'Reuters story')
        self.assertContains(anon, 'AP story')

        # Request with exclusion cookie should not see the cached page.
        filtered = self._home(excluded_sources='Reuters')
        self.assertNotContains(filtered, 'Reuters story')
        self.assertContains(filtered, 'AP story')
        self.assertEqual(filtered.get('Cache-Control'), 'private, no-cache')

    def test_new_source_not_in_cookie_is_selected(self):
        # We can't add a real new source to the registry in a unit test without
        # modifying the module, so we simulate by excluding all current sources
        # except one and asserting the remaining one is shown.
        self._create_story('Reuters', 'Reuters story', ['all'])
        excluded = ','.join([n for n in self.source_names if n != 'Reuters'])
        response = self._home(excluded_sources=excluded)
        self.assertContains(response, 'Reuters story')


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class SourcePickerAPITests(TestCase):
    """Tests for load_more_stories excluded parameter."""

    def setUp(self):
        cache.clear()
        self.now = timezone.now()

    def _create_story(self, source, title, categories=None):
        story = Story.objects.create(
            source=source,
            title=title,
            excerpt='Excerpt',
            url=f'https://example.com/{source}/{title.replace(" ", "-")}',
            language='en',
            category='world',
            published=self.now,
            url_hash=f'{source}-{title}',
            title_fingerprint=f'{source}-{title}',
        )
        if categories:
            for slug in categories:
                StoryCategory.objects.create(story=story, slug=slug)
        return story

    def test_api_excludes_source(self):
        self._create_story('Reuters', 'Reuters story', ['all'])
        self._create_story('AP', 'AP story', ['all'])
        response = self.client.get('/api/stories/?lang=en&category=all&offset=0&excluded=AP')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        titles = [s['title'] for s in data['stories']]
        self.assertIn('Reuters story', titles)
        self.assertNotIn('AP story', titles)

    def test_api_without_excluded_unchanged(self):
        self._create_story('Reuters', 'Reuters story', ['all'])
        self._create_story('AP', 'AP story', ['all'])
        response = self.client.get('/api/stories/?lang=en&category=all&offset=0')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        titles = [s['title'] for s in data['stories']]
        self.assertIn('Reuters story', titles)
        self.assertIn('AP story', titles)


class SourcePickerCssGuardTests(TestCase):
    """Static guard tests for the source-picker CSS fix.

    These tests exist to prevent accidental regression of the layout that
    caused source names to squeeze to one letter per line and tiles to
    overlap in languages with long bias badges.
    """

    def setUp(self):
        self.css_path = Path(__file__).resolve().parent / 'static' / 'news' / 'css' / 'app.css'
        self.css = self.css_path.read_text(encoding='utf-8')

    def _rule_block(self, selector):
        pattern = re.escape(selector) + r'\s*\{[^}]*\}'
        match = re.search(pattern, self.css, re.DOTALL)
        self.assertIsNotNone(match, f'Could not find {selector} rule in app.css')
        return match.group(0)

    def test_source_options_rows_size_to_content(self):
        block = self._rule_block('.source-options')
        self.assertRegex(block, r'grid-auto-rows\s*:\s*max-content')

    def test_source_option_name_has_guard_against_squeeze(self):
        block = self._rule_block('.source-option-name')
        self.assertRegex(block, r'min-width\s*:\s*6em')
        self.assertRegex(block, r'overflow-wrap\s*:\s*break-word')
        self.assertNotRegex(block, r'overflow-wrap\s*:\s*anywhere')

    def test_desktop_source_options_columns_are_wide_enough(self):
        media_pattern = (
            r'@media\s*\(\s*min-width\s*:\s*601px\s*\)\s*\{[^}]*'
            r'\.source-options\s*\{[^}]*\}\s*\}'
        )
        media_match = re.search(media_pattern, self.css, re.DOTALL)
        self.assertIsNotNone(media_match, 'Could not find desktop .source-options media rule')
        self.assertRegex(media_match.group(0), r'minmax\s*\(\s*220px')
