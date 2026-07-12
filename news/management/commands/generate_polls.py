#!/usr/bin/env python
"""Generate poll candidates daily using OpenAI for all 13 languages.

Usage:
    python manage.py generate_polls
    python manage.py generate_polls --dry-run      # Don't save to DB
    python manage.py generate_polls --language es  # Only one language
    python manage.py generate_polls --num 5        # Generate 5 per language

Environment:
    OPENAI_API_KEY     Required
    OPENAI_MODEL       Optional (default: gpt-4o-mini)
    EMAIL_HOST         Required for notifications
    EMAIL_HOST_USER    Required for notifications
    EMAIL_HOST_PASSWORD Required for notifications
"""

import json
import os
from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

from news.models import Poll, Story, PollGenerationConfig
from news.languages import LANGUAGE_NAMES, SUPPORTED_LANGUAGES


SYSTEM_PROMPT = """You are an expert poll designer for 24HourWire, a global, privacy-focused news aggregator that values neutrality, clarity, and engagement across many languages and cultures.

Your goal is to generate high-quality polls that feel native to the target language and culture. Create a healthy mix of:
- Timely/news-related polls (tied to current events)
- Fun/light/friendly polls (daily life, preferences, culture, humor)
- Thoughtful opinion polls (not partisan or inflammatory)

Strict rules:
- Questions must be short, clear, and natural in the target language.
- Never create leading, loaded, or politically inflammatory questions.
- Avoid anything that could be seen as endorsing a political party, candidate, or ideology.
- Options must be balanced and mutually exclusive where possible.
- For fun polls, lean playful and light rather than edgy.
- Each poll must have 2–4 options (3 is ideal for most).
- Generate polls that will feel relevant for the next 7–30 days.

Output ONLY valid JSON in this exact structure (no markdown, no extra text):

[
  {
    "language": "es",
    "question": "La pregunta en español aquí",
    "options": ["Opción 1", "Opción 2", "Opción 3"],
    "poll_type": "fun" | "topical" | "opinion" | "lifestyle" | "sports" | "culture",
    "english_translation": "English version of the question for review",
    "suggested_duration_days": 14
  }
]

Valid poll_type values: topical, fun, lifestyle, opinion, sports, culture."""


def build_user_prompt(language, language_name, num_polls, current_date, recent_topics, existing_poll_questions):
    """Build the user prompt for OpenAI."""
    return f"""Generate {num_polls} new poll ideas for the following language: {language} ({language_name}).

Current date: {current_date}

Recent high-interest topics from the last 48 hours (use these for topical ideas when relevant):
{recent_topics}

Existing active or recently active polls (avoid creating similar questions):
{existing_poll_questions}

Requirements:
- Aim for roughly this distribution: 35% topical, 30% fun, 20% lifestyle, 10% opinion, 5% sports/culture.
- Prioritize variety. Do not repeat themes from the existing polls list.
- Some polls should feel evergreen and fun even if not tied to news.
- For non-English languages, make the actual poll feel natural to native speakers.

Return only the JSON array."""


class Command(BaseCommand):
    help = 'Generate poll candidates using OpenAI for all supported languages'

    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            type=str,
            help='Generate for a specific language code only (e.g., es)',
        )
        parser.add_argument(
            '--num',
            type=int,
            default=3,
            help='Number of polls to generate per language (default: 3)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show generated polls without saving to database',
        )

    def handle(self, *args, **options):
        # Support multiple LLM providers via environment variables
        # Priority: XAI_API_KEY > GROQ_API_KEY > GOOGLE_API_KEY > OPENAI_API_KEY
        api_key = (
            os.environ.get('XAI_API_KEY') or
            os.environ.get('GROQ_API_KEY') or
            os.environ.get('GOOGLE_API_KEY') or
            os.environ.get('OPENAI_API_KEY')
        )
        if not api_key:
            self.stdout.write(self.style.ERROR(
                'No LLM API key found. Set one of: XAI_API_KEY (Grok), GROQ_API_KEY (recommended, free $200), '
                'GOOGLE_API_KEY (free 1500 req/day), or OPENAI_API_KEY (cheap).'
            ))
            return

        # Determine provider and configure client
        provider = self._detect_provider()
        client, model = self._create_client(provider, api_key)
        if not client:
            return
        dry_run = options['dry_run']
        target_language = options['language']
        
        # Load config from database (allows staff to adjust via /polls/manage/)
        config = PollGenerationConfig.get_active_config()
        num_polls = options['num'] if options['num'] != 3 else config.polls_per_language
        
        if not config.is_enabled and not dry_run:
            self.stdout.write(self.style.WARNING(
                'Automatic poll generation is disabled in PollGenerationConfig. '
                'Use --dry-run to preview, or enable in /polls/manage/.'
            ))
            return

        languages = [target_language] if target_language else sorted(SUPPORTED_LANGUAGES)
        
        # Validate target language
        if target_language and target_language not in SUPPORTED_LANGUAGES:
            self.stdout.write(self.style.ERROR(
                f"Unsupported language: {target_language}. Supported: {', '.join(sorted(SUPPORTED_LANGUAGES))}"
            ))
            return

        current_date = timezone.now().strftime('%Y-%m-%d')
        total_created = 0
        total_errors = 0
        created_polls = []

        for lang in languages:
            lang_name = LANGUAGE_NAMES.get(lang, lang)
            self.stdout.write(f"\nGenerating {num_polls} polls for {lang_name} ({lang})...")

            # Gather context
            recent_topics = self._get_recent_topics(lang)
            existing_questions = self._get_existing_poll_questions(lang)

            user_prompt = build_user_prompt(
                language=lang,
                language_name=lang_name,
                num_polls=num_polls,
                current_date=current_date,
                recent_topics=recent_topics,
                existing_poll_questions=existing_questions,
            )

            # Retry logic for transient LLM failures
            polls_data = None
            last_error = None
            for attempt in range(1, 4):
                try:
                    # Use the appropriate API method for the provider
                    # (try/except instead of hasattr so tests with MagicMock work correctly)
                    try:
                        response = client.chat.completions.create(
                            model=model,
                            messages=[
                                {"role": "system", "content": SYSTEM_PROMPT},
                                {"role": "user", "content": user_prompt},
                            ],
                            temperature=0.8,
                            max_tokens=2000,
                        )
                    except AttributeError:
                        # Google Gemini wrapper
                        response = client.chat_completions_create(
                            model=model,
                            messages=[
                                {"role": "system", "content": SYSTEM_PROMPT},
                                {"role": "user", "content": user_prompt},
                            ],
                            temperature=0.8,
                            max_tokens=2000,
                        )
                    raw_content = response.choices[0].message.content.strip()
                    polls_data = self._parse_response(raw_content)
                    break
                except Exception as e:
                    last_error = e
                    self.stdout.write(self.style.WARNING(
                        f"  LLM attempt {attempt}/3 failed for {lang}: {e}"
                    ))
                    import time
                    time.sleep(2 ** attempt)  # Exponential backoff: 2, 4, 8 seconds
            
            if polls_data is None:
                total_errors += 1
                self.stdout.write(self.style.ERROR(
                    f"  Failed after 3 attempts for {lang}: {last_error}"
                ))
                continue
            
            for poll_data in polls_data:
                if dry_run:
                    self.stdout.write(self.style.NOTICE(
                        f"  [DRY RUN] {poll_data['question'][:60]}..."
                    ))
                    continue
                
                # Skip if question already exists (idempotency)
                if Poll.objects.filter(
                    language=lang,
                    question__iexact=poll_data['question'],
                    created_at__gte=timezone.now() - timedelta(days=30),
                ).exists():
                    self.stdout.write(self.style.WARNING(
                        f"  Skipped duplicate: {poll_data['question'][:50]}..."
                    ))
                    continue
                
                # Calculate expiration
                duration = poll_data.get('suggested_duration_days', 14)
                ends_at = timezone.now() + timedelta(days=duration)
                
                # For English polls, translation is same as question
                english_translation = poll_data.get('english_translation', poll_data['question'])
                if lang == 'en':
                    english_translation = poll_data['question']
                
                poll = Poll.objects.create(
                    language=lang,
                    question=poll_data['question'],
                    options=poll_data['options'],
                    poll_type=poll_data.get('poll_type', 'topical'),
                    english_translation=english_translation,
                    status='pending_review',
                    is_active=False,
                    ends_at=ends_at,
                    source='auto',
                )
                total_created += 1
                created_polls.append(poll)
                self.stdout.write(self.style.SUCCESS(
                    f"  Created: {poll.question[:60]}..."
                ))

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Created {total_created} polls, {total_errors} errors."
        ))

        # Send email notification only when actual new polls were created
        if total_created > 0 and not dry_run:
            self._send_notification_email(total_created, total_errors, created_polls)

    def _get_recent_topics(self, language):
        """Get recent story titles as topical inspiration."""
        cutoff = timezone.now() - timedelta(hours=48)
        stories = Story.objects.filter(
            language=language,
            published__gte=cutoff,
        ).order_by('-published')[:15]
        
        if not stories:
            return "No recent stories available."
        
        topics = []
        for s in stories:
            topics.append(f"- {s.title[:100]}")
        return "\n".join(topics)

    def _get_existing_poll_questions(self, language):
        """Get recent active/recent poll questions to avoid repetition."""
        cutoff = timezone.now() - timedelta(days=30)
        polls = Poll.objects.filter(
            language=language,
            created_at__gte=cutoff,
        ).order_by('-created_at')[:20]
        
        if not polls:
            return "No existing polls."
        
        lines = []
        for p in polls:
            lines.append(f"- {p.question[:100]}")
        return "\n".join(lines)

    def _parse_response(self, raw_content):
        """Parse OpenAI JSON response, handling common formatting issues."""
        # Strip markdown code fences if present
        content = raw_content.strip()
        if content.startswith('```json'):
            content = content[7:]
        if content.startswith('```'):
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
        
        data = json.loads(content)
        
        # Ensure it's a list
        if isinstance(data, dict) and 'polls' in data:
            data = data['polls']
        if not isinstance(data, list):
            raise ValueError(f"Expected JSON array, got {type(data).__name__}")
        
        # Validate each poll
        valid_polls = []
        for item in data:
            if not isinstance(item, dict):
                continue
            if 'question' not in item or 'options' not in item:
                continue
            if not isinstance(item['options'], list) or len(item['options']) < 2:
                continue
            # Normalize poll_type
            pt = item.get('poll_type', 'topical')
            if pt not in [c[0] for c in Poll.POLL_TYPE_CHOICES]:
                pt = 'topical'
            item['poll_type'] = pt
            valid_polls.append(item)
        
        return valid_polls

    def _send_notification_email(self, created_count, error_count, created_polls):
        """Send simple email notification to admin with poll summaries."""
        subject = f"24HourWire: {created_count} new polls ready for review"
        
        poll_list = "\n".join(
            f"- [{p.language}] {p.question[:80]}"
            for p in created_polls[:10]
        )
        if len(created_polls) > 10:
            poll_list += f"\n... and {len(created_polls) - 10} more"
        
        body = (
            f"{created_count} new poll candidates were generated and are ready for review.\n\n"
            f"New polls:\n{poll_list}\n\n"
            f"Review them here:\n"
            f"https://24hourwire.news/polls/manage/?status=pending_review\n\n"
            f"Errors: {error_count}\n"
            f"Generated at: {timezone.now().strftime('%Y-%m-%d %H:%M UTC')}\n"
        )
        
        from_email = getattr(settings, 'EMAIL_FROM', settings.EMAIL_HOST_USER)
        recipient = 'admin@24hourwire.news'
        
        if not settings.EMAIL_HOST or not from_email:
            self.stdout.write(self.style.WARNING(
                'Email settings not configured. Skipping notification.'
            ))
            return
        
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=from_email,
                recipient_list=[recipient],
                fail_silently=True,
            )
            self.stdout.write(self.style.SUCCESS('Notification email sent to admin.'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Failed to send email: {e}'))

    def _detect_provider(self):
        """Determine which LLM provider to use based on env vars."""
        if os.environ.get('XAI_API_KEY'):
            return 'xai'
        if os.environ.get('GROQ_API_KEY'):
            return 'groq'
        if os.environ.get('GOOGLE_API_KEY'):
            return 'google'
        return 'openai'

    def _create_client(self, provider, api_key):
        """Create LLM client and select default model for the provider."""
        if provider == 'xai':
            try:
                from openai import OpenAI
                # xAI Grok is OpenAI-compatible — just change base_url
                base_url = os.environ.get('XAI_BASE_URL', 'https://api.x.ai/v1')
                client = OpenAI(api_key=api_key, base_url=base_url)
                model = os.environ.get('XAI_MODEL', 'grok-3')
                self.stdout.write(self.style.SUCCESS(f'Using xAI Grok with model {model}'))
                return client, model
            except ImportError:
                self.stdout.write(self.style.ERROR(
                    'openai package required for xAI Grok. Run: pip install openai'
                ))
                return None, None

        elif provider == 'groq':
            try:
                from openai import OpenAI
                # Groq is OpenAI-compatible — just change base_url
                base_url = os.environ.get('GROQ_BASE_URL', 'https://api.groq.com/openai/v1')
                client = OpenAI(api_key=api_key, base_url=base_url)
                model = os.environ.get('GROQ_MODEL', 'llama-3.3-70b-versatile')
                self.stdout.write(self.style.SUCCESS(f'Using Groq with model {model}'))
                return client, model
            except ImportError:
                self.stdout.write(self.style.ERROR(
                    'openai package required for Groq. Run: pip install openai'
                ))
                return None, None

        elif provider == 'google':
            try:
                import google.generativeai as genai
                genai.configure(api_key=api_key)
                model_name = os.environ.get('GOOGLE_MODEL', 'gemini-1.5-flash')
                self.stdout.write(self.style.SUCCESS(f'Using Google Gemini ({model_name})'))
                # Return a wrapper that mimics OpenAI's chat.completions.create interface
                return GoogleGeminiWrapper(model_name), model_name
            except ImportError:
                self.stdout.write(self.style.ERROR(
                    'google-generativeai package required. Run: pip install google-generativeai'
                ))
                return None, None

        else:  # openai
            try:
                from openai import OpenAI
                client = OpenAI(api_key=api_key)
                model = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')
                self.stdout.write(self.style.SUCCESS(f'Using OpenAI with model {model}'))
                return client, model
            except ImportError:
                self.stdout.write(self.style.ERROR(
                    'openai package not installed. Run: pip install openai'
                ))
                return None, None


class GoogleGeminiWrapper:
    """Minimal wrapper to make Google Gemini look like OpenAI's client."""

    def __init__(self, model_name):
        import google.generativeai as genai
        self.model = genai.GenerativeModel(model_name)

    class _FakeChoice:
        def __init__(self, content):
            self.message = self._FakeMessage(content)

    class _FakeMessage:
        def __init__(self, content):
            self.content = content

    class _FakeResponse:
        def __init__(self, choices):
            self.choices = choices

    def chat_completions_create(self, **kwargs):
        """Accept same kwargs as OpenAI but use Gemini API."""
        messages = kwargs.get('messages', [])
        # Concatenate system + user prompts
        prompt_parts = []
        for msg in messages:
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            label = 'System' if role == 'system' else 'User' if role == 'user' else 'Assistant'
            prompt_parts.append(f"[{label}]\n{content}")
        full_prompt = "\n\n".join(prompt_parts)

        response = self.model.generate_content(
            full_prompt,
            generation_config={
                'temperature': kwargs.get('temperature', 0.8),
                'max_output_tokens': kwargs.get('max_tokens', 2000),
            }
        )
        content = response.text if hasattr(response, 'text') else str(response)
        return self._FakeResponse([self._FakeChoice(content)])
