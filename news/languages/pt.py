from collections import OrderedDict

CODE = 'pt'
NAME = 'Português'

FEEDS = [
    ('Folha de S.Paulo', 'https://news.google.com/rss/search?q=site:folha.uol.com.br&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('O Globo', 'https://news.google.com/rss/search?q=site:oglobo.globo.com&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Estadão', 'https://news.google.com/rss/search?q=site:estadao.com.br&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('UOL', 'https://news.google.com/rss/search?q=site:uol.com.br&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('G1', 'https://news.google.com/rss/search?q=site:g1.globo.com&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('R7', 'https://news.google.com/rss/search?q=site:r7.com&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('BBC Brasil', 'https://news.google.com/rss/search?q=site:bbc.com/portuguese&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('DW Brasil', 'https://rss.dw.com/xml/rss-pt-all'),
    ('CartaCapital', 'https://news.google.com/rss/search?q=site:cartacapital.com.br&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Exame', 'https://news.google.com/rss/search?q=site:exame.com&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('IstoÉ', 'https://news.google.com/rss/search?q=site:istoe.com.br&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Valor Econômico', 'https://news.google.com/rss/search?q=site:valor.globo.com&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    
    # Category-specific feeds
    # Sports
    ('Globo Esporte', 'https://news.google.com/rss/search?q=site:ge.globo.com&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Lance!', 'https://news.google.com/rss/search?q=site:lance.com.br&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('ESPN Brasil', 'https://news.google.com/rss/search?q=site:espn.com.br&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('UOL Esporte', 'https://news.google.com/rss/search?q=site:uol.com.br/esporte&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Folha Esporte', 'https://news.google.com/rss/search?q=site:folha.uol.com.br/esporte&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Estadão Esporte', 'https://news.google.com/rss/search?q=site:esporte.estadao.com.br&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    
    # Business
    ('Valor Econômico Economia', 'https://news.google.com/rss/search?q=site:valor.globo.com&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Exame Economia', 'https://news.google.com/rss/search?q=site:exame.com/economia&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Estadão Economia', 'https://news.google.com/rss/search?q=site:economia.estadao.com.br&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Folha Economia', 'https://news.google.com/rss/search?q=site:folha.uol.com.br/mercado&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('G1 Economia', 'https://news.google.com/rss/search?q=site:g1.globo.com/economia&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('BBC Brasil Economia', 'https://news.google.com/rss/search?q=site:bbc.com/portuguese&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    
    # Technology
    ('G1 Tecnologia', 'https://news.google.com/rss/search?q=site:g1.globo.com/tecnologia&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('TecMundo', 'https://news.google.com/rss/search?q=site:tecmundo.com.br&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('TechTudo', 'https://news.google.com/rss/search?q=site:techtudo.com.br&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('UOL Tecnologia', 'https://news.google.com/rss/search?q=site:uol.com.br/tilt&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Folha Tecnologia', 'https://news.google.com/rss/search?q=site:folha.uol.com.br/tec&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    
    # World News
    ('BBC Brasil Internacional', 'https://news.google.com/rss/search?q=site:bbc.com/portuguese/internacional&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('G1 Mundo', 'https://news.google.com/rss/search?q=site:g1.globo.com/mundo&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('DW Brasil Internacional', 'https://rss.dw.com/xml/rss-pt-all'),
    ('Folha Mundo', 'https://news.google.com/rss/search?q=site:folha.uol.com.br/mundo&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Estadão Internacional', 'https://news.google.com/rss/search?q=site:internacional.estadao.com.br&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    
    # Science
    ('BBC Brasil Ciência', 'https://news.google.com/rss/search?q=site:bbc.com/portuguese/ciencia&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('G1 Ciência', 'https://news.google.com/rss/search?q=site:g1.globo.com/ciencia-e-saude&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Folha Ciência', 'https://news.google.com/rss/search?q=site:folha.uol.com.br/ciencia&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('UOL Ciência', 'https://news.google.com/rss/search?q=site:uol.com.br/ciencia&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    
    # Health
    ('G1 Saúde', 'https://news.google.com/rss/search?q=site:g1.globo.com/bemestar&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('UOL Saúde', 'https://news.google.com/rss/search?q=site:uol.com.br/vivabem&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Folha Saúde', 'https://news.google.com/rss/search?q=site:folha.uol.com.br/equilibrio&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Estadão Saúde', 'https://news.google.com/rss/search?q=site:saude.estadao.com.br&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    
    # Entertainment
    ('G1 Pop', 'https://news.google.com/rss/search?q=site:g1.globo.com/pop-arte&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('UOL Entretenimento', 'https://news.google.com/rss/search?q=site:uol.com.br/entretenimento&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Folha Ilustrada', 'https://news.google.com/rss/search?q=site:folha.uol.com.br/ilustrada&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Estadão Cultura', 'https://news.google.com/rss/search?q=site:cultura.estadao.com.br&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('O Globo Cultura', 'https://news.google.com/rss/search?q=site:oglobo.globo.com/cultura&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    
    # Politics
    ('G1 Política', 'https://news.google.com/rss/search?q=site:g1.globo.com/politica&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Folha Política', 'https://news.google.com/rss/search?q=site:folha.uol.com.br/poder&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('Estadão Política', 'https://news.google.com/rss/search?q=site:politica.estadao.com.br&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('O Globo Política', 'https://news.google.com/rss/search?q=site:oglobo.globo.com/politica&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('CartaCapital Política', 'https://news.google.com/rss/search?q=site:cartacapital.com.br/politica&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
    ('UOL Política', 'https://news.google.com/rss/search?q=site:uol.com.br/politica&hl=pt-BR&gl=BR&ceid=BR:pt-419'),
]

SOURCE_INFO = {
    'Folha de S.Paulo': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/folha-de-s-paulo/'),
    'O Globo': ('Center', '#666', 'https://mediabiasfactcheck.com/o-globo/'),
    'Estadão': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/estado-de-s-paulo/'),
    'UOL': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'G1': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'R7': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/'),
    'BBC Brasil': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'DW Brasil': ('Center', '#666', 'https://mediabiasfactcheck.com/deutsche-welle/'),
    'CartaCapital': ('Left', '#999', 'https://mediabiasfactcheck.com/'),
    'Exame': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'IstoÉ': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Valor Econômico': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    
    # Category-specific sources
    'Globo Esporte': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Lance!': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'ESPN Brasil': ('Center', '#666', 'https://mediabiasfactcheck.com/espn/'),
    'UOL Esporte': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Folha Esporte': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/folha-de-s-paulo/'),
    'Estadão Esporte': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/estado-de-s-paulo/'),
    'Valor Econômico Economia': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Exame Economia': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Estadão Economia': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/estado-de-s-paulo/'),
    'Folha Economia': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/folha-de-s-paulo/'),
    'G1 Economia': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'BBC Brasil Economia': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'G1 Tecnologia': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'TecMundo': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'TechTudo': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'UOL Tecnologia': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Folha Tecnologia': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/folha-de-s-paulo/'),
    'BBC Brasil Internacional': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'G1 Mundo': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'DW Brasil Internacional': ('Center', '#666', 'https://mediabiasfactcheck.com/deutsche-welle/'),
    'Folha Mundo': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/folha-de-s-paulo/'),
    'Estadão Internacional': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/estado-de-s-paulo/'),
    'BBC Brasil Ciência': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/bbc/'),
    'G1 Ciência': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Folha Ciência': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/folha-de-s-paulo/'),
    'UOL Ciência': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'G1 Saúde': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'UOL Saúde': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Folha Saúde': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/folha-de-s-paulo/'),
    'Estadão Saúde': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/estado-de-s-paulo/'),
    'G1 Pop': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'UOL Entretenimento': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Folha Ilustrada': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/folha-de-s-paulo/'),
    'Estadão Cultura': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/estado-de-s-paulo/'),
    'O Globo Cultura': ('Center', '#666', 'https://mediabiasfactcheck.com/o-globo/'),
    'G1 Política': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
    'Folha Política': ('Left-Center', '#888', 'https://mediabiasfactcheck.com/folha-de-s-paulo/'),
    'Estadão Política': ('Right-Center', '#777', 'https://mediabiasfactcheck.com/estado-de-s-paulo/'),
    'O Globo Política': ('Center', '#666', 'https://mediabiasfactcheck.com/o-globo/'),
    'CartaCapital Política': ('Left', '#999', 'https://mediabiasfactcheck.com/'),
    'UOL Política': ('Center', '#666', 'https://mediabiasfactcheck.com/'),
}

DEFAULT_SOURCES = ['Folha de S.Paulo', 'O Globo', 'G1', 'BBC Brasil', 'DW Brasil', 'Valor Econômico']

SOURCES = [
    ('Folha de S.Paulo', 'Left-Center'),
    ('BBC Brasil', 'Left-Center'),
    ('DW Brasil', 'Center'),
    ('O Globo', 'Center'),
    ('UOL', 'Center'),
    ('G1', 'Center'),
    ('Exame', 'Center'),
    ('IstoÉ', 'Center'),
    ('Valor Econômico', 'Center'),
    ('Estadão', 'Right-Center'),
    ('R7', 'Right-Center'),
    ('CartaCapital', 'Left'),
    
    # Category-specific sources
    ('Globo Esporte', 'Center'),
    ('Lance!', 'Center'),
    ('ESPN Brasil', 'Center'),
    ('UOL Esporte', 'Center'),
    ('Folha Esporte', 'Left-Center'),
    ('Estadão Esporte', 'Right-Center'),
    ('Valor Econômico Economia', 'Center'),
    ('Exame Economia', 'Center'),
    ('Estadão Economia', 'Right-Center'),
    ('Folha Economia', 'Left-Center'),
    ('G1 Economia', 'Center'),
    ('BBC Brasil Economia', 'Left-Center'),
    ('G1 Tecnologia', 'Center'),
    ('TecMundo', 'Center'),
    ('TechTudo', 'Center'),
    ('UOL Tecnologia', 'Center'),
    ('Folha Tecnologia', 'Left-Center'),
    ('BBC Brasil Internacional', 'Left-Center'),
    ('G1 Mundo', 'Center'),
    ('DW Brasil Internacional', 'Center'),
    ('Folha Mundo', 'Left-Center'),
    ('Estadão Internacional', 'Right-Center'),
    ('BBC Brasil Ciência', 'Left-Center'),
    ('G1 Ciência', 'Center'),
    ('Folha Ciência', 'Left-Center'),
    ('UOL Ciência', 'Center'),
    ('G1 Saúde', 'Center'),
    ('UOL Saúde', 'Center'),
    ('Folha Saúde', 'Left-Center'),
    ('Estadão Saúde', 'Right-Center'),
    ('G1 Pop', 'Center'),
    ('UOL Entretenimento', 'Center'),
    ('Folha Ilustrada', 'Left-Center'),
    ('Estadão Cultura', 'Right-Center'),
    ('O Globo Cultura', 'Center'),
    ('G1 Política', 'Center'),
    ('Folha Política', 'Left-Center'),
    ('Estadão Política', 'Right-Center'),
    ('O Globo Política', 'Center'),
    ('CartaCapital Política', 'Left'),
    ('UOL Política', 'Center'),
]

CATEGORY_KEYWORDS = {
    'politics': [
        'governo', 'presidente', 'ministro', 'eleição', 'voto', 'campanha',
        'congresso', 'senado', 'parlamento', 'lei', 'reforma', 'partido',
        'lula', 'bolsonaro', 'planalto', 'câmara', 'deputado', 'senador',
        'stf', 'supremo', 'orçamento', 'política', 'oposição',
    ],
    'business': [
        'bolsa', 'economia', 'mercado', 'empresa', 'banco', 'finanças',
        'investimento', 'real', 'dólar', 'inflação', 'desemprego', 'pib', 'crescimento',
        'ação', 'dividendo', 'crédito', 'dívida', 'exportação', 'importação', 'ibovespa',
        'indústria', 'comércio', 'emprego', 'salário', 'imposto',
    ],
    'technology': [
        'tecnologia', 'inteligência artificial', 'software', 'ataque cibernético', 'digital',
        'robô', 'aplicativo', 'smartphone', 'internet', 'computação', 'dados',
        'cibersegurança', 'algoritmo', 'plataforma', 'redes sociais', 'startup',
        'google', 'apple', 'microsoft', 'amazon', 'meta', 'tesla',
    ],
    'science': [
        'ciência', 'pesquisa', 'descoberta', 'espécie', 'genética', 'clima',
        'terremoto', 'vulcão', 'planeta', 'espaço', 'universo', 'física',
        'química', 'biologia', 'laboratório', 'estudo', 'científico', 'nasa',
        'fóssil', 'evolução', 'biodiversidade', 'oceano',
    ],
    'health': [
        'hospital', 'médico', 'medicina', 'vacina', 'pandemia', 'saúde', 'doença',
        'tratamento', 'vírus', 'clínica', 'paciente', 'cirurgia', 'terapia', 'sintoma',
        'diagnóstico', 'farmacêutico', 'nutrição', 'exercício', 'bem-estar', 'covid',
        'câncer', 'diabetes', 'coração', 'cérebro', 'sus',
    ],
    'sports': [
        'futebol', 'liga', 'champions', 'copa', 'mundial', 'olimpíadas', 'esporte',
        'time', 'jogador', 'jogo', 'gol', 'tênis', 'basquete', 'vôlei',
        'técnico', 'estádio', 'torneio', 'campeonato', 'árbitro',
        'flamengo', 'corinthians', 'palmeiras', 'brasileirão', 'libertadores',
    ],
    'brasil': [
        'brasil', 'governo', 'presidente', 'lula', 'congresso', 'câmara', 'senado',
        'brasília', 'são paulo', 'rio de janeiro', 'pt', 'psdb', 'pmdb', 'pl', 'psol',
        'portugal', 'lisboa', 'porto', 'assembléia', 'republica', 'ps', 'psd', 'be', 'cds',
    ],
    'world': [
        'ucrânia', 'rússia', 'china', 'irã', 'israel', 'gaza', 'médio oriente', 'europa',
        'ásia', 'áfrica', 'américa latina', 'guerra', 'diplomático', 'imigração',
        'refugiado', 'mundial', 'internacional', 'onu', 'otan', 'conflito', 'crise',
        'militar', 'exército', 'paz', 'acordo', 'tratado', 'sanções',
    ],
    'entertainment': [
        'filme', 'cinema', 'ator', 'atriz', 'oscar', 'celebridade',
        'música', 'álbum', 'show', 'turnê', 'netflix', 'streaming', 'bilheteria',
        'teatro', 'série', 'temporada', 'final de temporada',
        'cantor', 'banda', 'spotify',
        'disney', 'hollywood', 'prêmio', 'tapete vermelho',
        'comédia', 'drama', 'terror',
        'jogo', 'gaming', 'youtube', 'tiktok',
        'influenciador', 'viral', 'podcast', 'best-seller', 'livro',
        'televisão', 'programa', 'globo', 'novela',
    ],
}

STOP_WORDS = {
    'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas', 'e', 'ou', 'mas',
    'em', 'de', 'do', 'da', 'dos', 'das', 'no', 'na', 'nos', 'nas', 'a', 'ao', 'aos',
    'para', 'por', 'com', 'sem', 'sobre', 'entre', 'até', 'desde',
    'é', 'são', 'era', 'eram', 'foi', 'ser', 'estar', 'está', 'estão',
    'tem', 'têm', 'tinha', 'ter', 'há', 'foi',
    'que', 'qual', 'quem', 'como', 'quando', 'onde', 'porque',
    'este', 'esta', 'estes', 'estas', 'esse', 'essa', 'esses', 'essas',
    'aquele', 'aquela', 'aqueles', 'aquelas',
    'ele', 'ela', 'eles', 'elas', 'eu', 'tu', 'nós', 'vocês',
    'meu', 'minha', 'teu', 'tua', 'seu', 'sua', 'nosso', 'nossa',
    'mais', 'muito', 'também', 'já', 'ainda', 'só', 'não', 'sim', 'nem',
    'após', 'antes', 'entre', 'sob', 'através',
}

SOURCE_ATTRIBUTION = r'\s*(Folha de S\.Paulo|O Globo|Estadão|UOL|G1|R7|BBC Brasil|DW Brasil|CartaCapital|Exame|IstoÉ|Valor Econômico)\s*$'

GENERIC_TEXT = [
    'cobertura completa de notícias',
    'agregado de',
    'clique aqui para mais',
]

CATEGORY_NAMES = OrderedDict([
    ('all', 'Todos'),
    ('most_covered', 'Mais Cobertos'),
    ('world', 'Mundo'),
    ('brasil', 'Brasil'),
    ('politics', 'Política'),
    ('business', 'Economia'),
    ('technology', 'Tecnologia'),
    ('science', 'Ciência'),
    ('health', 'Saúde'),
    ('sports', 'Esportes'),
    ('entertainment', 'Entretenimento'),
])

CATEGORY_KEYWORDS_WEIGHTED = {
    'politics': {
        'high': ['lula', 'bolsonaro', 'presidente', 'congresso', 'senado', 'câmara', 'stf', 'supremo'],
        'medium': ['governo', 'ministro', 'eleição', 'voto', 'campanha', 'lei', 'reforma', 'partido', 'deputado', 'senador', 'orçamento', 'política', 'oposição'],
        'low': []
    },
    'business': {
        'high': ['bolsa', 'ibovespa', 'real', 'dólar', 'ação', 'dividendo', 'inflação'],
        'medium': ['economia', 'mercado', 'empresa', 'banco', 'finanças', 'investimento', 'desemprego', 'pib', 'crescimento', 'crédito', 'dívida', 'exportação', 'importação', 'indústria', 'comércio', 'emprego', 'salário', 'imposto'],
        'low': []
    },
    'technology': {
        'high': ['inteligência artificial', 'ataque cibernético', 'cibersegurança', 'algoritmo'],
        'medium': ['tecnologia', 'software', 'digital', 'robô', 'aplicativo', 'smartphone', 'internet', 'computação', 'dados', 'plataforma', 'redes sociais', 'startup', 'google', 'apple', 'microsoft', 'amazon', 'meta', 'tesla'],
        'low': []
    },
    'science': {
        'high': ['nasa', 'genética', 'evolução', 'biodiversidade'],
        'medium': ['ciência', 'pesquisa', 'descoberta', 'espécie', 'clima', 'terremoto', 'vulcão', 'planeta', 'espaço', 'universo', 'física', 'química', 'biologia', 'laboratório', 'estudo', 'científico', 'fóssil', 'oceano'],
        'low': []
    },
    'health': {
        'high': ['hospital', 'médico', 'medicina', 'vacina', 'pandemia', 'covid', 'câncer', 'diabetes', 'sus'],
        'medium': ['saúde', 'doença', 'tratamento', 'vírus', 'clínica', 'paciente', 'cirurgia', 'terapia', 'sintoma', 'diagnóstico', 'farmacêutico', 'nutrição', 'exercício', 'bem-estar', 'coração', 'cérebro'],
        'low': []
    },
    'sports': {
        'high': ['flamengo', 'corinthians', 'palmeiras', 'brasileirão', 'copa libertadores', 'copa do mundo'],
        'medium': ['futebol', 'liga', 'champions', 'copa', 'olimpíadas', 'esporte', 'time', 'jogador', 'jogo', 'gol', 'tênis', 'basquete', 'vôlei', 'técnico', 'estádio', 'torneio', 'campeonato', 'árbitro'],
        'low': []
    },
    'brasil': {
        'high': ['brasil', 'governo', 'presidente', 'lula', 'congresso', 'câmara', 'senado', 'brasília', 'são paulo', 'rio de janeiro'],
        'medium': ['pt', 'psdb', 'pmdb', 'pl', 'psol', 'portugal', 'lisboa', 'porto', 'assembléia', 'republica', 'ps', 'psd', 'be', 'cds'],
        'low': []
    },
    'world': {
        'high': ['ucrânia', 'rússia', 'guerra', 'crise', 'gaza', 'israel', 'putin'],
        'medium': ['china', 'irã', 'israel', 'gaza', 'médio oriente', 'europa', 'ásia', 'áfrica', 'américa latina', 'diplomático', 'imigração', 'refugiado', 'mundial', 'internacional', 'onu', 'otan', 'conflito', 'militar', 'exército', 'paz', 'acordo', 'tratado', 'sanções'],
        'low': []
    },
    'entertainment': {
        'high': ['oscar', 'globo', 'netflix', 'disney', 'hollywood', 'spotify'],
        'medium': ['filme', 'cinema', 'ator', 'atriz', 'celebridade', 'música', 'álbum', 'show', 'turnê', 'streaming', 'bilheteria', 'teatro', 'série', 'temporada', 'final de temporada', 'cantor', 'banda', 'prêmio', 'tapete vermelho', 'comédia', 'drama', 'terror', 'jogo', 'gaming', 'youtube', 'tiktok', 'influenciador', 'viral', 'podcast', 'best-seller', 'livro', 'televisão', 'programa', 'novela'],
        'low': []
    },
}

UI_STRINGS = {
    'subtitle': 'Escolha seu viés | Serviços de notícias e outros feeds | Últimas 24 horas',
    'how_it_works': 'Como funciona',
    'privacy_text': 'Respeitamos sua privacidade. Este site usa anúncios contextuais (sem cookies de rastreamento) e mostra manchetes/resumos sob fair use.',
    'privacy_link': 'Política de Privacidade',
    'got_it': 'Entendi',
    'sources': 'Fontes:',
    'center_default': 'Fontes centrais (padrão)',
    'all_sources': 'Todas as fontes',
    'center_only': 'Apenas centro',
    'left_center_only': 'Apenas centro-esquerda',
    'left_only': 'Apenas esquerda',
    'right_only': 'Apenas direita',
    'clear_all': 'Limpar tudo',
    'sources_suffix': 'fontes',
    'covered_by_2': 'Histórias cobertas por 2 ou mais fontes',
    'paywall_title': 'Site com paywall',
    'sources_label': 'fontes',
    'read_full': 'Ler história completa',
    'find_coverage': 'Encontrar cobertura',
    'search_related': 'Buscar cobertura relacionada',
    'bias_rating': 'Classificação de viés',
    'ago': 'atrás',
    'show_stories': 'Mostrar',
    'stories': 'histórias',
    'no_stories': 'Nenhuma história nesta categoria',
    'footer_copy': 'Conteúdo de notícias © respectivos editores. Manchetes e resumos usados sob fair use para fins informativos.',
    'footer_sources': 'Fontes:',
    'footer_and': 'e',
    'footer_terms': 'Termos',
    'footer_privacy': 'Privacidade',
    'footer_about': 'Sobre',
    # Header translations
    'logo_tagline': 'Notícias de diferentes perspectivas',
    'search_placeholder': 'Pesquisar notícias...',
    'toggle_theme': 'Alternar tema',
    'filter_label': 'Filtrar por:',
    # Bias filter buttons
    'filter_all': 'Todos',
    'filter_left': 'Esquerda',
    'filter_left_center': 'Centro-esquerda',
    'filter_center': 'Centro',
    'filter_right_center': 'Centro-direita',
    'filter_right': 'Direita',
    # Story card buttons
    'find_coverage_btn': 'Encontrar cobertura',
    'different_angle_btn': 'Outro ângulo',
    'share_btn': 'Compartilhar',
    'different_perspectives': 'Outras perspectivas',
    # Different Angle modal
    'different_angle_title': 'Outra perspectiva',
    'original_label': 'Original:',
    'loading_related': 'Carregando notícias relacionadas...',
    'no_related_stories': 'Nenhuma notícia relacionada encontrada',
    'error_loading': 'Erro ao carregar',
    # Share modal
    'share_story_title': 'Compartilhar notícia',
    'share_on_x': 'Compartilhar no X',
    'share_facebook': 'Compartilhar no Facebook',
    'share_linkedin': 'Compartilhar no LinkedIn',
    'copy_link': 'Copiar link',
    'copied': 'Copiado!',
    'close': 'Fechar',
}

PAYWALLED_SOURCES = {
    'Folha de S.Paulo',
    'Estadão',
    'O Globo',
    'Valor Econômico',
}