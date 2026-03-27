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
    'us': [
        'stati uniti', 'usa', 'america del nord', 'florida', 'texas', 'california',
        'new york', 'miami', 'los angeles', 'chicago', 'washington', 'trump', 'biden',
        'casa bianca', 'congresso', 'senato', 'fbi', 'cia', 'pentagono',
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
    ('us', 'USA'),
    ('politics', 'Politica'),
    ('business', 'Economia'),
    ('technology', 'Tecnologia'),
    ('science', 'Scienza'),
    ('health', 'Salute'),
    ('sports', 'Sport'),
    ('entertainment', 'Intrattenimento'),
])

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
}

PAYWALLED_SOURCES = {
    'Corriere della Sera',
    'La Repubblica',
    'La Stampa',
    'Il Sole 24 Ore',
    'Il Fatto Quotidiano',
}
