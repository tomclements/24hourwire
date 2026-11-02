"""Tests for HTML-entity normalization and XSS safety."""

import re

from django.core.cache import cache
from django.core.management import call_command
from django.test import TestCase, Client, override_settings
from django.utils import timezone
from io import StringIO

from news.models import Story, StoryCategory, clean_feed_text, clean_title, normalize_stored_title, normalize_text, title_fingerprint
from news.management.commands.fetch_news import Command as FetchNewsCommand
from news.management.commands.fix_entities import Command as FixEntitiesCommand


class NormalizeTextTests(TestCase):
    """Unit tests for the shared normalize_text helper."""

    def test_decodes_hex_entities(self):
        # &#x201c; / &#x201d; are left/right double quotation marks (curly quotes).
        self.assertEqual(
            normalize_text('Variety &#x201c;Quote&#x201d;'),
            'Variety \u201cQuote\u201d'
        )

    def test_decodes_double_encoded_entities(self):
        self.assertEqual(normalize_text('Tom &amp;amp; Jerry'), 'Tom & Jerry')
        # &#x2019; is the right single quotation mark (curly apostrophe).
        self.assertEqual(normalize_text('&amp;#x2019;'), '\u2019')

    def test_nbsp_collapsed_to_space(self):
        self.assertEqual(normalize_text('a&nbsp;b'), 'a b')

    def test_idempotent_after_three_passes(self):
        # Cap raised to 3; these should fully decode and be stable.
        self.assertEqual(normalize_text('&amp;#x201c;'), '\u201c')
        self.assertEqual(normalize_text(normalize_text('&amp;#x201c;')), '\u201c')

    def test_idempotent_preserves_angle_brackets(self):
        """Repeated decoding must not treat decoded tags as real tags."""
        cases = [
            ('5 &lt; 6 &gt; 4', '5 < 6 > 4'),
            ('&lt;script&gt;x', '<script>x'),
            ('&amp;amp;amp;', '&'),
        ]
        for raw, expected in cases:
            with self.subTest(raw=raw):
                once = normalize_text(raw)
                twice = normalize_text(once)
                self.assertEqual(once, expected)
                self.assertEqual(twice, expected)

    def test_none_and_empty_return_empty_string(self):
        self.assertEqual(normalize_text(None), '')
        self.assertEqual(normalize_text(''), '')

    def test_a_less_than_b_survives(self):
        self.assertEqual(normalize_text('a < b'), 'a < b')
        self.assertEqual(normalize_text(normalize_text('a < b')), 'a < b')


class CleanFeedTextTests(TestCase):
    """Unit tests for clean_feed_text (raw feed input)."""

    def test_strips_tags_once_before_decoding(self):
        # Literal <b> is stripped; encoded &lt;i&gt; is decoded to a literal tag.
        self.assertEqual(clean_feed_text('<b>x</b> &lt;i&gt;'), 'x <i>')

    def test_none_and_empty_return_empty_string(self):
        self.assertEqual(clean_feed_text(None), '')
        self.assertEqual(clean_feed_text(''), '')


class CleanTitleTests(TestCase):
    """Unit tests for clean_title using clean_feed_text."""

    def test_strips_tags_and_decodes_entities(self):
        self.assertEqual(
            clean_title('<b>Tom &amp;amp; Jerry&#x2019;s</b>'),
            'Tom & Jerry\u2019s'
        )


class NormalizeStoredTitleTests(TestCase):
    """Decode-only title cleanup must be idempotent."""

    def test_decodes_but_preserves_literal_tags(self):
        title = '&lt;b&gt;bold&lt;/b&gt; &amp;amp;'
        self.assertEqual(normalize_stored_title(title), '<b>bold</b> &')
        self.assertEqual(normalize_stored_title(normalize_stored_title(title)), '<b>bold</b> &')

    def test_removes_stray_space_before_punctuation(self):
        self.assertEqual(normalize_stored_title('LIVE : update'), 'LIVE: update')


class CleanExcerptTests(TestCase):
    """Tests for Story.get_clean_excerpt."""

    def test_hex_entities_decoded(self):
        story = Story(
            title='Title',
            excerpt='From the &#x201c;Summer House&#x201d; love triangle.',
        )
        self.assertIn('\u201cSummer House\u201d', story.get_clean_excerpt())

    def test_double_encoded_entities_decoded(self):
        story = Story(
            title='Title',
            excerpt='Tom &amp;amp; Jerry &#x2019;s return was unexpected this season.',
        )
        excerpt = story.get_clean_excerpt()
        self.assertIn('Tom & Jerry', excerpt)
        self.assertIn('\u2019s return', excerpt)

    def test_a_less_than_b_survives(self):
        story = Story(
            title='Title',
            excerpt='Some math shows that a < b is true.',
        )
        self.assertIn('a < b', story.get_clean_excerpt())

    def test_less_than_and_script_literals_survive_in_excerpt(self):
        story = Story(
            title='Title',
            excerpt='a < b and <script>x</script> here, long enough text',
        )
        excerpt = story.get_clean_excerpt()
        self.assertIn('a < b', excerpt)
        self.assertIn('<script>x</script>', excerpt)


class ScrubLeftoverMarkupTitleTests(TestCase):
    """Tests for FetchNewsCommand.scrub_leftover_markup_titles."""

    def setUp(self):
        self.now = timezone.now()

    def test_stored_title_with_literal_angle_brackets_unchanged(self):
        title = '5 < 6 > 4 <script>x</script>'
        story = Story.objects.create(
            source='Test',
            title=title,
            excerpt='Excerpt.',
            url='https://example.com/test/angle-brackets',
            language='en',
            category='world',
            published=self.now,
            url_hash='angle-brackets',
            title_fingerprint=title_fingerprint(title),
        )
        count = FetchNewsCommand().scrub_leftover_markup_titles()
        story.refresh_from_db()
        self.assertEqual(count, 0)
        self.assertEqual(story.title, title)
        self.assertEqual(story.title_fingerprint, title_fingerprint(title))

    def test_stored_title_with_allowed_markup_is_cleaned(self):
        title = '<span>LIVE</span> Big news'
        story = Story.objects.create(
            source='Test',
            title=title,
            excerpt='Excerpt.',
            url='https://example.com/test/span-live',
            language='en',
            category='world',
            published=self.now,
            url_hash='span-live',
            title_fingerprint=title_fingerprint(title),
        )
        count = FetchNewsCommand().scrub_leftover_markup_titles()
        story.refresh_from_db()
        self.assertEqual(count, 1)
        self.assertEqual(story.title, 'LIVE Big news')
        self.assertEqual(story.title_fingerprint, title_fingerprint('LIVE Big news'))


@override_settings(CACHES={'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}})
class EntityXSSTests(TestCase):
    """Ensure decoded text is re-escaped by templates and the API."""

    def setUp(self):
        cache.clear()
        self.now = timezone.now()

    def _create_story(self, title, excerpt='Excerpt'):
        story = Story.objects.create(
            source='Reuters',
            title=title,
            excerpt=excerpt,
            url=f'https://example.com/reuters/xss-test',
            language='en',
            category='world',
            published=self.now,
            url_hash='xss-test',
            title_fingerprint='xss-test',
        )
        StoryCategory.objects.create(story=story, slug='all')
        return story

    def _run_fix_entities(self):
        FixEntitiesCommand(stdout=StringIO(), stderr=StringIO()).handle(apply=True)

    def test_homepage_escapes_decoded_script_tags(self):
        # Title contains encoded script tags; normalize_text decodes them to
        # literal <script>. The template must re-escape them for safe display.
        self._create_story('&lt;script&gt;alert(1)&lt;/script&gt; &amp;lt;b&amp;gt;')
        self._run_fix_entities()
        response = Client().get('/?lang=en')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertNotIn('<script>alert(1)', body)
        self.assertIn('&lt;script&gt;', body)

    def test_homepage_escapes_decoded_script_tags_in_excerpt(self):
        self._create_story(
            title='Safe title',
            excerpt='See this: &lt;script&gt;alert(1)&lt;/script&gt; and more text here to make it long enough.',
        )
        self._run_fix_entities()
        response = Client().get('/?lang=en')
        self.assertEqual(response.status_code, 200)
        body = response.content.decode()
        self.assertNotIn('<script>alert(1)', body)
        self.assertIn('&lt;script&gt;', body)

    def test_api_returns_plain_text_for_js_escape(self):
        self._create_story('&lt;script&gt;alert(1)&lt;/script&gt;')
        self._run_fix_entities()
        response = Client().get('/api/stories/?lang=en&category=all&offset=0')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        titles = [s['title'] for s in data['stories']]
        # API returns the decoded plain text; client-side esc() must escape it.
        self.assertIn('<script>alert(1)</script>', titles)
        self.assertNotIn('&lt;script&gt;', titles)


class FixEntitiesCommandTests(TestCase):
    """Tests for the fix_entities management command."""

    def setUp(self):
        self.now = timezone.now()
        self.story = Story.objects.create(
            source='Variety',
            title='Variety &#x201c;Quote&#x201d;',
            excerpt='From the &#x201c;Summer House&#x201d; triangle.',
            url='https://example.com/variety/entities',
            language='en',
            category='entertainment',
            published=self.now,
            url_hash='variety-entities',
            title_fingerprint='old-fingerprint',
        )

    def _call_command(self, apply=False):
        out = StringIO()
        err = StringIO()
        cmd = FixEntitiesCommand(stdout=out, stderr=err)
        cmd.handle(apply=apply)
        return out.getvalue(), err.getvalue()

    def test_dry_run_changes_nothing(self):
        output, _ = self._call_command(apply=False)
        self.story.refresh_from_db()
        self.assertEqual(self.story.title, 'Variety &#x201c;Quote&#x201d;')
        self.assertIn('DRY-RUN', output)
        self.assertIn('Changed:  1', output)

    def test_apply_updates_and_is_idempotent(self):
        output1, _ = self._call_command(apply=True)
        self.story.refresh_from_db()
        self.assertEqual(self.story.title, 'Variety \u201cQuote\u201d')
        self.assertIn('\u201cSummer House\u201d', self.story.excerpt)
        self.assertNotEqual(self.story.title_fingerprint, 'old-fingerprint')
        self.assertIn('Updated 1 stories', output1)

        output2, _ = self._call_command(apply=True)
        self.assertIn('Changed:  0', output2)
        self.assertIn('No changes needed', output2)



class FixEntitiesEncodedTagTests(TestCase):
    """Idempotence when stored titles contain encoded HTML tags."""

    def setUp(self):
        self.now = timezone.now()
        self.story = Story.objects.create(
            source='Test',
            title='&lt;b&gt;bold&lt;/b&gt; &amp;amp;',
            excerpt='Excerpt.',
            url='https://example.com/test/encoded-tags',
            language='en',
            category='world',
            published=self.now,
            url_hash='encoded-tags',
            title_fingerprint='encoded-tags',
        )

    def test_dry_run_then_double_apply_is_idempotent(self):
        out1 = StringIO()
        err1 = StringIO()
        call_command('fix_entities', stdout=out1, stderr=err1)
        dry_output = out1.getvalue()
        self.story.refresh_from_db()
        self.assertEqual(self.story.title, '&lt;b&gt;bold&lt;/b&gt; &amp;amp;')
        self.assertIn('DRY-RUN', dry_output)
        self.assertIn('Changed:  1', dry_output)

        out2 = StringIO()
        err2 = StringIO()
        call_command('fix_entities', '--apply', stdout=out2, stderr=err2)
        apply_output1 = out2.getvalue()
        self.story.refresh_from_db()
        self.assertEqual(self.story.title, '<b>bold</b> &')
        self.assertIn('Changed:  1', apply_output1)

        out3 = StringIO()
        err3 = StringIO()
        call_command('fix_entities', '--apply', stdout=out3, stderr=err3)
        apply_output2 = out3.getvalue()
        self.story.refresh_from_db()
        self.assertEqual(self.story.title, '<b>bold</b> &')
        self.assertIn('Changed:  0', apply_output2)
