from collections import OrderedDict

CODE = 'zh'
NAME = '中文'

FEEDS = [
    ('新华社', 'https://news.google.com/rss/search?q=site:xinhuanet.com&hl=zh-CN&gl=CN&ceid=CN:zh-Hans'),
    ('人民日报', 'https://news.google.com/rss/search?q=site:people.com.cn&hl=zh-CN&gl=CN&ceid=CN:zh-Hans'),
    ('央视新闻', 'https://news.google.com/rss/search?q=site:cctv.com&hl=zh-CN&gl=CN&ceid=CN:zh-Hans'),
    ('BBC中文', 'https://feeds.bbci.co.uk/zhongwen/trad/rss.xml'),
    ('南华早报', 'https://www.scmp.com/rss/5/feed'),
    ('联合早报', 'https://www.zaobao.com.sg/rss'),
    ('DW中文', 'https://rss.dw.com/xml/rss-zh-all'),
    ('法国国际广播电台', 'https://www.rfi.fr/cn/rss'),
    ('端传媒', 'https://news.google.com/rss/search?q=site:theinitium.com&hl=zh-CN&gl=CN&ceid=CN:zh-Hans'),
    ('澎湃新闻', 'https://news.google.com/rss/search?q=site:thepaper.cn&hl=zh-CN&gl=CN&ceid=CN:zh-Hans'),
]

SOURCE_INFO = {
    '新华社': ('Center', '#666', 'https://mediabiasfactcheck.com/xinhua/'),
    '人民日报': ('Center', '#666', 'https://mediabiasfactcheck.com/peoples-daily/'),
    '央视新闻': ('Center', '#666', 'https://mediabiasfactcheck.com/cctv/'),
    'BBC中文': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    '南华早报': ('Center', '#666', 'https://mediabiasfactcheck.com/south-china-morning-post/'),
    '联合早报': ('Center', '#666', 'https://mediabiasfactcheck.com/zaobao/'),
    'DW中文': ('Center', '#666', 'https://mediabiasfactcheck.com/deutsche-welle/'),
    '法国国际广播电台': ('Center', '#666', 'https://mediabiasfactcheck.com/rfi/'),
    '端传媒': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/the-initium/'),
    '澎湃新闻': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
}

DEFAULT_SOURCES = ['新华社', '央视新闻', 'BBC中文', '南华早报', '联合早报', '澎湃新闻']

SOURCES = [
    ('新华社', 'Center'),
    ('人民日报', 'Center'),
    ('央视新闻', 'Center'),
    ('南华早报', 'Center'),
    ('联合早报', 'Center'),
    ('澎湃新闻', 'Center'),
    ('BBC中文', 'Left-Center'),
    ('端传媒', 'Left-Center'),
    ('DW中文', 'Center'),
    ('法国国际广播电台', 'Center'),
]

CATEGORY_KEYWORDS = {
    'politics': [
        '政府', '主席', '总理', '部长', '选举', '投票', '竞选',
        '人大', '政协', '国务院', '法律', '改革', '党',
        '习近平', '李强', '政治局', '反对派', '政治',
    ],
    'business': [
        '股市', '经济', '市场', '企业', '银行', '金融',
        '投资', '人民币', '美元', '通胀', '失业', 'gdp', '增长',
        '股票', '股息', '信贷', '债务', '出口', '进口',
        '工业', '贸易', '就业', '工资', '税收', '上证',
    ],
    'technology': [
        '科技', '人工智能', '软件', '网络攻击', '数字',
        '机器人', '应用', '智能手机', '互联网', '计算机', '数据',
        '网络安全', '算法', '平台', '社交媒体', '创业',
        '谷歌', '苹果', '微软', '亚马逊', '腾讯', '阿里巴巴', '华为', '特斯拉',
    ],
    'science': [
        '科学', '研究', '发现', '物种', '基因', '气候',
        '地震', '火山', '行星', '太空', '宇宙', '物理',
        '化学', '生物', '实验室', '研究', '科学家', 'nasa',
        '化石', '进化', '生物多样性', '海洋',
    ],
    'health': [
        '医院', '医生', '医学', '疫苗', '疫情', '健康', '疾病',
        '治疗', '病毒', '诊所', '患者', '手术', '疗法', '症状',
        '诊断', '制药', '营养', '健身', '新冠',
        '癌症', '糖尿病', '心脏', '大脑',
    ],
    'sports': [
        '足球', '联赛', '冠军杯', '世界杯', '奥运会', '体育',
        '球队', '球员', '比赛', '进球', '网球', '篮球', '乒乓',
        '教练', '体育场', '锦标赛', '裁判',
        '中超', 'nba', 'cba', '英超',
    ],
    'us': [
        '美国', '佛罗里达', '德克萨斯', '加利福尼亚',
        '纽约', '迈阿密', '洛杉矶', '芝加哥', '华盛顿', '特朗普', '拜登',
        '白宫', '国会', '参议院', 'fbi', 'cia', '五角大楼',
    ],
    'world': [
        '乌克兰', '俄罗斯', '中国', '伊朗', '以色列', '加沙', '中东', '欧洲',
        '亚洲', '非洲', '拉丁美洲', '战争', '外交', '移民',
        '难民', '国际', '联合国', '北约', '冲突', '危机',
        '军事', '军队', '和平', '协议', '条约', '制裁',
    ],
    'entertainment': [
        '电影', '影院', '演员', '女演员', '奥斯卡', '明星',
        '音乐', '专辑', '演唱会', '巡演', '网飞', '流媒体', '票房',
        '戏剧', '电视剧', '季', '季终',
        '歌手', '乐队', '声破天',
        '迪士尼', '好莱坞', '奖', '红毯',
        '喜剧', '恐怖',
        '游戏', '电竞', '油管', '抖音',
        '网红', '爆款', '播客', '畅销书', '书',
        '电视', '节目',
    ],
}

STOP_WORDS = {
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
    '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好',
    '自己', '这', '他', '她', '它', '们', '那', '些', '什么', '谁', '怎么', '为什么',
    '把', '被', '让', '给', '从', '向', '对', '为', '以', '因为', '所以', '但是',
    '与', '或', '而', '如果', '虽然', '可是',
}

SOURCE_ATTRIBUTION = r'\s*(新华社|人民日报|央视新闻|BBC中文|南华早报|联合早报|DW中文|法国国际广播电台|端传媒|澎湃新闻)\s*$'

GENERIC_TEXT = [
    '全面新闻报道',
    '聚合自',
    '点击此处了解更多',
]

CATEGORY_NAMES = OrderedDict([
    ('all', '全部'),
    ('most_covered', '最受关注'),
    ('world', '国际'),
    ('us', '美国'),
    ('politics', '政治'),
    ('business', '商业'),
    ('technology', '科技'),
    ('science', '科学'),
    ('health', '健康'),
    ('sports', '体育'),
    ('entertainment', '娱乐'),
])

UI_STRINGS = {
    'subtitle': '选择你的立场 | 通讯社和其他信息源 | 过去24小时',
    'how_it_works': '工作原理',
    'privacy_text': '我们尊重您的隐私。本网站使用情境广告（无追踪Cookie）并根据合理使用原则显示标题/摘要。',
    'privacy_link': '隐私政策',
    'got_it': '知道了',
    'sources': '来源：',
    'center_default': '中立来源（默认）',
    'all_sources': '所有来源',
    'center_only': '仅中立',
    'left_center_only': '仅中左',
    'left_only': '仅左派',
    'right_only': '仅右派',
    'clear_all': '清除全部',
    'sources_suffix': '个来源',
    'covered_by_2': '被2个或更多来源报道的新闻',
    'paywall_title': '付费网站',
    'sources_label': '个来源',
    'read_full': '阅读完整文章',
    'find_coverage': '查找报道',
    'search_related': '搜索相关报道',
    'bias_rating': '立场评级',
    'ago': '前',
    'show_stories': '显示',
    'stories': '条',
    'no_stories': '此分类暂无新闻',
    'footer_copy': '新闻内容版权归各出版商所有。标题和摘要根据合理使用原则提供，仅供参考。',
    'footer_sources': '来源：',
    'footer_and': '和',
    'footer_terms': '条款',
    'footer_privacy': '隐私',
    'footer_about': '关于',
}

PAYWALLED_SOURCES = {
    '南华早报',
}
