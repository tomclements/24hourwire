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
    
    # Category-specific feeds
    # Sports
    ('NDTV खेल', 'https://sports.ndtv.com/rss'),
    ('Aaj Tak खेल', 'https://www.aajtak.in/sports/rss'),
    ('Zee News खेल', 'https://zeenews.india.com/rss/sports-news.xml'),
    ('ABP News खेल', 'https://www.abplive.com/sports/feed'),
    ('Hindustan खेल', 'https://www.livehindustan.com/sports/rss'),
    ('Amar Ujala खेल', 'https://www.amarujala.com/sports/rss.xml'),
    
    # Business
    ('NDTV बिजनेस', 'https://www.ndtv.com/business/rss'),
    ('Zee Business', 'https://www.zeebiz.com/rss'),
    ('Aaj Tak बिजनेस', 'https://www.aajtak.in/business/rss'),
    ('ABP News बिजनेस', 'https://www.abplive.com/business/feed'),
    ('Hindustan बिजनेस', 'https://www.livehindustan.com/business/rss'),
    ('Amar Ujala बिजनेस', 'https://www.amarujala.com/business/rss.xml'),
    
    # Technology
    ('NDTech Hindi', 'https://www.navbharattimes.com/tech/rss'),
    ('Aaj Tak टेक', 'https://www.aajtak.in/technology/rss'),
    ('Zee News टेक', 'https://zeenews.india.com/rss/technology-news.xml'),
    ('Hindustan टेक', 'https://www.livehindustan.com/technology/rss'),
    
    # World News
    ('BBC हिन्दी अंतरराष्ट्रीय', 'https://feeds.bbci.co.uk/hindi/rss.xml'),
    ('DW हिन्दी विश्व', 'https://rss.dw.com/xml/rss-hi-all'),
    ('Aaj Tak विदेश', 'https://www.aajtak.in/world/rss'),
    ('Zee News विदेश', 'https://zeenews.india.com/rss/world-news.xml'),
    ('NDTV विदेश', 'https://www.ndtv.com/world/rss'),
    ('ABP News विदेश', 'https://www.abplive.com/world/feed'),
    
    # Science
    ('NDTV विज्ञान', 'https://www.ndtv.com/science/rss'),
    ('Zee News विज्ञान', 'https://zeenews.india.com/rss/science-and-environment.xml'),
    ('Aaj Tak विज्ञान', 'https://www.aajtak.in/science/rss'),
    
    # Health
    ('NDTV स्वास्थ्य', 'https://www.ndtv.com/health/rss'),
    ('Zee News स्वास्थ्य', 'https://zeenews.india.com/rss/health-news.xml'),
    ('Aaj Tak स्वास्थ्य', 'https://www.aajtak.in/health/rss'),
    
    # Entertainment
    ('NDTV मनोरंजन', 'https://www.ndtv.com/entertainment/rss'),
    ('Zee News मनोरंजन', 'https://zeenews.india.com/rss/entertainment-news.xml'),
    ('Aaj Tak मनोरंजन', 'https://www.aajtak.in/entertainment/rss'),
    ('ABP News मनोरंजन', 'https://www.abplive.com/entertainment/feed'),
    
    # Politics
    ('BBC हिन्दी भारत', 'https://feeds.bbci.co.uk/hindi/rss.xml'),
    ('NDTV राजनीति', 'https://www.ndtv.com/india/rss'),
    ('Aaj Tak राजनीति', 'https://www.aajtak.in/india/rss'),
    ('Zee News राजनीति', 'https://zeenews.india.com/rss/india-news.xml'),
    ('ABP News राजनीति', 'https://www.abplive.com/india/feed'),
    ('Hindustan राजनीति', 'https://www.livehindustan.com/uttar-pradesh/rss'),
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
    
    # Category-specific sources
    'NDTV खेल': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/ndtv/'),
    'Aaj Tak खेल': ('Center', '#666', 'https://mediabiasfactcheck.com/aaj-tak/'),
    'Zee News खेल': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/zee-news/'),
    'ABP News खेल': ('Center', '#666', 'https://mediabiasfactcheck.com/abp-news/'),
    'Hindustan खेल': ('Center', '#666', 'https://mediabiasfactcheck.com/hindustan/'),
    'Amar Ujala खेल': ('Center', '#666', 'https://mediabiasfactcheck.com/amar-ujala/'),
    'NDTV बिजनेस': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/ndtv/'),
    'Zee Business': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/zee-news/'),
    'Aaj Tak बिजनेस': ('Center', '#666', 'https://mediabiasfactcheck.com/aaj-tak/'),
    'ABP News बिजनेस': ('Center', '#666', 'https://mediabiasfactcheck.com/abp-news/'),
    'Hindustan बिजनेस': ('Center', '#666', 'https://mediabiasfactcheck.com/hindustan/'),
    'Amar Ujala बिजनेस': ('Center', '#666', 'https://mediabiasfactcheck.com/amar-ujala/'),
    'NDTech Hindi': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Aaj Tak टेक': ('Center', '#666', 'https://mediabiasfactcheck.com/aaj-tak/'),
    'Zee News टेक': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/zee-news/'),
    'Hindustan टेक': ('Center', '#666', 'https://mediabiasfactcheck.com/hindustan/'),
    'BBC हिन्दी अंतरराष्ट्रीय': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'DW हिन्दी विश्व': ('Center', '#666', 'https://mediabiasfactcheck.com/deutsche-welle/'),
    'Aaj Tak विदेश': ('Center', '#666', 'https://mediabiasfactcheck.com/aaj-tak/'),
    'Zee News विदेश': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/zee-news/'),
    'NDTV विदेश': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/ndtv/'),
    'ABP News विदेश': ('Center', '#666', 'https://mediabiasfactcheck.com/abp-news/'),
    'NDTV विज्ञान': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/ndtv/'),
    'Zee News विज्ञान': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/zee-news/'),
    'Aaj Tak विज्ञान': ('Center', '#666', 'https://mediabiasfactcheck.com/aaj-tak/'),
    'NDTV स्वास्थ्य': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/ndtv/'),
    'Zee News स्वास्थ्य': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/zee-news/'),
    'Aaj Tak स्वास्थ्य': ('Center', '#666', 'https://mediabiasfactcheck.com/aaj-tak/'),
    'NDTV मनोरंजन': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/ndtv/'),
    'Zee News मनोरंजन': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/zee-news/'),
    'Aaj Tak मनोरंजन': ('Center', '#666', 'https://mediabiasfactcheck.com/aaj-tak/'),
    'ABP News मनोरंजन': ('Center', '#666', 'https://mediabiasfactcheck.com/abp-news/'),
    'BBC हिन्दी भारत': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'NDTV राजनीति': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/ndtv/'),
    'Aaj Tak राजनीति': ('Center', '#666', 'https://mediabiasfactcheck.com/aaj-tak/'),
    'Zee News राजनीति': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/zee-news/'),
    'ABP News राजनीति': ('Center', '#666', 'https://mediabiasfactcheck.com/abp-news/'),
    'Hindustan राजनीति': ('Center', '#666', 'https://mediabiasfactcheck.com/hindustan/'),
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
    
    # Category-specific sources
    ('NDTV खेल', 'Left-Center'),
    ('Aaj Tak खेल', 'Center'),
    ('Zee News खेल', 'Right-Center'),
    ('ABP News खेल', 'Center'),
    ('Hindustan खेल', 'Center'),
    ('Amar Ujala खेल', 'Center'),
    ('NDTV बिजनेस', 'Left-Center'),
    ('Zee Business', 'Right-Center'),
    ('Aaj Tak बिजनेस', 'Center'),
    ('ABP News बिजनेस', 'Center'),
    ('Hindustan बिजनेस', 'Center'),
    ('Amar Ujala बिजनेस', 'Center'),
    ('NDTech Hindi', 'Center'),
    ('Aaj Tak टेक', 'Center'),
    ('Zee News टेक', 'Right-Center'),
    ('Hindustan टेक', 'Center'),
    ('BBC हिन्दी अंतरराष्ट्रीय', 'Left-Center'),
    ('DW हिन्दी विश्व', 'Center'),
    ('Aaj Tak विदेश', 'Center'),
    ('Zee News विदेश', 'Right-Center'),
    ('NDTV विदेश', 'Left-Center'),
    ('ABP News विदेश', 'Center'),
    ('NDTV विज्ञान', 'Left-Center'),
    ('Zee News विज्ञान', 'Right-Center'),
    ('Aaj Tak विज्ञान', 'Center'),
    ('NDTV स्वास्थ्य', 'Left-Center'),
    ('Zee News स्वास्थ्य', 'Right-Center'),
    ('Aaj Tak स्वास्थ्य', 'Center'),
    ('NDTV मनोरंजन', 'Left-Center'),
    ('Zee News मनोरंजन', 'Right-Center'),
    ('Aaj Tak मनोरंजन', 'Center'),
    ('ABP News मनोरंजन', 'Center'),
    ('BBC हिन्दी भारत', 'Left-Center'),
    ('NDTV राजनीति', 'Left-Center'),
    ('Aaj Tak राजनीति', 'Center'),
    ('Zee News राजनीति', 'Right-Center'),
    ('ABP News राजनीति', 'Center'),
    ('Hindustan राजनीति', 'Center'),
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
    'india': [
        'भारत', 'प्रधानमंत्री', 'संसद', 'राज्यसभा', 'लोकसभा', 'राष्ट्रपति', 'सरकार',
        'दिल्ली', 'मुंबई', 'बेंगलुरु', 'भाजपा', 'कांग्रेस', 'आप', 'सपा', 'बसपा',
        'दक्षिण एशिया', 'पाकिस्तान', 'बांग्लादेश', 'श्रीलंका', 'नेपाल', 'भूटान', 'मालदीव', 'अफगानिस्तान',
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
    ('india', 'भारत'),
    ('politics', 'राजनीति'),
    ('business', 'व्यापार'),
    ('technology', 'तकनीक'),
    ('science', 'विज्ञान'),
    ('health', 'स्वास्थ्य'),
    ('sports', 'खेल'),
    ('entertainment', 'मनोरंजन'),
])

CATEGORY_KEYWORDS_WEIGHTED = {
    'politics': {
        'high': ['प्रधानमंत्री', 'संसद', 'राज्यसभा', 'लोकसभा', 'भाजपा', 'कांग्रेस', 'आप'],
        'medium': ['सरकार', 'मुख्यमंत्री', 'मंत्री', 'चुनाव', 'वोट', 'अभियान', 'कानून', 'सुधार', 'पार्टी', 'सपा', 'बसपा', 'विपक्ष', 'गठबंधन', 'राजनीति', 'प्रधानमंत्री कार्यालय'],
        'low': []
    },
    'business': {
        'high': ['सेंसेक्स', 'रुपया', 'डॉलर', 'शेयर', 'लाभांश', 'महंगाई'],
        'medium': ['शेयर बाजार', 'अर्थव्यवस्था', 'बाजार', 'कंपनी', 'बैंक', 'वित्त', 'निवेश', 'बेरोजगारी', 'जीडीपी', 'विकास', 'ऋण', 'निर्यात', 'आयात', 'उद्योग', 'व्यापार', 'रोजगार', 'वेतन', 'कर'],
        'low': []
    },
    'technology': {
        'high': ['कृत्रिम बुद्धिमत्ता', 'साइबर हमला', 'साइबर सुरक्षा', 'एल्गोरिदम'],
        'medium': ['तकनीक', 'सॉफ्टवेयर', 'डिजिटल', 'रोबोट', 'ऐप', 'स्मार्टफोन', 'इंटरनेट', 'कंप्यूटर', 'डेटा', 'प्लेटफॉर्म', 'सोशल मीडिया', 'स्टार्टअप', 'गूगल', 'एप्पल', 'माइक्रोसॉफ्ट', 'अमेज़न', 'मेटा', 'टेस्ला'],
        'low': []
    },
    'science': {
        'high': ['नासा', 'आनुवंशिकी', 'विकास', 'जैव विविधता'],
        'medium': ['विज्ञान', 'अनुसंधान', 'खोज', 'प्रजाति', 'जलवायु', 'भूकंप', 'ज्वालामुखी', 'ग्रह', 'अंतरिक्ष', 'ब्रह्मांड', 'भौतिकी', 'रसायन', 'जीव विज्ञान', 'प्रयोगशाला', 'वैज्ञानिक', 'जीवाश्म', 'महासागर'],
        'low': []
    },
    'health': {
        'high': ['अस्पताल', 'डॉक्टर', 'चिकित्सा', 'वैक्सीन', 'महामारी', 'कोविड', 'कैंसर', 'मधुमेह'],
        'medium': ['स्वास्थ्य', 'बीमारी', 'उपचार', 'वायरस', 'क्लिनिक', 'मरीज', 'सर्जरी', 'चिकित्सा', 'लक्षण', 'निदान', 'फार्मास्यूटिकल', 'पोषण', 'व्यायाम', 'हृदय', 'मस्तिष्क'],
        'low': []
    },
    'sports': {
        'high': ['भारत', 'पाकिस्तान', 'ऑस्ट्रेलिया', 'आईपीएल', 'आईसीसी', 'विश्व कप'],
        'medium': ['क्रिकेट', 'फुटबॉल', 'हॉकी', 'ओलंपिक', 'खेल', 'टीम', 'खिलाड़ी', 'मैच', 'गोल', 'टेनिस', 'बास्केटबॉल', 'कोच', 'स्टेडियम', 'टूर्नामेंट', 'चैंपियनशिप', 'अंपायर'],
        'low': []
    },
    'india': {
        'high': ['भारत', 'प्रधानमंत्री', 'संसद', 'राज्यसभा', 'लोकसभा', 'राष्ट्रपति', 'सरकार', 'दिल्ली', 'मुंबई', 'बेंगलुरु'],
        'medium': ['भाजपा', 'कांग्रेस', 'आप', 'सपा', 'बसपा', 'दक्षिण एशिया', 'पाकिस्तान', 'बांग्लादेश', 'श्रीलंका', 'नेपाल', 'भूटान', 'मालदीव', 'अफगानिस्तान'],
        'low': []
    },
    'world': {
        'high': ['यूक्रेन', 'रूस', 'युद्ध', 'संकट', 'गाजा', 'इज़राइल', 'पुतिन'],
        'medium': ['चीन', 'ईरान', 'इज़राइल', 'गाजा', 'मध्य पूर्व', 'यूरोप', 'एशिया', 'अफ्रीका', 'लैटिन अमेरिका', 'कूटनीतिक', 'आप्रवासन', 'शरणार्थी', 'विश्व', 'अंतरराष्ट्रीय', 'संयुक्त राष्ट्र', 'नाटो', 'संघर्ष', 'सैन्य', 'सेना', 'शांति', 'समझौता', 'संधि', 'प्रतिबंध'],
        'low': []
    },
    'entertainment': {
        'high': ['ऑस्कर', 'नेटफ्लिक्स', 'डिज़्नी', 'हॉलीवुड', 'स्पॉटिफाई', 'बॉलीवुड'],
        'medium': ['फिल्म', 'सिनेमा', 'अभिनेता', 'अभिनेत्री', 'सेलिब्रिटी', 'संगीत', 'एल्बम', 'कॉन्सर्ट', 'टूर', 'स्ट्रीमिंग', 'बॉक्स ऑफिस', 'नाटक', 'सीरीज', 'सीजन', 'सीजन फिनाले', 'गायक', 'बैंड', 'पुरस्कार', 'रेड कार्पेट', 'कॉमेडी', 'ड्रामा', 'हॉरर', 'वीडियो गेम', 'गेमिंग', 'यूट्यूब', 'टिकटॉक', 'इन्फ्लुएंसर', 'वायरल', 'पॉडकास्ट', 'बेस्टसेलर', 'किताब', 'टेलीविजन', 'कार्यक्रम'],
        'low': []
    },
}

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
    # Header translations
    'logo_tagline': 'विभिन्न दृष्टिकोणों से समाचार',
    'search_placeholder': 'समाचार खोजें...',
    'toggle_theme': 'थीम बदलें',
    'filter_label': 'फिल्टर:',
    # Bias filter buttons
    'filter_all': 'सभी',
    'filter_left': 'वाम',
    'filter_left_center': 'मध्य-वाम',
    'filter_center': 'केंद्र',
    'filter_right_center': 'मध्य-दक्षिण',
    'filter_right': 'दक्षिण',
    # Story card buttons
    'find_coverage_btn': 'कवरेज खोजें',
    'different_angle_btn': 'दूसरा एंगल',
    'share_btn': 'साझा करें',
    'different_perspectives': 'अलग-अलग नजरिए',
    # Different Angle modal
    'different_angle_title': 'एक अलग दृष्टिकोण',
    'original_label': 'मूल:',
    'loading_related': 'संबंधित खबरें लोड हो रही हैं...',
    'no_related_stories': 'कोई संबंधित खबर नहीं मिली',
    'error_loading': 'लोडिंग में त्रुटि',
    # Share modal
    'share_story_title': 'खबर साझा करें',
    'share_on_x': 'X पर साझा करें',
    'share_facebook': 'Facebook पर साझा करें',
    'share_linkedin': 'LinkedIn पर साझा करें',
    'copy_link': 'लिंक कॉपी करें',
    'copied': 'कॉपी किया गया!',
    'close': 'बंद करें',
}

PAYWALLED_SOURCES = set()
