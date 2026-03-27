from collections import OrderedDict

CODE = 'hi'
NAME = 'हिन्दी'

FEEDS = [
    ('BBC हिन्दी', 'https://feeds.bbci.co.uk/hindi/rss.xml'),
    ('NDTV हिन्दी', 'https://feeds.feedburner.com/ndtvnews-hindi'),
    ('Aaj Tak', 'https://news.google.com/rss/search?q=site:aajtak.in&hl=hi&gl=IN&ceid=IN:hi'),
    ('Zee News', 'https://news.google.com/rss/search?q=site:zeenews.india.com&hl=hi&gl=IN&ceid=IN:hi'),
    ('ABP News', 'https://news.google.com/rss/search?q=site:abplive.com&hl=hi&gl=IN&ceid=IN:hi'),
    ('Hindustan', 'https://news.google.com/rss/search?q=site:livehindustan.com&hl=hi&gl=IN&ceid=IN:hi'),
    ('Dainik Bhaskar', 'https://news.google.com/rss/search?q=site:bhaskar.com&hl=hi&gl=IN&ceid=IN:hi'),
    ('Amar Ujala', 'https://news.google.com/rss/search?q=site:amarujala.com&hl=hi&gl=IN&ceid=IN:hi'),
    ('DW हिन्दी', 'https://rss.dw.com/xml/rss-hi-all'),
    ('TV9 भारतवर्ष', 'https://news.google.com/rss/search?q=site:tv9hindi.com&hl=hi&gl=IN&ceid=IN:hi'),
]

SOURCE_INFO = {
    'BBC हिन्दी': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'NDTV हिन्दी': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/ndtv/'),
    'Aaj Tak': ('Center', '#666', 'https://mediabiasfactcheck.com/aaj-tak/'),
    'Zee News': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/zee-news/'),
    'ABP News': ('Center', '#666', 'https://mediabiasfactcheck.com/abp-news/'),
    'Hindustan': ('Center', '#666', 'https://mediabiasfactcheck.com/hindustan/'),
    'Dainik Bhaskar': ('Center', '#666', 'https://mediabiasfactcheck.com/dainik-bhaskar/'),
    'Amar Ujala': ('Center', '#666', 'https://mediabiasfactcheck.com/amar-ujala/'),
    'DW हिन्दी': ('Center', '#666', 'https://mediabiasfactcheck.com/deutsche-welle/'),
    'TV9 भारतवर्ष': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
}

DEFAULT_SOURCES = ['BBC हिन्दी', 'NDTV हिन्दी', 'Aaj Tak', 'Hindustan', 'Dainik Bhaskar', 'DW हिन्दी']

SOURCES = [
    ('BBC हिन्दी', 'Left-Center'),
    ('NDTV हिन्दी', 'Left-Center'),
    ('DW हिन्दी', 'Center'),
    ('Aaj Tak', 'Center'),
    ('ABP News', 'Center'),
    ('Hindustan', 'Center'),
    ('Dainik Bhaskar', 'Center'),
    ('Amar Ujala', 'Center'),
    ('TV9 भारतवर्ष', 'Center'),
    ('Zee News', 'Right-Center'),
]

CATEGORY_KEYWORDS = {
    'politics': [
        'सरकार', 'प्रधानमंत्री', 'मुख्यमंत्री', 'मंत्री', 'चुनाव', 'वोट', 'अभियान',
        'संसद', 'राज्यसभा', 'लोकसभा', 'कानून', 'सुधार', 'पार्टी',
        'भाजपा', 'कांग्रेस', 'आप', 'सपा', 'बसपा',
        'विपक्ष', 'गठबंधन', 'राजनीति', 'प्रधानमंत्री कार्यालय',
    ],
    'business': [
        'शेयर बाजार', 'अर्थव्यवस्था', 'बाजार', 'कंपनी', 'बैंक', 'वित्त',
        'निवेश', 'रुपया', 'डॉलर', 'महंगाई', 'बेरोजगारी', 'जीडीपी', 'विकास',
        'शेयर', 'लाभांश', 'ऋण', 'निर्यात', 'आयात',
        'उद्योग', 'व्यापार', 'रोजगार', 'वेतन', 'कर', 'सेंसेक्स',
    ],
    'technology': [
        'तकनीक', 'कृत्रिम बुद्धिमत्ता', 'सॉफ्टवेयर', 'साइबर हमला', 'डिजिटल',
        'रोबोट', 'ऐप', 'स्मार्टफोन', 'इंटरनेट', 'कंप्यूटर', 'डेटा',
        'साइबर सुरक्षा', 'एल्गोरिदम', 'प्लेटफॉर्म', 'सोशल मीडिया', 'स्टार्टअप',
        'गूगल', 'एप्पल', 'माइक्रोसॉफ्ट', 'अमेज़न', 'मेटा', 'टेस्ला',
    ],
    'science': [
        'विज्ञान', 'अनुसंधान', 'खोज', 'प्रजाति', 'आनुवंशिकी', 'जलवायु',
        'भूकंप', 'ज्वालामुखी', 'ग्रह', 'अंतरिक्ष', 'ब्रह्मांड', 'भौतिकी',
        'रसायन', 'जीव विज्ञान', 'प्रयोगशाला', 'वैज्ञानिक', 'नासा',
        'जीवाश्म', 'विकास', 'जैव विविधता', 'महासागर',
    ],
    'health': [
        'अस्पताल', 'डॉक्टर', 'चिकित्सा', 'वैक्सीन', 'महामारी', 'स्वास्थ्य', 'बीमारी',
        'उपचार', 'वायरस', 'क्लिनिक', 'मरीज', 'सर्जरी', 'चिकित्सा', 'लक्षण',
        'निदान', 'फार्मास्यूटिकल', 'पोषण', 'व्यायाम', 'कोविड',
        'कैंसर', 'मधुमेह', 'हृदय', 'मस्तिष्क',
    ],
    'sports': [
        'क्रिकेट', 'आईपीएल', 'फुटबॉल', 'हॉकी', 'विश्व कप', 'ओलंपिक', 'खेल',
        'टीम', 'खिलाड़ी', 'मैच', 'गोल', 'टेनिस', 'बास्केटबॉल',
        'कोच', 'स्टेडियम', 'टूर्नामेंट', 'चैंपियनशिप', 'अंपायर',
        'भारत', 'पाकिस्तान', 'ऑस्ट्रेलिया', 'आईसीसी',
    ],
    'us': [
        'संयुक्त राज्य अमेरिका', 'अमेरिका', 'फ्लोरिडा', 'टेक्सास', 'कैलिफोर्निया',
        'न्यूयॉर्क', 'मियामी', 'लॉस एंजिल्स', 'शिकागो', 'वॉशिंगटन', 'ट्रम्प', 'बाइडेन',
        'व्हाइट हाउस', 'कांग्रेस', 'सीनेट', 'एफबीआई', 'सीआईए', 'पेंटागन',
    ],
    'world': [
        'यूक्रेन', 'रूस', 'चीन', 'ईरान', 'इज़राइल', 'गाजा', 'मध्य पूर्व', 'यूरोप',
        'एशिया', 'अफ्रीका', 'लैटिन अमेरिका', 'युद्ध', 'कूटनीतिक', 'आप्रवासन',
        'शरणार्थी', 'विश्व', 'अंतरराष्ट्रीय', 'संयुक्त राष्ट्र', 'नाटो', 'संघर्ष', 'संकट',
        'सैन्य', 'सेना', 'शांति', 'समझौता', 'संधि', 'प्रतिबंध',
    ],
    'entertainment': [
        'फिल्म', 'सिनेमा', 'अभिनेता', 'अभिनेत्री', 'ऑस्कर', 'सेलिब्रिटी',
        'संगीत', 'एल्बम', 'कॉन्सर्ट', 'टूर', 'नेटफ्लिक्स', 'स्ट्रीमिंग', 'बॉक्स ऑफिस',
        'नाटक', 'सीरीज', 'सीजन', 'सीजन फिनाले',
        'गायक', 'बैंड', 'स्पॉटिफाई',
        'डिज़नी', 'हॉलीवुड', 'पुरस्कार', 'रेड कार्पेट',
        'कॉमेडी', 'ड्रामा', 'हॉरर',
        'वीडियो गेम', 'गेमिंग', 'यूट्यूब', 'टिकटॉक',
        'इन्फ्लुएंसर', 'वायरल', 'पॉडकास्ट', 'बेस्टसेलर', 'किताब',
        'टेलीविजन', 'कार्यक्रम', 'बॉलीवुड',
    ],
}

STOP_WORDS = {
    'का', 'की', 'के', 'में', 'से', 'को', 'पर', 'ने', 'है', 'हैं', 'था', 'थे', 'थी',
    'और', 'या', 'लेकिन', 'अगर', 'तो', 'जब', 'कि', 'यह', 'वह', 'ये', 'वे',
    'एक', 'इस', 'उस', 'इन', 'उन', 'कुछ', 'सब', 'हर', 'अपना', 'अपनी',
    'मैं', 'तुम', 'हम', 'आप', 'वो',
    'क्या', 'कौन', 'कब', 'कहाँ', 'क्यों', 'कैसे',
    'नया', 'नई', 'कहा', 'बताया', 'के अनुसार',
    'बहुत', 'भी', 'सिर्फ', 'नहीं', 'हां', 'ना',
}

SOURCE_ATTRIBUTION = r'\s*(BBC हिन्दी|NDTV हिन्दी|Aaj Tak|Zee News|ABP News|Hindustan|Dainik Bhaskar|Amar Ujala|DW हिन्दी|TV9 भारतवर्ष)\s*$'

GENERIC_TEXT = [
    'व्यापक समाचार कवरेज',
    'से संकलित',
    'अधिक जानकारी के लिए यहां क्लिक करें',
]

CATEGORY_NAMES = OrderedDict([
    ('all', 'सभी'),
    ('most_covered', 'सबसे अधिक कवर'),
    ('world', 'विश्व'),
    ('us', 'अमेरिका'),
    ('politics', 'राजनीति'),
    ('business', 'व्यापार'),
    ('technology', 'तकनीक'),
    ('science', 'विज्ञान'),
    ('health', 'स्वास्थ्य'),
    ('sports', 'खेल'),
    ('entertainment', 'मनोरंजन'),
])

UI_STRINGS = {
    'subtitle': 'अपना झुकाव चुनें | वायर सेवाएं और अन्य फीड | पिछले 24 घंटे',
    'how_it_works': 'यह कैसे काम करता है',
    'privacy_text': 'हम आपकी गोपनीयता का सम्मान करते हैं। यह साइट संदर्भिक विज्ञापन (कोई ट्रैकिंग कुकी नहीं) का उपयोग करती है और शीर्षक/सारांश फेयर यूज के तहत दिखाती है।',
    'privacy_link': 'गोपनीयता नीति',
    'got_it': 'समझ गए',
    'sources': 'स्रोत:',
    'center_default': 'केंद्रीय स्रोत (डिफ़ॉल्ट)',
    'all_sources': 'सभी स्रोत',
    'center_only': 'केवल केंद्र',
    'left_center_only': 'केवल मध्य-वाम',
    'left_only': 'केवल वाम',
    'right_only': 'केवल दक्षिण',
    'clear_all': 'सब साफ़ करें',
    'sources_suffix': 'स्रोत',
    'covered_by_2': '2 या अधिक स्रोतों द्वारा कवर की गई कहानियां',
    'paywall_title': 'भुगतान वाली साइट',
    'sources_label': 'स्रोत',
    'read_full': 'पूरी कहानी पढ़ें',
    'find_coverage': 'कवरेज खोजें',
    'search_related': 'संबंधित कवरेज खोजें',
    'bias_rating': 'झुकाव रेटिंग',
    'ago': 'पहले',
    'show_stories': 'दिखाएं',
    'stories': 'कहानियां',
    'no_stories': 'इस श्रेणी में कोई कहानी नहीं',
    'footer_copy': 'समाचार सामग्री © संबंधित प्रकाशक। शीर्षक और सारांश सूचनात्मक उद्देश्यों के लिए फेयर यूज के तहत उपयोग किए गए हैं।',
    'footer_sources': 'स्रोत:',
    'footer_and': 'और',
    'footer_terms': 'शर्तें',
    'footer_privacy': 'गोपनीयता',
    'footer_about': 'के बारे में',
}

PAYWALLED_SOURCES = set()
