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
                'merchandise': {
                    'title': 'World Cup 2026 Gear',
                    'items': [
                        {
                            'name': 'adidas FIFA World Cup 2026 Official Match Ball',
                            'url': 'https://www.amazon.com/s?k=adidas+world+cup+2026+official+match+ball&tag=24hourwire-20',
                            'image': 'https://m.media-amazon.com/images/I/61yY3Y1Zz7L._AC_SL1000_.jpg',
                        },
                        {
                            'name': 'Nike Pitch Training Soccer Ball',
                            'url': 'https://www.amazon.com/s?k=nike+pitch+training+soccer+ball&tag=24hourwire-20',
                            'image': 'https://m.media-amazon.com/images/I/71QJ7m9yZzL._AC_SL1500_.jpg',
                        },
                        {
                            'name': 'Brazil National Team Jersey 2026',
                            'url': 'https://www.amazon.com/s?k=brazil+soccer+jersey+2026&tag=24hourwire-20',
                            'image': 'https://m.media-amazon.com/images/I/71Z3L3ZzZzL._AC_SL1500_.jpg',
                        },
                        {
                            'name': 'Argentina National Team Jersey 2026',
                            'url': 'https://www.amazon.com/s?k=argentina+soccer+jersey+2026&tag=24hourwire-20',
                            'image': 'https://m.media-amazon.com/images/I/71A3L3ZzZzL._AC_SL1500_.jpg',
                        },
                        {
                            'name': 'France National Team Jersey 2026',
                            'url': 'https://www.amazon.com/s?k=france+soccer+jersey+2026&tag=24hourwire-20',
                            'image': 'https://m.media-amazon.com/images/I/71B3L3ZzZzL._AC_SL1500_.jpg',
                        },
                        {
                            'name': 'Germany National Team Jersey 2026',
                            'url': 'https://www.amazon.com/s?k=germany+soccer+jersey+2026&tag=24hourwire-20',
                            'image': 'https://m.media-amazon.com/images/I/71C3L3ZzZzL._AC_SL1500_.jpg',
                        },
                        {
                            'name': 'USA National Team Jersey 2026',
                            'url': 'https://www.amazon.com/s?k=usa+soccer+jersey+2026&tag=24hourwire-20',
                            'image': 'https://m.media-amazon.com/images/I/71D3L3ZzZzL._AC_SL1500_.jpg',
                        },
                        {
                            'name': 'Mexico National Team Jersey 2026',
                            'url': 'https://www.amazon.com/s?k=mexico+soccer+jersey+2026&tag=24hourwire-20',
                            'image': 'https://m.media-amazon.com/images/I/71E3L3ZzZzL._AC_SL1500_.jpg',
                        },
                    ]
                },
                'translations': {
                    'es': {
                        'headline': 'Cobertura en vivo de la Copa Mundial de la FIFA desde todos los angulos',
                        'description': 'La Copa Mundial de la FIFA 2026 se organiza en Estados Unidos, Canada y Mexico. Obtenga las ultimas noticias, cobertura de partidos, convocatorias de equipos y analisis de fuentes de todo el mundo.',
                    },
                    'fr': {
                        'headline': 'Couverture en direct de la Coupe du monde FIFA sous tous les angles',
                        'description': 'La Coupe du monde de la FIFA 2026 est organisee aux Etats-Unis, au Canada et au Mexique. Obtenez les dernieres nouvelles, la couverture des matchs, les convocations et les analyses de sources du monde entier.',
                    },
                    'de': {
                        'headline': 'Live-Berichterstattung uber die FIFA Weltmeisterschaft aus allen Blickwinkeln',
                        'description': 'Die FIFA Weltmeisterschaft 2026 wird in den USA, Kanada und Mexiko ausgetragen. Erhalten Sie die neuesten Nachrichten, Spielberichte, Kaderbekanntgaben und Analysen aus Quellen auf der ganzen Welt.',
                    },
                },
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
                'translations': {
                    'es': {
                        'headline': 'Comercio, diplomacia y desarrollos geopoliticos',
                        'description': 'Siga la evolucion de la relacion entre Estados Unidos y China, desde las negociaciones comerciales y aranceles hasta las cumbres diplomaticas y el posicionamiento militar en el Indo-Pacifico.',
                    },
                    'zh': {
                        'headline': '贸易、外交与地缘政治动态',
                        'description': '追踪中美关系的发展动态，从贸易谈判和关税到外交峰会及印太地区的军事姿态。',
                    },
                },
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
                'translations': {
                    'es': {
                        'headline': 'Politica, etica y el futuro de la inteligencia artificial',
                        'description': 'Mantengase informado sobre los esfuerzos globales de regulacion de IA, desde la Ley de IA de la UE hasta las ordenes ejecutivas de EE.UU. y los marcos emergentes en todo el mundo. Cobertura de big tech, antitrust, privacidad de datos y politica de innovacion.',
                    },
                    'de': {
                        'headline': 'Politik, Ethik und die Zukunft der kunstlichen Intelligenz',
                        'description': 'Bleiben Sie uber globale KI-Regulierungsbemuhungen informiert, von der EU-KI-Verordnung bis zu US-Executive Orders und neuen Rahmenwerken weltweit. Berichterstattung zu Big Tech, Kartellrecht, Datenschutz und Innovationspolitik.',
                    },
                },
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
                'translations': {
                    'es': {
                        'headline': 'Cobertura continua de la guerra y su impacto global',
                        'description': 'Cobertura integral de la guerra entre Rusia y Ucrania, incluyendo actualizaciones del campo de batalla, esfuerzos diplomaticos, impacto humanitario y repercusiones globales de sanciones y energia.',
                    },
                    'de': {
                        'headline': 'Laufende Berichterstattung uber den Krieg und seine globalen Auswirkungen',
                        'description': 'Umfassende Berichterstattung zum Russland-Ukraine-Krieg, einschliesslich Schlachtfeld-Updates, diplomatischer Bemuhungen, humanitarem Einfluss und globalen Sanktions- und Energieauswirkungen.',
                    },
                },
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
                'translations': {
                    'es': {
                        'headline': 'Israel, Gaza, Libano y desarrollos regionales',
                        'description': 'Siga los rapidos desarrollos en Medio Oriente, desde el conflicto Israel-Gaza hasta la diplomacia regional, las preocupaciones humanitarias y los cambios geopoliticos mas amplios.',
                    },
                    'ar': {
                        'headline': 'تطورات اسرائيل وغزة ولبنان والمنطقة',
                        'description': 'تابع التطورات السريعة في الشرق الأوسط، من النزاع الاسرائيلي الفلسطيني الى الدبلوماسية الاقليمية والمخاوف الانسانية والتحولات الجيوسياسية الاقليمية.',
                    },
                },
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
                'translations': {
                    'es': {
                        'headline': 'Inflacion, tasas de interes, comercio y temores de recesion',
                        'description': 'Siga el pulso de la economia global: decisiones de bancos centrales, datos de inflacion, disputas comerciales, movimientos del mercado e indicadores de recesion de diversas fuentes financieras.',
                    },
                    'de': {
                        'headline': 'Inflation, Zinsen, Handel und Rezessionsangste',
                        'description': 'Verfolgen Sie den Puls der globalen Wirtschaft: Zentralbankentscheidungen, Inflationsdaten, Handelsstreitigkeiten, Marktbewegungen und Rezessionsindikatoren aus verschiedenen Finanzquellen.',
                    },
                },
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
                'translations': {
                    'es': {
                        'headline': 'Elecciones de la UE, ascenso de la extrema derecha y debates sobre migracion',
                        'description': 'Sigua los desarrollos politicos europeos: politica de la UE, elecciones nacionales, el ascenso de partidos de extrema derecha, debates sobre migracion y el futuro del proyecto europeo.',
                    },
                    'de': {
                        'headline': 'EU-Wahlen, Rechtsruck und Migrationsdebatten',
                        'description': 'Verfolgen Sie europaische politische Entwicklungen: EU-Politik, nationale Wahlen, der Aufstieg rechtspopulistischer Parteien, Migrationsdebatten und die Zukunft des europaischen Projekts.',
                    },
                },
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
