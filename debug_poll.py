import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'
import django
django.setup()

from django.test import Client
from django.utils import timezone
from datetime import timedelta
from news.models import Story, Poll

# Create data
for i in range(12):
    Story.objects.create(source='BBC', title=f'Test story {i}', excerpt='Test', url=f'https://debug.example.com/s{i}', language='en', category='world', published=timezone.now(), url_hash=f'dh{i}', title_fingerprint=f'df{i}')

Poll.objects.create(language='en', question='Test poll question?', options=['Option 1', 'Option 2'], poll_type='topical', status='active', is_active=True, ends_at=timezone.now() + timedelta(days=7))

c = Client()
r = c.get('/')
content = r.content.decode()
print('Status:', r.status_code)
print('Stories in all tab:', content.count('data-title="test story'))
print('Poll card:', 'poll-card-inline' in content)
print('Poll question:', 'Test poll question?' in content)
