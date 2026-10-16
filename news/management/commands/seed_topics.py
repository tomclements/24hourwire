from django.core.management.base import BaseCommand
from news.models import Topic
from news.topic_matching import GEOPOLITICS_NEGATIVES, keywords_union_from_rules


def _rules(anchors=None, medium=None, weak=None, negatives=None,
           deny_categories=None, min_score=2):
    """Build a match_rules dict and keywords union for seeding."""
    rules = {
        'anchors': list(anchors or []),
        'medium': list(medium or []),
        'weak': list(weak or []),
        'negatives': list(negatives or []),
        'deny_categories': list(deny_categories or []),
        'min_score': min_score,
    }
    return rules, keywords_union_from_rules(rules)


class Command(BaseCommand):
    help = 'Seed initial topic hubs for evergreen landing pages'

    def handle(self, *args, **options):
        geo_neg = list(GEOPOLITICS_NEGATIVES)

        topics = []

        # --- US-Iran War ---
        rules, kws = _rules(
            anchors=[
                'iran', 'iranian', 'tehran', 'strait of hormuz', 'hormuz',
                'irgc', 'pezeshkian', 'khamenei', 'araghchi', 'ghalibaf',
                'centcom', 'central command', 'houthis',
            ],
            medium=[
                'us strikes', 'oil price', 'blockade', 'saudi arabia',
                'kuwait', 'bahrain', 'oman', 'uae', 'missile', 'nuclear',
                'ceasefire', 'mou',
            ],
            weak=['jordan', 'naval', 'rubio'],
            negatives=geo_neg,
            deny_categories=['sports', 'entertainment'],
        )
        topics.append({
            'slug': 'us-iran-war',
            'title': 'US-Iran War & Strait of Hormuz Crisis',
            'headline': 'Strikes, shipping disruptions, and the oil price shock',
            'description': 'Ongoing coverage of the US-Iran military conflict, including air strikes, the Strait of Hormuz blockade, regional escalation, oil market disruption, and diplomatic efforts.',
            'keywords': kws,
            'match_rules': rules,
            'categories': ['world', 'politics', 'business'],
            'languages': ['en', 'ar', 'fa', 'tr', 'fr', 'de', 'es'],
            'priority': 10,
            'meta_title': 'US-Iran War & Strait of Hormuz News | 24HourWire',
            'meta_description': 'Live coverage of the US-Iran conflict, Strait of Hormuz disruptions, oil market impacts, and regional escalation from diverse global sources.',
            'translations': {
                'es': {
                    'title': 'Guerra EE.UU.-Irán y crisis del Estrecho de Ormuz',
                    'headline': 'Guerra EE.UU.-Irán y crisis del Estrecho de Ormuz',
                    'description': 'Cobertura en curso del conflicto militar entre Estados Unidos e Irán, incluyendo ataques aéreos, el bloqueo del Estrecho de Ormuz, la escalada regional y los esfuerzos diplomáticos.',
                    'meta_title': 'Guerra EE.UU.-Irán y crisis del Estrecho de Ormuz',
                },
                'ar': {
                    'title': 'الحرب الأمريكية-الإيرانية وأزمة مضيق هرمز',
                    'headline': 'الحرب الأمريكية-الإيرانية وأزمة مضيق هرمز',
                    'description': 'تغطية مستمرة للصراع العسكري الأمريكي-الإيراني، بما في ذلك الضربات الجوية وحصار مضيق هرمز والتصعيد الإقليمي وجهود الدبلوماسية.',
                    'meta_title': 'الحرب الأمريكية-الإيرانية وأزمة مضيق هرمز',
                },
                'fr': {
                    'title': "Guerre États-Unis-Iran et crise du détroit d'Ormuz",
                    'headline': "Guerre États-Unis-Iran et crise du détroit d'Ormuz",
                    'description': "Couverture en cours du conflit militaire entre les États-Unis et l'Iran, incluant les frappes aériennes, le blocus du détroit d'Ormuz, l'escalade régionale et les efforts diplomatiques.",
                    'meta_title': "Guerre États-Unis-Iran et crise du détroit d'Ormuz",
                },
                'de': {
                    'title': 'USA-Iran-Krieg und Straße-von-Hormus-Krise',
                    'headline': 'USA-Iran-Krieg und Straße-von-Hormus-Krise',
                    'description': 'Laufende Berichterstattung über den USA-iranischen Militärkonflikt, einschließlich Luftangriffen, der Straße-von-Hormus-Blockade, regionaler Eskalation und diplomatischen Bemühungen.',
                    'meta_title': 'USA-Iran-Krieg und Straße-von-Hormus-Krise',
                },
            },
        })

        # --- AI Regulation ---
        rules, kws = _rules(
            anchors=[
                'artificial intelligence', 'ai act', 'chatgpt', 'openai',
                'anthropic', 'deepseek', 'machine learning', 'llm',
                'eu ai act',
            ],
            medium=[
                'tech policy', 'antitrust', 'big tech', 'data privacy',
                'gdpr', 'kimi', 'gold eagle',
            ],
            weak=['ai', 'regulation'],
            negatives=[],
            deny_categories=['sports'],
        )
        topics.append({
            'slug': 'ai-regulation',
            'title': 'AI & Tech Regulation',
            'headline': 'Policy, ethics, and the future of artificial intelligence',
            'description': 'Stay informed on global AI regulation efforts, from the EU AI Act to US executive orders and emerging frameworks worldwide. Coverage of big tech, antitrust, data privacy, and innovation policy.',
            'keywords': kws,
            'match_rules': rules,
            'categories': ['technology', 'business', 'world'],
            'languages': ['en', 'de', 'fr', 'es', 'it', 'pt', 'ja', 'zh'],
            'priority': 9,
            'meta_title': 'AI Regulation & Tech Policy News | 24HourWire',
            'meta_description': 'Global AI regulation news: EU AI Act, US tech policy, antitrust actions, and data privacy developments from diverse sources.',
            'translations': {
                'es': {
                    'title': 'Regulación de IA y tecnología',
                    'headline': 'Política, ética y el futuro de la inteligencia artificial',
                    'description': 'Manténgase informado sobre los esfuerzos globales de regulación de IA, desde la Ley de IA de la UE hasta las órdenes ejecutivas de EE.UU. y los marcos emergentes en todo el mundo. Cobertura de big tech, antitrust, privacidad de datos y política de innovación.',
                    'meta_title': 'Regulación de IA y tecnología',
                },
                'de': {
                    'title': 'KI- und Technologieregulierung',
                    'headline': 'Politik, Ethik und die Zukunft der künstlichen Intelligenz',
                    'description': 'Bleiben Sie über globale KI-Regulierungsbemühungen informiert, von der EU-KI-Verordnung bis zu US-Executive Orders und neuen Rahmenwerken weltweit. Berichterstattung zu Big Tech, Kartellrecht, Datenschutz und Innovationspolitik.',
                    'meta_title': 'KI- und Technologieregulierung',
                },
                'fr': {
                    'title': "Régulation de l'IA et de la technologie",
                    'headline': "Politique, éthique et avenir de l'intelligence artificielle",
                    'description': "Restez informé des efforts mondiaux de régulation de l'IA, de l'AI Act de l'UE aux décrets américains et aux cadres émergents dans le monde. Couverture des géants de la tech, de l'antitrust, de la protection des données et de la politique d'innovation.",
                    'meta_title': "Régulation de l'IA et de la technologie",
                },
                'ar': {
                    'title': 'تنظيم الذكاء الاصطناعي والتقنية',
                    'headline': 'السياسة والأخلاق ومستقبل الذكاء الاصطناعي',
                    'description': 'تابع الجهود العالمية لتنظيم الذكاء الاصطناعي، من قانون الذكاء الاصطناعي في الاتحاد الأوروبي إلى الأوامر التنفيذية الأمريكية والأطر الناشئة حول العالم. تغطية لكبار شركات التقنية ومكافحة الاحتكار وخصوصية البيانات وسياسة الابتكار.',
                    'meta_title': 'تنظيم الذكاء الاصطناعي والتقنية',
                },
            },
        })

        # --- Global Economy ---
        rules, kws = _rules(
            anchors=[
                'inflation', 'recession', 'interest rate', 'gdp', 'opec',
                'supply chain', 'central bank',
            ],
            medium=[
                'fed', 'ecb', 'tariff', 'unemployment', 'fiscal', 'monetary',
                'oil price', 'energy',
            ],
            weak=['trade', 'market', 'economy'],
            negatives=[],
            deny_categories=['sports', 'entertainment'],
        )
        topics.append({
            'slug': 'global-economy',
            'title': 'Global Economy',
            'headline': 'War-driven inflation, oil shocks, and recession fears',
            'description': 'Track the global economy under pressure from the Middle East conflict: energy price spikes, supply chain disruptions, central bank responses, inflation data, and recession indicators from diverse financial sources.',
            'keywords': kws,
            'match_rules': rules,
            'categories': ['business', 'world'],
            'languages': ['en', 'de', 'fr', 'es', 'it', 'pt', 'ja', 'zh', 'ar', 'ru'],
            'priority': 8,
            'meta_title': 'Global Economy: War-Driven Inflation & Markets | 24HourWire',
            'meta_description': 'Global economic news: war-driven inflation, energy price shocks, supply chain disruptions, and market movements from diverse international sources.',
            'translations': {
                'es': {
                    'title': 'Economía global',
                    'headline': 'Inflación impulsada por la guerra, choques de petróleo y temores de recesión',
                    'description': 'Siga la economía global bajo presión del conflicto en Medio Oriente: aumentos de precios energéticos, interrupciones de la cadena de suministro, respuestas de bancos centrales y datos de inflación.',
                    'meta_title': 'Economía global',
                },
                'de': {
                    'title': 'Globale Wirtschaft',
                    'headline': 'Kriegsbedingte Inflation, Ölschocks und Rezessionsängste',
                    'description': 'Verfolgen Sie die globale Wirtschaft unter Druck durch den Nahostkonflikt: Energiepreisanstiege, Lieferkettenstörungen, Zentralbankreaktionen und Inflationsdaten.',
                    'meta_title': 'Globale Wirtschaft',
                },
                'fr': {
                    'title': 'Économie mondiale',
                    'headline': "Inflation alimentée par la guerre, chocs pétroliers et craintes de récession",
                    'description': "Suivez l'économie mondiale sous pression du conflit au Moyen-Orient : flambée des prix de l'énergie, perturbations des chaînes d'approvisionnement, réponses des banques centrales et données inflationnistes.",
                    'meta_title': 'Économie mondiale',
                },
                'it': {
                    'title': 'Economia globale',
                    'headline': 'Inflazione guidata dalla guerra, shock petroliferi e timori di recessione',
                    'description': "Tieni d'occhio l'economia globale sotto pressione dal conflitto in Medio Oriente: aumenti dei prezzi energetici, interruzioni delle catene di approvvigionamento, risposte delle banche centrali e dati sull'inflazione.",
                    'meta_title': 'Economia globale',
                },
                'pt': {
                    'title': 'Economia global',
                    'headline': 'Inflação impulsionada pela guerra, choques de petróleo e temores de recessão',
                    'description': 'Acompanhe a economia global sob pressão do conflito no Oriente Médio: aumentos dos preços de energia, interrupções nas cadeias de suprimentos, respostas dos bancos centrais e dados de inflação.',
                    'meta_title': 'Economia global',
                },
                'ja': {
                    'title': '世界経済',
                    'headline': '戦争によるインフレ、石油ショック、景気後退への懸念',
                    'description': '中東の紛争による圧力の下での世界経済を追う：エネルギー価格の高騰、サプライチェーンの混乱、中央銀行の対応、インフレデータ。',
                    'meta_title': '世界経済',
                },
                'zh': {
                    'title': '全球经济',
                    'headline': '战争驱动的通胀、石油冲击与衰退担忧',
                    'description': '关注中东冲突压力下的全球经济：能源价格飙升、供应链中断、央行应对措施和通胀数据。',
                    'meta_title': '全球经济',
                },
                'ar': {
                    'title': 'الاقتصاد العالمي',
                    'headline': 'التضخم المدفوع بالحرب، صدمات النفط ومخاوف الركود',
                    'description': 'تابع الاقتصاد العالمي تحت ضغط الصراع في الشرق الأوسط: ارتفاع أسعار الطاقة، اضطرابات سلاسل الإمداد، ردود البنوك المركزية وبيانات التضخم.',
                    'meta_title': 'الاقتصاد العالمي',
                },
                'ru': {
                    'title': 'Мировая экономика',
                    'headline': 'Военная инфляция, нефтяные шоки и опасения рецессии',
                    'description': 'Следите за мировой экономикой под давлением конфликта на Ближнем Востоке: рост цен на энергоносители, сбои в цепочках поставок, реакция центральных банков и данные по инфляции.',
                    'meta_title': 'Мировая экономика',
                },
            },
        })

        # --- Ukraine Conflict ---
        rules, kws = _rules(
            anchors=[
                'ukraine', 'ukrainian', 'zelensky', 'zelenskyy', 'kyiv',
                'kiev', 'donbas', 'crimea',
            ],
            medium=[
                'putin', 'moscow', 'russia', 'russian', 'nato', 'sanctions',
                'invasion',
            ],
            weak=['war'],
            negatives=geo_neg,
            deny_categories=['sports', 'entertainment'],
        )
        topics.append({
            'slug': 'ukraine-conflict',
            'title': 'Ukraine Conflict',
            'headline': 'Ongoing coverage of the war and its global impact',
            'description': 'Comprehensive coverage of the Russia-Ukraine war, including battlefield updates, diplomatic efforts, humanitarian impact, and global sanctions and energy repercussions.',
            'keywords': kws,
            'match_rules': rules,
            'categories': ['world', 'politics', 'business'],
            'languages': ['en', 'de', 'fr', 'ru', 'pl', 'es', 'it'],
            'priority': 7,
            'meta_title': 'Ukraine Conflict News & Analysis | 24HourWire',
            'meta_description': 'Latest Ukraine war coverage: battlefield updates, diplomacy, sanctions, and humanitarian news from sources worldwide.',
            'translations': {
                'es': {
                    'title': 'Conflicto en Ucrania',
                    'headline': 'Cobertura continua de la guerra y su impacto global',
                    'description': 'Cobertura integral de la guerra entre Rusia y Ucrania, incluyendo actualizaciones del campo de batalla, esfuerzos diplomáticos, impacto humanitario y repercusiones globales de sanciones y energía.',
                    'meta_title': 'Conflicto en Ucrania',
                },
                'de': {
                    'title': 'Ukraine-Konflikt',
                    'headline': 'Laufende Berichterstattung über den Krieg und seine globalen Auswirkungen',
                    'description': 'Umfassende Berichterstattung zum Russland-Ukraine-Krieg, einschließlich Schlachtfeld-Updates, diplomatischer Bemühungen, humanitärem Einfluss und globalen Sanktions- und Energieauswirkungen.',
                    'meta_title': 'Ukraine-Konflikt',
                },
                'fr': {
                    'title': 'Conflit en Ukraine',
                    'headline': 'Couverture continue de la guerre et de son impact mondial',
                    'description': "Couverture complète de la guerre entre la Russie et l'Ukraine, incluant les mises à jour du champ de bataille, les efforts diplomatiques, l'impact humanitaire et les répercussions mondiales des sanctions et de l'énergie.",
                    'meta_title': 'Conflit en Ukraine',
                },
                'ru': {
                    'title': 'Конфликт в Украине',
                    'headline': 'Постоянное освещение войны и её глобальных последствий',
                    'description': 'Комплексное освещение войны между Россией и Украиной, включая обновления с поля боя, дипломатические усилия, гуманитарное воздействие и глобальные последствия санкций и энергетики.',
                    'meta_title': 'Конфликт в Украине',
                },
                'pl': {
                    'title': 'Konflikt na Ukrainie',
                    'headline': 'Bieżące relacje z wojny i jej globalnego wpływu',
                    'description': 'Kompleksowe relacje z wojny rosyjsko-ukraińskiej, w tym aktualizacje z pola walki, wysiłki dyplomatyczne, wpływ humanitarny oraz globalne reperkusje sankcji i energetyki.',
                    'meta_title': 'Konflikt na Ukrainie',
                },
                'it': {
                    'title': 'Conflitto in Ucraina',
                    'headline': 'Copertura continua della guerra e del suo impatto globale',
                    'description': 'Copertura completa della guerra tra Russia e Ucraina, inclusi aggiornamenti dal campo di battaglia, sforzi diplomatici, impatto umanitario e ripercussioni globali di sanzioni ed energia.',
                    'meta_title': 'Conflitto in Ucraina',
                },
            },
        })

        # --- US-China Relations ---
        rules, kws = _rules(
            anchors=[
                'us-china', 'xi jinping', 'taiwan', 'beijing', 'semiconductor',
                'indo-pacific', 'kim jong un', 'ai race',
            ],
            medium=[
                'china', 'chinese', 'trade war', 'tariff', 'bilateral',
                'chip', 'north korea', 'south korea', 'sanctions',
            ],
            weak=[],
            negatives=geo_neg,
            deny_categories=['sports', 'entertainment'],
        )
        topics.append({
            'slug': 'us-china-relations',
            'title': 'US-China Relations',
            'headline': 'Trade war, tech rivalry, and geopolitical competition',
            'description': 'Track the evolving rivalry between the United States and China, from trade negotiations and tariffs to the AI race, semiconductor restrictions, and military posturing in the Indo-Pacific.',
            'keywords': kws,
            'match_rules': rules,
            'categories': ['world', 'business', 'politics', 'technology'],
            'languages': ['en', 'zh', 'ja', 'ko', 'ar'],
            'priority': 6,
            'meta_title': 'US-China Relations: Trade & Tech Rivalry News | 24HourWire',
            'meta_description': 'Latest news on US-China relations, trade talks, the AI race, semiconductor restrictions, and diplomatic developments from sources across the political spectrum.',
            'translations': {
                'es': {
                    'title': 'Relaciones EE.UU.-China',
                    'headline': 'Guerra comercial, rivalidad tecnológica y competencia geopolítica',
                    'description': 'Siga la evolución de la rivalidad entre Estados Unidos y China, desde las negociaciones comerciales y aranceles hasta la carrera de IA, las restricciones de semiconductores y el posicionamiento militar en el Indo-Pacífico.',
                    'meta_title': 'Relaciones EE.UU.-China',
                },
                'zh': {
                    'title': '中美关系',
                    'headline': '贸易战、科技竞争与地缘政治博弈',
                    'description': '追踪中美之间不断演变的竞争关系，从贸易谈判和关税到人工智能竞赛、半导体限制以及印太地区的军事态势。',
                    'meta_title': '中美关系',
                },
                'fr': {
                    'title': 'Relations États-Unis-Chine',
                    'headline': 'Guerre commerciale, rivalité technologique et compétition géopolitique',
                    'description': "Suivez l'évolution de la rivalité entre les États-Unis et la Chine, des négociations commerciales et des tarifs douaniers à la course à l'IA, aux restrictions sur les semi-conducteurs et au positionnement militaire dans l'Indo-Pacifique.",
                    'meta_title': 'Relations États-Unis-Chine',
                },
            },
        })

        # --- Middle East / Israel-Palestine ---
        rules, kws = _rules(
            anchors=[
                'israel', 'israeli', 'gaza', 'palestine', 'palestinian',
                'hamas', 'hezbollah', 'west bank', 'unrwa', 'rafah',
            ],
            medium=[
                'lebanon', 'hostage', 'ceasefire', 'syria', 'yemen',
                'houthi', 'humanitarian',
            ],
            weak=['saudi', 'uae', 'oman', 'qatar'],
            negatives=geo_neg,
            deny_categories=['sports', 'entertainment'],
        )
        topics.append({
            'slug': 'middle-east-crisis',
            'title': 'Israel-Palestine Conflict',
            'headline': 'Gaza, West Bank, Lebanon, and humanitarian crisis',
            'description': 'Coverage of the Israel-Palestine conflict, including Gaza operations, West Bank developments, Lebanon border tensions, humanitarian conditions, and regional diplomatic efforts.',
            'keywords': kws,
            'match_rules': rules,
            'categories': ['world', 'politics'],
            'languages': ['en', 'ar', 'tr', 'fr', 'de', 'es'],
            'priority': 5,
            'meta_title': 'Israel-Palestine Conflict News | 24HourWire',
            'meta_description': 'Latest Israel-Palestine conflict coverage: Gaza, West Bank, Lebanon, humanitarian developments, and diplomatic efforts from diverse global sources.',
            'translations': {
                'es': {
                    'title': 'Conflicto israelí-palestino',
                    'headline': 'Conflicto israelí-palestino: Gaza, Cisjordania y crisis humanitaria',
                    'description': 'Cobertura del conflicto israelí-palestino, incluyendo operaciones en Gaza, desarrollos en Cisjordania, tensiones en la frontera con Líbano, condiciones humanitarias y esfuerzos diplomáticos regionales.',
                    'meta_title': 'Conflicto israelí-palestino',
                },
                'ar': {
                    'title': 'الصراع الإسرائيلي-الفلسطيني',
                    'headline': 'الصراع الإسرائيلي-الفلسطيني: غزة والضفة الغربية والأزمة الإنسانية',
                    'description': 'تغطية الصراع الإسرائيلي-الفلسطيني، بما في ذلك العمليات في غزة والتطورات في الضفة الغربية والتوترات على الحدود اللبنانية والوضع الإنساني وجهود الدبلوماسية الإقليمية.',
                    'meta_title': 'الصراع الإسرائيلي-الفلسطيني',
                },
                'de': {
                    'title': 'Israelisch-palästinensischer Konflikt',
                    'headline': 'Israelisch-palästinensischer Konflikt: Gaza, Westjordanland und humanitäre Krise',
                    'description': 'Berichterstattung über den israelisch-palästinensischen Konflikt, einschließlich Operationen in Gaza, Entwicklungen im Westjordanland, Spannungen an der libanesischen Grenze, humanitäre Bedingungen und regionale diplomatische Bemühungen.',
                    'meta_title': 'Israelisch-palästinensischer Konflikt',
                },
                'fr': {
                    'title': 'Conflit israélo-palestinien',
                    'headline': 'Conflit israélo-palestinien : Gaza, Cisjordanie et crise humanitaire',
                    'description': 'Couverture du conflit israélo-palestinien, incluant les opérations à Gaza, les développements en Cisjordanie, les tensions à la frontière libanaise, les conditions humanitaires et les efforts diplomatiques régionaux.',
                    'meta_title': 'Conflit israélo-palestinien',
                },
            },
        })

        # --- US Elections 2026 ---
        rules, kws = _rules(
            anchors=[
                'midterm', 'midterms', 'us election', '2026 election',
            ],
            medium=[
                'election', 'senate', 'governor', 'campaign', 'ballot',
                'primary', 'gop', 'democrat', 'republican',
            ],
            weak=['vote', 'poll', 'house'],
            negatives=[],
            deny_categories=['sports'],
        )
        topics.append({
            'slug': 'us-elections-2026',
            'title': 'US Elections 2026',
            'headline': 'Midterms, state races, and the road to 2028',
            'description': 'Follow the 2026 US midterm elections, state-level races, ballot measures, and the shifting political landscape ahead of the 2028 presidential cycle.',
            'keywords': kws,
            'match_rules': rules,
            'categories': ['politics', 'us'],
            'languages': ['en'],
            'priority': 4,
            'meta_title': 'US Elections 2026: Midterms & State Races | 24HourWire',
            'meta_description': '2026 US midterm election coverage: Senate, House, and governor races from left, center, and right sources.',
            'translations': {
                'es': {
                    'title': 'Elecciones de EE.UU. 2026',
                    'headline': 'Elecciones legislativas, carreras estatales y el camino hacia 2028',
                    'description': 'Siga las elecciones legislativas de 2026 en Estados Unidos, las carreras a nivel estatal, las consultas populares y el cambiante panorama político de cara al ciclo presidencial de 2028.',
                    'meta_title': 'Elecciones de EE.UU. 2026',
                },
                'fr': {
                    'title': 'Élections américaines de 2026',
                    'headline': 'Midterms, courses étatiques et la route vers 2028',
                    'description': "Suivez les élections de mi-mandat américaines de 2026, les courses au niveau des États, les référendums et le paysage politique changeant avant le cycle présidentiel de 2028.",
                    'meta_title': 'Élections américaines de 2026',
                },
                'de': {
                    'title': 'US-Wahlen 2026',
                    'headline': 'Midterms, Staatswahlen und der Weg nach 2028',
                    'description': 'Verfolgen Sie die US-Zwischenwahlen 2026, Wahlen auf Staatsebene, Volksabstimmungen und die sich wandelnde politische Landschaft vor dem Präsidentschaftswahlkampf 2028.',
                    'meta_title': 'US-Wahlen 2026',
                },
                'pt': {
                    'title': 'Eleições nos EUA 2026',
                    'headline': 'Midterms, disputas estaduais e o caminho para 2028',
                    'description': 'Acompanhe as eleições de meio de mandato nos EUA em 2026, as disputas estaduais, as proposições de voto e o cenário político em mudança antes do ciclo presidencial de 2028.',
                    'meta_title': 'Eleições nos EUA 2026',
                },
                'it': {
                    'title': 'Elezioni USA 2026',
                    'headline': 'Midterm, gare statali e la strada verso il 2028',
                    'description': 'Segui le elezioni di metà mandato degli Stati Uniti del 2026, le gare a livello statale, i referendum e il mutante panorama politico in vista del ciclo presidenziale del 2028.',
                    'meta_title': 'Elezioni USA 2026',
                },
                'ar': {
                    'title': 'انتخابات الولايات المتحدة 2026',
                    'headline': 'الانتخابات النصفية وسباقات الولايات والطريق إلى 2028',
                    'description': 'تابع انتخابات التجديد النصفي الأمريكية لعام 2026 وسباقات المستوى الولائي ومقترحات الاقتراع والمشهد السياسي المتغير قبيل الانتخابات الرئاسية لعام 2028.',
                    'meta_title': 'انتخابات الولايات المتحدة 2026',
                },
                'ru': {
                    'title': 'Выборы в США 2026',
                    'headline': 'Промежуточные выборы, штатские гонки и путь к 2028 году',
                    'description': 'Следите за промежуточными выборами в США в 2026 году, statewide-гонками, референдумами и меняющимся политическим ландшафтом перед президентским циклом 2028 года.',
                    'meta_title': 'Выборы в США 2026',
                },
                'ja': {
                    'title': '2026年美国中間選挙',
                    'headline': '中間選挙、州レース、そして2028年へ',
                    'description': '2026年の米国中間選挙、州レベルの選挙、住民投票、2028年大統領選サイクルに向けて変化する政治情勢を追う。',
                    'meta_title': '2026年美国中間選挙',
                },
                'zh': {
                    'title': '2026年美国选举',
                    'headline': '中期选举、州级竞选与通往2028之路',
                    'description': '关注2026年美国中期选举、州级竞选、选票措施以及2028年总统周期前不断变化的政治格局。',
                    'meta_title': '2026年美国选举',
                },
                'ko': {
                    'title': '2026년 미국 선거',
                    'headline': '중간선거, 주 단위 선거, 그리고 2028년을 향한 길',
                    'description': '2026년 미국 중간선거, 주 단위 선거, 주민발의안, 2028년 대선을 앞둔 변화하는 정치 지형을 따른다.',
                    'meta_title': '2026년 미국 선거',
                },
                'tr': {
                    'title': '2026 ABD Seçimleri',
                    'headline': 'Kongre seçimleri, eyalet yarışları ve 2028 yolculuğu',
                    'description': '2026 ABD ara seçimlerini, eyalet düzeyindeki yarışları, halk oylamalarını ve 2028 başkanlık seçimleri öncesinde değişen siyasi manzarayı takip edin.',
                    'meta_title': '2026 ABD Seçimleri',
                },
                'hi': {
                    'title': '2026 अमेरिकी चुनाव',
                    'headline': 'मध्यावधि चुनाव, राज्य स्तरीय दौड़ और 2028 की ओर रास्ता',
                    'description': '2026 के अमेरिकी मध्यावधि चुनावों, राज्य स्तरीय दौड़, मतदान उपायों और 2028 राष्ट्रपति चक्र से पहले बदलती राजनीतिक स्थिति का अनुसरण करें।',
                    'meta_title': '2026 अमेरिकी चुनाव',
                },
            },
        })

        # --- European Politics ---
        rules, kws = _rules(
            anchors=[
                'european union', 'eu commission', 'eu parliament', 'brexit',
                'eurozone', 'schengen', 'european council', 'macron', 'scholz',
                'meloni', 'sanchez', 'starmer', 'merkel',
            ],
            medium=[
                'eu', 'europe', 'european', 'brussels', 'euro', 'nato',
                'trade deal', 'summit', 'coalition', 'snap election',
            ],
            weak=['election', 'referendum', 'vote'],
            negatives=geo_neg,
            deny_categories=['sports', 'entertainment'],
        )
        topics.append({
            'slug': 'european-politics',
            'title': 'European Politics',
            'headline': 'EU institutions, elections, and cross-border policy debates',
            'description': 'Coverage of European politics, from EU institutions and elections to national governments, coalitions, and policy debates shaping the continent.',
            'keywords': kws,
            'match_rules': rules,
            'categories': ['world', 'politics'],
            'languages': ['en', 'de', 'fr', 'es', 'it', 'pt', 'pl'],
            'priority': 3,
            'meta_title': 'European Politics: EU & National News | 24HourWire',
            'meta_description': 'European political news: EU institutions, elections, coalitions, and policy debates from diverse sources across the continent.',
            'translations': {
                'es': {
                    'title': 'Política europea',
                    'headline': 'Instituciones de la UE, elecciones y debates políticos transfronterizos',
                    'description': 'Cobertura de la política europea, desde las instituciones de la UE y las elecciones hasta los gobiernos nacionales, las coaliciones y los debates políticos que dan forma al continente.',
                    'meta_title': 'Política europea',
                },
                'fr': {
                    'title': 'Politique européenne',
                    'headline': "Institutions de l'UE, élections et débats politiques transfrontaliers",
                    'description': "Couverture de la politique européenne, des institutions de l'UE et des élections aux gouvernements nationaux, aux coalitions et aux débats politiques qui façonnent le continent.",
                    'meta_title': 'Politique européenne',
                },
                'de': {
                    'title': 'Europäische Politik',
                    'headline': 'EU-Institutionen, Wahlen und grenzüberschreitende politische Debatten',
                    'description': 'Berichterstattung über europäische Politik, von EU-Institutionen und Wahlen bis zu nationalen Regierungen, Koalitionen und politischen Debatten, die den Kontinent prägen.',
                    'meta_title': 'Europäische Politik',
                },
                'it': {
                    'title': 'Politica europea',
                    'headline': 'Istituzioni UE, elezioni e dibattiti politici transfrontalieri',
                    'description': "Copertura della politica europea, dalle istituzioni dell'UE e dalle elezioni ai governi nazionali, alle coalizioni e ai dibattiti politici che plasmano il continente.",
                    'meta_title': 'Politica europea',
                },
                'pt': {
                    'title': 'Política europeia',
                    'headline': 'Instituições da UE, eleições e debates políticos transfronteiriços',
                    'description': 'Cobertura da política europeia, das instituições da UE e das eleições aos governos nacionais, coalizões e debates políticos que moldam o continente.',
                    'meta_title': 'Política europeia',
                },
                'pl': {
                    'title': 'Polityka europejska',
                    'headline': 'Instytucje UE, wybory i transgraniczne debaty polityczne',
                    'description': 'Relacje z polityki europejskiej, od instytucji UE i wyborów po rządy narodowe, koalicje i debaty polityczne kształtujące kontynent.',
                    'meta_title': 'Polityka europejska',
                },
            },
        })

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
