"""
Test cases for story categorization system - Updated with Regional Categories

Run with: python manage.py test_categories

This file contains test cases for all 13 supported languages to verify
the regional categorization system works correctly.

Test Format: (title, expected_categories, notes)
"""

# ============================================================================
# ENGLISH TEST CASES (en)
# ============================================================================
TEST_CASES_EN = [
    # Regional Categories - United States
    ("Biden signs executive order on climate change", ["united-states", "politics"], "White House action"),
    ("Supreme Court rules on voting rights case", ["united-states", "politics"], "US Supreme Court"),
    ("FBI investigates cyberattack on government servers", ["united-states", "technology"], "FBI + tech"),
    ("Congress passes infrastructure bill", ["united-states", "politics"], "US Congress"),
    
    # Regional Categories - United Kingdom
    ("UK Parliament debates Brexit trade deal", ["united-kingdom", "politics"], "UK Parliament"),
    ("Downing Street announces new policy", ["united-kingdom", "politics"], "UK government"),
    ("London mayor proposes transport changes", ["united-kingdom"], "UK/London"),
    
    # Regional Categories - Europe
    ("European Union imposes new sanctions on Russia", ["europe", "world"], "EU action"),
    ("Macron meets with EU leaders in Brussels", ["europe", "politics"], "France/EU politics"),
    ("Bundestag debates climate policy in Berlin", ["europe"], "Germany/Europe"),
    ("European Parliament votes on directive", ["europe", "politics"], "EU Parliament"),
    
    # Regional Categories - Asia-Pacific
    ("China announces new economic policy", ["asia-pacific", "business"], "Asia-Pacific region"),
    ("Xi Jinping visits Japan", ["asia-pacific", "politics"], "China/Japan"),
    ("India launches new space mission", ["asia-pacific", "science"], "India space"),
    
    # Topic Categories
    ("OpenAI releases new GPT model", ["technology"], "AI/tech"),
    ("Tesla announces self-driving car update", ["technology"], "Autonomous vehicles"),
    ("NASA discovers water on Mars", ["science"], "Space"),
    ("FDA approves new cancer treatment drug", ["health"], "Medical approval"),
    ("NBA playoffs: Lakers advance to finals", ["sports"], "Basketball"),
    ("Taylor Swift announces world tour dates", ["entertainment"], "Music"),
    ("Stock market reaches record high", ["business"], "Finance"),
    ("Trade war escalates between US and China", ["business", "world"], "Trade + geopolitics"),
    
    # World News
    ("Earthquake strikes Japan, tsunami warning issued", ["world"], "Natural disaster"),
    ("UN condemns violence in Middle East", ["world"], "UN action"),
    ("Ukraine and Russia agree to ceasefire", ["world"], "International conflict"),
]

# ============================================================================
# SPANISH TEST CASES (es)
# ============================================================================
TEST_CASES_ES = [
    # Regional Categories - España
    ("El Congreso aprueba nueva ley en España", ["espana", "politics"], "Spanish politics"),
    ("Pedro Sánchez se reúne con líderes europeos", ["espana", "europa", "politics"], "Spain/EU politics"),
    ("El gobierno español anuncia reformas", ["espana", "politics"], "Spanish government"),
    ("Cataluña debate autonomía", ["espana", "politics"], "Catalonia/Spain"),
    
    # Regional Categories - México
    ("AMLO anuncia reforma energética en México", ["mexico", "politics"], "Mexico politics"),
    ("El Congreso mexicano debate presupuesto", ["mexico", "business"], "Mexico congress"),
    ("Cámara de Diputados aprueba ley", ["mexico", "politics"], "Mexico parliament"),
    ("Ciudad de México inaugura metro", ["mexico"], "Mexico City"),
    
    # Regional Categories - Latinoamérica
    ("Milei implementa ajuste económico en Argentina", ["latinoamerica", "business"], "Argentina/LatAm"),
    ("Lula promete inversiones en Brasil", ["latinoamerica", "politics"], "Brazil/LatAm politics"),
    ("Colombia y Perú firman acuerdo", ["latinoamerica", "politics"], "Colombia/Peru"),
    ("Buenos Aires y Santiago acuerdan cooperación", ["latinoamerica", "politics"], "Argentina/Chile"),
    ("Chile aprueba nueva constitución", ["latinoamerica", "politics"], "Chile politics"),
    
    # Regional Categories - Europa
    ("Bruselas sanciona a Rusia por guerra", ["europa", "world"], "EU action"),
    ("Parlamento Europeo vota directiva", ["europa", "politics"], "EU parliament"),
    
    # Topic Categories
    ("Real Madrid gana la Champions League", ["sports"], "Football"),
    ("Nueva vacuna contra el COVID-19", ["health"], "Health"),
    ("Inteligencia artificial revoluciona industria", ["technology"], "Technology"),
    ("Bolsa de Madrid sube un 2%", ["business"], "Business"),
    ("Terremoto en Chile genera alerta", ["world"], "Natural disaster"),
]

# ============================================================================
# GERMAN TEST CASES (de)
# ============================================================================
TEST_CASES_DE = [
    # Regional Categories - Deutschland
    ("Bundestag debattiert Klimapolitik", ["deutschland", "politics"], "German politics"),
    ("Scholz trifft Macron in Paris", ["deutschland", "europa", "politics"], "Germany/EU politics"),
    ("SPD und CDU verhandeln Koalition", ["deutschland", "politics"], "German parties"),
    ("Berlin erhöht Budget für Verkehr", ["deutschland", "business"], "Berlin/Germany"),
    ("Bayern debattiert Bildungspolitik", ["deutschland"], "Bavaria/Germany"),
    
    # Regional Categories - Österreich
    ("Wien erhöht Budget für Verkehr", ["osterreich", "business"], "Austria"),
    ("Österreich öffnet Grenzen", ["osterreich", "europa"], "Austria/Europe"),
    ("Bundeskanzler besucht Deutschland", ["osterreich", "europa"], "Austria chancellor"),
    
    # Regional Categories - Schweiz
    ("Schweizer Bank meldet Gewinn", ["schweiz", "business"], "Switzerland business"),
    ("Bundesrat entscheidet über Reform", ["schweiz", "politics"], "Swiss politics"),
    ("Zürich eröffnet neue Tramlinie", ["schweiz"], "Zurich/Switzerland"),
    
    # Regional Categories - Europa
    ("EU-Kommission verhängt Sanktionen", ["europa", "world"], "EU action"),
    ("Europäisches Parlament stimmt ab", ["europa", "politics"], "EU parliament"),
    ("Frankreich und Deutschland einigen sich", ["europa", "politics"], "France/Germany/EU"),
    
    # Topic Categories
    ("Bayern München gewinnt Bundesliga", ["sports"], "Football"),
    ("DAX erreicht Rekordstand", ["business"], "Stock market"),
    ("Deutsche Bahn streikt wieder", ["deutschland", "business"], "Germany transport"),
]

# ============================================================================
# FRENCH TEST CASES (fr)
# ============================================================================
TEST_CASES_FR = [
    # Regional Categories - France
    ("Macron annonce réforme des retraites", ["france", "politics"], "France politics"),
    ("Assemblée nationale vote loi", ["france", "politics"], "French parliament"),
    ("Paris accueille sommet climat", ["france", "science"], "France/Climate"),
    ("Marseille inaugure nouveau stade", ["france"], "Marseille/France"),
    
    # Regional Categories - Belgique
    ("Bruxelles impose sanctions à la Russie", ["belgique", "europe", "world"], "Belgium/EU"),
    ("Commission européenne décide", ["belgique", "europe", "politics"], "EU Commission"),
    
    # Regional Categories - Suisse
    ("La Suisse ouvre frontières", ["suisse", "europe"], "Switzerland"),
    ("Genève accueille conférence", ["suisse", "world"], "Geneva"),
    
    # Regional Categories - Europe
    ("Union européenne élargit sanctions", ["europe", "world"], "EU action"),
    
    # Topic Categories
    ("PSG remporte Ligue des Champions", ["sports"], "Football"),
    ("Tour de France commence à Nice", ["france", "sports"], "Cycling"),
    ("Bourse de Paris en hausse", ["business"], "Stock market"),
]

# ============================================================================
# OTHER LANGUAGES TEST CASES (Abbreviated)
# ============================================================================
TEST_CASES_IT = [
    # Italy
    ("Meloni incontra leader UE a Roma", ["italia", "europa", "politics"], "Italy/EU politics"),
    ("Parlamento europeo vota nuove leggi", ["europe", "politics"], "EU politics"),
    ("Juventus vince campionato italiano", ["italia", "sports"], "Italy sports"),
]

TEST_CASES_PT = [
    # Portuguese
    ("Lula anuncia programa social no Brasil", ["brasil", "politics"], "Brazil politics"),
    ("Governo português aprova orçamento", ["portugal", "politics"], "Portugal politics"),
    ("Flamengo conquista título brasileiro", ["brasil", "sports"], "Brazil sports"),
]

TEST_CASES_JA = [
    # Japanese
    ("日本政府、新しい経済政策を発表", ["japan", "business"], "Japan government"),
    ("中国と日本、貿易協定に署名", ["japan", "asia", "business"], "Japan/Asia"),
    ("東京五輪、2024年に開催", ["japan", "sports"], "Japan Olympics"),
]

TEST_CASES_KO = [
    # Korean
    ("대통령실, 새 정책 발표", ["korea", "politics"], "Korea politics"),
    ("한국과 일본, 무역 협정 체결", ["korea", "asia", "business"], "Korea/Asia"),
    ("삼성전자, 신제품 출시", ["korea", "technology"], "Korea tech"),
]

TEST_CASES_ZH = [
    # Chinese
    ("中国政府宣布新的经济政策", ["china", "business"], "China policy"),
    ("香港实施新法律", ["hongkong", "politics"], "Hong Kong"),
    ("台湾科技公司发布新产品", ["taiwan", "technology"], "Taiwan tech"),
]

TEST_CASES_RU = [
    # Russian
    ("Путин выступил с посланием к Федеральному собранию", ["russia", "politics"], "Russia politics"),
    ("Евросоюз ввел новые санкции", ["europe", "world"], "EU action"),
    ("Беларусь и Россия подписали соглашение", ["russia", "cis", "politics"], "CIS politics"),
]

TEST_CASES_AR = [
    # Arabic
    ("السعودية تعلن عن رؤية 2030 جديدة", ["gulf", "business"], "Saudi Arabia/Gulf"),
    ("مصر توقع اتفاقية مع الاتحاد الأوروبي", ["egypt", "world"], "Egypt"),
    ("لبنان يواجه أزمة اقتصادية", ["levant", "business"], "Lebanon/Levant"),
    ("المغرب يستضيف قمة عربية", ["maghreb", "politics"], "Morocco/Maghreb"),
]

TEST_CASES_HI = [
    # Hindi
    ("भारत सरकार ने नई नीति की घोषणा की", ["india", "politics"], "India government"),
    ("संसद में कृषि कानून पर बहस", ["india", "politics"], "India parliament"),
    ("पाकिस्तान के साथ व्यापार वार्ता", ["india", "south-asia", "business"], "South Asia"),
]

TEST_CASES_TR = [
    # Turkish
    ("Erdoğan yeni ekonomi paketini açıkladı", ["turkey", "business"], "Turkey economy"),
    ("Türkiye ve Yunanistan anlaşma imzaladı", ["turkey", "balkans", "politics"], "Turkey/Balkans"),
    ("İstanbul'da seçim sonuçları belli oldu", ["turkey", "politics"], "Istanbul/Turkey"),
]

# ============================================================================
# MASTER TEST CASES LIST (for backward compatibility)
# ============================================================================
# Default to English test cases
TEST_CASES = TEST_CASES_EN

# Map of all test cases by language
LANGUAGE_TEST_CASES = {
    'en': TEST_CASES_EN,
    'es': TEST_CASES_ES,
    'de': TEST_CASES_DE,
    'fr': TEST_CASES_FR,
    'it': TEST_CASES_IT,
    'pt': TEST_CASES_PT,
    'ja': TEST_CASES_JA,
    'ko': TEST_CASES_KO,
    'zh': TEST_CASES_ZH,
    'ru': TEST_CASES_RU,
    'ar': TEST_CASES_AR,
    'hi': TEST_CASES_HI,
    'tr': TEST_CASES_TR,
}

# ============================================================================
# CONFLICTING CATEGORIES (Optional validation)
# ============================================================================
CONFLICTING_CATEGORIES = [
    # Regional conflicts - stories shouldn't be tagged with mutually exclusive regions
    ("united-states", "united-kingdom"),
    ("united-states", "europe"),
    ("espana", "mexico"),
    ("espana", "latinoamerica"),
    ("mexico", "latinoamerica"),
    ("deutschland", "france"),
    ("deutschland", "osterreich"),
    ("china", "japan"),
    ("china", "taiwan"),
]
