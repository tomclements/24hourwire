from django.core.management.base import BaseCommand
from news.models import Topic


class Command(BaseCommand):
    help = 'Seed initial topic hubs for evergreen landing pages'

    def handle(self, *args, **options):
        topics = [
            {
                'slug': 'world-cup-2026',
                'title': 'World Cup 2026',
                'headline': 'Live coverage of the FIFA World Cup from every angle',
                'description': 'The 2026 FIFA World Cup is being hosted across the United States, Canada, and Mexico. Get the latest news, match coverage, squad announcements, and analysis from sources around the world.',
                'keywords': ['world cup', 'copa mundial', 'coupe du monde', 'weltmeisterschaft', 'fifa', 'mundial', 'football', 'soccer', 'world cup 2026'],
                'categories': ['sports', 'world'],
                'languages': ['en', 'es', 'fr', 'de', 'pt', 'it', 'ar', 'ja', 'zh', 'ko'],
                'priority': 10,
                'meta_title': 'World Cup 2026 News & Coverage | 24HourWire',
                'meta_description': 'Live World Cup 2026 coverage from diverse global sources. Match previews, squad news, and analysis from every angle.',
            },
            {
                'slug': 'us-china-relations',
                'title': 'US-China Relations',
                'headline': 'Trade, diplomacy, and geopolitical developments',
                'description': 'Track the evolving relationship between the United States and China, from trade negotiations and tariffs to diplomatic summits and military posturing in the Indo-Pacific.',
                'keywords': ['china', 'xi jinping', 'trade war', 'tariff', 'beijing', 'us-china', 'bilateral', 'taiwan', 'indo-pacific', 'sanctions'],
                'categories': ['world', 'business', 'politics'],
                'languages': ['en', 'zh', 'ja', 'ko', 'ar'],
                'priority': 9,
                'meta_title': 'US-China Relations: Trade & Diplomacy News | 24HourWire',
                'meta_description': 'Latest news on US-China relations, trade talks, tariffs, and diplomatic developments from sources across the political spectrum.',
            },
            {
                'slug': 'ai-regulation',
                'title': 'AI & Tech Regulation',
                'headline': 'Policy, ethics, and the future of artificial intelligence',
                'description': 'Stay informed on global AI regulation efforts, from the EU AI Act to US executive orders and emerging frameworks worldwide. Coverage of big tech, antitrust, data privacy, and innovation policy.',
                'keywords': ['artificial intelligence', 'ai', 'regulation', 'ai act', 'chatgpt', 'openai', 'antitrust', 'big tech', 'data privacy', 'gdpr', 'tech policy', 'machine learning', 'llm'],
                'categories': ['technology', 'business', 'world'],
                'languages': ['en', 'de', 'fr', 'es', 'it', 'pt', 'ja', 'zh'],
                'priority': 8,
                'meta_title': 'AI Regulation & Tech Policy News | 24HourWire',
                'meta_description': 'Global AI regulation news: EU AI Act, US tech policy, antitrust actions, and data privacy developments from diverse sources.',
            },
            {
                'slug': 'ukraine-conflict',
                'title': 'Ukraine Conflict',
                'headline': 'Ongoing coverage of the war and its global impact',
                'description': 'Comprehensive coverage of the Russia-Ukraine war, including battlefield updates, diplomatic efforts, humanitarian impact, and global sanctions and energy repercussions.',
                'keywords': ['ukraine', 'russia', 'putin', 'zelensky', 'invasion', 'war', 'kyiv', 'moscow', 'crimea', 'donbas', 'nato', 'sanctions'],
                'categories': ['world', 'politics', 'business'],
                'languages': ['en', 'de', 'fr', 'ru', 'pl', 'es', 'it'],
                'priority': 7,
                'meta_title': 'Ukraine Conflict News & Analysis | 24HourWire',
                'meta_description': 'Latest Ukraine war coverage: battlefield updates, diplomacy, sanctions, and humanitarian news from sources worldwide.',
            },
            {
                'slug': 'middle-east-crisis',
                'title': 'Middle East Crisis',
                'headline': 'Israel, Gaza, Lebanon, and regional developments',
                'description': 'Track the fast-moving developments across the Middle East, from the Israel-Gaza conflict to regional diplomacy, humanitarian concerns, and wider geopolitical shifts.',
                'keywords': ['israel', 'gaza', 'palestine', 'hamas', 'lebanon', 'hezbollah', 'iran', 'middle east', 'ceasefire', 'hostage', 'rafah', 'west bank'],
                'categories': ['world', 'politics'],
                'languages': ['en', 'ar', 'tr', 'fr', 'de', 'es'],
                'priority': 6,
                'meta_title': 'Middle East Crisis: Israel-Gaza & Regional News | 24HourWire',
                'meta_description': 'Latest Middle East crisis coverage: Israel-Gaza conflict, regional diplomacy, and humanitarian developments from diverse global sources.',
            },
            {
                'slug': 'climate-energy',
                'title': 'Climate & Energy',
                'headline': 'Climate policy, extreme weather, and the green transition',
                'description': 'Coverage of climate change policy, renewable energy transitions, extreme weather events, COP conferences, and environmental regulation from around the world.',
                'keywords': ['climate', 'carbon', 'renewable', 'cop', 'green', 'energy transition', 'extreme weather', 'flood', 'drought', 'temperature', 'paris agreement', 'emissions'],
                'categories': ['world', 'science', 'business'],
                'languages': ['en', 'de', 'fr', 'es', 'it', 'pt', 'ja', 'zh', 'ar'],
                'priority': 5,
                'meta_title': 'Climate Change & Energy Transition News | 24HourWire',
                'meta_description': 'Global climate policy news, renewable energy updates, extreme weather coverage, and COP developments from diverse sources.',
            },
            {
                'slug': 'us-elections-2026',
                'title': 'US Elections 2026',
                'headline': 'Midterms, state races, and the road to 2028',
                'description': 'Follow the 2026 US midterm elections, state-level races, ballot measures, and the shifting political landscape ahead of the 2028 presidential cycle.',
                'keywords': ['election', 'midterm', 'senate', 'house', 'governor', 'campaign', 'vote', 'ballot', 'primary', 'poll', 'gop', 'democrat', 'republican'],
                'categories': ['politics', 'us'],
                'languages': ['en'],
                'priority': 4,
                'meta_title': 'US Elections 2026: Midterms & State Races | 24HourWire',
                'meta_description': '2026 US midterm election coverage: Senate, House, and governor races from left, center, and right sources.',
            },
            {
                'slug': 'global-economy',
                'title': 'Global Economy',
                'headline': 'Inflation, interest rates, trade, and recession fears',
                'description': 'Track the pulse of the global economy: central bank decisions, inflation data, trade disputes, market movements, and recession indicators from diverse financial sources.',
                'keywords': ['inflation', 'recession', 'interest rate', 'fed', 'ecb', 'trade', 'tariff', 'gdp', 'unemployment', 'market', 'economy', 'fiscal', 'monetary'],
                'categories': ['business', 'world'],
                'languages': ['en', 'de', 'fr', 'es', 'it', 'pt', 'ja', 'zh', 'ar', 'ru'],
                'priority': 3,
                'meta_title': 'Global Economy: Inflation, Trade & Markets | 24HourWire',
                'meta_description': 'Global economic news: inflation, interest rates, trade disputes, and market movements from diverse international sources.',
            },
            {
                'slug': 'european-politics',
                'title': 'European Politics',
                'headline': 'EU elections, far-right surge, and migration debates',
                'description': 'Follow European political developments: EU policy, national elections, the rise of far-right parties, migration debates, and the future of the European project.',
                'keywords': ['eu', 'european union', 'brussels', 'migration', 'far right', 'populist', 'euro', 'schengen', 'von der leyen', 'european parliament', 'brexit'],
                'categories': ['world', 'politics', 'europe'],
                'languages': ['en', 'de', 'fr', 'es', 'it', 'pt', 'pl'],
                'priority': 2,
                'meta_title': 'European Politics & EU News | 24HourWire',
                'meta_description': 'European political news: EU policy, elections, migration debates, and the far-right surge from diverse continental sources.',
            },
            {
                'slug': 'health-pandemic',
                'title': 'Health & Pandemic Preparedness',
                'headline': 'WHO updates, vaccine news, and global health policy',
                'description': 'Stay informed on global health developments: WHO updates, vaccine research, pandemic preparedness, healthcare policy, and disease outbreaks worldwide.',
                'keywords': ['who', 'vaccine', 'pandemic', 'health', 'disease', 'outbreak', 'virus', 'covid', 'healthcare', 'medicine', 'fda', 'cdc', 'public health'],
                'categories': ['health', 'world', 'science'],
                'languages': ['en', 'de', 'fr', 'es', 'it', 'pt', 'ja', 'zh', 'ar'],
                'priority': 1,
                'meta_title': 'Global Health & Pandemic News | 24HourWire',
                'meta_description': 'Global health coverage: WHO updates, vaccine news, pandemic preparedness, and healthcare policy from diverse sources.',
            },
        ]

        created_count = 0
        updated_count = 0

        for data in topics:
            topic, created = Topic.objects.update_or_create(
                slug=data['slug'],
                defaults=data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'Created topic: {topic.title}'))
            else:
                updated_count += 1
                self.stdout.write(self.style.NOTICE(f'Updated topic: {topic.title}'))

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created {created_count} topics, updated {updated_count} topics.'
        ))
