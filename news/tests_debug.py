from django.test import TestCase, Client
from django.utils import timezone
from datetime import timedelta
from news.models import Story, Poll

class PollDebugInactiveTest(TestCase):
    def test_debug_inactive(self):
        for i in range(12):
            Story.objects.create(
                source='BBC', title=f'Test story {i}', excerpt='Test',
                url=f'https://debug.example.com/s{i}', language='en', category='world',
                published=timezone.now(), url_hash=f'h{i}', title_fingerprint=f'f{i}'
            )
        
        poll = Poll.objects.create(
            language='en', question='Test poll question?', options=['Option 1', 'Option 2'],
            poll_type='topical', status='active', is_active=True,
            ends_at=timezone.now() + timedelta(days=7)
        )
        
        poll.is_active = False
        poll.save()
        
        c = Client()
        r = c.get('/')
        content = r.content.decode()
        
        print(f"\n=== DEBUG INACTIVE ===")
        print(f"Status: {r.status_code}")
        print(f"Poll card in response: {'poll-card-inline' in content}")
        print(f"=== END DEBUG ===\n")
        
        self.assertNotContains(r, 'poll-card-inline')
