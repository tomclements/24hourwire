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
    'us': [
        'estados unidos', 'eua', 'amárica do norte', 'flórida', 'texas', 'califórnia',
        'nova york', 'miami', 'los angeles', 'chicago', 'washington', 'trump', 'biden',
        'casa branca', 'congresso', 'senado', 'fbi', 'cia', 'pentágono',
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
    ('us', 'EUA'),
    ('politics', 'Política'),
    ('business', 'Economia'),
    ('technology', 'Tecnologia'),
    ('science', 'Ciência'),
    ('health', 'Saúde'),
    ('sports', 'Esportes'),
    ('entertainment', 'Entretenimento'),
])

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
}

PAYWALLED_SOURCES = {
    'Folha de S.Paulo',
    'Estadão',
    'O Globo',
    'Valor Econômico',
}