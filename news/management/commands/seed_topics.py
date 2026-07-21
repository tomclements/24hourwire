from django.core.management.base import BaseCommand
from news.models import Topic


class Command(BaseCommand):
    help = 'Seed initial topic hubs for evergreen landing pages'

    def handle(self, *args, **options):
        topics = [
            {
                'slug': 'us-iran-war',
                'title': 'US-Iran War & Strait of Hormuz Crisis',
                'headline': 'Strikes, shipping disruptions, and the oil price shock',
                'description': 'Ongoing coverage of the US-Iran military conflict, including air strikes, the Strait of Hormuz blockade, regional escalation, oil market disruption, and diplomatic efforts.',
                'keywords': ['iran', 'strait of hormuz', 'us strikes', 'oil price', 'hormuz', 'irgc', 'central command', 'centcom', 'blockade', 'naval', 'missile', 'nuclear', 'rubio', 'pezeushkian', 'khamenei', 'houthis', 'saudi arabia', 'kuwait', 'bahrain', 'jordan'],
                'categories': ['world', 'politics', 'business'],
                'languages': ['en', 'ar', 'fa', 'tr', 'fr', 'de', 'es'],
                'priority': 10,
                'meta_title': 'US-Iran War & Strait of Hormuz News | 24HourWire',
                'meta_description': 'Live coverage of the US-Iran conflict, Strait of Hormuz disruptions, oil market impacts, and regional escalation from diverse global sources.',
                'translations': {
                    'es': {
                        'headline': 'Guerra EE.UU.-Iran y crisis del Estrecho de Ormuz',
                        'description': 'Cobertura en curso del conflicto militar entre Estados Unidos e Iran, incluyendo ataques aereos, el bloqueo del Estrecho de Ormuz, la escalada regional y los esfuerzos diplomaticos.',
                    },
                    'ar': {
                        'headline': 'الحرب الأمريكية-الإيرانية وأزمة مضيق هرمز',
                        'description': 'تغطية مستمرة للصراع العسكري الأمريكي-الإيراني، بما في ذلك الضربات الجوية وحصار مضيق هرمز والتصعيد الإقليمي وجهود الدبلوماسية.',
                    },
                    'fr': {
                        'headline': 'Guerre Etats-Unis-Iran et crise du detroit d\'Ormuz',
                        'description': 'Couverture en cours du conflit militaire entre les Etats-Unis et l\'Iran, incluant les frappes aeriennes, le blocus du detroit d\'Ormuz, l\'escalade regionale et les efforts diplomatiques.',
                    },
                    'de': {
                        'headline': 'USA-Iran-Krieg und Strae-von-Hormus-Krise',
                        'description': 'Laufende Berichterstattung uber den USA-iranischen Militaerkonflikt, einschliesslich Luftangriffen, der Strasse von Hormus-Blockade, regionaler Eskalation und diplomatischen Bemuhungen.',
                    },
                },
            },
            {
                'slug': 'ai-regulation',
                'title': 'AI & Tech Regulation',
                'headline': 'Policy, ethics, and the future of artificial intelligence',
                'description': 'Stay informed on global AI regulation efforts, from the EU AI Act to US executive orders and emerging frameworks worldwide. Coverage of big tech, antitrust, data privacy, and innovation policy.',
                'keywords': ['artificial intelligence', 'ai', 'regulation', 'ai act', 'chatgpt', 'openai', 'antitrust', 'big tech', 'data privacy', 'gdpr', 'tech policy', 'machine learning', 'llm', 'anthropic', 'gold eagle', 'deepseek', 'kimi'],
                'categories': ['technology', 'business', 'world'],
                'languages': ['en', 'de', 'fr', 'es', 'it', 'pt', 'ja', 'zh'],
                'priority': 9,
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
                'slug': 'global-economy',
                'title': 'Global Economy',
                'headline': 'War-driven inflation, oil shocks, and recession fears',
                'description': 'Track the global economy under pressure from the Middle East conflict: energy price spikes, supply chain disruptions, central bank responses, inflation data, and recession indicators from diverse financial sources.',
                'keywords': ['inflation', 'recession', 'interest rate', 'fed', 'ecb', 'trade', 'tariff', 'gdp', 'unemployment', 'market', 'economy', 'fiscal', 'monetary', 'oil price', 'energy', 'opec', 'supply chain'],
                'categories': ['business', 'world'],
                'languages': ['en', 'de', 'fr', 'es', 'it', 'pt', 'ja', 'zh', 'ar', 'ru'],
                'priority': 8,
                'meta_title': 'Global Economy: War-Driven Inflation & Markets | 24HourWire',
                'meta_description': 'Global economic news: war-driven inflation, energy price shocks, supply chain disruptions, and market movements from diverse international sources.',
                'translations': {
                    'es': {
                        'headline': 'Inflacion impulsada por la guerra, choques de petroleo y temores de recesion',
                        'description': 'Siga la economia global bajo presion del conflicto en Medio Oriente: aumentos de precios energeticos, interrupciones de la cadena de suministro, respuestas de bancos centrales y datos de inflacion.',
                    },
                    'de': {
                        'headline': 'Kriegsbedingte Inflation, Oelschocks und Rezessionsangste',
                        'description': 'Verfolgen Sie die globale Wirtschaft unter Druck durch den Nahostkonflikt: Energiepreisanstiege, Lieferkettenstoerungen, Zentralbankreaktionen und Inflationsdaten.',
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
                'slug': 'us-china-relations',
                'title': 'US-China Relations',
                'headline': 'Trade war, tech rivalry, and geopolitical competition',
                'description': 'Track the evolving rivalry between the United States and China, from trade negotiations and tariffs to the AI race, semiconductor restrictions, and military posturing in the Indo-Pacific.',
                'keywords': ['china', 'xi jinping', 'trade war', 'tariff', 'beijing', 'us-china', 'bilateral', 'taiwan', 'indo-pacific', 'sanctions', 'semiconductor', 'chip', 'ai race'],
                'categories': ['world', 'business', 'politics', 'technology'],
                'languages': ['en', 'zh', 'ja', 'ko', 'ar'],
                'priority': 6,
                'meta_title': 'US-China Relations: Trade & Tech Rivalry News | 24HourWire',
                'meta_description': 'Latest news on US-China relations, trade talks, the AI race, semiconductor restrictions, and diplomatic developments from sources across the political spectrum.',
                'translations': {
                    'es': {
                        'headline': 'Guerra comercial, rivalidad tecnologica y competencia geopolitica',
                        'description': 'Siga la evolucion de la rivalidad entre Estados Unidos y China, desde las negociaciones comerciales y aranceles hasta la carrera de IA, las restricciones de semiconductores y el posicionamiento militar en el Indo-Pacifico.',
                    },
                    'zh': {
                        'headline': '贸易战、科技竞争与地缘政治博弈',
                        'description': '追踪中美之间不断演变的竞争关系，从贸易谈判和关税到人工智能竞赛、半导体限制以及印太地区的军事态势。',
                    },
                },
            },
            {
                'slug': 'middle-east-crisis',
                'title': 'Israel-Palestine Conflict',
                'headline': 'Gaza, West Bank, Lebanon, and humanitarian crisis',
                'description': 'Coverage of the Israel-Palestine conflict, including Gaza operations, West Bank developments, Lebanon border tensions, humanitarian conditions, and regional diplomatic efforts.',
                'keywords': ['israel', 'gaza', 'palestine', 'hamas', 'lebanon', 'hezbollah', 'west bank', 'ceasefire', 'hostage', 'rafah', 'humanitarian', 'unrwa'],
                'categories': ['world', 'politics'],
                'languages': ['en', 'ar', 'tr', 'fr', 'de', 'es'],
                'priority': 5,
                'meta_title': 'Israel-Palestine Conflict News | 24HourWire',
                'meta_description': 'Latest Israel-Palestine conflict coverage: Gaza, West Bank, Lebanon, humanitarian developments, and diplomatic efforts from diverse global sources.',
                'translations': {
                    'es': {
                        'headline': 'Conflicto israeli-palestino: Gaza, Cisjordania y crisis humanitaria',
                        'description': 'Cobertura del conflicto israeli-palestino, incluyendo operaciones en Gaza, desarrollos en Cisjordania, tensiones en la frontera con Libano, condiciones humanitarias y esfuerzos diplomaticos regionales.',
                    },
                    'ar': {
                        'headline': 'الصراع الإسرائيلي-الفلسطيني: غزة والضفة الغربية والأزمة الإنسانية',
                        'description': 'تغطية الصراع الإسرائيلي-الفلسطيني، بما في ذلك العمليات في غزة والتطورات في الضفة الغربية والتوترات على الحدود اللبنانية والوضع الإنساني وجهود الدبلوماسية الإقليمية.',
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
