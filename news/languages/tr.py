from collections import OrderedDict

CODE = 'tr'
NAME = 'Türkçe'

FEEDS = [
    ('Anadolu Ajansı', 'https://www.aa.com.tr/tr/rss/default?cat=gundem'),
    ('NTV', 'https://www.ntv.com.tr/gundem.rss'),
    ('Habertürk', 'https://www.haberturk.com/rss'),
    ('Hürriyet', 'https://www.hurriyet.com.tr/rss/gundem'),
    ('Sözcü', 'https://www.sozcu.com.tr/rss/tum-haberler.xml'),
    ('Cumhuriyet', 'https://www.cumhuriyet.com.tr/rss/tum-haberler.xml'),
    ('Milliyet', 'https://www.milliyet.com.tr/rss/rssnew/gundem.xml'),
    ('Sabah', 'https://www.sabah.com.tr/rss/gundem.xml'),
    ('DW Türkçe', 'https://rss.dw.com/xml/rss-tr-all'),
    ('BBC Türkçe', 'https://feeds.bbci.co.uk/turkce/rss.xml'),
    ('T24', 'https://t24.com.tr/rss'),
    ('BirGün', 'https://www.birgun.net/rss'),
    
    # Category-specific feeds
    # Sports
    ('NTV Spor', 'https://www.ntvspor.net/rss'),
    ('Habertürk Spor', 'https://www.haberturk.com/rss/spor'),
    ('Hürriyet Spor', 'https://www.hurriyet.com.tr/rss/spor'),
    ('Milliyet Spor', 'https://www.milliyet.com.tr/rss/rssnew/spor.xml'),
    ('Sabah Spor', 'https://www.sabah.com.tr/rss/spor.xml'),
    ('Sözcü Spor', 'https://www.sozcu.com.tr/rss/spor.xml'),
    ('Fotomaç', 'https://www.fotomac.com.tr/rss'),
    ('Fanatik', 'https://www.fanatik.com.tr/rss'),
    ('TRT Spor', 'https://www.trtspor.com.tr/rss'),
    
    # Business
    ('Hürriyet Ekonomi', 'https://www.hurriyet.com.tr/rss/ekonomi'),
    ('Sabah Ekonomi', 'https://www.sabah.com.tr/rss/ekonomi.xml'),
    ('Milliyet Ekonomi', 'https://www.milliyet.com.tr/rss/rssnew/ekonomi.xml'),
    ('NTV Ekonomi', 'https://www.ntv.com.tr/ekonomi.rss'),
    ('Habertürk Ekonomi', 'https://www.haberturk.com/rss/ekonomi'),
    ('Bloomberg HT', 'https://www.bloomberght.com/rss'),
    
    # Technology
    ('Hürriyet Teknoloji', 'https://www.hurriyet.com.tr/rss/teknoloji'),
    ('NTV Teknoloji', 'https://www.ntv.com.tr/teknoloji.rss'),
    ('Webrazzi', 'https://webrazzi.com/feed/'),
    ('ShiftDelete', 'https://shiftdelete.net/feed'),
    ('Chip Online', 'https://www.chip.com.tr/rss.xml'),
    
    # World News
    ('BBC Türkçe Dünya', 'https://feeds.bbci.co.uk/turkce/rss.xml'),
    ('DW Türkçe Dünya', 'https://rss.dw.com/xml/rss-tr-all'),
    ('Hürriyet Dünya', 'https://www.hurriyet.com.tr/rss/dunya'),
    ('NTV Dünya', 'https://www.ntv.com.tr/dunya.rss'),
    ('Sabah Dünya', 'https://www.sabah.com.tr/rss/dunya.xml'),
    ('Milliyet Dünya', 'https://www.milliyet.com.tr/rss/rssnew/dunya.xml'),
    
    # Science
    ('NTV Bilim', 'https://www.ntv.com.tr/bilim-teknoloji.rss'),
    ('Hürriyet Bilim', 'https://www.hurriyet.com.tr/rss/bilim'),
    ('Popular Science TR', 'https://www.popsci.com.tr/rss/'),
    
    # Health
    ('Hürriyet Sağlık', 'https://www.hurriyet.com.tr/rss/saglik'),
    ('NTV Sağlık', 'https://www.ntv.com.tr/saglik.rss'),
    ('Milliyet Sağlık', 'https://www.milliyet.com.tr/rss/rssnew/saglik.xml'),
    ('Sabah Sağlık', 'https://www.sabah.com.tr/rss/saglik.xml'),
    
    # Entertainment
    ('Hürriyet Kelebek', 'https://www.hurriyet.com.tr/rss/kelebek'),
    ('NTV Magazin', 'https://www.ntv.com.tr/magazin.rss'),
    ('Milliyet Magazin', 'https://www.milliyet.com.tr/rss/rssnew/magazin.xml'),
    ('Sabah Magazin', 'https://www.sabah.com.tr/rss/magazin.xml'),
    
    # Politics
    ('BBC Türkçe Türkiye', 'https://feeds.bbci.co.uk/turkce/rss.xml'),
    ('DW Türkçe Türkiye', 'https://rss.dw.com/xml/rss-tr-all'),
    ('Hürriyet Gündem', 'https://www.hurriyet.com.tr/rss/gundem'),
    ('NTV Gündem', 'https://www.ntv.com.tr/gundem.rss'),
    ('Cumhuriyet Gündem', 'https://www.cumhuriyet.com.tr/rss/gundem.xml'),
    ('T24 Gündem', 'https://t24.com.tr/rss'),
    ('BirGün Gündem', 'https://www.birgun.net/rss'),
]

SOURCE_INFO = {
    'Anadolu Ajansı': ('Center', '#666', 'https://mediabiasfactcheck.com/anadolu-agency/'),
    'NTV': ('Center', '#666', 'https://mediabiasfactcheck.com/ntv/'),
    'Habertürk': ('Center', '#666', 'https://mediabiasfactcheck.com/haberturk/'),
    'Hürriyet': ('Center', '#666', 'https://mediabiasfactcheck.com/hurriyet/'),
    'Sözcü': ('Left', '#999', 'https://mediabiasfactcheck.com/sozcu/'),
    'Cumhuriyet': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/cumhuriyet/'),
    'Milliyet': ('Center', '#666', 'https://mediabiasfactcheck.com/milliyet/'),
    'Sabah': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/sabah/'),
    'DW Türkçe': ('Center', '#666', 'https://mediabiasfactcheck.com/deutsche-welle/'),
    'BBC Türkçe': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'T24': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/'),
    'BirGün': ('Left', '#999', 'https://mediabiasfactcheck.com/'),
    
    # Category-specific sources
    'NTV Spor': ('Center', '#666', 'https://mediabiasfactcheck.com/ntv/'),
    'Habertürk Spor': ('Center', '#666', 'https://mediabiasfactcheck.com/haberturk/'),
    'Hürriyet Spor': ('Center', '#666', 'https://mediabiasfactcheck.com/hurriyet/'),
    'Milliyet Spor': ('Center', '#666', 'https://mediabiasfactcheck.com/milliyet/'),
    'Sabah Spor': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/sabah/'),
    'Sözcü Spor': ('Left', '#999', 'https://mediabiasfactcheck.com/sozcu/'),
    'Fotomaç': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Fanatik': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'TRT Spor': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Hürriyet Ekonomi': ('Center', '#666', 'https://mediabiasfactcheck.com/hurriyet/'),
    'Sabah Ekonomi': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/sabah/'),
    'Milliyet Ekonomi': ('Center', '#666', 'https://mediabiasfactcheck.com/milliyet/'),
    'NTV Ekonomi': ('Center', '#666', 'https://mediabiasfactcheck.com/ntv/'),
    'Habertürk Ekonomi': ('Center', '#666', 'https://mediabiasfactcheck.com/haberturk/'),
    'Bloomberg HT': ('Center', '#666', 'https://mediabiasfactcheck.com/bloomberg/'),
    'Hürriyet Teknoloji': ('Center', '#666', 'https://mediabiasfactcheck.com/hurriyet/'),
    'NTV Teknoloji': ('Center', '#666', 'https://mediabiasfactcheck.com/ntv/'),
    'Webrazzi': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'ShiftDelete': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Chip Online': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'BBC Türkçe Dünya': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'DW Türkçe Dünya': ('Center', '#666', 'https://mediabiasfactcheck.com/deutsche-welle/'),
    'Hürriyet Dünya': ('Center', '#666', 'https://mediabiasfactcheck.com/hurriyet/'),
    'NTV Dünya': ('Center', '#666', 'https://mediabiasfactcheck.com/ntv/'),
    'Sabah Dünya': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/sabah/'),
    'Milliyet Dünya': ('Center', '#666', 'https://mediabiasfactcheck.com/milliyet/'),
    'NTV Bilim': ('Center', '#666', 'https://mediabiasfactcheck.com/ntv/'),
    'Hürriyet Bilim': ('Center', '#666', 'https://mediabiasfactcheck.com/hurriyet/'),
    'Popular Science TR': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Hürriyet Sağlık': ('Center', '#666', 'https://mediabiasfactcheck.com/hurriyet/'),
    'NTV Sağlık': ('Center', '#666', 'https://mediabiasfactcheck.com/ntv/'),
    'Milliyet Sağlık': ('Center', '#666', 'https://mediabiasfactcheck.com/milliyet/'),
    'Sabah Sağlık': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/sabah/'),
    'Hürriyet Kelebek': ('Center', '#666', 'https://mediabiasfactcheck.com/hurriyet/'),
    'NTV Magazin': ('Center', '#666', 'https://mediabiasfactcheck.com/ntv/'),
    'Milliyet Magazin': ('Center', '#666', 'https://mediabiasfactcheck.com/milliyet/'),
    'Sabah Magazin': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/sabah/'),
    'BBC Türkçe Türkiye': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'DW Türkçe Türkiye': ('Center', '#666', 'https://mediabiasfactcheck.com/deutsche-welle/'),
    'Hürriyet Gündem': ('Center', '#666', 'https://mediabiasfactcheck.com/hurriyet/'),
    'NTV Gündem': ('Center', '#666', 'https://mediabiasfactcheck.com/ntv/'),
    'Cumhuriyet Gündem': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/cumhuriyet/'),
    'T24 Gündem': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/'),
    'BirGün Gündem': ('Left', '#999', 'https://mediabiasfactcheck.com/'),
}

DEFAULT_SOURCES = ['Anadolu Ajansı', 'NTV', 'Habertürk', 'BBC Türkçe', 'DW Türkçe', 'Cumhuriyet']

SOURCES = [
    ('Anadolu Ajansı', 'Center'),
    ('NTV', 'Center'),
    ('Habertürk', 'Center'),
    ('Hürriyet', 'Center'),
    ('Milliyet', 'Center'),
    ('DW Türkçe', 'Center'),
    ('BBC Türkçe', 'Left-Center'),
    ('Cumhuriyet', 'Left-Center'),
    ('T24', 'Left-Center'),
    ('Sabah', 'Right-Center'),
    ('Sözcü', 'Left'),
    ('BirGün', 'Left'),
    
    # Category-specific sources
    ('NTV Spor', 'Center'),
    ('Habertürk Spor', 'Center'),
    ('Hürriyet Spor', 'Center'),
    ('Milliyet Spor', 'Center'),
    ('Sabah Spor', 'Right-Center'),
    ('Sözcü Spor', 'Left'),
    ('Fotomaç', 'Center'),
    ('Fanatik', 'Center'),
    ('TRT Spor', 'Center'),
    ('Hürriyet Ekonomi', 'Center'),
    ('Sabah Ekonomi', 'Right-Center'),
    ('Milliyet Ekonomi', 'Center'),
    ('NTV Ekonomi', 'Center'),
    ('Habertürk Ekonomi', 'Center'),
    ('Bloomberg HT', 'Center'),
    ('Hürriyet Teknoloji', 'Center'),
    ('NTV Teknoloji', 'Center'),
    ('Webrazzi', 'Center'),
    ('ShiftDelete', 'Center'),
    ('Chip Online', 'Center'),
    ('BBC Türkçe Dünya', 'Left-Center'),
    ('DW Türkçe Dünya', 'Center'),
    ('Hürriyet Dünya', 'Center'),
    ('NTV Dünya', 'Center'),
    ('Sabah Dünya', 'Right-Center'),
    ('Milliyet Dünya', 'Center'),
    ('NTV Bilim', 'Center'),
    ('Hürriyet Bilim', 'Center'),
    ('Popular Science TR', 'Center'),
    ('Hürriyet Sağlık', 'Center'),
    ('NTV Sağlık', 'Center'),
    ('Milliyet Sağlık', 'Center'),
    ('Sabah Sağlık', 'Right-Center'),
    ('Hürriyet Kelebek', 'Center'),
    ('NTV Magazin', 'Center'),
    ('Milliyet Magazin', 'Center'),
    ('Sabah Magazin', 'Right-Center'),
    ('BBC Türkçe Türkiye', 'Left-Center'),
    ('DW Türkçe Türkiye', 'Center'),
    ('Hürriyet Gündem', 'Center'),
    ('NTV Gündem', 'Center'),
    ('Cumhuriyet Gündem', 'Left-Center'),
    ('T24 Gündem', 'Left-Center'),
    ('BirGün Gündem', 'Left'),
]

CATEGORY_KEYWORDS = {
    'politics': [
        'hükümet', 'cumhurbaşkanı', 'bakan', 'seçim', 'oy', 'kampanya',
        'meclis', 'senato', 'parlamento', 'yasası', 'reform', 'parti',
        'akp', 'chp', 'mhp', 'i̇yi parti', 'cumhurbaşkanlığı',
        'muhalefet', 'koalisyon', 'siyaset', 'erdogan',
    ],
    'business': [
        'borsa', 'ekonomi', 'piyasa', 'şirket', 'banka', 'finans',
        'yatırım', 'lira', 'dolar', 'euro', 'enflasyon', 'işsizlik', 'gsyh', 'büyüme',
        'hisse', 'temettü', 'kredi', 'borç', 'ihracat', 'ithalat',
        'sanayi', 'ticaret', 'istihdam', 'maaş', 'vergi',
    ],
    'technology': [
        'teknoloji', 'yapay zeka', 'yazılım', 'siber saldırı', 'dijital',
        'robot', 'uygulama', 'akıllı telefon', 'internet', 'bilgisayar', 'veri',
        'siber güvenlik', 'algoritma', 'platform', 'sosyal medya', 'girişim',
        'google', 'apple', 'microsoft', 'amazon', 'meta', 'tesla',
    ],
    'science': [
        'bilim', 'araştırma', 'keşif', 'tür', 'genetik', 'iklim',
        'deprem', 'volkan', 'gezegen', 'uzay', 'evren', 'fizik',
        'kimya', 'biyoloji', 'laboratuvar', 'bilim insanı', 'nasa',
        'fosil', 'evrim', 'biyoçeşitlilik', 'okyanus',
    ],
    'health': [
        'hastane', 'doktor', 'tıp', 'aşı', 'pandemi', 'sağlık', 'hastalık',
        'tedavi', 'virüs', 'klinik', 'hasta', 'cerrahi', 'terapi', 'belirti',
        'teşhis', 'eczacılık', 'beslenme', 'egzersiz', 'covid',
        'kanser', 'diyabet', 'kalp', 'beyin',
    ],
    'sports': [
        'futbol', 'lig', 'şampiyonlar', 'kupa', 'dünya kupası', 'olimpiyat', 'spor',
        'takım', 'oyuncu', 'maç', 'gol', 'tenis', 'basketbol', 'voleybol',
        'teknik direktör', 'stadyum', 'turnuva', 'şampiyona', 'hakem',
        'galatasaray', 'fenerbahçe', 'beşiktaş', 'trabzonspor', 'süper lig',
    ],
    'turkey': [
        'türkiye', 'türk', 'cumhurbaşkanı', 'erdoğan', 'meclis', 'hükümet', 'türkiye büyük millet meclisi',
        'ankara', 'istanbul', 'izmir', 'akp', 'chp', 'mhp', 'iyi parti', 'hdp', 'saadet',
        'balkanlar', 'yunanistan', 'bulgaristan', 'romanya', 'sırbistan', 'arnavutluk', 'bosna', 'kosova', 'kuzey makedonya',
    ],
    'world': [
        'ukrayna', 'rusya', 'çin', 'iran', 'israil', 'gazze', 'orta doğu', 'avrupa',
        'asya', 'afrika', 'latin amerika', 'savaş', 'diplomat', 'göç',
        'mülteci', 'dünya', 'uluslararası', 'bm', 'nato', 'çatışma', 'kriz',
        'askeri', 'ordu', 'barış', 'anlaşma', 'antlaşma', 'yaptırım',
    ],
    'entertainment': [
        'film', 'sinema', 'oyuncu', 'akademi ödülü', 'ünlü',
        'müzik', 'albüm', 'konser', 'turne', 'netflix', 'yayın', 'gişe',
        'tiyatro', 'dizi', 'sezon', 'sezon finali',
        'şarkıcı', 'grup', 'spotify',
        'disney', 'hollywood', 'ödül', 'kırmızı halı',
        'komedi', 'korku',
        'oyun', 'espor', 'youtube', 'tiktok',
        'influencer', 'viral', 'podcast', 'çok satan', 'kitap',
        'televizyon', 'program',
    ],
}

STOP_WORDS = {
    'bir', 've', 'ile', 'için', 'de', 'da', 'den', 'dan',
    'bu', 'şu', 'o', 'ki', 'ne', 'hem', 'ya', 'veya', 'ama', 'fakat',
    'ben', 'sen', 'o', 'biz', 'siz', 'onlar',
    'benim', 'senin', 'onun', 'bizim', 'sizin', 'onların',
    'var', 'yok', 'olan', 'oldu', 'olacak', 'olmak',
    'yeni', 'söyledi', 'açıkladı', 'göre',
    'çok', 'daha', 'en', 'az', 'bile', 'ancak',
    'sonra', 'önce', 'arasında', 'üzerinde', 'altında',
}

SOURCE_ATTRIBUTION = r'\s*(Anadolu Ajansı|NTV|Habertürk|Hürriyet|Sözcü|Cumhuriyet|Milliyet|Sabah|DW Türkçe|BBC Türkçe|T24|BirGün)\s*$'

GENERIC_TEXT = [
    'kapsamlı haber kapsamı',
    'kaynak',
    'daha fazla bilgi için tıklayın',
]

CATEGORY_NAMES = OrderedDict([
    ('all', 'Tümü'),
    ('most_covered', 'En Çok Haber Olan'),
    ('world', 'Dünya'),
    ('turkey', 'Türkiye'),
    ('politics', 'Siyaset'),
    ('business', 'Ekonomi'),
    ('technology', 'Teknoloji'),
    ('science', 'Bilim'),
    ('health', 'Sağlık'),
    ('sports', 'Spor'),
    ('entertainment', 'Eğlence'),
])

CATEGORY_KEYWORDS_WEIGHTED = {
    'politics': {
        'high': ['cumhurbaşkanı', 'erdoğan', 'meclis', 'hükümet', 'akp', 'chp', 'mhp'],
        'medium': ['bakan', 'seçim', 'oy', 'kampanya', 'yasası', 'reform', 'parti', 'iyi parti', 'hdp', 'saadet', 'muhalefet', 'koalisyon', 'siyaset'],
        'low': []
    },
    'business': {
        'high': ['borsa', 'lira', 'dolar', 'euro', 'hisse', 'temettü', 'enflasyon'],
        'medium': ['ekonomi', 'piyasa', 'şirket', 'banka', 'finans', 'yatırım', 'işsizlik', 'gsyh', 'büyüme', 'kredi', 'borç', 'ihracat', 'ithalat', 'sanayi', 'ticaret', 'istihdam', 'maaş', 'vergi'],
        'low': []
    },
    'technology': {
        'high': ['yapay zeka', 'siber saldırı', 'siber güvenlik', 'algoritma'],
        'medium': ['teknoloji', 'yazılım', 'dijital', 'robot', 'uygulama', 'akıllı telefon', 'internet', 'bilgisayar', 'veri', 'platform', 'sosyal medya', 'girişim', 'google', 'apple', 'microsoft', 'amazon', 'meta', 'tesla'],
        'low': []
    },
    'science': {
        'high': ['nasa', 'genetik', 'evrim', 'biyoçeşitlilik'],
        'medium': ['bilim', 'araştırma', 'keşif', 'tür', 'iklim', 'deprem', 'volkan', 'gezegen', 'uzay', 'evren', 'fizik', 'kimya', 'biyoloji', 'laboratuvar', 'bilim insanı', 'fosil', 'okyanus'],
        'low': []
    },
    'health': {
        'high': ['hastane', 'doktor', 'tıp', 'aşı', 'pandemi', 'covid', 'kanser', 'diyabet'],
        'medium': ['sağlık', 'hastalık', 'tedavi', 'virüs', 'klinik', 'hasta', 'cerrahi', 'terapi', 'belirti', 'teşhis', 'eczacılık', 'beslenme', 'egzersiz', 'kalp', 'beyin'],
        'low': []
    },
    'sports': {
        'high': ['galatasaray', 'fenerbahçe', 'beşiktaş', 'trabzonspor', 'süper lig'],
        'medium': ['futbol', 'lig', 'şampiyonlar', 'kupa', 'dünya kupası', 'olimpiyat', 'spor', 'takım', 'oyuncu', 'maç', 'gol', 'tenis', 'basketbol', 'voleybol', 'teknik direktör', 'stadyum', 'turnuva', 'şampiyona', 'hakem'],
        'low': []
    },
    'turkey': {
        'high': ['türkiye', 'türk', 'cumhurbaşkanı', 'erdoğan', 'meclis', 'hükümet', 'türkiye büyük millet meclisi', 'ankara', 'istanbul', 'izmir'],
        'medium': ['akp', 'chp', 'mhp', 'iyi parti', 'hdp', 'saadet', 'balkanlar', 'yunanistan', 'bulgaristan', 'romanya', 'sırbistan', 'arnavutluk', 'bosna', 'kosova', 'kuzey makedonya'],
        'low': []
    },
    'world': {
        'high': ['ukrayna', 'rusya', 'savaş', 'kriz', 'gazze', 'israil', 'putin'],
        'medium': ['çin', 'iran', 'israil', 'gazze', 'orta doğu', 'avrupa', 'asya', 'afrika', 'latin amerika', 'diplomat', 'göç', 'mülteci', 'dünya', 'uluslararası', 'bm', 'nato', 'çatışma', 'askeri', 'ordu', 'barış', 'anlaşma', 'antlaşma', 'yaptırım'],
        'low': []
    },
    'entertainment': {
        'high': ['akademi ödülü', 'netflix', 'disney', 'hollywood', 'spotify'],
        'medium': ['film', 'sinema', 'oyuncu', 'ünlü', 'müzik', 'albüm', 'konser', 'turne', 'yayın', 'gişe', 'tiyatro', 'dizi', 'sezon', 'sezon finali', 'şarkıcı', 'grup', 'ödül', 'kırmızı halı', 'komedi', 'korku', 'oyun', 'espor', 'youtube', 'tiktok', 'influencer', 'viral', 'podcast', 'çok satan', 'kitap', 'televizyon', 'program'],
        'low': []
    },
}

UI_STRINGS = {
    'subtitle': 'Yöneliminizi seçin | Haber ajansları ve diğer kaynaklar | Son 24 saat',
    'how_it_works': 'Nasıl çalışır',
    'privacy_text': 'Gizliliğinize saygı duyuyoruz. Bu site bağlamsal reklamlar kullanır (izleme çerezi yok) ve başlıkları/özetleri adil kullanım kapsamında gösterir.',
    'privacy_link': 'Gizlilik Politikası',
    'got_it': 'Anladım',
    'sources': 'Kaynaklar:',
    'center_default': 'Merkez kaynaklar (varsayılan)',
    'all_sources': 'Tüm kaynaklar',
    'center_only': 'Sadece merkez',
    'left_center_only': 'Sadece sol-merkez',
    'left_only': 'Sadece sol',
    'right_only': 'Sadece sağ',
    'clear_all': 'Tümünü temizle',
    'sources_suffix': 'kaynak',
    'covered_by_2': '2 veya daha fazla kaynak tarafından haber yapılan içerikler',
    'paywall_title': 'Ücretli site',
    'sources_label': 'kaynak',
    'read_full': 'Tam haberi oku',
    'find_coverage': 'Haber bul',
    'search_related': 'İlgili haberleri ara',
    'bias_rating': 'Yönelim değerlendirmesi',
    'ago': 'önce',
    'show_stories': 'Göster',
    'stories': 'haber',
    'no_stories': 'Bu kategoride haber yok',
    'footer_copy': 'Haber içeriği © ilgili yayıncılar. Başlıklar ve özetler bilgilendirme amacıyla adil kullanım kapsamında kullanılmıştır.',
    'footer_sources': 'Kaynaklar:',
    'footer_and': 've',
    'footer_terms': 'Koşullar',
    'footer_privacy': 'Gizlilik',
    'footer_about': 'Hakkında',
}

PAYWALLED_SOURCES = {
    'Hürriyet',
    'Sabah',
}
