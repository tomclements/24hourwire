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
    'us': [
        'états-unis', 'ee.uu.', 'amérique du nord', 'floride', 'texas', 'californie',
        'new york', 'miami', 'los angeles', 'chicago', 'washington', 'trump', 'biden',
        'blanc', 'congrès', 'sénat', 'fbi', 'cia', 'pentagone',
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
    ('us', 'É.-U.'),
    ('politics', 'Politique'),
    ('business', 'Économie'),
    ('technology', 'Technologie'),
    ('science', 'Science'),
    ('health', 'Santé'),
    ('sports', 'Sports'),
    ('entertainment', 'Divertissement'),
])

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
