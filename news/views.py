from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from collections import OrderedDict
from django.http import HttpResponse
from django.core.management import call_command
import threading
import re
from .models import Story
from .sources_config import LANGUAGE_SOURCE_INFO, DEFAULT_SOURCES, SOURCES, LANGUAGE_NAMES, PAYWALLED_SOURCES


CATEGORY_KEYWORDS = {
    'politics': [
        'trump', 'biden', 'congress', 'senate', 'election', 'vote', 'voting', 'campaign',
        'republican', 'democrat', 'president', 'administration', 'governor', 'lawmaker',
        'legislation', 'democratic', 'political', 'parliament', 'impeach', 'supreme court',
        'ruling', 'policy', 'white house', 'cabinet', 'secretary', 'convention', 'primary',
        'ballot', 'midterm', 'senator', 'representative', 'gop', 'dnc', 'rnc', 'capitol',
        'partisan', 'bipartisan', 'filibuster', 'veto', 'executive order', 'federal',
        # Spanish
        'elecciones', 'gobierno', 'presidente', 'congreso', 'senado', 'voto', 'campaña',
        'partido', 'política', 'ministro', 'ley', 'diputado', 'alcalde', 'gobernador',
        'elección', 'parlamento', 'constitución', 'reforma', 'oposición'
    ],
    'business': [
        'stock market', 'economy', 'economic', 'trade', 'tariff', 'inflation', 'federal reserve',
        'gdp', 'recession', 'unemployment', 'jobs report', 'earnings', 'revenue', 'profit',
        'bank', 'finance', 'financial', 'investment', 'wall street', 'ceo', 'opec', 'crypto',
        'bitcoin', 'bond', 'investor', 'shares', 'commodity', 'crude oil', 'dow jones',
        'nasdaq', 's&p', 'ipo', 'merger', 'acquisition', 'quarterly', 'fiscal',
        'interest rate', 'treasury', 'market', 'business', 'corporate', 'startup',
        # Spanish
        'bolsa', 'economía', 'mercado', 'empresa', 'negocio', 'banco', 'finanzas',
        'inversión', 'dólar', 'peso', ' euro ', 'inflación', 'desempleo', 'pib',
        'acciones', 'divisa', 'crédito', 'deuda', 'exportación', 'importación'
    ],
    'technology': [
        'tech', 'ai ', 'artificial intelligence', 'software', 'startup', 'silicon valley',
        'cyberattack', 'hacker', 'data breach', 'digital', 'robot', 'elon musk', 'iphone',
        'android', 'chip', 'semiconductor', 'cloud computing', 'openai', 'nvidia', 'meta ',
        'google ', 'microsoft', 'apple ', 'amazon ', 'facebook', 'twitter', 'x ', 'tesla',
        'cybersecurity', 'blockchain', 'cryptocurrency', 'app ', 'algorithm', 'machine learning',
        'deep learning', 'chatgpt', 'neural', 'quantum computing', '5g', 'iot',
        # Spanish
        'tecnología', 'inteligencia artificial', 'software', 'ciberataque', 'digital',
        'robot', 'aplicación', 'smartphone', 'internet', 'computación', 'datos',
        'ciberseguridad', 'algoritmo', 'plataforma', 'redes sociales'
    ],
    'science': [
        'nasa', 'spacex', 'space', 'mars', 'climate change', 'earthquake', 'volcano',
        'researcher', 'laboratory', 'experiment', 'discovery', 'species', 'genetic',
        'cosmos', 'astronomy', 'physics', 'chemistry', 'biology', 'geology', 'ocean',
        'arctic', 'antarctic', 'fossil', 'dinosaur', 'evolution', 'ecosystem', 'biodiversity',
        'telescope', 'satellite', 'rocket', 'asteroid', 'comet', 'solar', 'lunar',
        'planet', 'galaxy', 'universe', 'quantum', 'molecule', 'atom', 'nuclear',
        # Spanish
        'ciencia', 'investigación', 'descubrimiento', 'especie', 'genético', 'clima',
        'terremoto', 'volcán', 'planeta', 'espacio', 'universo', 'física', 'química',
        'biología', 'laboratorio', 'estudio', 'científico', 'nasa', 'astronáutica'
    ],
    'health': [
        'hospital', 'doctor', 'medical', 'medicine', 'drug', 'fda ', 'vaccine', 'pandemic',
        'cancer', 'diabetes', 'heart disease', 'brain ', 'treatment', 'therapy', 'surgery',
        'patient', 'outbreak', 'virus', 'covid', 'epidemic', 'healthcare', 'clinic', 'nurse',
        'physician', 'mental health', 'depression', 'anxiety', 'stroke', 'symptom', 'diagnosis',
        'clinical trial', 'pharmaceutical', 'opioid', 'obesity', 'nutrition', 'fitness',
        'exercise', 'sleep', 'stress', 'immunity', 'infection', 'antibiotic', 'chronic',
        'acute', 'emergency', 'pediatric', 'geriatric', 'oncology', 'cardiology',
        # Spanish
        'hospital', 'médico', 'medicina', 'vacuna', 'pandemia', 'salud', 'enfermedad',
        'tratamiento', 'virus', 'clínica', 'paciente', 'cirugía', 'terapia', 'síntoma',
        'diagnóstico', 'farmacéutico', 'nutrición', 'ejercicio', 'bienestar', 'covid'
    ],
    'sports': [
        'nba', 'nfl', 'mlb', 'nhl', 'championship', 'playoffs', 'super bowl', 'world cup',
        'olympics', 'marathon', 'tennis', 'golf', 'soccer', 'basketball', 'baseball',
        'football', 'coach', 'injury', 'tournament', 'athlete', 'score', 'draft', 'trade',
        'fifa', 'uefa', 'premier league', 'la liga', 'serie a', ' bundesliga', 'ligue 1',
        'champions league', 'world series', 'grand slam', 'wimbledon', 'masters',
        'quarterback', 'pitcher', 'striker', 'midfielder', 'goalkeeper', 'referee',
        'stadium', 'arena', 'league', 'division', 'conference', 'wild card', 'mvp',
        'all-star', 'rookie', 'veteran', 'retirement', 'contract', 'free agent',
        # Spanish
        'fútbol', 'liga', 'champions', 'copa', 'mundial', 'olimpiadas', 'deporte',
        'equipo', 'jugador', 'partido', 'gol', 'tenis', 'baloncesto', 'béisbol',
        'entrenador', 'estadio', 'torneo', 'campeonato', 'selección', 'árbitro',
        'clásico', 'derby', 'ascenso', 'descenso', 'tabla', 'posiciones'
    ],
    'us': [
        'california', 'texas', 'florida', 'new york', 'washington', 'chicago', 'los angeles',
        'miami', 'seattle', 'boston', 'atlanta', 'houston', 'dallas', 'phoenix', 'denver',
        'detroit', 'portland', 'philadelphia', 'san francisco', 'san diego', 'austin',
        'nashville', 'memphis', 'las vegas', 'sacramento', 'orlando', 'tampa', 'raleigh',
        'pittsburgh', 'cleveland', 'cincinnati', 'milwaukee', 'minneapolis', 'indianapolis',
        'columbus', 'charlotte', 'kansas city', 'st. louis', 'new orleans', 'baltimore',
        'maryland', 'virginia', 'nevada', 'arizona', 'georgia', 'north carolina',
        'pennsylvania', 'ohio', 'michigan', 'illinois', 'new jersey', 'massachusetts',
        'connecticut', 'colorado', 'oregon', 'washington state', 'idaho', 'utah',
        'alabama', 'south carolina', 'tennessee', 'kentucky', 'indiana', 'wisconsin',
        'iowa', 'nebraska', 'kansas', 'oklahoma', 'missouri', 'arkansas', 'louisiana',
        'mississippi', 'alaska', 'hawaii', 'fbi', 'cia', 'pentagon', 'capitol hill',
        'american', 'americans', 'u.s.', 'united states', 'america', 'midwest', 'south',
        'northeast', 'west coast', 'east coast', 'gulf', 'great lakes',
        # Spanish (US-related)
        'estados unidos', 'ee.uu.', 'norteamérica', 'florida', 'texas', 'california',
        'nueva york', 'miami', 'los ángeles', 'chicago', 'washington'
    ],
    'world': [
        'ukraine', 'russia', 'china', 'iran', 'israel', 'gaza', 'middle east', 'europe',
        'asia', 'africa', 'latin america', 'european union', 'nato', 'war', 'ceasefire',
        'diplomat', 'summit', 'border', 'immigration', 'refugee', 'global', 'international',
        'united nations', 'un ', 'who ', 'brexit', 'sanctions', 'embassy', 'foreign',
        'treaty', 'alliance', 'conflict', 'military', 'army', 'navy', 'air force',
        'missile', 'nuclear', 'weapon', 'terror', 'extremist', 'rebel', 'insurgent',
        'peacekeeping', 'humanitarian', 'crisis', 'disaster', 'famine', 'drought',
        'flood', 'hurricane', 'typhoon', 'earthquake', 'tsunami', 'volcano',
        # Spanish
        'ucrania', 'rusia', 'china', 'irán', 'israel', 'gaza', 'medio oriente', 'europa',
        'asia', 'áfrica', 'américa latina', 'guerra', 'diplomático', 'inmigración',
        'refugiado', 'mundial', 'internacional', 'onu', 'otan', 'conflicto', 'crisis',
        'militar', 'ejército', 'paz', 'acuerdo', 'tratado', 'sanciones'
    ],
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

CATEGORY_NAMES_ES = OrderedDict([
    ('all', 'Todo'),
    ('most_covered', 'Más Cubierto'),
    ('world', 'Mundo'),
    ('us', 'EE.UU.'),
    ('politics', 'Política'),
    ('business', 'Negocios'),
    ('technology', 'Tecnología'),
    ('science', 'Ciencia'),
    ('health', 'Salud'),
    ('sports', 'Deportes'),
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
    
    # Check each category - story can be in multiple categories
    # Order matters: more specific categories first
    
    # Sports (very specific keywords)
    sports_matches = 0
    for keyword in CATEGORY_KEYWORDS['sports']:
        if keyword in title_lower:
            sports_matches += 1
            if sports_matches >= 1:
                categories.append('sports')
                break
    
    # Health (specific)
    health_matches = 0
    for keyword in CATEGORY_KEYWORDS['health']:
        if keyword in title_lower:
            health_matches += 1
            if health_matches >= 1:
                categories.append('health')
                break
    
    # Technology (specific)
    tech_matches = 0
    for keyword in CATEGORY_KEYWORDS['technology']:
        if keyword in title_lower:
            tech_matches += 1
            if tech_matches >= 1:
                categories.append('technology')
                break
    
    # Science (specific)
    science_matches = 0
    for keyword in CATEGORY_KEYWORDS['science']:
        if keyword in title_lower:
            science_matches += 1
            if science_matches >= 1:
                categories.append('science')
                break
    
    # Business (specific)
    business_matches = 0
    for keyword in CATEGORY_KEYWORDS['business']:
        if keyword in title_lower:
            business_matches += 1
            if business_matches >= 1:
                categories.append('business')
                break
    
    # Politics (specific)
    politics_matches = 0
    for keyword in CATEGORY_KEYWORDS['politics']:
        if keyword in title_lower:
            politics_matches += 1
            if politics_matches >= 1:
                categories.append('politics')
                break
    
    # US (very broad, check after more specific categories)
    us_matches = 0
    for keyword in CATEGORY_KEYWORDS['us']:
        if keyword in title_lower:
            us_matches += 1
            if us_matches >= 1:
                categories.append('us')
                break
    
    # World (broad, check last)
    world_matches = 0
    for keyword in CATEGORY_KEYWORDS['world']:
        if keyword in title_lower:
            world_matches += 1
            if world_matches >= 1:
                categories.append('world')
                break
    
    # Default to 'world' if no categories matched
    if not categories:
        categories = ['world']
    
    return categories


def home(request):
    cutoff = timezone.now() - timedelta(hours=24)
    
    # Get language from request
    language = request.GET.get('lang', 'en')
    if language not in SOURCES:
        language = 'en'
    
    # Get sources for this language
    lang_sources = SOURCES.get(language, SOURCES['en'])
    lang_default_sources = DEFAULT_SOURCES.get(language, DEFAULT_SOURCES['en'])
    lang_source_info = LANGUAGE_SOURCE_INFO.get(language, LANGUAGE_SOURCE_INFO['en'])
    category_names = CATEGORY_NAMES_ES if language == 'es' else CATEGORY_NAMES
    
    selected_sources_param = request.GET.get('sources')
    
    if selected_sources_param == 'all':
        selected_sources = [s[0] for s in lang_sources]
    elif selected_sources_param == 'center':
        selected_sources = [s[0] for s in lang_sources if s[1] == 'Center']
    elif selected_sources_param == 'left-center':
        selected_sources = [s[0] for s in lang_sources if s[1] == 'Left-Center']
    elif selected_sources_param == 'left':
        selected_sources = [s[0] for s in lang_sources if s[1] == 'Left']
    elif selected_sources_param == 'right':
        selected_sources = [s[0] for s in lang_sources if s[1] == 'Right']
    elif selected_sources_param == 'clear' or selected_sources_param == '':
        selected_sources = []
    elif selected_sources_param:
        selected_sources = selected_sources_param.split(',')
    else:
        selected_sources = lang_default_sources
    
    all_stories = list(Story.objects.filter(published__gte=cutoff, language=language))
    
    for story in all_stories:
        story.story_categories = get_story_categories(story.title)
        bias_info = lang_source_info.get(story.source, ('Unknown', '#999', 'https://mediabiasfactcheck.com/'))
        story.bias_label = bias_info[0]
        story.bias_color = bias_info[1]
        story.bias_link = bias_info[2]
        story.is_paywalled = story.source in PAYWALLED_SOURCES
    
    stories = [s for s in all_stories if s.source in selected_sources]
    
    most_covered_stories = []
    story_groups = {}
    
    for story in stories:
        # Normalize title for matching: lowercase, remove punctuation, take first 70 chars
        normalized = re.sub(r'[^\w\s]', '', story.title.lower())[:70]
        
        # Try to find a matching group
        matched_key = None
        for existing_key in story_groups:
            # Compare word overlap - if 60%+ words match, consider it the same story
            words1 = set(existing_key.split())
            words2 = set(normalized.split())
            if not words1 or not words2:
                continue
            overlap = len(words1 & words2) / max(len(words1), len(words2))
            if overlap >= 0.6:
                matched_key = existing_key
                break
        
        if matched_key:
            story_groups[matched_key].append(story)
        else:
            story_groups[normalized] = [story]
    
    for key, title_stories in story_groups.items():
        if len(title_stories) >= 2:
            base_story = title_stories[0]
            base_story.covered_by_count = len(title_stories)
            base_story.covered_by_sources = list(set(s.source for s in title_stories))
            most_covered_stories.append(base_story)
    
    most_covered_stories.sort(key=lambda x: -x.covered_by_count)
    most_covered_stories = most_covered_stories[:20]
    
    grouped = {}
    for cat_id, cat_name in category_names.items():
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
        'sources': lang_sources,
        'selected_sources': selected_sources,
        'default_sources': lang_default_sources,
        'language': language,
        'language_names': LANGUAGE_NAMES,
    })


def fetch_news_trigger(request):
    def run_fetch():
        try:
            call_command('fetch_news')
        except Exception as e:
            print(f"Fetch error: {e}")
    
    thread = threading.Thread(target=run_fetch)
    thread.start()
    return HttpResponse('Fetch started.')


def terms_view(request):
    language = request.GET.get('lang', 'en')
    if language == 'es':
        return render(request, 'terms_es.html')
    return render(request, 'terms.html')


def privacy_view(request):
    language = request.GET.get('lang', 'en')
    if language == 'es':
        return render(request, 'privacy_es.html')
    return render(request, 'privacy.html')
