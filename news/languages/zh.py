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
    
    # Category-specific feeds
    # Sports
    ('新浪体育', 'https://sports.sina.com.cn/rss/all.xml'),
    ('腾讯体育', 'https://sports.qq.com/rss/allsports.xml'),
    ('网易体育', 'https://sports.163.com/rss/'),
    ('搜狐体育', 'https://sports.sohu.com/rss/'),
    ('南华早报体育', 'https://www.scmp.com/rss/3/feed'),
    ('联合早报体育', 'https://www.zaobao.com.sg/zht/sports/rss.xml'),
    
    # Business
    ('新浪财经', 'https://finance.sina.com.cn/rss/roll.xml'),
    ('腾讯财经', 'https://finance.qq.com/rss/qq_stock.xml'),
    ('网易财经', 'https://money.163.com/rss/'),
    ('财新', 'https://www.caixin.com/rss.xml'),
    ('南华早报商业', 'https://www.scmp.com/rss/2/feed'),
    ('联合早报财经', 'https://www.zaobao.com.sg/zht/finance/rss.xml'),
    
    # Technology
    ('腾讯科技', 'https://tech.qq.com/rss/qq_tech.xml'),
    ('新浪科技', 'https://tech.sina.com.cn/rss/roll.xml'),
    ('网易科技', 'https://tech.163.com/rss/'),
    ('搜狐科技', 'https://it.sohu.com/rss/'),
    ('36氪', 'https://36kr.com/feed'),
    ('虎嗅', 'https://www.huxiu.com/rss/0.xml'),
    
    # World News
    ('BBC中文国际', 'https://feeds.bbci.co.uk/zhongwen/simp/rss.xml'),
    ('DW中文国际', 'https://rss.dw.com/xml/rss-zh-all'),
    ('端传媒国际', 'https://theinitium.com/rss/'),
    ('联合早报国际', 'https://www.zaobao.com.sg/zht/world/rss.xml'),
    
    # Science
    ('腾讯科技科学', 'https://tech.qq.com/rss/science.xml'),
    ('新浪科技科学', 'https://tech.sina.com.cn/rss/science.xml'),
    ('果壳', 'https://www.guokr.com/rss/'),
    ('科学网', 'https://www.sciencenet.cn/xml/news.aspx'),
    
    # Health
    ('腾讯健康', 'https://health.qq.com/rss/'),
    ('新浪健康', 'https://health.sina.com.cn/rss/'),
    ('39健康网', 'https://www.39.net/rss/'),
    
    # Entertainment
    ('腾讯娱乐', 'https://ent.qq.com/rss/qq_ent.xml'),
    ('新浪娱乐', 'https://ent.sina.com.cn/rss/'),
    ('网易娱乐', 'https://ent.163.com/rss/'),
    ('搜狐娱乐', 'https://yule.sohu.com/rss/'),
    
    # Politics
    ('BBC中文政治', 'https://feeds.bbci.co.uk/zhongwen/trad/rss.xml'),
    ('DW中文政治', 'https://rss.dw.com/xml/rss-zh-all'),
    ('端传媒时政', 'https://theinitium.com/rss/'),
    ('澎湃新闻政治', 'https://www.thepaper.cn/rss.jsp'),
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
    
    # Category-specific sources
    '新浪体育': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '腾讯体育': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '网易体育': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '搜狐体育': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '南华早报体育': ('Center', '#666', 'https://mediabiasfactcheck.com/south-china-morning-post/'),
    '联合早报体育': ('Center', '#666', 'https://mediabiasfactcheck.com/zaobao/'),
    '新浪财经': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '腾讯财经': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '网易财经': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '财新': ('Center', '#666', 'https://mediabiasfactcheck.com/caixin/'),
    '南华早报商业': ('Center', '#666', 'https://mediabiasfactcheck.com/south-china-morning-post/'),
    '联合早报财经': ('Center', '#666', 'https://mediabiasfactcheck.com/zaobao/'),
    '腾讯科技': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '新浪科技': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '网易科技': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '搜狐科技': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '36氪': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '虎嗅': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'BBC中文国际': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'DW中文国际': ('Center', '#666', 'https://mediabiasfactcheck.com/deutsche-welle/'),
    '端传媒国际': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/the-initium/'),
    '联合早报国际': ('Center', '#666', 'https://mediabiasfactcheck.com/zaobao/'),
    '腾讯科技科学': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '新浪科技科学': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '果壳': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '科学网': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '腾讯健康': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '新浪健康': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '39健康网': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '腾讯娱乐': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '新浪娱乐': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '网易娱乐': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    '搜狐娱乐': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'BBC中文政治': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'DW中文政治': ('Center', '#666', 'https://mediabiasfactcheck.com/deutsche-welle/'),
    '端传媒时政': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/the-initium/'),
    '澎湃新闻政治': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
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
    
    # Category-specific sources
    ('新浪体育', 'Center'),
    ('腾讯体育', 'Center'),
    ('网易体育', 'Center'),
    ('搜狐体育', 'Center'),
    ('南华早报体育', 'Center'),
    ('联合早报体育', 'Center'),
    ('新浪财经', 'Center'),
    ('腾讯财经', 'Center'),
    ('网易财经', 'Center'),
    ('财新', 'Center'),
    ('南华早报商业', 'Center'),
    ('联合早报财经', 'Center'),
    ('腾讯科技', 'Center'),
    ('新浪科技', 'Center'),
    ('网易科技', 'Center'),
    ('搜狐科技', 'Center'),
    ('36氪', 'Center'),
    ('虎嗅', 'Center'),
    ('BBC中文国际', 'Left-Center'),
    ('DW中文国际', 'Center'),
    ('端传媒国际', 'Left-Center'),
    ('联合早报国际', 'Center'),
    ('腾讯科技科学', 'Center'),
    ('新浪科技科学', 'Center'),
    ('果壳', 'Center'),
    ('科学网', 'Center'),
    ('腾讯健康', 'Center'),
    ('新浪健康', 'Center'),
    ('39健康网', 'Center'),
    ('腾讯娱乐', 'Center'),
    ('新浪娱乐', 'Center'),
    ('网易娱乐', 'Center'),
    ('搜狐娱乐', 'Center'),
    ('BBC中文政治', 'Left-Center'),
    ('DW中文政治', 'Center'),
    ('端传媒时政', 'Left-Center'),
    ('澎湃新闻政治', 'Center'),
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
    'china': [
        '中国', '北京', '上海', '广州', '深圳', '国家主席', '国务院', '全国人大', '政协', '共产党',
        '香港', '澳门', '台湾', '台北', '高雄', '民进党', '国民党',
        '亚洲', '日本', '韩国', '印度', '东南亚', '东盟', '亚太',
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
    ('china', '中国'),
    ('politics', '政治'),
    ('business', '商业'),
    ('technology', '科技'),
    ('science', '科学'),
    ('health', '健康'),
    ('sports', '体育'),
    ('entertainment', '娱乐'),
])

CATEGORY_KEYWORDS_WEIGHTED = {
    'politics': {
        'high': ['习近平', '李强', '国务院', '全国人大', '政协', '政治局', '共产党'],
        'medium': ['政府', '主席', '总理', '部长', '选举', '投票', '竞选', '人大', '法律', '改革', '党', '反对派', '政治'],
        'low': []
    },
    'business': {
        'high': ['上证', '股市', '人民币', '美元', '股票', '股息', '通胀'],
        'medium': ['经济', '市场', '企业', '银行', '金融', '投资', '失业', 'gdp', '增长', '信贷', '债务', '出口', '进口', '工业', '贸易', '就业', '工资', '税收'],
        'low': []
    },
    'technology': {
        'high': ['人工智能', '网络攻击', '网络安全', '算法', '腾讯', '阿里巴巴', '华为'],
        'medium': ['科技', '软件', '数字', '机器人', '应用', '智能手机', '互联网', '计算机', '数据', '平台', '社交媒体', '创业', '谷歌', '苹果', '微软', '亚马逊', '特斯拉'],
        'low': []
    },
    'science': {
        'high': ['nasa', '基因', '进化', '生物多样性'],
        'medium': ['科学', '研究', '发现', '物种', '气候', '地震', '火山', '行星', '太空', '宇宙', '物理', '化学', '生物', '实验室', '科学家', '化石', '海洋'],
        'low': []
    },
    'health': {
        'high': ['医院', '医生', '医学', '疫苗', '疫情', '新冠', '癌症', '糖尿病'],
        'medium': ['健康', '疾病', '治疗', '病毒', '诊所', '患者', '手术', '疗法', '症状', '诊断', '制药', '营养', '健身', '心脏', '大脑'],
        'low': []
    },
    'sports': {
        'high': ['中超', '国足', '英超', 'nba', 'cba'],
        'medium': ['足球', '联赛', '冠军杯', '世界杯', '奥运会', '体育', '球队', '球员', '比赛', '进球', '网球', '篮球', '乒乓', '教练', '体育场', '锦标赛', '裁判'],
        'low': []
    },
    'china': {
        'high': ['中国', '北京', '上海', '广州', '深圳', '国家主席', '国务院', '全国人大', '政协'],
        'medium': ['共产党', '香港', '澳门', '台湾', '台北', '高雄', '民进党', '国民党', '亚洲', '日本', '韩国', '印度', '东南亚', '东盟', '亚太'],
        'low': []
    },
    'world': {
        'high': ['乌克兰', '俄罗斯', '战争', '危机', '加沙', '以色列', '普京'],
        'medium': ['中国', '伊朗', '以色列', '加沙', '中东', '欧洲', '亚洲', '非洲', '拉丁美洲', '外交', '移民', '难民', '国际', '联合国', '北约', '冲突', '军事', '军队', '和平', '协议', '条约', '制裁'],
        'low': []
    },
    'entertainment': {
        'high': ['奥斯卡', '网飞', '迪士尼', '好莱坞', '声破天'],
        'medium': ['电影', '影院', '演员', '女演员', '明星', '音乐', '专辑', '演唱会', '巡演', '流媒体', '票房', '戏剧', '电视剧', '季', '季终', '歌手', '乐队', '奖', '红毯', '喜剧', '恐怖', '游戏', '电竞', '油管', '抖音', '网红', '爆款', '播客', '畅销书', '书', '电视', '节目'],
        'low': []
    },
}

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
    # Header translations
    'logo_tagline': '多角度新闻',
    'search_placeholder': '搜索新闻...',
    'toggle_theme': '切换主题',
    'filter_label': '筛选：',
    # Bias filter buttons
    'filter_all': '全部',
    'filter_left': '左派',
    'filter_left_center': '中左',
    'filter_center': '中间',
    'filter_right_center': '中右',
    'filter_right': '右派',
    # Story card buttons
    'find_coverage_btn': '查找报道',
    'different_angle_btn': '另一角度',
    'share_btn': '分享',
    'different_perspectives': '不同视角',
    # Different Angle modal
    'different_angle_title': '换个角度看',
    'original_label': '原文：',
    'loading_related': '正在加载相关报道...',
    'no_related_stories': '未找到相关报道',
    'error_loading': '加载错误',
    # Share modal
    'share_story_title': '分享文章',
    'share_on_x': '分享到X',
    'share_facebook': '分享到Facebook',
    'share_linkedin': '分享到LinkedIn',
    'copy_link': '复制链接',
    'copied': '已复制！',
    'close': '关闭',
}

PAYWALLED_SOURCES = {
    '南华早报',
}
