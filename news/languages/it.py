from collections import OrderedDict

CODE = 'it'
NAME = 'Italiano'

FEEDS = [
    ('Corriere della Sera', 'https://xml2.corriereobjects.it/rss/homepage.xml'),
    ('La Repubblica', 'https://www.repubblica.it/rss/homepage/rss2.0.xml'),
    ('Il Corriere', 'https://news.google.com/rss/search?q=site:corriere.it&hl=it&gl=IT&ceid=IT:it'),
    ('ANSA', 'https://www.ansa.it/sito/ansait_rss.xml'),
    ('La Stampa', 'https://www.lastampa.it/rss/homepage.xml'),
    ('Il Sole 24 Ore', 'https://www.ilsole24ore.com/rss/homepage.xml'),
    ('Il Messaggero', 'https://www.ilmessaggero.it/rss/homepage.xml'),
    ('Il Fatto Quotidiano', 'https://www.ilfattoquotidiano.it/feed/'),
    ('Avvenire', 'https://www.avvenire.it/rss'),
    ('AGI', 'https://www.agi.it/rss/homepage.xml'),
    ('Sky TG24', 'https://news.google.com/rss/search?q=site:tg24.sky.it&hl=it&gl=IT&ceid=IT:it'),
    ('Fanpage', 'https://www.fanpage.it/feed/'),
    ('HuffPost Italia', 'https://news.google.com/rss/search?q=site:huffingtonpost.it&hl=it&gl=IT&ceid=IT:it'),
    
    # Category-specific feeds
    # Sports
    ('Gazzetta dello Sport', 'https://www.gazzetta.it/rss/home.xml'),
    ('Corriere dello Sport', 'https://www.corrieredellosport.it/rss/home.xml'),
    ('Tuttosport', 'https://www.tuttosport.com/rss/home.xml'),
    ('Sky Sport', 'https://sport.sky.it/rss/sport.xml'),
    ('La Repubblica Sport', 'https://www.repubblica.it/rss/sport/rss2.0.xml'),
    ('Corriere Sport', 'https://xml2.corriereobjects.it/rss/sport.xml'),
    ('La Stampa Sport', 'https://www.lastampa.it/rss/sport.xml'),
    
    # Business
    ('Il Sole 24 Ore Economia', 'https://www.ilsole24ore.com/rss/economia.xml'),
    ('ANSA Economia', 'https://www.ansa.it/economia/rss.xml'),
    ('La Repubblica Economia', 'https://www.repubblica.it/rss/economia/rss2.0.xml'),
    ('Corriere Economia', 'https://xml2.corriereobjects.it/rss/economia.xml'),
    ('La Stampa Economia', 'https://www.lastampa.it/rss/economia.xml'),
    ('AGI Economia', 'https://www.agi.it/rss/economia.xml'),
    
    # Technology
    ('La Repubblica Tecnologia', 'https://www.repubblica.it/rss/tecnologia/rss2.0.xml'),
    ('Corriere Tecnologia', 'https://xml2.corriereobjects.it/rss/tecnologia.xml'),
    ('Il Sole 24 Ore Tech', 'https://www.ilsole24ore.com/rss/tecnologia.xml'),
    ('ANSA Tech', 'https://www.ansa.it/tecnologia/rss.xml'),
    ('Wired Italia', 'https://www.wired.it/feed/'),
    ('HDblog', 'https://www.hdblog.it/rss/home.xml'),
    
    # World News
    ('La Repubblica Esteri', 'https://www.repubblica.it/rss/esteri/rss2.0.xml'),
    ('Corriere Esteri', 'https://xml2.corriereobjects.it/rss/esteri.xml'),
    ('ANSA Mondo', 'https://www.ansa.it/mondo/rss.xml'),
    ('Il Messaggero Esteri', 'https://www.ilmessaggero.it/rss/esteri.xml'),
    ('La Stampa Esteri', 'https://www.lastampa.it/rss/esteri.xml'),
    ('Sky TG24 Esteri', 'https://tg24.sky.it/rss/esteri.xml'),
    
    # Science
    ('ANSA Scienza', 'https://www.ansa.it/scienza/rss.xml'),
    ('La Repubblica Scienza', 'https://www.repubblica.it/rss/scienze/rss2.0.xml'),
    ('Corriere Scienze', 'https://xml2.corriereobjects.it/rss/scienze.xml'),
    ('Le Scienze', 'https://www.lescienze.it/rss/news.xml'),
    ('Focus Italia', 'https://www.focus.it/rss.xml'),
    
    # Health
    ('ANSA Salute', 'https://www.ansa.it/salute/rss.xml'),
    ('La Repubblica Salute', 'https://www.repubblica.it/rss/salute/rss2.0.xml'),
    ('Corriere Salute', 'https://xml2.corriereobjects.it/rss/salute.xml'),
    ('La Stampa Salute', 'https://www.lastampa.it/rss/salute.xml'),
    
    # Entertainment
    ('ANSA Spettacolo', 'https://www.ansa.it/spettacolo/rss.xml'),
    ('La Repubblica Spettacoli', 'https://www.repubblica.it/rss/spettacoli/rss2.0.xml'),
    ('Corriere Spettacoli', 'https://xml2.corriereobjects.it/rss/spettacoli.xml'),
    ('La Stampa Cultura', 'https://www.lastampa.it/rss/cultura.xml'),
    ('Sky TG24 Spettacolo', 'https://tg24.sky.it/rss/spettacolo.xml'),
    ('Vanity Fair Italia', 'https://www.vanityfair.it/rss.xml'),
    
    # Politics
    ('La Repubblica Politica', 'https://www.repubblica.it/rss/politica/rss2.0.xml'),
    ('Corriere Politica', 'https://xml2.corriereobjects.it/rss/politica.xml'),
    ('ANSA Politica', 'https://www.ansa.it/politica/rss.xml'),
    ('Il Fatto Quotidiano Politica', 'https://www.ilfattoquotidiano.it/tag/politica/feed/'),
    ('La Stampa Politica', 'https://www.lastampa.it/rss/politica.xml'),
    ('Il Messaggero Politica', 'https://www.ilmessaggero.it/rss/politica.xml'),
]

SOURCE_INFO = {
    'Corriere della Sera': ('Center', '#666', 'https://mediabiasfactcheck.com/corriere-della-sera/'),
    'La Repubblica': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/repubblica/'),
    'Il Corriere': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'ANSA': ('Center', '#666', 'https://mediabiasfactcheck.com/ansa/'),
    'La Stampa': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/la-stampa/'),
    'Il Sole 24 Ore': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/il-sole-24-ore/'),
    'Il Messaggero': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Il Fatto Quotidiano': ('Left', '#999', 'https://mediabiasfactcheck.com/'),
    'Avvenire': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/'),
    'AGI': ('Center', '#666', 'https://mediabiasfactcheck.com/agi/'),
    'Sky TG24': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Fanpage': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/'),
    'HuffPost Italia': ('Left', '#999', 'https://mediabiasfactcheck.com/'),
    
    # Category-specific sources
    'Gazzetta dello Sport': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Corriere dello Sport': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Tuttosport': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Sky Sport': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'La Repubblica Sport': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/repubblica/'),
    'Corriere Sport': ('Center', '#666', 'https://mediabiasfactcheck.com/corriere-della-sera/'),
    'La Stampa Sport': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/la-stampa/'),
    'Il Sole 24 Ore Economia': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/il-sole-24-ore/'),
    'ANSA Economia': ('Center', '#666', 'https://mediabiasfactcheck.com/ansa/'),
    'La Repubblica Economia': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/repubblica/'),
    'Corriere Economia': ('Center', '#666', 'https://mediabiasfactcheck.com/corriere-della-sera/'),
    'La Stampa Economia': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/la-stampa/'),
    'AGI Economia': ('Center', '#666', 'https://mediabiasfactcheck.com/agi/'),
    'La Repubblica Tecnologia': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/repubblica/'),
    'Corriere Tecnologia': ('Center', '#666', 'https://mediabiasfactcheck.com/corriere-della-sera/'),
    'Il Sole 24 Ore Tech': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/il-sole-24-ore/'),
    'ANSA Tech': ('Center', '#666', 'https://mediabiasfactcheck.com/ansa/'),
    'Wired Italia': ('Center', '#666', 'https://mediabiasfactcheck.com/wired/'),
    'HDblog': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'La Repubblica Esteri': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/repubblica/'),
    'Corriere Esteri': ('Center', '#666', 'https://mediabiasfactcheck.com/corriere-della-sera/'),
    'ANSA Mondo': ('Center', '#666', 'https://mediabiasfactcheck.com/ansa/'),
    'Il Messaggero Esteri': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'La Stampa Esteri': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/la-stampa/'),
    'Sky TG24 Esteri': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'ANSA Scienza': ('Center', '#666', 'https://mediabiasfactcheck.com/ansa/'),
    'La Repubblica Scienza': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/repubblica/'),
    'Corriere Scienze': ('Center', '#666', 'https://mediabiasfactcheck.com/corriere-della-sera/'),
    'Le Scienze': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Focus Italia': ('Center', '#666', 'https://mediabiasfactcheck.com/focus/'),
    'ANSA Salute': ('Center', '#666', 'https://mediabiasfactcheck.com/ansa/'),
    'La Repubblica Salute': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/repubblica/'),
    'Corriere Salute': ('Center', '#666', 'https://mediabiasfactcheck.com/corriere-della-sera/'),
    'La Stampa Salute': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/la-stampa/'),
    'ANSA Spettacolo': ('Center', '#666', 'https://mediabiasfactcheck.com/ansa/'),
    'La Repubblica Spettacoli': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/repubblica/'),
    'Corriere Spettacoli': ('Center', '#666', 'https://mediabiasfactcheck.com/corriere-della-sera/'),
    'La Stampa Cultura': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/la-stampa/'),
    'Sky TG24 Spettacolo': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Vanity Fair Italia': ('Center', '#666', 'https://mediabiasfactcheck.com/vanity-fair/'),
    'La Repubblica Politica': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/repubblica/'),
    'Corriere Politica': ('Center', '#666', 'https://mediabiasfactcheck.com/corriere-della-sera/'),
    'ANSA Politica': ('Center', '#666', 'https://mediabiasfactcheck.com/ansa/'),
    'Il Fatto Quotidiano Politica': ('Left', '#999', 'https://mediabiasfactcheck.com/'),
    'La Stampa Politica': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/la-stampa/'),
    'Il Messaggero Politica': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
}

DEFAULT_SOURCES = ['Corriere della Sera', 'La Repubblica', 'ANSA', 'La Stampa', 'AGI', 'Sky TG24']

SOURCES = [
    ('Corriere della Sera', 'Center'),
    ('ANSA', 'Center'),
    ('AGI', 'Center'),
    ('Sky TG24', 'Center'),
    ('Il Messaggero', 'Center'),
    ('La Repubblica', 'Left-Center'),
    ('La Stampa', 'Left-Center'),
    ('Avvenire', 'Left-Center'),
    ('Fanpage', 'Left-Center'),
    ('Il Sole 24 Ore', 'Right-Center'),
    ('Il Fatto Quotidiano', 'Left'),
    ('HuffPost Italia', 'Left'),
    ('Il Corriere', 'Center'),
    
    # Category-specific sources
    ('Gazzetta dello Sport', 'Center'),
    ('Corriere dello Sport', 'Center'),
    ('Tuttosport', 'Center'),
    ('Sky Sport', 'Center'),
    ('La Repubblica Sport', 'Left-Center'),
    ('Corriere Sport', 'Center'),
    ('La Stampa Sport', 'Left-Center'),
    ('Il Sole 24 Ore Economia', 'Right-Center'),
    ('ANSA Economia', 'Center'),
    ('La Repubblica Economia', 'Left-Center'),
    ('Corriere Economia', 'Center'),
    ('La Stampa Economia', 'Left-Center'),
    ('AGI Economia', 'Center'),
    ('La Repubblica Tecnologia', 'Left-Center'),
    ('Corriere Tecnologia', 'Center'),
    ('Il Sole 24 Ore Tech', 'Right-Center'),
    ('ANSA Tech', 'Center'),
    ('Wired Italia', 'Center'),
    ('HDblog', 'Center'),
    ('La Repubblica Esteri', 'Left-Center'),
    ('Corriere Esteri', 'Center'),
    ('ANSA Mondo', 'Center'),
    ('Il Messaggero Esteri', 'Center'),
    ('La Stampa Esteri', 'Left-Center'),
    ('Sky TG24 Esteri', 'Center'),
    ('ANSA Scienza', 'Center'),
    ('La Repubblica Scienza', 'Left-Center'),
    ('Corriere Scienze', 'Center'),
    ('Le Scienze', 'Center'),
    ('Focus Italia', 'Center'),
    ('ANSA Salute', 'Center'),
    ('La Repubblica Salute', 'Left-Center'),
    ('Corriere Salute', 'Center'),
    ('La Stampa Salute', 'Left-Center'),
    ('ANSA Spettacolo', 'Center'),
    ('La Repubblica Spettacoli', 'Left-Center'),
    ('Corriere Spettacoli', 'Center'),
    ('La Stampa Cultura', 'Left-Center'),
    ('Sky TG24 Spettacolo', 'Center'),
    ('Vanity Fair Italia', 'Center'),
    ('La Repubblica Politica', 'Left-Center'),
    ('Corriere Politica', 'Center'),
    ('ANSA Politica', 'Center'),
    ('Il Fatto Quotidiano Politica', 'Left'),
    ('La Stampa Politica', 'Left-Center'),
    ('Il Messaggero Politica', 'Center'),
]

CATEGORY_KEYWORDS = {
    'politics': [
        'governo', 'presidente', 'ministro', 'elezione', 'voto', 'campagna',
        'parlamento', 'senato', 'camera', 'legge', 'riforma', 'partito',
        'meloni', 'salvini', 'conte', 'draghi', 'quirinale', 'palazzo chigi',
        'opposizione', 'maggioranza', 'politica', 'sinistra', 'destra',
    ],
    'business': [
        'borsa', 'economia', 'mercato', 'azienda', 'banca', 'finanza',
        'investimento', 'euro', 'inflazione', 'disoccupazione', 'pil', 'crescita',
        'azione', 'dividendo', 'credito', 'debito', 'esportazione', 'importazione',
        'ftse mib', 'industria', 'commercio', 'lavoro', 'stipendio', 'tasse',
    ],
    'technology': [
        'tecnologia', 'intelligenza artificiale', 'software', 'cyberattacco', 'digitale',
        'robot', 'app', 'smartphone', 'internet', 'informatica', 'dati',
        'cybersicurezza', 'algoritmo', 'piattaforma', 'social network', 'startup',
        'google', 'apple', 'microsoft', 'amazon', 'meta', 'tesla',
    ],
    'science': [
        'scienza', 'ricerca', 'scoperta', 'specie', 'genetica', 'clima',
        'terremoto', 'vulcano', 'pianeta', 'spazio', 'universo', 'fisica',
        'chimica', 'biologia', 'laboratorio', 'studio', 'scienziato', 'nasa',
        'fossile', 'evoluzione', 'biodiversità', 'oceano',
    ],
    'health': [
        'ospedale', 'medico', 'medicina', 'vaccino', 'pandemia', 'salute', 'malattia',
        'trattamento', 'virus', 'clinica', 'paziente', 'chirurgia', 'terapia', 'sintomo',
        'diagnosi', 'farmaceutico', 'nutrizione', 'esercizio', 'benessere', 'covid',
        'cancro', 'diabete', 'cuore', 'cervello', 'ssn',
    ],
    'sports': [
        'calcio', 'serie a', 'champions', 'coppa', 'mondiale', 'olimpiadi', 'sport',
        'squadra', 'giocatore', 'partita', 'gol', 'tennis', 'basket', 'pallavolo',
        'allenatore', 'stadio', 'torneo', 'campionato', 'arbitro',
        'juventus', 'milan', 'inter', 'napoli', 'roma', 'serie b', 'formule 1',
    ],
    'italia': [
        'italia', 'governo', 'presidente', 'meloni', 'parlamento', 'camera', 'senato',
        'roma', 'milano', 'napoli', 'fdi', 'lega', 'pd', 'm5s', 'forza italia',
        'europa', 'ue', 'commissione europea', 'parlamento europeo', 'germania', 'francia', 'spagna',
    ],
    'world': [
        'ucraina', 'russia', 'cina', 'iran', 'israele', 'gaza', 'medio oriente', 'europa',
        'asia', 'africa', 'america latina', 'guerra', 'diplomatico', 'immigrazione',
        'rifugiato', 'mondiale', 'internazionale', 'onu', 'nato', 'conflitto', 'crisi',
        'militare', 'esercito', 'pace', 'accordo', 'trattato', 'sanzioni',
    ],
    'entertainment': [
        'film', 'cinema', 'attore', 'attrice', 'oscar', 'david di donatello', 'celebrità',
        'musica', 'album', 'concerto', 'tour', 'netflix', 'streaming', 'botteghino',
        'teatro', 'serie', 'stagione', 'finale di stagione',
        'cantante', 'band', 'spotify',
        'disney', 'hollywood', 'premio', 'tappeto rosso',
        'commedia', 'dramma', 'horror',
        'videogioco', 'gaming', 'youtube', 'tiktok',
        'influencer', 'virale', 'podcast', 'bestseller', 'libro',
        'televisione', 'programma', 'sanremo', 'festival',
    ],
}

STOP_WORDS = {
    'il', 'lo', 'la', 'i', 'gli', 'le', 'un', 'uno', 'una', 'e', 'o', 'ma',
    'in', 'di', 'del', 'della', 'dei', 'delle', 'al', 'alla', 'ai', 'alle',
    'a', 'da', 'per', 'con', 'su', 'tra', 'fra',
    'è', 'sono', 'era', 'erano', 'fu', 'essere', 'avere', 'ha', 'hanno',
    'che', 'quale', 'chi', 'come', 'quando', 'dove', 'perché',
    'questo', 'questa', 'questi', 'queste', 'quello', 'quella', 'quelli', 'quelle',
    'lui', 'lei', 'loro', 'io', 'tu', 'noi', 'voi',
    'mio', 'mia', 'tuo', 'tua', 'suo', 'sua', 'nostro', 'nostra',
    'più', 'molto', 'anche', 'già', 'ancora', 'solo', 'non', 'sì', 'né',
    'dopo', 'prima', 'tra', 'sotto', 'sopra',
}

SOURCE_ATTRIBUTION = r'\s*(Corriere della Sera|La Repubblica|ANSA|La Stampa|Il Sole 24 Ore|Il Messaggero|Il Fatto Quotidiano|Avvenire|AGI|Sky TG24|Fanpage|HuffPost Italia|Il Corriere)\s*$'

GENERIC_TEXT = [
    'copertura completa delle notizie',
    'aggregato da',
    'clicca qui per altro',
]

CATEGORY_NAMES = OrderedDict([
    ('all', 'Tutti'),
    ('most_covered', 'Più Coperti'),
    ('world', 'Mondo'),
    ('italia', 'Italia'),
    ('politics', 'Politica'),
    ('business', 'Economia'),
    ('technology', 'Tecnologia'),
    ('science', 'Scienza'),
    ('health', 'Salute'),
    ('sports', 'Sport'),
    ('entertainment', 'Intrattenimento'),
])

CATEGORY_KEYWORDS_WEIGHTED = {
    'politics': {
        'high': ['meloni', 'salvini', 'conte', 'draghi', 'quirinale', 'palazzo chigi', 'parlamento', 'camera', 'senato'],
        'medium': ['governo', 'presidente', 'ministro', 'elezione', 'voto', 'campagna', 'legge', 'riforma', 'partito', 'opposizione', 'maggioranza', 'politica', 'sinistra', 'destra'],
        'low': []
    },
    'business': {
        'high': ['borsa', 'ftse mib', 'euro', 'azione', 'dividendo', 'inflazione'],
        'medium': ['economia', 'mercato', 'azienda', 'banca', 'finanza', 'investimento', 'disoccupazione', 'pil', 'crescita', 'credito', 'debito', 'esportazione', 'importazione', 'industria', 'commercio', 'lavoro', 'stipendio', 'tasse'],
        'low': []
    },
    'technology': {
        'high': ['intelligenza artificiale', 'cyberattacco', 'cybersicurezza', 'algoritmo'],
        'medium': ['tecnologia', 'software', 'digitale', 'robot', 'app', 'smartphone', 'internet', 'informatica', 'dati', 'piattaforma', 'social network', 'startup', 'google', 'apple', 'microsoft', 'amazon', 'meta', 'tesla'],
        'low': []
    },
    'science': {
        'high': ['nasa', 'genetica', 'evoluzione', 'biodiversità'],
        'medium': ['scienza', 'ricerca', 'scoperta', 'specie', 'clima', 'terremoto', 'vulcano', 'pianeta', 'spazio', 'universo', 'fisica', 'chimica', 'biologia', 'laboratorio', 'studio', 'scienziato', 'fossile', 'oceano'],
        'low': []
    },
    'health': {
        'high': ['ospedale', 'medico', 'medicina', 'vaccino', 'pandemia', 'covid', 'cancro', 'diabete', 'ssn'],
        'medium': ['salute', 'malattia', 'trattamento', 'virus', 'clinica', 'paziente', 'chirurgia', 'terapia', 'sintomo', 'diagnosi', 'farmaceutico', 'nutrizione', 'esercizio', 'benessere', 'cuore', 'cervello'],
        'low': []
    },
    'sports': {
        'high': ['juventus', 'milan', 'inter', 'napoli', 'roma', 'serie a', 'serie b', 'coppa italia'],
        'medium': ['calcio', 'serie', 'champions', 'coppa', 'mondiale', 'olimpiadi', 'sport', 'squadra', 'giocatore', 'partita', 'gol', 'tennis', 'basket', 'pallavolo', 'allenatore', 'stadio', 'torneo', 'campionato', 'arbitro', 'formule 1'],
        'low': []
    },
    'italia': {
        'high': ['italia', 'governo', 'presidente', 'meloni', 'parlamento', 'camera', 'senato', 'roma', 'milano', 'napoli'],
        'medium': ['fdi', 'lega', 'pd', 'm5s', 'forza italia', 'europa', 'ue', 'commissione europea', 'parlamento europeo', 'germania', 'francia', 'spagna'],
        'low': []
    },
    'world': {
        'high': ['ucraina', 'russia', 'guerra', 'crisi', 'gaza', 'israele', 'putin'],
        'medium': ['cina', 'iran', 'israele', 'gaza', 'medio oriente', 'europa', 'asia', 'africa', 'america latina', 'diplomatico', 'immigrazione', 'rifugiato', 'mondiale', 'internazionale', 'onu', 'nato', 'conflitto', 'militare', 'esercito', 'pace', 'accordo', 'trattato', 'sanzioni'],
        'low': []
    },
    'entertainment': {
        'high': ['oscar', 'david di donatello', 'sanremo', 'netflix', 'disney', 'hollywood', 'spotify'],
        'medium': ['film', 'cinema', 'attore', 'attrice', 'celebrità', 'musica', 'album', 'concerto', 'tour', 'streaming', 'botteghino', 'teatro', 'serie', 'stagione', 'finale di stagione', 'cantante', 'band', 'premio', 'tappeto rosso', 'commedia', 'dramma', 'horror', 'videogioco', 'gaming', 'youtube', 'tiktok', 'influencer', 'virale', 'podcast', 'bestseller', 'libro', 'televisione', 'programma', 'festival'],
        'low': []
    },
}

UI_STRINGS = {
    'subtitle': 'Scegli il tuo orientamento | Servizi di notizie e altri feed | Ultime 24 ore',
    'how_it_works': 'Come funziona',
    'privacy_text': 'Rispettiamo la tua privacy. Questo sito usa annunci contestuali (senza cookie di tracciamento) e mostra titoli/riassunti sotto fair use.',
    'privacy_link': 'Informativa sulla Privacy',
    'got_it': 'Capito',
    'sources': 'Fonti:',
    'center_default': 'Fonti centrali (predefinito)',
    'all_sources': 'Tutte le fonti',
    'center_only': 'Solo centro',
    'left_center_only': 'Solo centro-sinistra',
    'left_only': 'Solo sinistra',
    'right_only': 'Solo destra',
    'clear_all': 'Cancella tutto',
    'sources_suffix': 'fonti',
    'covered_by_2': 'Storie coperte da 2 o più fonti',
    'paywall_title': 'Sito a pagamento',
    'sources_label': 'fonti',
    'read_full': 'Leggi la storia completa',
    'find_coverage': 'Trova copertura',
    'search_related': 'Cerca copertura correlata',
    'bias_rating': 'Valutazione orientamento',
    'ago': 'fa',
    'show_stories': 'Mostra',
    'stories': 'storie',
    'no_stories': 'Nessuna storia in questa categoria',
    'footer_copy': 'Contenuti notizie © rispettivi editori. Titoli e riassunti utilizzati sotto fair use a scopo informativo.',
    'footer_sources': 'Fonti:',
    'footer_and': 'e',
    'footer_terms': 'Termini',
    'footer_privacy': 'Privacy',
    'footer_about': 'Chi siamo',
    # Header translations
    'logo_tagline': 'Notizie da diverse prospettive',
    'search_placeholder': 'Cerca notizie...',
    'toggle_theme': 'Cambia tema',
    'filter_label': 'Filtra per:',
    # Bias filter buttons
    'filter_all': 'Tutti',
    'filter_left': 'Sinistra',
    'filter_left_center': 'Centro-sinistra',
    'filter_center': 'Centro',
    'filter_right_center': 'Centro-destra',
    'filter_right': 'Destra',
    # Story card buttons
    'find_coverage_btn': 'Trova copertura',
    'different_angle_btn': 'Un altro angolo',
    'share_btn': 'Condividi',
    'different_perspectives': 'Altre prospettive',
    # Different Angle modal
    'different_angle_title': 'Un\'altra prospettiva',
    'original_label': 'Originale:',
    'loading_related': 'Caricamento articoli correlati...',
    'no_related_stories': 'Nessun articolo correlato trovato',
    'error_loading': 'Errore di caricamento',
    # Share modal
    'share_story_title': 'Condividi articolo',
    'share_on_x': 'Condividi su X',
    'share_facebook': 'Condividi su Facebook',
    'share_linkedin': 'Condividi su LinkedIn',
    'copy_link': 'Copia link',
    'copied': 'Copiato!',
    'close': 'Chiudi',
}

PAYWALLED_SOURCES = {
    'Corriere della Sera',
    'La Repubblica',
    'La Stampa',
    'Il Sole 24 Ore',
    'Il Fatto Quotidiano',
}
