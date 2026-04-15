from collections import OrderedDict

CODE = 'ja'
NAME = '日本語'

FEEDS = [
    ('NHK', 'https://www3.nhk.or.jp/rss/news/cat0.xml'),
    ('朝日新聞', 'https://www.asahi.com/rss/asahi/newsheadlines.rdf'),
    ('読売新聞', 'https://www.yomiuri.co.jp/rss/news/flash.xml'),
    ('毎日新聞', 'https://mainichi.jp/rss/etc/mainichi-flash.rss'),
    ('日経新聞', 'https://www.nikkei.com/rss/newflash.rdf'),
    ('共同通信', 'https://news.google.com/rss/search?q=site:47news.jp&hl=ja&gl=JP&ceid=JP:ja'),
    ('東京新聞', 'https://www.tokyo-np.co.jp/rss/index.xml'),
    ('産経新聞', 'https://www.sankei.com/rss/flash/flash.rdf'),
    ('時事通信', 'https://news.google.com/rss/search?q=site:jiji.com&hl=ja&gl=JP&ceid=JP:ja'),
    ('ITmedia', 'https://rss.itmedia.co.jp/rss/2.0/itmedia_news.xml'),
    
    # Category-specific feeds
    # Sports
    ('日刊スポーツ', 'https://www.nikkansports.com/rss/index.xml'),
    ('スポーツニッポン', 'https://www.sponichi.co.jp/rss/index.xml'),
    ('スポーツ報知', 'https://www.hochi.co.jp/rss/index.xml'),
    ('Soccer King', 'https://www.soccer-king.jp/feed'),
    ('NHKスポーツ', 'https://www3.nhk.or.jp/rss/news/cat5.xml'),
    ('朝日スポーツ', 'https://www.asahi.com/rss/asahi/sports.rdf'),
    ('読売スポーツ', 'https://www.yomiuri.co.jp/rss/y/sports/index.xml'),
    ('日経スポーツ', 'https://www.nikkei.com/rss/sports.rdf'),
    
    # Business
    ('日経ビジネス', 'https://www.nikkei.com/rss/economy.rdf'),
    ('朝日経済', 'https://www.asahi.com/rss/asahi/business.rdf'),
    ('NHK経済', 'https://www3.nhk.or.jp/rss/news/cat3.xml'),
    ('読売経済', 'https://www.yomiuri.co.jp/rss/y/economy/index.xml'),
    ('毎日経済', 'https://mainichi.jp/rss/etc/mainichi-economy.rss'),
    ('東洋経済', 'https://toyokeizai.net/list/feed/rss'),
    
    # Technology
    ('ITmedia News', 'https://rss.itmedia.co.jp/rss/2.0/itmedia_news.xml'),
    ('Gizmodo Japan', 'https://www.gizmodo.jp/rss/index.xml'),
    ('Engadget Japanese', 'https://japanese.engadget.com/rss.xml'),
    ('TechCrunch Japan', 'https://jp.techcrunch.com/rss'),
    ('ASCII.jp', 'https://ascii.jp/rss.xml'),
    ('Impress Watch', 'https://www.watch.impress.co.jp/rss/headline.rdf'),
    
    # World News
    ('NHK国際', 'https://www3.nhk.or.jp/rss/news/cat6.xml'),
    ('朝日国際', 'https://www.asahi.com/rss/asahi/world.rdf'),
    ('読売国際', 'https://www.yomiuri.co.jp/rss/y/world/index.xml'),
    ('毎日国際', 'https://mainichi.jp/rss/etc/mainichi-world.rss'),
    ('日経国際', 'https://www.nikkei.com/rss/world.rdf'),
    
    # Science
    ('NHK科学', 'https://www3.nhk.or.jp/rss/news/cat2.xml'),
    ('朝日科学', 'https://www.asahi.com/rss/asahi/science.rdf'),
    ('読売科学', 'https://www.yomiuri.co.jp/rss/y/science/index.xml'),
    ('毎日科学', 'https://mainichi.jp/rss/etc/mainichi-science.rss'),
    ('日経科学', 'https://www.nikkei.com/rss/science.rdf'),
    
    # Health
    ('朝日健康', 'https://www.asahi.com/rss/asahi/health.rdf'),
    ('読売医療', 'https://www.yomiuri.co.jp/rss/y/medical/index.xml'),
    ('日経メディカル', 'https://medical.nikkeibp.co.jp/rss/all.rdf'),
    ('NHK健康', 'https://www3.nhk.or.jp/rss/news/cat4.xml'),
    
    # Entertainment
    ('朝日エンタメ', 'https://www.asahi.com/rss/asahi/entertainment.rdf'),
    ('読売芸能', 'https://www.yomiuri.co.jp/rss/y/geino/index.xml'),
    ('日経エンタテインメント', 'https://www.nikkei.com/rss/entertainment.rdf'),
    ('Oricon News', 'https://www.oricon.co.jp/rss/news.xml'),
    
    # Politics
    ('NHK政治', 'https://www3.nhk.or.jp/rss/news/cat1.xml'),
    ('朝日政治', 'https://www.asahi.com/rss/asahi/politics.rdf'),
    ('読売政治', 'https://www.yomiuri.co.jp/rss/y/politics/index.xml'),
    ('毎日政治', 'https://mainichi.jp/rss/etc/mainichi-politics.rss'),
    ('日経政治', 'https://www.nikkei.com/rss/politics.rdf'),
]

SOURCE_INFO = {
    'NHK': ('Center', '#666', 'https://mediabiasfactcheck.com/nhk/'),
    '朝日新聞': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/asahi-shimbun/'),
    '読売新聞': ('Center', '#666', 'https://mediabiasfactcheck.com/yomiuri-shimbun/'),
    '毎日新聞': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/mainichi-shimbun/'),
    '日経新聞': ('Center', '#666', 'https://mediabiasfactcheck.com/nikkei/'),
    '共同通信': ('Center', '#666', 'https://mediabiasfactcheck.com/kyodo-news/'),
    '東京新聞': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/'),
    '産経新聞': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/sankei-shimbun/'),
    '時事通信': ('Center', '#666', 'https://mediabiasfactcheck.com/jiji-press/'),
    'ITmedia': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    
    # Category-specific sources
    '日刊スポーツ': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'スポーツニッポン': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'スポーツ報知': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Soccer King': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'NHKスポーツ': ('Center', '#666', 'https://mediabiasfactcheck.com/nhk/'),
    '朝日スポーツ': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/asahi-shimbun/'),
    '読売スポーツ': ('Center', '#666', 'https://mediabiasfactcheck.com/yomiuri-shimbun/'),
    '日経スポーツ': ('Center', '#666', 'https://mediabiasfactcheck.com/nikkei/'),
    '日経ビジネス': ('Center', '#666', 'https://mediabiasfactcheck.com/nikkei/'),
    '朝日経済': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/asahi-shimbun/'),
    'NHK経済': ('Center', '#666', 'https://mediabiasfactcheck.com/nhk/'),
    '読売経済': ('Center', '#666', 'https://mediabiasfactcheck.com/yomiuri-shimbun/'),
    '毎日経済': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/mainichi-shimbun/'),
    '東洋経済': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'ITmedia News': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Gizmodo Japan': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Engadget Japanese': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'TechCrunch Japan': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'ASCII.jp': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Impress Watch': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'NHK国際': ('Center', '#666', 'https://mediabiasfactcheck.com/nhk/'),
    '朝日国際': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/asahi-shimbun/'),
    '読売国際': ('Center', '#666', 'https://mediabiasfactcheck.com/yomiuri-shimbun/'),
    '毎日国際': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/mainichi-shimbun/'),
    '日経国際': ('Center', '#666', 'https://mediabiasfactcheck.com/nikkei/'),
    'NHK科学': ('Center', '#666', 'https://mediabiasfactcheck.com/nhk/'),
    '朝日科学': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/asahi-shimbun/'),
    '読売科学': ('Center', '#666', 'https://mediabiasfactcheck.com/yomiuri-shimbun/'),
    '毎日科学': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/mainichi-shimbun/'),
    '日経科学': ('Center', '#666', 'https://mediabiasfactcheck.com/nikkei/'),
    '朝日健康': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/asahi-shimbun/'),
    '読売医療': ('Center', '#666', 'https://mediabiasfactcheck.com/yomiuri-shimbun/'),
    '日経メディカル': ('Center', '#666', 'https://mediabiasfactcheck.com/nikkei/'),
    'NHK健康': ('Center', '#666', 'https://mediabiasfactcheck.com/nhk/'),
    '朝日エンタメ': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/asahi-shimbun/'),
    '読売芸能': ('Center', '#666', 'https://mediabiasfactcheck.com/yomiuri-shimbun/'),
    '日経エンタテインメント': ('Center', '#666', 'https://mediabiasfactcheck.com/nikkei/'),
    'Oricon News': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'NHK政治': ('Center', '#666', 'https://mediabiasfactcheck.com/nhk/'),
    '朝日政治': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/asahi-shimbun/'),
    '読売政治': ('Center', '#666', 'https://mediabiasfactcheck.com/yomiuri-shimbun/'),
    '毎日政治': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/mainichi-shimbun/'),
    '日経政治': ('Center', '#666', 'https://mediabiasfactcheck.com/nikkei/'),
}

DEFAULT_SOURCES = ['NHK', '読売新聞', '日経新聞', '共同通信', '朝日新聞', '時事通信']

SOURCES = [
    ('NHK', 'Center'),
    ('読売新聞', 'Center'),
    ('日経新聞', 'Center'),
    ('共同通信', 'Center'),
    ('時事通信', 'Center'),
    ('ITmedia', 'Center'),
    ('朝日新聞', 'Left-Center'),
    ('毎日新聞', 'Left-Center'),
    ('東京新聞', 'Left-Center'),
    ('産経新聞', 'Right-Center'),
    
    # Category-specific sources
    ('日刊スポーツ', 'Center'),
    ('スポーツニッポン', 'Center'),
    ('スポーツ報知', 'Center'),
    ('Soccer King', 'Center'),
    ('NHKスポーツ', 'Center'),
    ('朝日スポーツ', 'Left-Center'),
    ('読売スポーツ', 'Center'),
    ('日経スポーツ', 'Center'),
    ('日経ビジネス', 'Center'),
    ('朝日経済', 'Left-Center'),
    ('NHK経済', 'Center'),
    ('読売経済', 'Center'),
    ('毎日経済', 'Left-Center'),
    ('東洋経済', 'Center'),
    ('ITmedia News', 'Center'),
    ('Gizmodo Japan', 'Center'),
    ('Engadget Japanese', 'Center'),
    ('TechCrunch Japan', 'Center'),
    ('ASCII.jp', 'Center'),
    ('Impress Watch', 'Center'),
    ('NHK国際', 'Center'),
    ('朝日国際', 'Left-Center'),
    ('読売国際', 'Center'),
    ('毎日国際', 'Left-Center'),
    ('日経国際', 'Center'),
    ('NHK科学', 'Center'),
    ('朝日科学', 'Left-Center'),
    ('読売科学', 'Center'),
    ('毎日科学', 'Left-Center'),
    ('日経科学', 'Center'),
    ('朝日健康', 'Left-Center'),
    ('読売医療', 'Center'),
    ('日経メディカル', 'Center'),
    ('NHK健康', 'Center'),
    ('朝日エンタメ', 'Left-Center'),
    ('読売芸能', 'Center'),
    ('日経エンタテインメント', 'Center'),
    ('Oricon News', 'Center'),
    ('NHK政治', 'Center'),
    ('朝日政治', 'Left-Center'),
    ('読売政治', 'Center'),
    ('毎日政治', 'Left-Center'),
    ('日経政治', 'Center'),
]

CATEGORY_KEYWORDS = {
    'politics': [
        '政府', '首相', '大臣', '選挙', '投票', 'キャンペーン',
        '国会', '参議院', '衆議院', '法律', '改革', '政党',
        '自民党', '立憲民主党', '公明党', '維新', '内閣',
        '野党', '与党', '政治', '首相官邸',
    ],
    'business': [
        '株式', '経済', '市場', '企業', '銀行', '金融',
        '投資', '円', 'ドル', 'インフレ', '失業', 'gdp', '成長',
        '株', '配当', '信用', '債務', '輸出', '輸入',
        '産業', '貿易', '雇用', '給与', '税金', '日経平均',
    ],
    'technology': [
        'テクノロジー', '人工知能', 'ソフトウェア', 'サイバー攻撃', 'デジタル',
        'ロボット', 'アプリ', 'スマートフォン', 'インターネット', 'コンピュータ', 'データ',
        'サイバーセキュリティ', 'アルゴリズム', 'プラットフォーム', 'SNS', 'スタートアップ',
        'グーグル', 'アップル', 'マイクロソフト', 'アマゾン', 'メタ', 'テスラ', 'ソニー',
    ],
    'science': [
        '科学', '研究', '発見', '種', '遺伝子', '気候',
        '地震', '火山', '惑星', '宇宙', '物理学',
        '化学', '生物学', '研究所', '学者', 'NASA',
        '化石', '進化', '生物多様性', '海洋', 'JAXA',
    ],
    'health': [
        '病院', '医師', '医学', 'ワクチン', 'パンデミック', '健康', '病気',
        '治療', 'ウイルス', 'クリニック', '患者', '手術', '療法', '症状',
        '診断', '医薬品', '栄養', '運動', 'コロナ',
        'がん', '糖尿病', '心臓', '脳', '厚労省',
    ],
    'sports': [
        'サッカー', 'リーグ', 'チャンピオンズ', 'カップ', 'ワールド', '五輪', 'スポーツ',
        'チーム', '選手', '試合', 'ゴール', 'テニス', 'バスケ', '野球',
        '監督', 'スタジアム', '大会', '審判',
        '大谷', '巨人', '阪神', '広島', 'Jリーグ', 'メジャーリーグ',
    ],
    'japan': [
        '日本', '首相', '内閣', '国会', '衆議院', '参議院', '政府',
        '東京', '大阪', '横浜', '自民党', '立憲民主党', '公明党', '維新', '共産党',
        'アジア', '中国', '韓国', 'インド', '東南アジア', 'ASEAN', 'アジア太平洋',
    ],
    'world': [
        'ウクライナ', 'ロシア', '中国', 'イラン', 'イスラエル', 'ガザ', '中東', '欧州',
        'アジア', 'アフリカ', 'ラテンアメリカ', '戦争', '外交', '移民',
        '難民', '国際', '国連', 'NATO', '紛争', '危機',
        '軍事', '軍', '和平', '合意', '条約', '制裁',
    ],
    'entertainment': [
        '映画', 'シネマ', '俳優', '女優', 'アカデミー賞', '有名人',
        '音楽', 'アルバム', 'コンサート', 'ツアー', 'ネットフリックス', '配信', '興行',
        '演劇', 'ドラマ', 'シーズン', '最終回',
        '歌手', 'バンド', 'スポティファイ',
        'ディズニー', 'ハリウッド', '賞', 'レッドカーペット',
        'コメディ', 'ホラー',
        'ゲーム', 'eスポーツ', 'ユーチューブ', 'ティックトック',
        'インフルエンサー', 'バイラル', 'ポッドキャスト', 'ベストセラー', '本',
        'テレビ', '番組',
    ],
}

STOP_WORDS = {
    'の', 'に', 'は', 'を', 'が', 'で', 'と', 'も', 'から', 'まで',
    'へ', 'より', 'など', 'ので', 'けど', 'けれど', 'ば',
    'だ', 'です', 'である', 'ます', 'ました', 'ない',
    'これ', 'それ', 'あれ', 'この', 'その', 'あの',
    '彼', '彼女', '彼ら', '私', '僕', '君', '俺',
    'ここ', 'そこ', 'あそこ', 'どこ',
    '何', '誰', 'いつ', 'どう', 'なぜ', 'いくら',
    '新しい', '言う', '言った', 'による',
}

SOURCE_ATTRIBUTION = r'\s*(NHK|朝日新聞|読売新聞|毎日新聞|日経新聞|共同通信|東京新聞|産経新聞|時事通信|ITmedia)\s*$'

GENERIC_TEXT = [
    '包括的なニュース報道',
    'から集約',
    '詳細はこちら',
]

CATEGORY_NAMES = OrderedDict([
    ('all', 'すべて'),
    ('most_covered', '最も報道された'),
    ('world', '世界'),
    ('japan', '日本'),
    ('politics', '政治'),
    ('business', '経済'),
    ('technology', 'テクノロジー'),
    ('science', '科学'),
    ('health', '健康'),
    ('sports', 'スポーツ'),
    ('entertainment', 'エンタメ'),
])

CATEGORY_KEYWORDS_WEIGHTED = {
    'politics': {
        'high': ['首相', '内閣', '国会', '衆議院', '参議院', '自民党', '立憲民主党', '公明党'],
        'medium': ['政府', '大臣', '選挙', '投票', 'キャンペーン', '法律', '改革', '政党', '維新', '共産党', '野党', '与党', '政治', '首相官邸'],
        'low': []
    },
    'business': {
        'high': ['日経平均', '円', 'ドル', '株', '配当', 'インフレ'],
        'medium': ['株式', '経済', '市場', '企業', '銀行', '金融', '投資', '失業', 'gdp', '成長', '信用', '債務', '輸出', '輸入', '産業', '貿易', '雇用', '給与', '税金'],
        'low': []
    },
    'technology': {
        'high': ['人工知能', 'サイバー攻撃', 'サイバーセキュリティ', 'アルゴリズム'],
        'medium': ['テクノロジー', 'ソフトウェア', 'デジタル', 'ロボット', 'アプリ', 'スマートフォン', 'インターネット', 'コンピュータ', 'データ', 'プラットフォーム', 'SNS', 'スタートアップ', 'グーグル', 'アップル', 'マイクロソフト', 'アマゾン', 'メタ', 'テスラ', 'ソニー'],
        'low': []
    },
    'science': {
        'high': ['NASA', 'JAXA', '遺伝子', '進化', '生物多様性'],
        'medium': ['科学', '研究', '発見', '種', '気候', '地震', '火山', '惑星', '宇宙', '物理学', '化学', '生物学', '研究所', '学者', '化石', '海洋'],
        'low': []
    },
    'health': {
        'high': ['病院', '医師', '医学', 'ワクチン', 'パンデミック', 'コロナ', 'がん', '糖尿病', '厚労省'],
        'medium': ['健康', '病気', '治療', 'ウイルス', 'クリニック', '患者', '手術', '療法', '症状', '診断', '医薬品', '栄養', '運動', '心臓', '脳'],
        'low': []
    },
    'sports': {
        'high': ['大谷', '巨人', '阪神', '広島', 'Jリーグ', 'メジャーリーグ'],
        'medium': ['サッカー', 'リーグ', 'チャンピオンズ', 'カップ', 'ワールド', '五輪', 'スポーツ', 'チーム', '選手', '試合', 'ゴール', 'テニス', 'バスケ', '野球', '監督', 'スタジアム', '大会', '審判'],
        'low': []
    },
    'japan': {
        'high': ['日本', '首相', '内閣', '国会', '衆議院', '参議院', '政府', '東京', '大阪', '横浜'],
        'medium': ['自民党', '立憲民主党', '公明党', '維新', '共産党', 'アジア', '中国', '韓国', 'インド', '東南アジア', 'ASEAN', 'アジア太平洋'],
        'low': []
    },
    'world': {
        'high': ['ウクライナ', 'ロシア', '戦争', '危機', 'ガザ', 'イスラエル', 'プーチン'],
        'medium': ['中国', 'イラン', 'イスラエル', 'ガザ', '中東', '欧州', 'アジア', 'アフリカ', 'ラテンアメリカ', '外交', '移民', '難民', '国際', '国連', 'NATO', '紛争', '軍事', '軍', '和平', '合意', '条約', '制裁'],
        'low': []
    },
    'entertainment': {
        'high': ['アカデミー賞', 'ネットフリックス', 'ディズニー', 'ハリウッド', 'スポティファイ'],
        'medium': ['映画', 'シネマ', '俳優', '女優', '有名人', '音楽', 'アルバム', 'コンサート', 'ツアー', '配信', '興行', '演劇', 'ドラマ', 'シーズン', '最終回', '歌手', 'バンド', '賞', 'レッドカーペット', 'コメディ', 'ホラー', 'ゲーム', 'eスポーツ', 'ユーチューブ', 'ティックトック', 'インフルエンサー', 'バイラル', 'ポッドキャスト', 'ベストセラー', '本', 'テレビ', '番組'],
        'low': []
    },
}

UI_STRINGS = {
    'subtitle': 'バイアスを選択 | ワイヤーサービスとその他のフィード | 過去24時間',
    'how_it_works': '仕組み',
    'privacy_text': 'プライバシーを尊重しています。このサイトはコンテキスト広告（追跡Cookieなし）を使用し、フェアユースに基づいて見出し/要約を表示します。',
    'privacy_link': 'プライバシーポリシー',
    'got_it': '了解',
    'sources': 'ソース:',
    'center_default': '中央ソース（デフォルト）',
    'all_sources': 'すべてのソース',
    'center_only': '中央のみ',
    'left_center_only': '中道左派のみ',
    'left_only': '左派のみ',
    'right_only': '右派のみ',
    'clear_all': 'すべてクリア',
    'sources_suffix': 'ソース',
    'covered_by_2': '2つ以上のソースで報道されたニュース',
    'paywall_title': '有料サイト',
    'sources_label': 'ソース',
    'read_full': '記事全文を読む',
    'find_coverage': '報道を探す',
    'search_related': '関連報道を検索',
    'bias_rating': 'バイアス評価',
    'ago': '前',
    'show_stories': '表示',
    'stories': '件',
    'no_stories': 'このカテゴリにはニュースがありません',
    'footer_copy': 'ニュースコンテンツ © 各出版社。見出しと要約は情報提供を目的としたフェアユースに基づいて使用されています。',
    'footer_sources': 'ソース:',
    'footer_and': 'と',
    'footer_terms': '利用規約',
    'footer_privacy': 'プライバシー',
    'footer_about': 'について',
}

PAYWALLED_SOURCES = {
    '日経新聞',
    '朝日新聞',
    '読売新聞',
    '毎日新聞',
}
