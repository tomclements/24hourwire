from collections import OrderedDict

CODE = 'ar'
NAME = 'العربية'

FEEDS = [
    ('Al Jazeera', 'https://www.aljazeera.com/xml/rss/all.xml'),
    ('BBC Arabic', 'https://feeds.bbci.co.uk/arabic/rss.xml'),
    ('France 24 Arabic', 'https://www.france24.com/ar/rss'),
    ('DW Arabic', 'https://rss.dw.com/xml/rss-ar-all'),
    ('Sky News Arabia', 'https://www.skynewsarabia.com/rss'),
    ('RT Arabic', 'https://arabic.rt.com/rss/'),
    ('Al Arabiya', 'https://www.alarabiya.net/tools/rss/ar.xml'),
    ('Asharq Al-Awsat', 'https://aawsat.com/feed'),
    ('Al-Masry Al-Youm', 'https://news.google.com/rss/search?q=site:almasryalyoum.com&hl=ar&gl=EG&ceid=EG:ar'),
    ('Youm7', 'https://news.google.com/rss/search?q=site:youm7.com&hl=ar&gl=EG&ceid=EG:ar'),
    
    # Category-specific feeds
    # Sports
    ('BBC Arabic Sport', 'https://feeds.bbci.co.uk/arabic/sport/rss.xml'),
    ('Al Jazeera Sport', 'https://www.aljazeera.com/xml/rss/all.xml'),
    ('Sky News Arabia Sport', 'https://www.skynewsarabia.com/sport/rss'),
    ('RT Arabic Sport', 'https://arabic.rt.com/sport/rss/'),
    ('Al Arabiya Sport', 'https://www.alarabiya.net/sport/rss.xml'),
    ('Bein Sports', 'https://www.beinsports.com/ar/rss'),
    ('Goal Arabic', 'https://www.goal.com/ar/rss.xml'),
    ('Kooora', 'https://www.kooora.com/rss/'),
    
    # Business
    ('BBC Arabic Business', 'https://feeds.bbci.co.uk/arabic/business/rss.xml'),
    ('Al Jazeera Business', 'https://www.aljazeera.com/xml/rss/all.xml'),
    ('Sky News Arabia Business', 'https://www.skynewsarabia.com/business/rss'),
    ('RT Arabic Business', 'https://arabic.rt.com/business/rss/'),
    ('Al Arabiya Business', 'https://www.alarabiya.net/business/rss.xml'),
    ('Al-Masry Al-Youm Economy', 'https://www.almasryalyoum.com/rss/economy'),
    ('Youm7 Economy', 'https://www.youm7.com/rss/Economy'),
    ('CNBC Arabia', 'https://www.cnbcarabia.com/rss/'),
    
    # Technology
    ('BBC Arabic Technology', 'https://feeds.bbci.co.uk/arabic/science/rss.xml'),
    ('Al Jazeera Technology', 'https://www.aljazeera.com/xml/rss/all.xml'),
    ('Sky News Arabia Technology', 'https://www.skynewsarabia.com/technology/rss'),
    ('RT Arabic Technology', 'https://arabic.rt.com/technology/rss/'),
    ('Al Arabiya Technology', 'https://www.alarabiya.net/technology/rss.xml'),
    
    # World News
    ('BBC Arabic World', 'https://feeds.bbci.co.uk/arabic/world/rss.xml'),
    ('Al Jazeera World', 'https://www.aljazeera.com/xml/rss/all.xml'),
    ('France 24 Arabic World', 'https://www.france24.com/ar/rss'),
    ('DW Arabic World', 'https://rss.dw.com/xml/rss-ar-all'),
    ('Sky News Arabia World', 'https://www.skynewsarabia.com/rss'),
    ('RT Arabic World', 'https://arabic.rt.com/world/rss/'),
    ('Al Arabiya World', 'https://www.alarabiya.net/rss.xml'),
    ('Asharq Al-Awsat World', 'https://aawsat.com/feed'),
    
    # Science
    ('BBC Arabic Science', 'https://feeds.bbci.co.uk/arabic/science/rss.xml'),
    ('Al Jazeera Science', 'https://www.aljazeera.com/xml/rss/all.xml'),
    ('Sky News Arabia Science', 'https://www.skynewsarabia.com/science/rss'),
    ('RT Arabic Science', 'https://arabic.rt.com/science/rss/'),
    
    # Health
    ('BBC Arabic Health', 'https://feeds.bbci.co.uk/arabic/health/rss.xml'),
    ('Al Jazeera Health', 'https://www.aljazeera.com/xml/rss/all.xml'),
    ('Sky News Arabia Health', 'https://www.skynewsarabia.com/health/rss'),
    ('RT Arabic Health', 'https://arabic.rt.com/health/rss/'),
    ('Al Arabiya Health', 'https://www.alarabiya.net/health/rss.xml'),
    
    # Entertainment
    ('BBC Arabic Arts', 'https://feeds.bbci.co.uk/arabic/artandculture/rss.xml'),
    ('Al Jazeera Culture', 'https://www.aljazeera.com/xml/rss/all.xml'),
    ('Sky News Arabia Entertainment', 'https://www.skynewsarabia.com/entertainment/rss'),
    ('RT Arabic Culture', 'https://arabic.rt.com/culture/rss/'),
    ('Al Arabiya Entertainment', 'https://www.alarabiya.net/entertainment/rss.xml'),
    
    # Politics
    ('BBC Arabic Politics', 'https://feeds.bbci.co.uk/arabic/middleeast/rss.xml'),
    ('Al Jazeera Politics', 'https://www.aljazeera.com/xml/rss/all.xml'),
    ('France 24 Arabic Politics', 'https://www.france24.com/ar/rss'),
    ('DW Arabic Politics', 'https://rss.dw.com/xml/rss-ar-all'),
    ('Sky News Arabia Politics', 'https://www.skynewsarabia.com/politics/rss'),
    ('RT Arabic Politics', 'https://arabic.rt.com/politics/rss/'),
    ('Al Arabiya Politics', 'https://www.alarabiya.net/politics/rss.xml'),
]

SOURCE_INFO = {
    'Al Jazeera': ('Left', '#999', 'https://mediabiasfactcheck.com/al-jazeera/'),
    'BBC Arabic': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'France 24 Arabic': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/france-24/'),
    'DW Arabic': ('Center', '#666', 'https://mediabiasfactcheck.com/deutsche-welle/'),
    'Sky News Arabia': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RT Arabic': ('Right', '#666', 'https://mediabiasfactcheck.com/rt/'),
    'Al Arabiya': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/al-arabiya/'),
    'Asharq Al-Awsat': ('Center', '#666', 'https://mediabiasfactcheck.com/asharq-al-awsat/'),
    'Al-Masry Al-Youm': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Youm7': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    
    # Category-specific sources
    'BBC Arabic Sport': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'Al Jazeera Sport': ('Left', '#999', 'https://mediabiasfactcheck.com/al-jazeera/'),
    'Sky News Arabia Sport': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RT Arabic Sport': ('Right', '#666', 'https://mediabiasfactcheck.com/rt/'),
    'Al Arabiya Sport': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/al-arabiya/'),
    'Bein Sports': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Goal Arabic': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Kooora': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'BBC Arabic Business': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'Al Jazeera Business': ('Left', '#999', 'https://mediabiasfactcheck.com/al-jazeera/'),
    'Sky News Arabia Business': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RT Arabic Business': ('Right', '#666', 'https://mediabiasfactcheck.com/rt/'),
    'Al Arabiya Business': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/al-arabiya/'),
    'Al-Masry Al-Youm Economy': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Youm7 Economy': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'CNBC Arabia': ('Center', '#666', 'https://mediabiasfactcheck.com/cnbc/'),
    'BBC Arabic Technology': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'Al Jazeera Technology': ('Left', '#999', 'https://mediabiasfactcheck.com/al-jazeera/'),
    'Sky News Arabia Technology': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RT Arabic Technology': ('Right', '#666', 'https://mediabiasfactcheck.com/rt/'),
    'Al Arabiya Technology': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/al-arabiya/'),
    'BBC Arabic World': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'Al Jazeera World': ('Left', '#999', 'https://mediabiasfactcheck.com/al-jazeera/'),
    'France 24 Arabic World': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/france-24/'),
    'DW Arabic World': ('Center', '#666', 'https://mediabiasfactcheck.com/deutsche-welle/'),
    'Sky News Arabia World': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RT Arabic World': ('Right', '#666', 'https://mediabiasfactcheck.com/rt/'),
    'Al Arabiya World': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/al-arabiya/'),
    'Asharq Al-Awsat World': ('Center', '#666', 'https://mediabiasfactcheck.com/asharq-al-awsat/'),
    'BBC Arabic Science': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'Al Jazeera Science': ('Left', '#999', 'https://mediabiasfactcheck.com/al-jazeera/'),
    'Sky News Arabia Science': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RT Arabic Science': ('Right', '#666', 'https://mediabiasfactcheck.com/rt/'),
    'BBC Arabic Health': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'Al Jazeera Health': ('Left', '#999', 'https://mediabiasfactcheck.com/al-jazeera/'),
    'Sky News Arabia Health': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RT Arabic Health': ('Right', '#666', 'https://mediabiasfactcheck.com/rt/'),
    'Al Arabiya Health': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/al-arabiya/'),
    'BBC Arabic Arts': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'Al Jazeera Culture': ('Left', '#999', 'https://mediabiasfactcheck.com/al-jazeera/'),
    'Sky News Arabia Entertainment': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RT Arabic Culture': ('Right', '#666', 'https://mediabiasfactcheck.com/rt/'),
    'Al Arabiya Entertainment': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/al-arabiya/'),
    'BBC Arabic Politics': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'Al Jazeera Politics': ('Left', '#999', 'https://mediabiasfactcheck.com/al-jazeera/'),
    'France 24 Arabic Politics': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/france-24/'),
    'DW Arabic Politics': ('Center', '#666', 'https://mediabiasfactcheck.com/deutsche-welle/'),
    'Sky News Arabia Politics': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'RT Arabic Politics': ('Right', '#666', 'https://mediabiasfactcheck.com/rt/'),
    'Al Arabiya Politics': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/al-arabiya/'),
}

DEFAULT_SOURCES = ['Al Jazeera', 'BBC Arabic', 'France 24 Arabic', 'DW Arabic', 'Al Arabiya']

SOURCES = [
    ('Al Jazeera', 'Left'),
    ('BBC Arabic', 'Left-Center'),
    ('France 24 Arabic', 'Left-Center'),
    ('DW Arabic', 'Center'),
    ('Sky News Arabia', 'Center'),
    ('Asharq Al-Awsat', 'Center'),
    ('Al-Masry Al-Youm', 'Center'),
    ('Youm7', 'Center'),
    ('Al Arabiya', 'Right-Center'),
    ('RT Arabic', 'Right'),
    
    # Category-specific sources
    ('BBC Arabic Sport', 'Left-Center'),
    ('Al Jazeera Sport', 'Left'),
    ('Sky News Arabia Sport', 'Center'),
    ('RT Arabic Sport', 'Right'),
    ('Al Arabiya Sport', 'Right-Center'),
    ('Bein Sports', 'Center'),
    ('Goal Arabic', 'Center'),
    ('Kooora', 'Center'),
    ('BBC Arabic Business', 'Left-Center'),
    ('Al Jazeera Business', 'Left'),
    ('Sky News Arabia Business', 'Center'),
    ('RT Arabic Business', 'Right'),
    ('Al Arabiya Business', 'Right-Center'),
    ('Al-Masry Al-Youm Economy', 'Center'),
    ('Youm7 Economy', 'Center'),
    ('CNBC Arabia', 'Center'),
    ('BBC Arabic Technology', 'Left-Center'),
    ('Al Jazeera Technology', 'Left'),
    ('Sky News Arabia Technology', 'Center'),
    ('RT Arabic Technology', 'Right'),
    ('Al Arabiya Technology', 'Right-Center'),
    ('BBC Arabic World', 'Left-Center'),
    ('Al Jazeera World', 'Left'),
    ('France 24 Arabic World', 'Left-Center'),
    ('DW Arabic World', 'Center'),
    ('Sky News Arabia World', 'Center'),
    ('RT Arabic World', 'Right'),
    ('Al Arabiya World', 'Right-Center'),
    ('Asharq Al-Awsat World', 'Center'),
    ('BBC Arabic Science', 'Left-Center'),
    ('Al Jazeera Science', 'Left'),
    ('Sky News Arabia Science', 'Center'),
    ('RT Arabic Science', 'Right'),
    ('BBC Arabic Health', 'Left-Center'),
    ('Al Jazeera Health', 'Left'),
    ('Sky News Arabia Health', 'Center'),
    ('RT Arabic Health', 'Right'),
    ('Al Arabiya Health', 'Right-Center'),
    ('BBC Arabic Arts', 'Left-Center'),
    ('Al Jazeera Culture', 'Left'),
    ('Sky News Arabia Entertainment', 'Center'),
    ('RT Arabic Culture', 'Right'),
    ('Al Arabiya Entertainment', 'Right-Center'),
    ('BBC Arabic Politics', 'Left-Center'),
    ('Al Jazeera Politics', 'Left'),
    ('France 24 Arabic Politics', 'Left-Center'),
    ('DW Arabic Politics', 'Center'),
    ('Sky News Arabia Politics', 'Center'),
    ('RT Arabic Politics', 'Right'),
    ('Al Arabiya Politics', 'Right-Center'),
]

CATEGORY_KEYWORDS = {
    'politics': [
        'حكومة', 'رئيس', 'وزير', 'انتخاب', 'تصويت', 'حملة',
        'برلمان', 'مجلس', 'قانون', 'إصلاح', 'حزب',
        'رئيس الوزراء', 'معارضة', 'ائتلاف', 'ديمقراطية', 'سياسة',
    ],
    'business': [
        'بورصة', 'اقتصاد', 'سوق', 'شركة', 'بنك', 'مال',
        'استثمار', 'دولار', 'ريال', 'درهم', 'تضخم', 'بطالة', 'ناتج', 'نمو',
        'سهم', 'أرباح', 'ائتمان', 'دين', 'تصدير', 'استيراد',
        'تجارة', 'صناعة', 'عمل', 'راتب', 'ضريبة', 'نفط',
    ],
    'technology': [
        'تكنولوجيا', 'ذكاء اصطناعي', 'برمجيات', 'هجوم إلكتروني', 'رقمي',
        'روبوت', 'تطبيق', 'هاتف ذكي', 'إنترنت', 'حاسوب', 'بيانات',
        'أمن سيبراني', 'خوارزمية', 'منصة', 'شبكات اجتماعية', 'شركة ناشئة',
        'غوغل', 'أبل', 'مايكروسوفت', 'أمازون', 'ميتا', 'تسلا',
    ],
    'science': [
        'علم', 'بحث', 'اكتشاف', 'نوع', 'وراثة', 'مناخ',
        'زلزال', 'بركان', 'كوكب', 'فضاء', 'كون', 'فيزياء',
        'كيمياء', 'أحياء', 'مختبر', 'دراسة', 'عالم', 'ناسا',
        'حفريات', 'تطور', 'تنوع بيولوجي', 'محيط',
    ],
    'health': [
        'مستشفى', 'طبيب', 'طب', 'لقاح', 'جائحة', 'صحة', 'مرض',
        'علاج', 'فيروس', 'عيادة', 'مريض', 'جراحة', 'علاج', 'عرض',
        'تشخيص', 'صيدلة', 'تغذية', 'تمارين', 'رفاهية', 'كورونا',
        'سرطان', 'سكر', 'قلب', 'دماغ',
    ],
    'sports': [
        'كرة قدم', 'دوري', 'أبطال', 'كأس', 'عالم', 'أولمبياد', 'رياضة',
        'فريق', 'لاعب', 'مباراة', 'هدف', 'تنس', 'كرة سلة',
        'مدرب', 'ملعب', 'بطولة', 'حكم',
        'الأهلي', 'الزمالك', 'الهلال', 'النصر', 'دوري أبطال',
    ],
    'gulf': [
        'السعودية', 'الإمارات', 'قطر', 'الكويت', 'البحرين', 'عمان',
        'الرياض', 'أبو ظبي', 'الدوحة', 'الكويت', 'مسقط', 'المنامة',
        'مصر', 'القاهرة', 'الإسكندرية', 'السيسي', 'البرلمان',
        'سوريا', 'لبنان', 'الأردن', 'العراق', 'فلسطين', 'دمشق', 'بيروت', 'عمان', 'بغداد',
        'المغرب', 'تونس', 'الجزائر', 'ليبيا', 'الرباط', 'تونس', 'الجزائر', 'طرابلس',
    ],
    'world': [
        'أوكرانيا', 'روسيا', 'الصين', 'إيران', 'إسرائيل', 'غزة', 'الشرق الأوسط', 'أوروبا',
        'آسيا', 'أفريقيا', 'أمريكا اللاتينية', 'حرب', 'دبلوماسي', 'هجرة',
        'لاجئ', 'عالمي', 'دولي', 'الأمم المتحدة', 'الناتو', 'نزاع', 'أزمة',
        'عسكري', 'جيش', 'سلام', 'اتفاق', 'معاهدة', 'عقوبات',
    ],
    'entertainment': [
        'فيلم', 'سينما', 'ممثل', 'ممثلة', 'أوسكار', 'شهرة',
        'موسيقى', 'ألبوم', 'حفل', 'جولة', 'نتفليكس', 'بث', 'شباك التذاكر',
        'مسرح', 'مسلسل', 'موسم', 'نهاية الموسم',
        'مغني', 'فرقة', 'سبوتيفاي',
        'ديزني', 'هوليوود', 'جائزة', 'السجادة الحمراء',
        'كوميديا', 'دراما', 'رعب',
        'لعبة فيديو', 'ألعاب', 'يوتيوب', 'تيك توك',
        'مؤثر', 'محتوى viral', 'بودكاست', 'كتاب',
        'تلفزيون', 'برنامج',
    ],
}

STOP_WORDS = {
    'ال', 'و', 'أو', 'لكن', 'في', 'من', 'على', 'إلى', 'ل', 'ب', 'ك',
    'هو', 'هي', 'هم', 'هن', 'أنت', 'أنا', 'نحن',
    'هذا', 'هذه', 'هؤلاء', 'ذلك', 'تلك',
    'الذي', 'التي', 'الذين', 'اللواتي',
    'كان', 'كانت', 'يكون', 'تكون', 'هو', 'هي',
    'هل', 'لا', 'ما', 'لم', 'لن', 'قد',
    'بعد', 'قبل', 'بين', 'فوق', 'تحت',
    'جديد', 'جديدة', 'قال', 'قالت', 'حسب',
}

SOURCE_ATTRIBUTION = r'\s*(الجزيرة|بي بي سي|فرانس 24|دويتشه فيله|سكاي نيوز|رويترز|العربية|الشرق الأوسط|المصري اليوم|اليوم السابع)\s*$'

GENERIC_TEXT = [
    'تغطية إخبارية شاملة',
    'تم تجميعه من',
    'انقر هنا للمزيد',
]

CATEGORY_NAMES = OrderedDict([
    ('all', 'الكل'),
    ('most_covered', 'الأكثر تغطية'),
    ('world', 'العالم'),
    ('gulf', 'العربية'),
    ('politics', 'سياسة'),
    ('business', 'اقتصاد'),
    ('technology', 'تكنولوجيا'),
    ('science', 'علوم'),
    ('health', 'صحة'),
    ('sports', 'رياضة'),
    ('entertainment', 'ترفيه'),
])

CATEGORY_KEYWORDS_WEIGHTED = {
    'politics': {
        'high': ['رئيس', 'حكومة', 'وزير', 'برلمان', 'مجلس', 'حزب', 'معارضة', 'ائتلاف'],
        'medium': ['انتخاب', 'تصويت', 'حملة', 'قانون', 'إصلاح', 'ديمقراطية', 'سياسة'],
        'low': []
    },
    'business': {
        'high': ['بورصة', 'دولار', 'ريال', 'درهم', 'سهم', 'أرباح', 'تضخم', 'نفط'],
        'medium': ['اقتصاد', 'سوق', 'شركة', 'بنك', 'مال', 'استثمار', 'بطالة', 'ناتج', 'نمو', 'ائتمان', 'دين', 'تصدير', 'استيراد', 'تجارة', 'صناعة', 'عمل', 'راتب', 'ضريبة'],
        'low': []
    },
    'technology': {
        'high': ['ذكاء اصطناعي', 'هجوم إلكتروني', 'أمن سيبراني', 'خوارزمية'],
        'medium': ['تكنولوجيا', 'برمجيات', 'رقمي', 'روبوت', 'تطبيق', 'هاتف ذكي', 'إنترنت', 'حاسوب', 'بيانات', 'منصة', 'شبكات اجتماعية', 'شركة ناشئة', 'غوغل', 'أبل', 'مايكروسوفت', 'أمازون', 'ميتا', 'تسلا'],
        'low': []
    },
    'science': {
        'high': ['ناسا', 'وراثة', 'تطور', 'تنوع بيولوجي'],
        'medium': ['علم', 'بحث', 'اكتشاف', 'نوع', 'مناخ', 'زلزال', 'بركان', 'كوكب', 'فضاء', 'كون', 'فيزياء', 'كيمياء', 'أحياء', 'مختبر', 'دراسة', 'عالم', 'حفريات', 'محيط'],
        'low': []
    },
    'health': {
        'high': ['مستشفى', 'طبيب', 'طب', 'لقاح', 'جائحة', 'كورونا', 'سرطان', 'سكر'],
        'medium': ['صحة', 'مرض', 'علاج', 'فيروس', 'عيادة', 'مريض', 'جراحة', 'علاج', 'عرض', 'تشخيص', 'صيدلة', 'تغذية', 'تمارين', 'رفاهية', 'قلب', 'دماغ'],
        'low': []
    },
    'sports': {
        'high': ['الأهلي', 'الزمالك', 'الهلال', 'النصر', 'دوري أبطال'],
        'medium': ['كرة قدم', 'دوري', 'أبطال', 'كأس', 'عالم', 'أولمبياد', 'رياضة', 'فريق', 'لاعب', 'مباراة', 'هدف', 'تنس', 'كرة سلة', 'مدرب', 'ملعب', 'بطولة', 'حكم'],
        'low': []
    },
    'gulf': {
        'high': ['السعودية', 'الإمارات', 'قطر', 'الكويت', 'البحرين', 'عمان', 'الرياض', 'أبو ظبي', 'الدوحة'],
        'medium': ['مصر', 'القاهرة', 'الإسكندرية', 'السيسي', 'البرلمان', 'سوريا', 'لبنان', 'الأردن', 'العراق', 'فلسطين', 'دمشق', 'بيروت', 'عمان', 'بغداد', 'المغرب', 'تونس', 'الجزائر', 'ليبيا', 'الرباط', 'تونس', 'الجزائر', 'طرابلس'],
        'low': []
    },
    'world': {
        'high': ['أوكرانيا', 'روسيا', 'حرب', 'أزمة', 'غزة', 'إسرائيل', 'بوتين'],
        'medium': ['الصين', 'إيران', 'إسرائيل', 'غزة', 'الشرق الأوسط', 'أوروبا', 'آسيا', 'أفريقيا', 'أمريكا اللاتينية', 'دبلوماسي', 'هجرة', 'لاجئ', 'عالمي', 'دولي', 'الأمم المتحدة', 'الناتو', 'نزاع', 'عسكري', 'جيش', 'سلام', 'اتفاق', 'معاهدة', 'عقوبات'],
        'low': []
    },
    'entertainment': {
        'high': ['أوسكار', 'نتفليكس', 'ديزني', 'هوليوود', 'سبوتيفاي'],
        'medium': ['فيلم', 'سينما', 'ممثل', 'ممثلة', 'شهرة', 'موسيقى', 'ألبوم', 'حفل', 'جولة', 'بث', 'شباك التذاكر', 'مسرح', 'مسلسل', 'موسم', 'نهاية الموسم', 'مغني', 'فرقة', 'جائزة', 'السجادة الحمراء', 'كوميديا', 'دراما', 'رعب', 'لعبة فيديو', 'ألعاب', 'يوتيوب', 'تيك توك', 'مؤثر', 'محتوى viral', 'بودكاست', 'كتاب', 'تلفزيون', 'برنامج'],
        'low': []
    },
}

UI_STRINGS = {
    'subtitle': 'اختر توجهك | خدمات الأنباء والتغذية الأخرى | آخر 24 ساعة',
    'how_it_works': 'كيف يعمل',
    'privacy_text': 'نحترم خصوصيتك. يستخدم هذا الموقع إعلانات سياقية (بدون ملفات تعريف الارتباط التتبعية) ويعرض العناوين/الملخصات بموجب الاستخدام العادل.',
    'privacy_link': 'سياسة الخصوصية',
    'got_it': 'فهمت',
    'sources': 'المصادر:',
    'center_default': 'المصادر المركزية (افتراضي)',
    'all_sources': 'جميع المصادر',
    'center_only': 'الوسط فقط',
    'left_center_only': 'اليسار الوسط فقط',
    'left_only': 'اليسار فقط',
    'right_only': 'اليمين فقط',
    'clear_all': 'مسح الكل',
    'sources_suffix': 'مصادر',
    'covered_by_2': 'أخبار مغطاة من مصدرين أو أكثر',
    'paywall_title': 'موقع مدفوع',
    'sources_label': 'مصادر',
    'read_full': 'اقرأ القصة كاملة',
    'find_coverage': 'ابحث عن تغطية',
    'search_related': 'ابحث عن تغطية ذات صلة',
    'bias_rating': 'تقييم التوجه',
    'ago': 'منذ',
    'show_stories': 'عرض',
    'stories': 'أخبار',
    'no_stories': 'لا توجد أخبار في هذه الفئة',
    'footer_copy': 'محتوى الأخبار © الناشرون المعنية. يتم استخدام العناوين والملخصات بموجب الاستخدام العادل لأغراض إعلامية.',
    'footer_sources': 'المصادر:',
    'footer_and': 'و',
    'footer_terms': 'الشروط',
    'footer_privacy': 'الخصوصية',
    'footer_about': 'حول',
    # Header translations
    'logo_tagline': 'أخبار من منظور مختلف',
    'search_placeholder': 'البحث في الأخبار...',
    'toggle_theme': 'تبديل السمة',
    'filter_label': 'تصفية حسب:',
    # Bias filter buttons
    'filter_all': 'الكل',
    'filter_left': 'اليسار',
    'filter_left_center': 'الوسط اليسار',
    'filter_center': 'الوسط',
    'filter_right_center': 'الوسط اليمين',
    'filter_right': 'اليمين',
    # Story card buttons
    'find_coverage_btn': 'البحث عن تغطية',
    'different_angle_btn': 'زاوية أخرى',
    'share_btn': 'مشاركة',
    'different_perspectives': 'منظور مختلف',
    # Different Angle modal
    'different_angle_title': 'منظور مختلف',
    'original_label': 'الأصل:',
    'loading_related': 'جاري تحميل الأخبار ذات الصلة...',
    'no_related_stories': 'لم يتم العثور على أخبار ذات صلة',
    'error_loading': 'خطأ في التحميل',
    # Share modal
    'share_story_title': 'مشاركة الخبر',
    'share_on_x': 'المشاركة على X',
    'share_facebook': 'المشاركة على Facebook',
    'share_linkedin': 'المشاركة على LinkedIn',
    'copy_link': 'نسخ الرابط',
    'copied': 'تم النسخ!',
    'close': 'إغلاق',
}

PAYWALLED_SOURCES = set()
