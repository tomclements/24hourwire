from collections import OrderedDict

CODE = 'ko'
NAME = '한국어'

FEEDS = [
    ('연합뉴스', 'https://news.google.com/rss/search?q=site:yna.co.kr&hl=ko&gl=KR&ceid=KR:ko'),
    ('KBS', 'https://news.google.com/rss/search?q=site:kbs.co.kr&hl=ko&gl=KR&ceid=KR:ko'),
    ('MBC', 'https://news.google.com/rss/search?q=site:imbc.com&hl=ko&gl=KR&ceid=KR:ko'),
    ('SBS', 'https://news.google.com/rss/search?q=site:sbs.co.kr&hl=ko&gl=KR&ceid=KR:ko'),
    ('조선일보', 'https://news.google.com/rss/search?q=site:chosun.com&hl=ko&gl=KR&ceid=KR:ko'),
    ('중앙일보', 'https://news.google.com/rss/search?q=site:joongang.co.kr&hl=ko&gl=KR&ceid=KR:ko'),
    ('동아일보', 'https://news.google.com/rss/search?q=site:donga.com&hl=ko&gl=KR&ceid=KR:ko'),
    ('한겨레', 'https://news.google.com/rss/search?q=site:hani.co.kr&hl=ko&gl=KR&ceid=KR:ko'),
    ('경향신문', 'https://news.google.com/rss/search?q=site:khan.co.kr&hl=ko&gl=KR&ceid=KR:ko'),
    ('BBC 한국어', 'https://news.google.com/rss/search?q=site:bbc.com/korean&hl=ko&gl=KR&ceid=KR:ko'),
]

SOURCE_INFO = {
    '연합뉴스': ('Center', '#666', 'https://mediabiasfactcheck.com/yonhap-news-agency/'),
    'KBS': ('Center', '#666', 'https://mediabiasfactcheck.com/kbs/'),
    'MBC': ('Center', '#666', 'https://mediabiasfactcheck.com/mbc/'),
    'SBS': ('Center', '#666', 'https://mediabiasfactcheck.com/sbs/'),
    '조선일보': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/chosun-ilbo/'),
    '중앙일보': ('Center', '#666', 'https://mediabiasfactcheck.com/joongang-ilbo/'),
    '동아일보': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/donga-ilbo/'),
    '한겨레': ('Left', '#999', 'https://mediabiasfactcheck.com/hankyoreh/'),
    '경향신문': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/kyunghyang-shinmun/'),
    'BBC 한국어': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
}

DEFAULT_SOURCES = ['연합뉴스', 'KBS', '중앙일보', '한겨레', 'BBC 한국어', '경향신문']

SOURCES = [
    ('연합뉴스', 'Center'),
    ('KBS', 'Center'),
    ('MBC', 'Center'),
    ('SBS', 'Center'),
    ('중앙일보', 'Center'),
    ('한겨레', 'Left'),
    ('경향신문', 'Left-Center'),
    ('BBC 한국어', 'Left-Center'),
    ('조선일보', 'Right-Center'),
    ('동아일보', 'Right-Center'),
]

CATEGORY_KEYWORDS = {
    'politics': [
        '정부', '대통령', '총리', '장관', '선거', '투표', '캠페인',
        '국회', '상원', '하원', '법률', '개혁', '정당',
        '국민의힘', '더불어민주당', '대통령실', '야당', '여당', '정치',
    ],
    'business': [
        '주식', '경제', '시장', '기업', '은행', '금융',
        '투자', '원화', '달러', '인플레이션', '실업', 'gdp', '성장',
        '주식', '배당', '신용', '부채', '수출', '수입',
        '산업', '무역', '고용', '급여', '세금', '코스피',
    ],
    'technology': [
        '기술', '인공지능', '소프트웨어', '사이버공격', '디지털',
        '로봇', '앱', '스마트폰', '인터넷', '컴퓨터', '데이터',
        '사이버보안', '알고리즘', '플랫폼', 'sns', '스타트업',
        '삼성', 'lg', 'sk', '네이버', '카카오', '구글', '애플', '현대',
    ],
    'science': [
        '과학', '연구', '발견', '종', '유전학', '기후',
        '지진', '화산', '행성', '우주', '물리학',
        '화학', '생물학', '연구소', '과학자', 'nasa',
        '화석', '진화', '생물다양성', '해양',
    ],
    'health': [
        '병원', '의사', '의학', '백신', '팬데믹', '건강', '질병',
        '치료', '바이러스', '의원', '환자', '수술', '요법', '증상',
        '진단', '제약', '영양', '운동', '코로나',
        '암', '당뇨', '심장', '뇌',
    ],
    'sports': [
        '축구', '리그', '챔피언스', '컵', '월드컵', '올림픽', '스포츠',
        '팀', '선수', '경기', '골', '테니스', '농구', '야구',
        '감독', '경기장', '대회', '심판',
        'k리그', '프로야구', '삼성', 'lg', '두산',
    ],
    'us': [
        '미국', '플로리다', '텍사스', '캘리포니아',
        '뉴욕', '마이애미', '로스앤젤레스', '시카고', '워싱턴', '트럼프', '바이든',
        '백악관', '의회', '상원', 'fbi', 'cia', '펜타곤',
    ],
    'world': [
        '우크라이나', '러시아', '중국', '이란', '이스라엘', '가자', '중동', '유럽',
        '아시아', '아프리카', '중남미', '전쟁', '외교', '이민',
        '난민', '세계', '국제', '유엔', '나토', '분쟁', '위기',
        '군사', '군', '평화', '합의', '조약', '제재', '북한', '한반도',
    ],
    'entertainment': [
        '영화', '배우', '여배우', '아카데미', '연예인',
        '음악', '앨범', '콘서트', '투어', '넷플릭스', '스트리밍', '흥행',
        '연극', '드라마', '시즌', '시즌 피날레',
        '가수', '밴드', '스포티파이', 'k팝', 'bts', '블랙핑크',
        '디즈니', '할리우드', '시상식', '레드카펫',
        '코미디', '공포',
        '게임', 'e스포츠', '유튜브', '틱톡',
        '인플루언서', '바이럴', '팟캐스트', '베스트셀러', '책',
        '텔레비전', '프로그램',
    ],
}

STOP_WORDS = {
    '의', '에', '는', '을', '를', '이', '가', '에서', '와', '과', '로', '으로',
    '도', '만', '부터', '까지', '한테', '에게', '보다', '처럼',
    '이다', '입니다', '했다', '합니다', '된다', '됩니다', '있는', '없는',
    '이것', '그것', '저것', '이런', '그런', '저런',
    '그', '저', '이', '그녀', '그들', '우리', '너희',
    '여기', '거기', '저기',
    '무엇', '누구', '언제', '어디', '왜', '어떻게',
    '새로운', '말했다', '밝혔다', '전했다',
}

SOURCE_ATTRIBUTION = r'\s*(연합뉴스|KBS|MBC|SBS|조선일보|중앙일보|동아일보|한겨레|경향신문|BBC)\s*$'

GENERIC_TEXT = [
    '종합 뉴스 보도',
    '에서 수집',
    '자세한 내용은 여기를 클릭',
]

CATEGORY_NAMES = OrderedDict([
    ('all', '전체'),
    ('most_covered', '가장 많이 보도'),
    ('world', '세계'),
    ('us', '미국'),
    ('politics', '정치'),
    ('business', '경제'),
    ('technology', '기술'),
    ('science', '과학'),
    ('health', '건강'),
    ('sports', '스포츠'),
    ('entertainment', '연예'),
])

UI_STRINGS = {
    'subtitle': '편향 선택 | 통신사 및 기타 피드 | 지난 24시간',
    'how_it_works': '작동 방식',
    'privacy_text': '귀하의 개인정보를 존중합니다. 이 사이트는 맥락 광고(추적 쿠키 없이)를 사용하고 공정 사용에 따라 헤드라인/요약을 표시합니다.',
    'privacy_link': '개인정보 처리방침',
    'got_it': '확인',
    'sources': '출처:',
    'center_default': '중립 출처 (기본)',
    'all_sources': '모든 출처',
    'center_only': '중립만',
    'left_center_only': '중도좌파만',
    'left_only': '좌파만',
    'right_only': '우파만',
    'clear_all': '모두 지우기',
    'sources_suffix': '출처',
    'covered_by_2': '2개 이상의 출처에서 보도된 뉴스',
    'paywall_title': '유료 사이트',
    'sources_label': '출처',
    'read_full': '전체 기사 읽기',
    'find_coverage': '보도 찾기',
    'search_related': '관련 보도 검색',
    'bias_rating': '편향 평가',
    'ago': '전',
    'show_stories': '표시',
    'stories': '건',
    'no_stories': '이 카테고리에 뉴스가 없습니다',
    'footer_copy': '뉴스 콘텐츠 © 해당 출판사. 헤드라인과 요약은 정보 제공 목적으로 공정 사용에 따라 사용됩니다.',
    'footer_sources': '출처:',
    'footer_and': '및',
    'footer_terms': '이용약관',
    'footer_privacy': '개인정보',
    'footer_about': '소개',
}

PAYWALLED_SOURCES = {
    '조선일보',
    '중앙일보',
    '동아일보',
}
