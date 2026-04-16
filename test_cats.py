#!/usr/bin/env python
"""Quick test of categorization system."""
import sys
import os

# Setup Django
os.chdir(r'C:\Users\tomcl\Source\24hourwire')
sys.path.insert(0, r'C:\Users\tomcl\Source\24hourwire')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from news.views import get_story_categories

# Test cases
test_titles = [
    ('Biden signs executive order on climate change', ['politics', 'us']),
    ('Supreme Court rules on voting rights', ['politics', 'us']),
    ('Fed raises interest rates to combat inflation', ['business']),
    ('OpenAI releases new GPT model', ['technology']),
    ('NASA discovers water on Mars', ['science']),
    ('FDA approves new cancer treatment', ['health']),
    ('NBA playoffs: Lakers advance to finals', ['sports']),
    ('South Africa considers fuel levy cut', ['world']),
    ('UK Parliament debates Brexit trade deal', ['politics', 'world']),
    ('Tesla announces self-driving car update', ['technology']),
    ('Wall Street reacts to quarterly earnings', ['business']),
    ('WHO declares end of pandemic emergency', ['health', 'world']),
]

print('Testing categorization with threshold=3:')
print('=' * 70)

passed = 0
failed = 0

for title, expected in test_titles:
    cats = get_story_categories(title)
    status = '✓' if all(e in cats for e in expected) else '✗'
    if status == '✓':
        passed += 1
    else:
        failed += 1
    print(f'{status} {title[:55]:<55}')
    print(f'   Expected: {expected}')
    print(f'   Got:      {cats}')
    print()

print(f'\nPassed: {passed}/{len(test_titles)} ({passed/len(test_titles)*100:.0f}%)')
