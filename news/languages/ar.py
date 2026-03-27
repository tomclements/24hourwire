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
    'us': [
        'الولايات المتحدة', 'أمريكا', 'فلوريدا', 'تكساس', 'كاليفورنيا',
        'نيويورك', 'ميامي', 'لوس أنجلوس', 'شيكاغو', 'واشنطن', 'ترامب', 'بايدن',
        'البيت الأبيض', 'كونغرس', 'مجلس الشيوخ', 'أف بي آي', 'سي آي إيه', 'بنتاغون',
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
    ('us', 'الولايات المتحدة'),
    ('politics', 'سياسة'),
    ('business', 'اقتصاد'),
    ('technology', 'تكنولوجيا'),
    ('science', 'علوم'),
    ('health', 'صحة'),
    ('sports', 'رياضة'),
    ('entertainment', 'ترفيه'),
])

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
}

PAYWALLED_SOURCES = set()
