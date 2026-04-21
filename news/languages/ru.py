from collections import OrderedDict

CODE = 'ru'
NAME = 'Русский'

FEEDS = [
    ('РИА Новости', 'https://ria.ru/export/rss2/index.xml'),
    ('Тасс', 'https://tass.ru/rss/v2.xml'),
    ('Интерфакс', 'https://www.interfax.ru/rss.asp'),
    ('Коммерсант', 'https://www.kommersant.ru/RSS/main.xml'),
    ('Ведомости', 'https://www.vedomosti.ru/rss/news'),
    ('РБК', 'https://www.rbc.ru/rss/finances.rss'),
    ('RT на русском', 'https://russian.rt.com/rss'),
    ('Lenta.ru', 'https://lenta.ru/rss'),
    ('Gazeta.ru', 'https://www.gazeta.ru/export/rss/lenta.xml'),
    ('Новая газета', 'https://novayagazeta.ru/rss'),
    ('Медуза', 'https://meduza.io/rss/all'),
    ('BBC Русская служба', 'https://feeds.bbci.co.uk/russian/rss.xml'),
    
    # Category-specific feeds
    # Sports
    ('Чемпионат', 'https://www.championat.com/rss/article/'),
    ('Спорт-Экспресс', 'https://www.sport-express.ru/football/rss.xml'),
    ('Советский Спорт', 'https://www.sovsport.ru/rss'),
    ('Бизнес Online Спорт', 'https://www.business-gazeta.ru/rss/sport'),
    ('Газета.ru Спорт', 'https://www.gazeta.ru/export/rss/sport.xml'),
    ('Lenta.ru Спорт', 'https://lenta.ru/rss/news/sport'),
    ('RT Спорт', 'https://russian.rt.com/rss/sport'),
    ('Матч ТВ', 'https://matchtv.ru/rss'),
    
    # Business
    ('РБК Экономика', 'https://www.rbc.ru/rss/economics.rss'),
    ('Коммерсант Экономика', 'https://www.kommersant.ru/RSS/section-economics.xml'),
    ('Ведомости Экономика', 'https://www.vedomosti.ru/rss/news'),
    ('Тасс Экономика', 'https://tass.ru/rss/v2.xml?section= ekonomika'),
    ('РИА Новости Экономика', 'https://ria.ru/export/rss2/economy/index.xml'),
    ('Lenta.ru Экономика', 'https://lenta.ru/rss/news/economics'),
    ('Gazeta.ru Бизнес', 'https://www.gazeta.ru/export/rss/business.xml'),
    
    # Technology
    ('Lenta.ru Наука', 'https://lenta.ru/rss/news/science'),
    ('Gazeta.ru Технологии', 'https://www.gazeta.ru/export/rss/tech.xml'),
    ('RT Технологии', 'https://russian.rt.com/rss/technology'),
    ('N+1', 'https://nplus1.ru/rss'),
    ('Хабр', 'https://habr.com/ru/rss/all/'),
    
    # World News
    ('Lenta.ru Мир', 'https://lenta.ru/rss/news/world'),
    ('Gazeta.ru Мир', 'https://www.gazeta.ru/export/rss/world.xml'),
    ('РИА Новости Мир', 'https://ria.ru/export/rss2/world/index.xml'),
    ('Тасс Мир', 'https://tass.ru/rss/v2.xml?section= mezhdunarodnaya-panorama'),
    ('BBC Русская служба Мир', 'https://feeds.bbci.co.uk/russian/rss.xml'),
    ('RT Мир', 'https://russian.rt.com/rss/world'),
    
    # Science
    ('Lenta.ru Наука', 'https://lenta.ru/rss/news/science'),
    ('Gazeta.ru Наука', 'https://www.gazeta.ru/export/rss/science.xml'),
    ('RT Наука', 'https://russian.rt.com/rss/science'),
    ('Популярная механика', 'https://www.popmech.ru/rss'),
    
    # Health
    ('Газета.ru Здоровье', 'https://www.gazeta.ru/export/rss/health.xml'),
    ('Lenta.ru Здоровье', 'https://lenta.ru/rss/news/health'),
    ('RT Здоровье', 'https://russian.rt.com/rss/health'),
    
    # Entertainment
    ('Lenta.ru Культура', 'https://lenta.ru/rss/news/culture'),
    ('Gazeta.ru Культура', 'https://www.gazeta.ru/export/rss/culture.xml'),
    ('RT Культура', 'https://russian.rt.com/rss/culture'),
    ('РИА Новости Культура', 'https://ria.ru/export/rss2/culture/index.xml'),
    
    # Politics
    ('Lenta.ru Политика', 'https://lenta.ru/rss/news/politics'),
    ('Gazeta.ru Политика', 'https://www.gazeta.ru/export/rss/politics.xml'),
    ('RT Политика', 'https://russian.rt.com/rss/politics'),
    ('РИА Новости Политика', 'https://ria.ru/export/rss2/politics/index.xml'),
    ('Тасс Политика', 'https://tass.ru/rss/v2.xml?section= politika'),
    ('Новая газета Политика', 'https://novayagazeta.ru/rss'),
    ('Медуза Политика', 'https://meduza.io/rss/politics'),
]

SOURCE_INFO = {
    'РИА Новости': ('Center', '#666', 'https://mediabiasfactcheck.com/ria-novosti/'),
    'Тасс': ('Center', '#666', 'https://mediabiasfactcheck.com/tass/'),
    'Интерфакс': ('Center', '#666', 'https://mediabiasfactcheck.com/interfax/'),
    'Коммерсант': ('Center', '#666', 'https://mediabiasfactcheck.com/kommersant/'),
    'Ведомости': ('Center', '#666', 'https://mediabiasfactcheck.com/vedomosti/'),
    'РБК': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RT на русском': ('Right', '#666', 'https://mediabiasfactcheck.com/rt/'),
    'Lenta.ru': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Gazeta.ru': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Новая газета': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/novaya-gazeta/'),
    'Медуза': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/meduza/'),
    ('BBC Русская служба'): ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    
    # Category-specific sources
    'Чемпионат': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Спорт-Экспресс': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Советский Спорт': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Бизнес Online Спорт': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Газета.ru Спорт': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Lenta.ru Спорт': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RT Спорт': ('Right', '#666', 'https://mediabiasfactcheck.com/rt/'),
    'Матч ТВ': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'РБК Экономика': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Коммерсант Экономика': ('Center', '#666', 'https://mediabiasfactcheck.com/kommersant/'),
    'Ведомости Экономика': ('Center', '#666', 'https://mediabiasfactcheck.com/vedomosti/'),
    'Тасс Экономика': ('Center', '#666', 'https://mediabiasfactcheck.com/tass/'),
    'РИА Новости Экономика': ('Center', '#666', 'https://mediabiasfactcheck.com/ria-novosti/'),
    'Lenta.ru Экономика': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Gazeta.ru Бизнес': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Lenta.ru Наука': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Gazeta.ru Технологии': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RT Технологии': ('Right', '#666', 'https://mediabiasfactcheck.com/rt/'),
    'N+1': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Хабр': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Lenta.ru Мир': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Gazeta.ru Мир': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'РИА Новости Мир': ('Center', '#666', 'https://mediabiasfactcheck.com/ria-novosti/'),
    'Тасс Мир': ('Center', '#666', 'https://mediabiasfactcheck.com/tass/'),
    'BBC Русская служба Мир': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'RT Мир': ('Right', '#666', 'https://mediabiasfactcheck.com/rt/'),
    'RT Наука': ('Right', '#666', 'https://mediabiasfactcheck.com/rt/'),
    'Популярная механика': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Газета.ru Здоровье': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Lenta.ru Здоровье': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RT Здоровье': ('Right', '#666', 'https://mediabiasfactcheck.com/rt/'),
    'Lenta.ru Культура': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Gazeta.ru Культура': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RT Культура': ('Right', '#666', 'https://mediabiasfactcheck.com/rt/'),
    'РИА Новости Культура': ('Center', '#666', 'https://mediabiasfactcheck.com/ria-novosti/'),
    'Lenta.ru Политика': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Gazeta.ru Политика': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RT Политика': ('Right', '#666', 'https://mediabiasfactcheck.com/rt/'),
    'РИА Новости Политика': ('Center', '#666', 'https://mediabiasfactcheck.com/ria-novosti/'),
    'Тасс Политика': ('Center', '#666', 'https://mediabiasfactcheck.com/tass/'),
    'Новая газета Политика': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/novaya-gazeta/'),
    'Медуза Политика': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/meduza/'),
}

DEFAULT_SOURCES = ['РИА Новости', 'Тасс', 'Интерфакс', 'Коммерсант', 'BBC Русская служба', 'Медуза']

SOURCES = [
    ('РИА Новости', 'Center'),
    ('Тасс', 'Center'),
    ('Интерфакс', 'Center'),
    ('Коммерсант', 'Center'),
    ('Ведомости', 'Center'),
    ('РБК', 'Center'),
    ('Lenta.ru', 'Center'),
    ('Gazeta.ru', 'Center'),
    ('BBC Русская служба', 'Left-Center'),
    ('Новая газета', 'Left-Center'),
    ('Медуза', 'Left-Center'),
    ('RT на русском', 'Right'),
    
    # Category-specific sources
    ('Чемпионат', 'Center'),
    ('Спорт-Экспресс', 'Center'),
    ('Советский Спорт', 'Center'),
    ('Бизнес Online Спорт', 'Center'),
    ('Газета.ru Спорт', 'Center'),
    ('Lenta.ru Спорт', 'Center'),
    ('RT Спорт', 'Right'),
    ('Матч ТВ', 'Center'),
    ('РБК Экономика', 'Center'),
    ('Коммерсант Экономика', 'Center'),
    ('Ведомости Экономика', 'Center'),
    ('Тасс Экономика', 'Center'),
    ('РИА Новости Экономика', 'Center'),
    ('Lenta.ru Экономика', 'Center'),
    ('Gazeta.ru Бизнес', 'Center'),
    ('Lenta.ru Наука', 'Center'),
    ('Gazeta.ru Технологии', 'Center'),
    ('RT Технологии', 'Right'),
    ('N+1', 'Center'),
    ('Хабр', 'Center'),
    ('Lenta.ru Мир', 'Center'),
    ('Gazeta.ru Мир', 'Center'),
    ('РИА Новости Мир', 'Center'),
    ('Тасс Мир', 'Center'),
    ('BBC Русская служба Мир', 'Left-Center'),
    ('RT Мир', 'Right'),
    ('RT Наука', 'Right'),
    ('Популярная механика', 'Center'),
    ('Газета.ru Здоровье', 'Center'),
    ('Lenta.ru Здоровье', 'Center'),
    ('RT Здоровье', 'Right'),
    ('Lenta.ru Культура', 'Center'),
    ('Gazeta.ru Культура', 'Center'),
    ('RT Культура', 'Right'),
    ('РИА Новости Культура', 'Center'),
    ('Lenta.ru Политика', 'Center'),
    ('Gazeta.ru Политика', 'Center'),
    ('RT Политика', 'Right'),
    ('РИА Новости Политика', 'Center'),
    ('Тасс Политика', 'Center'),
    ('Новая газета Политика', 'Left-Center'),
    ('Медуза Политика', 'Left-Center'),
]

CATEGORY_KEYWORDS = {
    'politics': [
        'правительство', 'президент', 'министр', 'выборы', 'голосование', 'кампания',
        'дума', 'совет федерации', 'парламент', 'закон', 'реформа', 'партия',
        'путин', 'медведев', 'кремль', 'оппозиция', 'политика',
    ],
    'business': [
        'биржа', 'экономика', 'рынок', 'компания', 'банк', 'финансы',
        'инвестиции', 'рубль', 'доллар', 'евро', 'инфляция', 'безработица', 'внп', 'рост',
        'акция', 'дивиденд', 'кредит', 'долг', 'экспорт', 'импорт',
        'промышленность', 'торговля', 'работа', 'зарплата', 'налог', 'нефть', 'газ',
    ],
    'technology': [
        'технология', 'искусственный интеллект', 'программное обеспечение', 'кибератака', 'цифровой',
        'робот', 'приложение', 'смартфон', 'интернет', 'информатика', 'данные',
        'кибербезопасность', 'алгоритм', 'платформа', 'социальные сети', 'стартап',
        'яндекс', 'гугл', 'эпл', 'майкрософт', 'амазон', 'мета', 'тесла',
    ],
    'science': [
        'наука', 'исследование', 'открытие', 'вид', 'генетика', 'климат',
        'землетрясение', 'вулкан', 'планета', 'космос', 'вселенная', 'физика',
        'химия', 'биология', 'лаборатория', 'исследование', 'ученый', 'наса',
        'ископаемое', 'эволюция', 'биоразнообразие', 'океан', 'роскосмос',
    ],
    'health': [
        'больница', 'врач', 'медицина', 'вакцина', 'пандемия', 'здоровье', 'болезнь',
        'лечение', 'вирус', 'клиника', 'пациент', 'хирургия', 'терапия', 'симптом',
        'диагноз', 'фармацевтический', 'питание', 'фитнес', 'благополучие', 'ковид',
        'рак', 'диабет', 'сердце', 'мозг',
    ],
    'sports': [
        'футбол', 'лига', 'чемпионская лига', 'кубок', 'мундиаль', 'олимпиада', 'спорт',
        'команда', 'игрок', 'матч', 'гол', 'теннис', 'баскетбол', 'хоккей',
        'тренер', 'стадион', 'турнир', 'чемпионат', 'арбитр',
        'спартак', 'цска', 'зенит', 'локомотив', 'рпл', 'кхл',
    ],
    'russia': [
        'россия', 'путин', 'правительство', 'дума', 'совет федерации', 'кремль',
        'москва', 'петербург', 'единая россия', 'кпрф', 'лдпр', 'справедливая россия',
        'снг', 'казахстан', 'беларусь', 'узбекистан', 'украина', 'грузия', 'армения',
        'европа', 'евросоюз', 'германия', 'франция', 'италия', 'польша', 'еврокомиссия',
    ],
    'world': [
        'украина', 'россия', 'китай', 'иран', 'израиль', 'газа', 'ближний восток', 'европа',
        'азия', 'африка', 'латинская америка', 'война', 'дипломат', 'иммиграция',
        'беженец', 'мировой', 'международный', 'оон', 'нато', 'конфликт', 'кризис',
        'военный', 'армия', 'мир', 'соглашение', 'договор', 'санкции',
    ],
    'entertainment': [
        'фильм', 'кино', 'актер', 'актриса', 'оскар', 'знаменитость',
        'музыка', 'альбом', 'концерт', 'тур', 'нетфликс', 'стриминг', 'прокат',
        'театр', 'сериал', 'сезон', 'финал сезона',
        'певец', 'группа', 'спотифай',
        'дисней', 'голливуд', 'премия', 'красная дорожка',
        'комедия', 'драма', 'ужасы',
        'видеоигра', 'гейминг', 'ютуб', 'тикток',
        'инфлюенсер', 'вирусный', 'подкаст', 'бестселлер', 'книга',
        'телевидение', 'программа',
    ],
}

STOP_WORDS = {
    'в', 'на', 'с', 'из', 'по', 'к', 'от', 'за', 'до', 'о', 'об', 'при',
    'и', 'или', 'но', 'а',
    'это', 'то', 'что', 'как', 'который', 'которая', 'которое', 'которые',
    'он', 'она', 'оно', 'они', 'мы', 'вы', 'я', 'ты',
    'его', 'её', 'их', 'наш', 'ваш', 'мой', 'твой', 'свой',
    'быть', 'был', 'была', 'было', 'были', 'будет', 'будут',
    'не', 'ни', 'да', 'нет',
    'после', 'перед', 'между', 'под', 'над',
    'более', 'очень', 'тоже', 'уже', 'еще', 'только', 'также',
    'новый', 'новая', 'новое', 'новые', 'сказал', 'сказала', 'по словам',
}

SOURCE_ATTRIBUTION = r'\s*(РИА Новости|Тасс|Интерфакс|Коммерсант|Ведомости|РБК|RT|Lenta\.ru|Gazeta\.ru|Новая газета|Медуза|BBC)\s*$'

GENERIC_TEXT = [
    'полное новостное покрытие',
    'собрано из',
    'нажмите здесь для подробностей',
]

CATEGORY_NAMES = OrderedDict([
    ('all', 'Все'),
    ('most_covered', 'Наиболее Освещённые'),
    ('world', 'Мир'),
    ('russia', 'Россия'),
    ('politics', 'Политика'),
    ('business', 'Бизнес'),
    ('technology', 'Технологии'),
    ('science', 'Наука'),
    ('health', 'Здоровье'),
    ('sports', 'Спорт'),
    ('entertainment', 'Развлечения'),
])

CATEGORY_KEYWORDS_WEIGHTED = {
    'politics': {
        'high': ['путин', 'медведев', 'кремль', 'дума', 'совет федерации', 'парламент'],
        'medium': ['правительство', 'президент', 'министр', 'выборы', 'голосование', 'кампания', 'закон', 'реформа', 'партия', 'оппозиция', 'политика'],
        'low': []
    },
    'business': {
        'high': ['биржа', 'рубль', 'доллар', 'евро', 'акция', 'дивиденд', 'инфляция', 'нефть', 'газ'],
        'medium': ['экономика', 'рынок', 'компания', 'банк', 'финансы', 'инвестиции', 'безработица', 'внп', 'рост', 'кредит', 'долг', 'экспорт', 'импорт', 'промышленность', 'торговля', 'работа', 'зарплата', 'налог'],
        'low': []
    },
    'technology': {
        'high': ['искусственный интеллект', 'кибератака', 'кибербезопасность', 'алгоритм', 'яндекс'],
        'medium': ['технология', 'программное обеспечение', 'цифровой', 'робот', 'приложение', 'смартфон', 'интернет', 'информатика', 'данные', 'платформа', 'социальные сети', 'стартап', 'гугл', 'эпл', 'майкрософт', 'амазон', 'мета', 'тесла'],
        'low': []
    },
    'science': {
        'high': ['наса', 'роскосмос', 'генетика', 'эволюция', 'биоразнообразие'],
        'medium': ['наука', 'исследование', 'открытие', 'вид', 'климат', 'землетрясение', 'вулкан', 'планета', 'космос', 'вселенная', 'физика', 'химия', 'биология', 'лаборатория', 'исследование', 'ученый', 'ископаемое', 'океан'],
        'low': []
    },
    'health': {
        'high': ['больница', 'врач', 'медицина', 'вакцина', 'пандемия', 'ковид', 'рак', 'диабет'],
        'medium': ['здоровье', 'болезнь', 'лечение', 'вирус', 'клиника', 'пациент', 'хирургия', 'терапия', 'симптом', 'диагноз', 'фармацевтический', 'питание', 'фитнес', 'благополучие', 'сердце', 'мозг'],
        'low': []
    },
    'sports': {
        'high': ['спартак', 'цска', 'зенит', 'локомотив', 'рпл', 'кхл'],
        'medium': ['футбол', 'лига', 'чемпионская лига', 'кубок', 'мундиаль', 'олимпиада', 'спорт', 'команда', 'игрок', 'матч', 'гол', 'теннис', 'баскетбол', 'хоккей', 'тренер', 'стадион', 'турнир', 'чемпионат', 'арбитр'],
        'low': []
    },
    'russia': {
        'high': ['россия', 'путин', 'правительство', 'дума', 'совет федерации', 'кремль', 'москва', 'петербург'],
        'medium': ['единая россия', 'кпрф', 'лдпр', 'справедливая россия', 'снг', 'казахстан', 'беларусь', 'узбекистан', 'украина', 'грузия', 'армения', 'европа', 'евросоюз', 'германия', 'франция', 'италия', 'польша', 'еврокомиссия'],
        'low': []
    },
    'world': {
        'high': ['украина', 'война', 'кризис', 'газа', 'израиль', 'зеленский'],
        'medium': ['россия', 'китай', 'иран', 'израиль', 'газа', 'ближний восток', 'европа', 'азия', 'африка', 'латинская америка', 'дипломат', 'иммиграция', 'беженец', 'мировой', 'международный', 'оон', 'нато', 'конфликт', 'военный', 'армия', 'мир', 'соглашение', 'договор', 'санкции'],
        'low': []
    },
    'entertainment': {
        'high': ['оскар', 'нетфликс', 'дисней', 'голливуд', 'спотифай'],
        'medium': ['фильм', 'кино', 'актер', 'актриса', 'знаменитость', 'музыка', 'альбом', 'концерт', 'тур', 'стриминг', 'прокат', 'театр', 'сериал', 'сезон', 'финал сезона', 'певец', 'группа', 'премия', 'красная дорожка', 'комедия', 'драма', 'ужасы', 'видеоигра', 'гейминг', 'ютуб', 'тикток', 'инфлюенсер', 'вирусный', 'подкаст', 'бестселлер', 'книга', 'телевидение', 'программа'],
        'low': []
    },
}

UI_STRINGS = {
    'subtitle': 'Выберите своё направление | Новостные агентства и другие источники | Последние 24 часа',
    'how_it_works': 'Как это работает',
    'privacy_text': 'Мы уважаем вашу конфиденциальность. Этот сайт использует контекстную рекламу (без отслеживающих файлов cookie) и показывает заголовки/аннотации в рамках добросовестного использования.',
    'privacy_link': 'Политика конфиденциальности',
    'got_it': 'Понятно',
    'sources': 'Источники:',
    'center_default': 'Центральные источники (по умолчанию)',
    'all_sources': 'Все источники',
    'center_only': 'Только центр',
    'left_center_only': 'Только левоцентристские',
    'left_only': 'Только левые',
    'right_only': 'Только правые',
    'clear_all': 'Очистить все',
    'sources_suffix': 'источников',
    'covered_by_2': 'Новости, освещённые 2 и более источниками',
    'paywall_title': 'Платный сайт',
    'sources_label': 'источников',
    'read_full': 'Читать полную статью',
    'find_coverage': 'Найти освещение',
    'search_related': 'Искать связанное освещение',
    'bias_rating': 'Оценка направления',
    'ago': 'назад',
    'show_stories': 'Показать',
    'stories': 'статей',
    'no_stories': 'Нет новостей в этой категории',
    'footer_copy': 'Новостной контент © соответствующие издатели. Заголовки и аннотации используются в рамках добросовестного использования в информационных целях.',
    'footer_sources': 'Источники:',
    'footer_and': 'и',
    'footer_terms': 'Условия',
    'footer_privacy': 'Конфиденциальность',
    'footer_about': 'О нас',
    # Header translations
    'logo_tagline': 'Новости с разных сторон',
    'search_placeholder': 'Поиск новостей...',
    'toggle_theme': 'Переключить тему',
    'filter_label': 'Фильтр:',
    # Bias filter buttons
    'filter_all': 'Все',
    'filter_left': 'Левые',
    'filter_left_center': 'Левоцентристские',
    'filter_center': 'Центристские',
    'filter_right_center': 'Правоцентристские',
    'filter_right': 'Правые',
    # Story card buttons
    'find_coverage_btn': 'Найти освещение',
    'different_angle_btn': 'Другой ракурс',
    'share_btn': 'Поделиться',
    'different_perspectives': 'Другие перспективы',
    # Different Angle modal
    'different_angle_title': 'Другая точка зрения',
    'original_label': 'Оригинал:',
    'loading_related': 'Загрузка связанных статей...',
    'no_related_stories': 'Связанные статьи не найдены',
    'error_loading': 'Ошибка загрузки',
    # Share modal
    'share_story_title': 'Поделиться статьёй',
    'share_on_x': 'Поделиться в X',
    'share_facebook': 'Поделиться в Facebook',
    'share_linkedin': 'Поделиться в LinkedIn',
    'copy_link': 'Копировать ссылку',
    'copied': 'Скопировано!',
    'close': 'Закрыть',
}

PAYWALLED_SOURCES = {
    'Коммерсант',
    'Ведомости',
    'РБК',
}
