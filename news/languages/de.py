from collections import OrderedDict

CODE = 'de'
NAME = 'Deutsch'

FEEDS = [
    ('Deutsche Welle', 'https://rss.dw.com/xml/rss-de-all'),
    ('Der Spiegel', 'https://www.spiegel.de/schlagzeilen/index.rss'),
    ('Die Zeit', 'https://newsfeed.zeit.de/index'),
    ('FAZ', 'https://www.faz.net/rss/aktuell/'),
    ('Süddeutsche Zeitung', 'https://www.sueddeutsche.de/news/rss'),
    ('Bild', 'https://www.bild.de/rssfeeds/rss3700658,variante.rss'),
    ('Tagesschau', 'https://www.tagesschau.de/xml/rss2/'),
    ('Handelsblatt', 'https://www.handelsblatt.com/contentexport/feed/schlagzeilen'),
    ('Focus', 'https://www.focus.de/index.rss'),
    ('Stern', 'https://www.stern.de/feed/standard/alle-nachrichten/'),
    ('Welt', 'https://www.welt.de/feeds/latest.rss'),
    ('Rheinische Post', 'https://www.rp-online.de/rss/'),
    ('taz', 'https://taz.de/rss.xml'),
    ('Tagesspiegel', 'https://www.tagesspiegel.de/contentexport/feed/rss'),
]

SOURCE_INFO = {
    'Deutsche Welle': ('Center', '#666', 'https://mediabiasfactcheck.com/deutsche-welle/'),
    'Der Spiegel': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/der-spiegel/'),
    'Die Zeit': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/die-zeit/'),
    'FAZ': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/frankfurter-allgemeine-zeitung/'),
    'Süddeutsche Zeitung': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/suddeutsche-zeitung/'),
    'Bild': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/bild/'),
    'Tagesschau': ('Center', '#666', 'https://mediabiasfactcheck.com/tagesschau/'),
    'Handelsblatt': ('Center', '#666', 'https://mediabiasfactcheck.com/handelsblatt/'),
    'Focus': ('Center', '#666', 'https://mediabiasfactcheck.com/focus/'),
    'Stern': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/stern/'),
    'Welt': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/die-welt/'),
    'Rheinische Post': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'taz': ('Left', '#999', 'https://mediabiasfactcheck.com/taz/'),
    'Tagesspiegel': ('Center', '#666', 'https://mediabiasfactcheck.com/tagesspiegel/'),
}

DEFAULT_SOURCES = ['Deutsche Welle', 'Der Spiegel', 'FAZ', 'Tagesschau', 'Die Zeit', 'Handelsblatt']

SOURCES = [
    ('Deutsche Welle', 'Center'),
    ('Tagesschau', 'Center'),
    ('Handelsblatt', 'Center'),
    ('Focus', 'Center'),
    ('Rheinische Post', 'Center'),
    ('Tagesspiegel', 'Center'),
    ('Der Spiegel', 'Left-Center'),
    ('Die Zeit', 'Left-Center'),
    ('Süddeutsche Zeitung', 'Left-Center'),
    ('Stern', 'Left-Center'),
    ('FAZ', 'Right-Center'),
    ('Bild', 'Right-Center'),
    ('Welt', 'Right-Center'),
    ('taz', 'Left'),
]

CATEGORY_KEYWORDS = {
    'politics': [
        'regierung', 'kanzler', 'minister', 'wahl', 'abstimmung', 'kampagne',
        'bundestag', 'bundesrat', 'parlament', 'gesetz', 'reform', 'partei',
        'spd', 'cdu', 'csu', 'grüne', 'fdp', 'afd', 'bundespräsident',
        'opposition', 'koalition', 'demokratie', 'politik',
    ],
    'business': [
        'börse', 'wirtschaft', 'markt', 'unternehmen', 'bank', 'finanzen',
        'investition', 'euro', 'inflation', 'arbeitslosigkeit', 'bip', 'wachstum',
        'aktie', 'dividende', 'kredit', 'schulden', 'export', 'import', 'dax',
        'konzern', 'handel', 'industrie', 'arbeit', 'gehalt', 'steuer',
    ],
    'technology': [
        'technologie', 'künstliche intelligenz', 'software', 'cyberangriff', 'digital',
        'roboter', 'anwendung', 'smartphone', 'internet', 'informatik', 'daten',
        'cybersicherheit', 'algorithmus', 'plattform', 'soziale netzwerke', 'startup',
        'google', 'apple', 'microsoft', 'amazon', 'meta', 'tesla', 'ki ',
    ],
    'science': [
        'wissenschaft', 'forschung', 'entdeckung', 'art', 'genetik', 'klima',
        'erdbeben', 'vulkan', 'planet', 'weltraum', 'universum', 'physik',
        'chemie', 'biologie', 'labor', 'studie', 'wissenschaftler', 'nasa',
        'fossil', 'evolution', 'biodiversität', 'ozean',
    ],
    'health': [
        'krankenhaus', 'arzt', 'medizin', 'impfung', 'pandemie', 'gesundheit', 'krankheit',
        'behandlung', 'virus', 'klinik', 'patient', 'chirurgie', 'therapie', 'symptom',
        'diagnose', 'pharmazeutisch', 'ernährung', 'fitness', 'wohlbefinden', 'covid',
        'krebs', 'diabetes', 'herz', 'gehirn',
    ],
    'sports': [
        'fußball', 'liga', 'champions', 'pokal', 'weltmeisterschaft', 'olympia', 'sport',
        'mannschaft', 'spieler', 'spiel', 'tor', 'tennis', 'basketball',
        'trainer', 'stadion', 'turnier', 'meisterschaft', 'schiedsrichter',
        'bundesliga', 'bayern', 'dortmund', 'formel 1', 'radfahren',
    ],
    'us': [
        'vereinigte staaten', 'usa', 'amerika', 'florida', 'texas', 'kalifornien',
        'new york', 'miami', 'los angeles', 'chicago', 'washington', 'trump', 'biden',
        'weißes haus', 'kongress', 'senat', 'fbi', 'cia', 'pentagon',
    ],
    'world': [
        'ukraine', 'russland', 'china', 'iran', 'israel', 'gaza', 'naher osten', 'europa',
        'asien', 'afrika', 'lateinamerika', 'krieg', 'diplomat', 'einwanderung',
        'flüchtling', 'weltweit', 'international', 'uno', 'nato', 'konflikt', 'krise',
        'militär', 'armee', 'frieden', 'abkommen', 'vertrag', 'sanktionen',
    ],
    'entertainment': [
        'film', 'kino', 'schauspieler', 'schauspielerin', 'oscar', 'berlinale', 'prominenz',
        'musik', 'album', 'konzert', 'tournee', 'netflix', 'streaming', 'kinokasse',
        'theater', 'serie', 'staffel', 'season finale',
        'sänger', 'band', 'spotify',
        'disney', 'hollywood', 'preis', 'roter teppich',
        'komödie', 'drama', 'horror',
        'videospiel', 'gaming', 'youtube', 'tiktok',
        'influencer', 'viral', 'podcast', 'bestseller', 'buch',
        'fernsehen', 'sendung',
    ],
}

STOP_WORDS = {
    'der', 'die', 'das', 'ein', 'eine', 'und', 'oder', 'aber',
    'in', 'auf', 'an', 'zu', 'für', 'von', 'mit', 'bei', 'aus', 'nach', 'über',
    'ist', 'sind', 'war', 'waren', 'wird', 'werden', 'sein', 'haben', 'hat',
    'dass', 'welche', 'welcher', 'welches', 'wie', 'was', 'wer', 'wo',
    'er', 'sie', 'es', 'sie', 'wir', 'ihr', 'du', 'ich',
    'sein', 'seine', 'seiner', 'seinem', 'ihre', 'ihrer', 'ihrem',
    'mein', 'meine', 'dein', 'deine', 'unser', 'unsere',
    'mehr', 'sehr', 'auch', 'noch', 'schon', 'nur', 'nicht', 'kein', 'keine',
    'nach', 'vor', 'zwischen', 'unter', 'über', 'durch',
    'wann', 'wo', 'warum', 'wie',
    'neu', 'neue', 'neuer', 'neues', 'sagte', 'sagen', 'laut',
}

SOURCE_ATTRIBUTION = r'\s*(Deutsche Welle|Der Spiegel|Die Zeit|FAZ|Süddeutsche Zeitung|Bild|Tagesschau|Handelsblatt|Focus|Stern|Welt|taz|Tagesspiegel|Rheinische Post)\s*$'

GENERIC_TEXT = [
    'umfassende nachrichtenberichterstattung',
    'zusammengestellt von',
    'klicken sie hier für mehr',
]

CATEGORY_NAMES = OrderedDict([
    ('all', 'Alle'),
    ('most_covered', 'Am Meisten Berichtet'),
    ('world', 'Welt'),
    ('us', 'USA'),
    ('politics', 'Politik'),
    ('business', 'Wirtschaft'),
    ('technology', 'Technologie'),
    ('science', 'Wissenschaft'),
    ('health', 'Gesundheit'),
    ('sports', 'Sport'),
    ('entertainment', 'Unterhaltung'),
])

UI_STRINGS = {
    'subtitle': 'Wählen Sie Ihre Ausrichtung | Nachrichtenagenturen und andere Feeds | Letzte 24 Stunden',
    'how_it_works': 'So funktioniert es',
    'privacy_text': 'Wir respektieren Ihre Privatsphäre. Diese Seite verwendet kontextbezogene Werbung (keine Tracking-Cookies) und zeigt Schlagzeilen/Zusammenfassungen unter Fair Use.',
    'privacy_link': 'Datenschutzerklärung',
    'got_it': 'Verstanden',
    'sources': 'Quellen:',
    'center_default': 'Zentrale Quellen (Standard)',
    'all_sources': 'Alle Quellen',
    'center_only': 'Nur Zentrum',
    'left_center_only': 'Nur Mitte-Links',
    'left_only': 'Nur Links',
    'right_only': 'Nur Rechts',
    'clear_all': 'Alle löschen',
    'sources_suffix': 'Quellen',
    'covered_by_2': 'Geschichten, die von 2 oder mehr Quellen berichtet werden',
    'paywall_title': 'Bezahlseite',
    'sources_label': 'Quellen',
    'read_full': 'Vollständigen Artikel lesen',
    'find_coverage': 'Berichterstattung finden',
    'search_related': 'Nach verwandter Berichterstattung suchen',
    'bias_rating': 'Ausrichtungsbewertung',
    'ago': 'vor',
    'show_stories': 'Anzeigen',
    'stories': 'Artikel',
    'no_stories': 'Keine Artikel in dieser Kategorie',
    'footer_copy': 'Nachrichteninhalte © jeweilige Verlage. Schlagzeilen und Zusammenfassungen unter Fair Use zu Informationszwecken.',
    'footer_sources': 'Quellen:',
    'footer_and': 'und',
    'footer_terms': 'Bedingungen',
    'footer_privacy': 'Datenschutz',
    'footer_about': 'Über uns',
}

PAYWALLED_SOURCES = {
    'Der Spiegel',
    'Die Zeit',
    'FAZ',
    'Süddeutsche Zeitung',
    'Handelsblatt',
    'Bild',
}
