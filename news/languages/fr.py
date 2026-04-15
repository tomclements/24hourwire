from collections import OrderedDict

CODE = 'fr'
NAME = 'Français'

FEEDS = [
    ('France 24', 'https://www.france24.com/fr/rss'),
    ('Le Monde', 'https://www.lemonde.fr/rss/une.xml'),
    ('Le Figaro', 'https://www.lefigaro.fr/rss/figaro_actualites.xml'),
    ('BFM TV', 'https://www.bfmtv.com/rss/info/'),
    ('20 Minutes', 'https://www.20minutes.fr/feeds/rss-une.xml'),
    ('Libération', 'https://www.liberation.fr/arc/outboundfeeds/rss-all/'),
    ('L\'Express', 'https://www.lexpress.fr/rss/'),
    ('France Info', 'https://www.francetvinfo.fr/titres.rss'),
    ('L\'Obs', 'https://www.nouvelobs.com/une/rss.xml'),
    ('Le Parisien', 'https://www.leparisien.fr/une/rss.xml'),
    ('RTL', 'https://www.rtl.fr/feeds/rss.xml'),
    ('Europe 1', 'https://www.europe1.fr/rss.xml'),
    ('RFI', 'https://www.rfi.fr/fr/rss'),
    ('Les Echos', 'https://www.lesechos.fr/rss/rss_une.xml'),
    
    # Category-specific feeds
    # Sports
    ('Le Monde Sport', 'https://www.lemonde.fr/sport/rss_full.xml'),
    ('L\'Equipe', 'https://www.lequipe.fr/rss/actu_rss.xml'),
    ('France 24 Sport', 'https://www.france24.com/fr/sport/rss'),
    ('Le Figaro Sport', 'https://www.lefigaro.fr/rss/figaro_sport.xml'),
    ('France Info Sport', 'https://www.francetvinfo.fr/sports.rss'),
    ('RMC Sport', 'https://rmcsport.bfmtv.com/rss/actualites/'),
    ('RTL Sport', 'https://www.rtl.fr/sport/feed'),
    ('20 Minutes Sport', 'https://www.20minutes.fr/rss/sport.xml'),
    
    # Business
    ('Le Monde Economie', 'https://www.lemonde.fr/economie/rss_full.xml'),
    ('Les Echos Economie', 'https://www.lesechos.fr/rss/rss_une.xml'),
    ('Le Figaro Economie', 'https://www.lefigaro.fr/rss/figaro_economie.xml'),
    ('France 24 Economie', 'https://www.france24.com/fr/economie/rss'),
    ('BFM Business', 'https://www.bfmtv.com/economie/rss/'),
    ('L\'Express Economie', 'https://www.lexpress.fr/rss/economie.xml'),
    ('France Info Economie', 'https://www.francetvinfo.fr/economie.rss'),
    
    # Technology
    ('Le Monde Technologie', 'https://www.lemonde.fr/technologies/rss_full.xml'),
    ('Le Figaro Technologie', 'https://www.lefigaro.fr/rss/figaro_tech.xml'),
    ('France 24 Technologie', 'https://www.france24.com/fr/technologies/rss'),
    ('France Info Technologie', 'https://www.francetvinfo.fr/technologie.rss'),
    ('L\'Express Technologie', 'https://www.lexpress.fr/rss/sciences-techniques.xml'),
    ('01net', 'https://www.01net.com/actualites/feed/'),
    ('Numerama', 'https://www.numerama.com/feed/'),
    
    # World News
    ('Le Monde International', 'https://www.lemonde.fr/international/rss_full.xml'),
    ('France 24 International', 'https://www.france24.com/fr/rss'),
    ('Le Figaro International', 'https://www.lefigaro.fr/rss/figaro_international.xml'),
    ('RFI International', 'https://www.rfi.fr/fr/rss'),
    ('Le Parisien International', 'https://www.leparisien.fr/international/rss.xml'),
    ('France Info International', 'https://www.francetvinfo.fr/monde.rss'),
    
    # Science
    ('Le Monde Sciences', 'https://www.lemonde.fr/sciences/rss_full.xml'),
    ('Le Figaro Sciences', 'https://www.lefigaro.fr/rss/figaro_sciences.xml'),
    ('France 24 Sciences', 'https://www.france24.com/fr/sciences/rss'),
    ('France Info Sciences', 'https://www.francetvinfo.fr/sciences.rss'),
    ('Futura-Sciences', 'https://www.futura-sciences.com/rss/actualites.xml'),
    
    # Health
    ('Le Monde Santé', 'https://www.lemonde.fr/sante/rss_full.xml'),
    ('Le Figaro Santé', 'https://www.lefigaro.fr/rss/figaro_sante.xml'),
    ('France Info Santé', 'https://www.francetvinfo.fr/sante.rss'),
    ('RTL Santé', 'https://www.rtl.fr/sante/feed'),
    ('Le Parisien Santé', 'https://www.leparisien.fr/sante/rss.xml'),
    
    # Entertainment
    ('Le Monde Culture', 'https://www.lemonde.fr/culture/rss_full.xml'),
    ('Le Figaro Culture', 'https://www.lefigaro.fr/rss/figaro_culture.xml'),
    ('France 24 Culture', 'https://www.france24.com/fr/culture/rss'),
    ('France Info Culture', 'https://www.francetvinfo.fr/culture.rss'),
    ('Libération Culture', 'https://www.liberation.fr/culture/feed/'),
    ('Le Parisien Loisirs', 'https://www.leparisien.fr/loisirs/rss.xml'),
    ('RTL Culture', 'https://www.rtl.fr/culture/feed'),
    
    # Politics
    ('Le Monde Politique', 'https://www.lemonde.fr/politique/rss_full.xml'),
    ('Le Figaro Politique', 'https://www.lefigaro.fr/rss/figaro_politique.xml'),
    ('France Info Politique', 'https://www.francetvinfo.fr/politique.rss'),
    ('L\'Obs Politique', 'https://www.nouvelobs.com/politique/rss.xml'),
    ('Libération Politique', 'https://www.liberation.fr/politique/feed/'),
    ('Le Parisien Politique', 'https://www.leparisien.fr/politique/rss.xml'),
    ('L\'Express Politique', 'https://www.lexpress.fr/rss/politique.xml'),
    ('France 24 Politique', 'https://www.france24.com/fr/politique/rss'),
]

SOURCE_INFO = {
    'France 24': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/france-24/'),
    'Le Monde': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/le-monde/'),
    'Le Figaro': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/le-figaro/'),
    'BFM TV': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '20 Minutes': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Libération': ('Left', '#999', 'https://mediabiasfactcheck.com/'),
    "L'Express": ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'France Info': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/'),
    "L'Obs": ('Left-Center', '#888', 'https://mediabiasfactcheck.com/'),
    'Le Parisien': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RTL': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Europe 1': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RFI': ('Center', '#666', 'https://mediabiasfactcheck.com/rfi/'),
    'Les Echos': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/'),
    
    # Category-specific sources
    'Le Monde Sport': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/le-monde/'),
    "L'Equipe": ('Center', '#666', 'https://mediabiasfactcheck.com/lequipe/'),
    'France 24 Sport': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/france-24/'),
    'Le Figaro Sport': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/le-figaro/'),
    'France Info Sport': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/'),
    'RMC Sport': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RTL Sport': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '20 Minutes Sport': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Le Monde Economie': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/le-monde/'),
    'Les Echos Economie': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/'),
    'Le Figaro Economie': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/le-figaro/'),
    'France 24 Economie': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/france-24/'),
    'BFM Business': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    "L'Express Economie": ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'France Info Economie': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/'),
    'Le Monde Technologie': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/le-monde/'),
    'Le Figaro Technologie': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/le-figaro/'),
    'France 24 Technologie': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/france-24/'),
    'France Info Technologie': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/'),
    "L'Express Technologie": ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '01net': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Numerama': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Le Monde International': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/le-monde/'),
    'France 24 International': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/france-24/'),
    'Le Figaro International': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/le-figaro/'),
    'RFI International': ('Center', '#666', 'https://mediabiasfactcheck.com/rfi/'),
    'Le Parisien International': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'France Info International': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/'),
    'Le Monde Sciences': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/le-monde/'),
    'Le Figaro Sciences': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/le-figaro/'),
    'France 24 Sciences': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/france-24/'),
    'France Info Sciences': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/'),
    'Futura-Sciences': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Le Monde Santé': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/le-monde/'),
    'Le Figaro Santé': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/le-figaro/'),
    'France Info Santé': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/'),
    'RTL Santé': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Le Parisien Santé': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Le Monde Culture': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/le-monde/'),
    'Le Figaro Culture': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/le-figaro/'),
    'France 24 Culture': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/france-24/'),
    'France Info Culture': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/'),
    'Libération Culture': ('Left', '#999', 'https://mediabiasfactcheck.com/'),
    'Le Parisien Loisirs': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RTL Culture': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Le Monde Politique': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/le-monde/'),
    'Le Figaro Politique': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/le-figaro/'),
    'France Info Politique': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/'),
    "L'Obs Politique": ('Left-Center', '#888', 'https://mediabiasfactcheck.com/'),
    'Libération Politique': ('Left', '#999', 'https://mediabiasfactcheck.com/'),
    'Le Parisien Politique': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    "L'Express Politique": ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'France 24 Politique': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/france-24/'),
}

DEFAULT_SOURCES = ['France 24', 'Le Monde', 'Le Figaro', 'BFM TV', 'France Info', 'Les Echos']

SOURCES = [
    ('France 24', 'Left-Center'),
    ('Le Monde', 'Left-Center'),
    ('France Info', 'Left-Center'),
    ("L'Obs", 'Left-Center'),
    ('RFI', 'Center'),
    ('BFM TV', 'Center'),
    ('20 Minutes', 'Center'),
    ("L'Express", 'Center'),
    ('Le Parisien', 'Center'),
    ('RTL', 'Center'),
    ('Europe 1', 'Center'),
    ('Le Figaro', 'Right-Center'),
    ('Les Echos', 'Right-Center'),
    ('Libération', 'Left'),
    
    # Category-specific sources
    ('Le Monde Sport', 'Left-Center'),
    ("L'Equipe", 'Center'),
    ('France 24 Sport', 'Left-Center'),
    ('Le Figaro Sport', 'Right-Center'),
    ('France Info Sport', 'Left-Center'),
    ('RMC Sport', 'Center'),
    ('RTL Sport', 'Center'),
    ('20 Minutes Sport', 'Center'),
    ('Le Monde Economie', 'Left-Center'),
    ('Les Echos Economie', 'Right-Center'),
    ('Le Figaro Economie', 'Right-Center'),
    ('France 24 Economie', 'Left-Center'),
    ('BFM Business', 'Center'),
    ("L'Express Economie", 'Center'),
    ('France Info Economie', 'Left-Center'),
    ('Le Monde Technologie', 'Left-Center'),
    ('Le Figaro Technologie', 'Right-Center'),
    ('France 24 Technologie', 'Left-Center'),
    ('France Info Technologie', 'Left-Center'),
    ("L'Express Technologie", 'Center'),
    ('01net', 'Center'),
    ('Numerama', 'Center'),
    ('Le Monde International', 'Left-Center'),
    ('France 24 International', 'Left-Center'),
    ('Le Figaro International', 'Right-Center'),
    ('RFI International', 'Center'),
    ('Le Parisien International', 'Center'),
    ('France Info International', 'Left-Center'),
    ('Le Monde Sciences', 'Left-Center'),
    ('Le Figaro Sciences', 'Right-Center'),
    ('France 24 Sciences', 'Left-Center'),
    ('France Info Sciences', 'Left-Center'),
    ('Futura-Sciences', 'Center'),
    ('Le Monde Santé', 'Left-Center'),
    ('Le Figaro Santé', 'Right-Center'),
    ('France Info Santé', 'Left-Center'),
    ('RTL Santé', 'Center'),
    ('Le Parisien Santé', 'Center'),
    ('Le Monde Culture', 'Left-Center'),
    ('Le Figaro Culture', 'Right-Center'),
    ('France 24 Culture', 'Left-Center'),
    ('France Info Culture', 'Left-Center'),
    ('Libération Culture', 'Left'),
    ('Le Parisien Loisirs', 'Center'),
    ('RTL Culture', 'Center'),
    ('Le Monde Politique', 'Left-Center'),
    ('Le Figaro Politique', 'Right-Center'),
    ('France Info Politique', 'Left-Center'),
    ("L'Obs Politique", 'Left-Center'),
    ('Libération Politique', 'Left'),
    ('Le Parisien Politique', 'Center'),
    ("L'Express Politique", 'Center'),
    ('France 24 Politique', 'Left-Center'),
]

CATEGORY_KEYWORDS = {
    'politics': [
        'gouvernement', 'président', 'ministre', 'élection', 'vote', 'campagne',
        'assemblée', 'sénat', 'parlement', 'loi', 'réforme', 'parti', 'gauche', 'droite',
        'macron', 'le pen', 'mélenchon', 'premier ministre', 'état', 'république',
        'député', 'sénateur', 'loi', 'budget', 'fiscalité', 'politique', 'opposition',
    ],
    'business': [
        'bourse', 'économie', 'marché', 'entreprise', 'banque', 'finance',
        'investissement', 'euro', 'inflation', 'chômage', 'pib', 'croissance',
        'action', 'dividende', 'crédit', 'dette', 'export', 'import', 'cac 40',
        'société', 'commerce', 'industrie', 'emploi', 'salaire', 'impôt',
    ],
    'technology': [
        'technologie', 'intelligence artificielle', 'logiciel', 'cyberattaque', 'numérique',
        'robot', 'application', 'smartphone', 'internet', 'informatique', 'données',
        'cybersécurité', 'algorithme', 'plateforme', 'réseaux sociaux', 'startup',
        'google', 'apple', 'microsoft', 'amazon', 'meta', 'tesla', 'ia ',
    ],
    'science': [
        'science', 'recherche', 'découverte', 'espèce', 'génétique', 'climat',
        'tremblement de terre', 'volcan', 'planète', 'espace', 'univers', 'physique',
        'chimie', 'biologie', 'laboratoire', 'étude', 'scientifique', 'nasa',
        'cnrs', 'adn', 'fossile', 'évolution', 'biodiversité', 'océan',
    ],
    'health': [
        'hôpital', 'médecin', 'médecine', 'vaccin', 'pandémie', 'santé', 'maladie',
        'traitement', 'virus', 'clinique', 'patient', 'chirurgie', 'thérapie', 'symptôme',
        'diagnostic', 'pharmaceutique', 'nutrition', 'exercice', 'bien-être', 'covid',
        'cancer', 'diabète', 'coeur', 'cerveau', 'sida', 'grippe',
    ],
    'sports': [
        'football', 'ligue', 'champions', 'coupe', 'mondial', 'olympiques', 'sport',
        'équipe', 'joueur', 'match', 'but', 'tennis', 'basketball', 'rugby',
        'entraîneur', 'stade', 'tournoi', 'championnat', 'sélection', 'arbitre',
        'psg', 'marseille', 'lyon', 'ligue 1', 'ligue des champions', 'roland garros',
        'tour de france', 'formule 1', 'cyclisme', 'natation',
    ],
    'france': [
        'france', 'président', 'macron', 'assemblée nationale', 'sénat', 'gouvernement',
        'paris', 'lyon', 'marseille', 'lr', 'ps', 'lrem', 'rn', 'eelv',
        'belgique', 'roi', 'bruxelles', 'flandre', 'wallonie', 'mr', 'ps', 'n-va',
        'suisse', 'conseil fédéral', 'berne', 'zurich', 'udc', 'ps', 'verts', 'plr',
        'commission européenne', 'bruxelles', 'parlement européen', 'europe', 'ue', 'allemagne', 'italie', 'espagne',
    ],
    'world': [
        'ukraine', 'russie', 'chine', 'iran', 'israël', 'gaza', 'moyen-orient', 'europe',
        'asie', 'afrique', 'amérique latine', 'guerre', 'diplomatique', 'immigration',
        'réfugié', 'mondial', 'international', 'onu', 'otan', 'conflit', 'crise',
        'militaire', 'armée', 'paix', 'accord', 'traité', 'sanctions',
    ],
    'entertainment': [
        'film', 'cinéma', 'acteur', 'actrice', 'oscar', 'césar', 'célébrité',
        'musique', 'album', 'concert', 'tournée', 'netflix', 'streaming', 'box-office',
        'théâtre', 'série', 'saison', 'finale de saison',
        'chanteur', 'groupe', 'spotify',
        'disney', 'hollywood', 'prix', 'tapis rouge',
        'comédie', 'drame', 'horreur',
        'jeu vidéo', 'gaming', 'youtube', 'tiktok',
        'influenceur', 'viral', 'podcast', 'best-seller', 'livre',
        'télévision', 'programme', 'festival', 'cannes',
    ],
}

STOP_WORDS = {
    'le', 'la', 'les', 'un', 'une', 'des', 'y', 'ou', 'mais',
    'en', 'de', 'du', 'des', 'au', 'aux', 'à', 'pour', 'par', 'avec', 'sans', 'sur',
    'est', 'sont', 'était', 'étaient', 'fut', 'être', 'avoir', 'a', 'ont',
    'que', 'quel', 'qui', 'comme', 'ce', 'cette', 'ces', 'celui', 'celle',
    'il', 'elle', 'ils', 'elles', 'son', 'sa', 'ses', 'mon', 'ma', 'mes', 'ton', 'ta', 'tes',
    'notre', 'nos', 'leur', 'leurs', 'je', 'tu', 'nous', 'vous',
    'me', 'te', 'se', 'le', 'la', 'les', 'lui', 'leur',
    'plus', 'très', 'aussi', 'bien', 'tout', 'tous', 'toute', 'toutes',
    'pas', 'ne', 'ni', 'si', 'oui', 'non',
    'après', 'avant', 'entre', 'sous', 'chez', 'dans', 'hors',
    'quand', 'où', 'comment', 'pourquoi', 'combien',
    'nouveau', 'nouvelle', 'nouveaux', 'nouvelles', 'dit', 'a dit', 'selon',
}

SOURCE_ATTRIBUTION = r'\s*(France 24|Le Monde|Le Figaro|BFM TV|Libération|Les Echos|L\'Express|L\'Obs|France Info|Le Parisien|RTL|Europe 1|RFI|20 Minutes)\s*$'

GENERIC_TEXT = [
    'couverture de news complète',
    'agrégé depuis',
    'cliquez ici pour plus',
]

CATEGORY_NAMES = OrderedDict([
    ('all', 'Tout'),
    ('most_covered', 'Plus Couvert'),
    ('world', 'Monde'),
    ('france', 'France'),
    ('politics', 'Politique'),
    ('business', 'Économie'),
    ('technology', 'Technologie'),
    ('science', 'Science'),
    ('health', 'Santé'),
    ('sports', 'Sports'),
    ('entertainment', 'Divertissement'),
])

CATEGORY_KEYWORDS_WEIGHTED = {
    'politics': {
        'high': ['macron', 'président', 'ministre', 'assemblée', 'sénat', 'parlement'],
        'medium': ['gouvernement', 'élection', 'vote', 'campagne', 'loi', 'réforme', 'parti', 'gauche', 'droite', 'mélenchon', 'le pen', 'premier ministre', 'état', 'république', 'député', 'sénateur', 'budget', 'fiscalité', 'politique', 'opposition'],
        'low': []
    },
    'business': {
        'high': ['bourse', 'cac 40', 'euro', 'action', 'dividende', 'inflation'],
        'medium': ['économie', 'marché', 'entreprise', 'banque', 'finance', 'investissement', 'chômage', 'pib', 'croissance', 'crédit', 'dette', 'export', 'import', 'société', 'commerce', 'industrie', 'emploi', 'salaire', 'impôt'],
        'low': []
    },
    'technology': {
        'high': ['intelligence artificielle', 'ia ', 'cyberattaque', 'cybersécurité', 'algorithme'],
        'medium': ['technologie', 'logiciel', 'numérique', 'robot', 'application', 'smartphone', 'internet', 'informatique', 'données', 'plateforme', 'réseaux sociaux', 'startup', 'google', 'apple', 'microsoft', 'amazon', 'meta', 'tesla'],
        'low': []
    },
    'science': {
        'high': ['nasa', 'cnrs', 'génétique', 'adn', 'evolution', 'biodiversité'],
        'medium': ['science', 'recherche', 'découverte', 'espèce', 'climat', 'tremblement de terre', 'volcan', 'planète', 'espace', 'univers', 'physique', 'chimie', 'biologie', 'laboratoire', 'étude', 'scientifique', 'fossile', 'océan'],
        'low': []
    },
    'health': {
        'high': ['hôpital', 'médecin', 'médecine', 'vaccin', 'pandémie', 'covid', 'cancer', 'diabète', 'sida'],
        'medium': ['santé', 'maladie', 'traitement', 'virus', 'clinique', 'patient', 'chirurgie', 'thérapie', 'symptôme', 'diagnostic', 'pharmaceutique', 'nutrition', 'exercice', 'bien-être', 'coeur', 'cerveau', 'grippe'],
        'low': []
    },
    'sports': {
        'high': ['psg', 'marseille', 'lyon', 'ligue 1', 'ligue des champions', 'roland garros', 'tour de france'],
        'medium': ['football', 'ligue', 'champions', 'coupe', 'mondial', 'olympiques', 'sport', 'équipe', 'joueur', 'match', 'but', 'tennis', 'basketball', 'rugby', 'entraîneur', 'stade', 'tournoi', 'championnat', 'sélection', 'arbitre', 'formule 1', 'cyclisme', 'natation'],
        'low': []
    },
    'france': {
        'high': ['france', 'président', 'macron', 'assemblée nationale', 'sénat', 'gouvernement', 'paris', 'lyon', 'marseille'],
        'medium': ['lr', 'ps', 'lrem', 'rn', 'eelv', 'belgique', 'roi', 'bruxelles', 'flandre', 'wallonie', 'mr', 'n-va', 'suisse', 'conseil fédéral', 'berne', 'zurich', 'udc', 'verts', 'plr', 'commission européenne', 'parlement européen', 'europe', 'ue', 'allemagne', 'italie', 'espagne'],
        'low': []
    },
    'world': {
        'high': ['ukraine', 'russie', 'guerre', 'crise', 'gaza', 'israël', 'poutine'],
        'medium': ['chine', 'iran', 'israël', 'gaza', 'moyen-orient', 'europe', 'asie', 'afrique', 'amérique latine', 'diplomatique', 'immigration', 'réfugié', 'mondial', 'international', 'onu', 'otan', 'conflit', 'militaire', 'armée', 'paix', 'accord', 'traité', 'sanctions'],
        'low': []
    },
    'entertainment': {
        'high': ['oscar', 'césar', 'cannes', 'netflix', 'disney', 'hollywood', 'spotify'],
        'medium': ['film', 'cinéma', 'acteur', 'actrice', 'célébrité', 'musique', 'album', 'concert', 'tournée', 'streaming', 'box-office', 'théâtre', 'série', 'saison', 'finale de saison', 'chanteur', 'groupe', 'prix', 'tapis rouge', 'comédie', 'drame', 'horreur', 'jeu vidéo', 'gaming', 'youtube', 'tiktok', 'influenceur', 'viral', 'podcast', 'best-seller', 'livre', 'télévision', 'programme', 'festival'],
        'low': []
    },
}

UI_STRINGS = {
    'subtitle': 'Choisissez votre biais | Services de presse et autres flux | Dernières 24 heures',
    'how_it_works': 'Comment ça marche',
    'privacy_text': 'Nous respectons votre vie privée. Ce site utilise des publicités contextuelles (pas de cookies de suivi) et affiche titres/résumés selon le fair use.',
    'privacy_link': 'Politique de confidentialité',
    'got_it': 'Compris',
    'sources': 'Sources :',
    'center_default': 'Sources centrales (par défaut)',
    'all_sources': 'Toutes les sources',
    'center_only': 'Centre seulement',
    'left_center_only': 'Centre-gauche seulement',
    'left_only': 'Gauche seulement',
    'right_only': 'Droite seulement',
    'clear_all': 'Tout effacer',
    'sources_suffix': 'sources',
    'covered_by_2': 'Histoires couvertes par 2 sources ou plus',
    'paywall_title': 'Site payant',
    'sources_label': 'sources',
    'read_full': 'Lire l\'article complet',
    'find_coverage': 'Trouver une couverture',
    'search_related': 'Rechercher une couverture connexe',
    'bias_rating': 'Évaluation du biais',
    'ago': 'il y a',
    'show_stories': 'Afficher',
    'stories': 'articles',
    'no_stories': 'Aucun article dans cette catégorie',
    'footer_copy': 'Contenu d\'actualité © éditeurs respectifs. Titres et résumés utilisés selon le fair use à titre informatif.',
    'footer_sources': 'Sources :',
    'footer_and': 'et',
    'footer_terms': 'Conditions',
    'footer_privacy': 'Confidentialité',
    'footer_about': 'À propos',
}

PAYWALLED_SOURCES = {
    'Le Monde',
    'Le Figaro',
    'Les Echos',
    "L'Express",
    "L'Obs",
    'Libération',
}
