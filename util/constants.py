class Constants:
    """Constantes de autenticação com Twitter."""
    CONSUMER_KEY = "IJRC3ULbIHzWdk5zLIuN4uBcC"
    CONSUMER_SECRET = "6qTujviv3WDWiR4UPaSMlXpWg4DbFRLhz73rrgM0d96mlyRHom"
    ACCESS_TOKEN = "40781310-F0AnV3prVf06YAiFULRvu61c1E2Iov0kQGX1rN83g"
    ACCESS_TOKEN_SECRET = "9R4DTGn1fdsrNuNlvSQITuGExMwycCHD7pr6wXsHHfrAv"

    """Arquivos JSON"""
    FOLDER_PATH: str = '../files/'
    FILE_FAKE_NAME: str = 'fake_news.json'
    FILE_REAL_NAME: str = 'real_news.json'
    FILE_FRIENDS: str = 'friends.json'
    FILE_FOLLOWERS: str = 'followers.json'
    FILE_RETWEETS: str = 'retweets.json'

    """Request Type"""
    REQUEST_TYPE_FRIENDS = 'friends/ids'
    REQUEST_TYPE_FOLLOWERS = 'followers/ids'

    """Termos de consulta"""
    SEARCH_TERM_FAKE: str = 'coronavírus lang:pt'

    """Propriedades consulta premium."""
    PRODUCT = 'fullarchive'
    LABEL = 'SearchFakeNews'

    """TIPO DE ACESSO ARQUIVO"""
    ARQUIVO_ESCRITA_ZERADA: str = 'w'
    ARQUIVO_APENAS_LEITURA: str = 'r'
