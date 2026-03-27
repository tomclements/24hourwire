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
    'us': [
        'amerika birleşik devletleri', 'abd', 'florida', 'texas', 'kaliforniya',
        'new york', 'miami', 'los angeles', 'chicago', 'washington', 'trump', 'biden',
        'beyaz saray', 'kongre', 'senato', 'fbi', 'cia', 'pentagon',
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
    ('us', 'ABD'),
    ('politics', 'Siyaset'),
    ('business', 'Ekonomi'),
    ('technology', 'Teknoloji'),
    ('science', 'Bilim'),
    ('health', 'Sağlık'),
    ('sports', 'Spor'),
    ('entertainment', 'Eğlence'),
])

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
