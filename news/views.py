from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from collections import OrderedDict
from .models import Story


SOURCE_BIAS = {
    'Reuters': ('Center', '#666', 'https://mediabiasfactcheck.com/reuters/'),
    'AP': ('Center', '#666', 'https://mediabiasfactcheck.com/associated-press/'),
    'BBC': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'NPR': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/npr/'),
    'France 24': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/france-24/'),
    'Deutsche Welle': ('Center', '#666', 'https://mediabiasfactcheck.com/deutsche-welle/'),
    'Al Jazeera': ('Left', '#999', 'https://mediabiasfactcheck.com/al-jazeera/'),
    'CBS News': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/cbs-news/'),
    'ABC News': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/abc-news/'),
    'NBC News': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/nbc-news/'),
    'Fox News': ('Right', '#666', 'https://mediabiasfactcheck.com/fox-news/'),
    'CNN': ('Left', '#999', 'https://mediabiasfactcheck.com/cnn/'),
    'Sky News': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/sky-news/'),
    'Bloomberg': ('Center', '#666', 'https://mediabiasfactcheck.com/bloomberg/'),
    'Forbes': ('Center', '#666', 'https://mediabiasfactcheck.com/forbes/'),
    'Yahoo News': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/yahoo-news/'),
    'Newsweek': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/newsweek/'),
    'Time': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/time/'),
    'Free Press': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'New York Post': ('Right', '#666', 'https://mediabiasfactcheck.com/new-york-post/'),
    'Washington Examiner': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/washington-examiner/'),
    'Daily Caller': ('Right', '#666', 'https://mediabiasfactcheck.com/daily-caller/'),
    'The Federalist': ('Right', '#666', 'https://mediabiasfactcheck.com/the-federalist/'),
    'National Review': ('Right', '#666', 'https://mediabiasfactcheck.com/national-review/'),
    'Daily Wire': ('Right', '#666', 'https://mediabiasfactcheck.com/daily-wire/'),
    'Epoch Times': ('Right', '#666', 'https://mediabiasfactcheck.com/epoch-times/'),
    'Townhall': ('Right', '#666', 'https://mediabiasfactcheck.com/townhall/'),
    'RedState': ('Right', '#666', 'https://mediabiasfactcheck.com/redstate/'),
}

DEFAULT_SOURCES = ['Reuters', 'AP', 'Deutsche Welle', 'Bloomberg', 'Forbes', 'Free Press']

SOURCES = [
    ('Reuters', 'Center'),
    ('AP', 'Center'),
    ('Deutsche Welle', 'Center'),
    ('Bloomberg', 'Center'),
    ('Forbes', 'Center'),
    ('Free Press', 'Center'),
    ('BBC', 'Left-Center'),
    ('CBS News', 'Left-Center'),
    ('ABC News', 'Left-Center'),
    ('NBC News', 'Left-Center'),
    ('Sky News', 'Left-Center'),
    ('NPR', 'Left-Center'),
    ('France 24', 'Left-Center'),
    ('Yahoo News', 'Left-Center'),
    ('Newsweek', 'Left-Center'),
    ('Time', 'Left-Center'),
    ('CNN', 'Left'),
    ('Al Jazeera', 'Left'),
    ('Mother Jones', 'Left'),
    ('HuffPost', 'Left'),
    ('The Nation', 'Left'),
    ('Salon', 'Left'),
    ('Jacobin', 'Left'),
    ('The Intercept', 'Left'),
    ('Democracy Now', 'Left'),
    ('Common Dreams', 'Left'),
    ('Truthout', 'Left'),
    ('Vox', 'Left'),
    ('Washington Examiner', 'Right-Center'),
    ('Townhall', 'Right'),
    ('New York Post', 'Right'),
    ('Daily Caller', 'Right'),
    ('RedState', 'Right'),
    ('The Federalist', 'Right'),
    ('National Review', 'Right'),
    ('Daily Wire', 'Right'),
    ('Epoch Times', 'Right'),
    ('Fox News', 'Right'),
]

CATEGORY_KEYWORDS = {
    'politics': ['trump', 'biden', 'congress', 'senate', 'election', 'vote', 'voting', 'campaign', 'republican', 'democrat', 'president', 'administration', 'governor', 'lawmaker', 'legislation', 'democratic', 'political', 'parliament', 'impeach', 'supreme court', 'ruling', 'policy', 'white house', 'cabinet', 'secretary', 'convention', 'primary', 'ballot', 'midterm', 'senator', 'representative'],
    'business': ['stock market', 'economy', 'economic', 'trade', 'tariff', 'inflation', 'federal reserve', 'gdp', 'recession', 'unemployment', 'jobs report', 'earnings', 'revenue', 'profit', 'bank', 'finance', 'financial', 'investment', 'wall street', 'ceo', 'opec', 'crypto', 'bitcoin', 'bond', 'investor', 'shares', 'commodity', 'crude oil'],
    'technology': ['tech', 'ai ', 'artificial intelligence', 'software', 'startup', 'silicon valley', 'cyberattack', 'hacker', 'data breach', 'digital', 'robot', 'elon musk', 'iphone', 'android', 'chip', 'semiconductor', 'cloud computing', 'openai', 'nvidia', 'meta ', 'google ', 'microsoft', 'apple ', 'amazon ', 'facebook'],
    'science': ['nasa', 'spacex', 'space', 'mars', 'climate change', 'earthquake', 'volcano', 'researcher', 'laboratory', 'experiment', 'discovery', 'species', 'genetic', 'cosmos', 'astronomy'],
    'health': ['hospital', 'doctor', 'medical', 'medicine', 'drug', 'fda ', 'vaccine', 'pandemic', 'cancer', 'diabetes', 'heart disease', 'brain ', 'treatment', 'therapy', 'surgery', 'patient', 'outbreak', 'virus', 'covid', 'epidemic', 'healthcare', 'clinic', 'nurse', 'physician', 'mental health', 'depression', 'anxiety', 'stroke'],
    'sports': ['nba', 'nfl', 'mlb', 'nhl', 'championship', 'playoffs', 'super bowl', 'world cup', 'olympics', 'marathon', 'tennis', 'golf', 'soccer', 'basketball', 'baseball', 'football', 'coach', 'injury', 'tournament', 'athlete', 'score', 'draft', 'trade'],
    'us': ['california', 'texas', 'florida', 'new york', 'washington', 'chicago', 'los angeles', 'miami', 'seattle', 'boston', 'atlanta', 'houston', 'dallas', 'phoenix', 'denver', 'detroit', 'portland', 'philadelphia', 'san francisco', 'san diego', 'austin', 'nashville', 'memphis', 'las vegas', 'sacramento', 'orlando', 'tampa', 'raleigh', 'pittsburgh', 'cleveland', 'cincinnati', 'milwaukee', 'minneapolis', 'indianapolis', 'columbus', 'charlotte', 'kansas city', 'st. louis', 'new orleans', 'baltimore', 'maryland', 'virginia', 'nevada', 'arizona', 'georgia', 'north carolina', 'pennsylvania', 'ohio', 'michigan', 'illinois'],
    'world': ['ukraine', 'russia', 'china', 'iran', 'israel', 'gaza', 'middle east', 'europe', 'asia', 'africa', 'latin america', 'european union', 'nato', 'war', 'ceasefire', 'diplomat', 'summit', 'border', 'immigration', 'refugee', 'global', 'international'],
}

CATEGORY_NAMES = OrderedDict([
    ('all', 'All'),
    ('most_covered', 'Most Covered'),
    ('world', 'World'),
    ('us', 'US'),
    ('politics', 'Politics'),
    ('business', 'Business'),
    ('technology', 'Technology'),
    ('science', 'Science'),
    ('health', 'Health'),
    ('sports', 'Sports'),
])


def categorize_story(title):
    title_lower = title.lower()
    
    for keyword in CATEGORY_KEYWORDS['sports']:
        if keyword in title_lower:
            return 'sports'
    
    for keyword in CATEGORY_KEYWORDS['health']:
        if keyword in title_lower:
            return 'health'
    
    for keyword in CATEGORY_KEYWORDS['technology']:
        if keyword in title_lower:
            return 'technology'
    
    for keyword in CATEGORY_KEYWORDS['science']:
        if keyword in title_lower:
            return 'science'
    
    for keyword in CATEGORY_KEYWORDS['business']:
        if keyword in title_lower:
            return 'business'
    
    for keyword in CATEGORY_KEYWORDS['politics']:
        if keyword in title_lower:
            return 'politics'
    
    for keyword in CATEGORY_KEYWORDS['us']:
        if keyword in title_lower:
            return 'us'
    
    for keyword in CATEGORY_KEYWORDS['world']:
        if keyword in title_lower:
            return 'world'
    
    return 'world'


def get_story_categories(title):
    title_lower = title.lower()
    categories = []
    
    for keyword in CATEGORY_KEYWORDS['politics']:
        if keyword in title_lower:
            categories.append('politics')
            break
    
    for keyword in CATEGORY_KEYWORDS['business']:
        if keyword in title_lower:
            categories.append('business')
            break
    
    for keyword in CATEGORY_KEYWORDS['technology']:
        if keyword in title_lower:
            categories.append('technology')
            break
    
    for keyword in CATEGORY_KEYWORDS['science']:
        if keyword in title_lower:
            categories.append('science')
            break
    
    for keyword in CATEGORY_KEYWORDS['health']:
        if keyword in title_lower:
            categories.append('health')
            break
    
    for keyword in CATEGORY_KEYWORDS['sports']:
        if keyword in title_lower:
            categories.append('sports')
            break
    
    for keyword in CATEGORY_KEYWORDS['us']:
        if keyword in title_lower:
            categories.append('us')
            break
    
    for keyword in CATEGORY_KEYWORDS['world']:
        if keyword in title_lower:
            categories.append('world')
            break
    
    if not categories:
        categories = ['world']
    
    return categories


def home(request):
    cutoff = timezone.now() - timedelta(hours=24)
    
    selected_sources_param = request.GET.get('sources')
    
    if selected_sources_param == 'all':
        selected_sources = [s[0] for s in SOURCES]
    elif selected_sources_param == 'center':
        selected_sources = [s[0] for s in SOURCES if s[1] == 'Center']
    elif selected_sources_param == 'left-center':
        selected_sources = [s[0] for s in SOURCES if s[1] == 'Left-Center']
    elif selected_sources_param == 'left':
        selected_sources = [s[0] for s in SOURCES if s[1] == 'Left']
    elif selected_sources_param == 'right':
        selected_sources = [s[0] for s in SOURCES if s[1] == 'Right']
    elif selected_sources_param == 'clear' or selected_sources_param == '':
        selected_sources = []
    elif selected_sources_param:
        selected_sources = selected_sources_param.split(',')
    else:
        selected_sources = DEFAULT_SOURCES
    
    all_stories = list(Story.objects.filter(published__gte=cutoff))
    
    for story in all_stories:
        story.story_categories = get_story_categories(story.title)
        bias_info = SOURCE_BIAS.get(story.source, ('Unknown', '#999', 'https://mediabiasfactcheck.com/'))
        story.bias_label = bias_info[0]
        story.bias_color = bias_info[1]
        story.bias_link = bias_info[2]
    
    stories = [s for s in all_stories if s.source in selected_sources]
    
    most_covered_stories = []
    story_groups = {}
    
    for story in stories:
        normalized_title = story.title.lower()[:150]
        key_words = set(normalized_title.split()) - {'the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'and', 'or', 'is', 'are', 'was', 'were', 'be', 'been', 'has', 'have', 'had', 'it', 'its', 'this', 'that', 'from', 'as', 'but', 'not', 'no', 'so', 'if', 'or', 'when', 'what', 'which', 'who', 'how', 'than', 'then', 'them', 'they', 'their', 'there', 'here', 'will', 'would', 'can', 'could', 'should', 'may', 'might', 'must'}
        key = ' '.join(sorted(key_words))[:100]
        
        if key not in story_groups:
            story_groups[key] = []
        story_groups[key].append(story)
    
    for key, title_stories in story_groups.items():
        if len(title_stories) >= 2:
            base_story = title_stories[0]
            base_story.covered_by_count = len(title_stories)
            base_story.covered_by_sources = list(set(s.source for s in title_stories))
            most_covered_stories.append(base_story)
    
    most_covered_stories.sort(key=lambda x: -x.covered_by_count)
    most_covered_stories = most_covered_stories[:20]
    
    grouped = {}
    for cat_id, cat_name in CATEGORY_NAMES.items():
        if cat_id == 'all':
            cat_stories = list(stories)
        elif cat_id == 'most_covered':
            cat_stories = most_covered_stories
        else:
            cat_stories = [s for s in stories if cat_id in s.story_categories]
        grouped[cat_id] = {
            'name': cat_name,
            'stories': cat_stories
        }
    
    return render(request, 'home.html', {
        'grouped': grouped,
        'sources': SOURCES,
        'selected_sources': selected_sources,
        'default_sources': DEFAULT_SOURCES
    })
