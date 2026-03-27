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
    'us': [
        'アメリカ', '米国', 'フロリダ', 'テキサス', 'カリフォルニア',
        'ニューヨーク', 'マイアミ', 'ロサンゼルス', 'シカゴ', 'ワシントン', 'トランプ', 'バイデン',
        'ホワイトハウス', '議会', '上院', 'FBI', 'CIA', 'ペンタゴン',
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
    ('us', 'アメリカ'),
    ('politics', '政治'),
    ('business', '経済'),
    ('technology', 'テクノロジー'),
    ('science', '科学'),
    ('health', '健康'),
    ('sports', 'スポーツ'),
    ('entertainment', 'エンタメ'),
])

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
