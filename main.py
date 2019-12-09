import tweepy
from password_constants import PasswordConstants
from vertice import Vertice


class Main:
    """Classe principal do sistema."""

    def __init__(self):
        self.__api = self.__authenticator()
        self.__tweets = []

    @staticmethod
    def __authenticator():
        """"Autentica as informações com o Twitter Dev."""
        auth = tweepy.OAuthHandler(PasswordConstants.CONSUMER_API_KEYS_KEY,
                                   PasswordConstants.CONSUMER_API_KEYS_SECRET_KEY)
        auth.set_access_token(PasswordConstants.ACCESS_TOKEN, PasswordConstants.ACCESS_TOKEN_SECRET)
        return tweepy.API(auth)

    def __query_tweets(self):
        """Parâmetros de pesquisa no Twitter."""
        search_words = "Bolsonaro"
        date_since = "2018-01-01"
        date_until = "2018-11-31"
        quantity_results = 5
        self.__tweets = tweepy.Cursor(self.__api.search, q=search_words, lang="pt", since=date_since)\
            .items(quantity_results)

    def execute(self):
        vertices = []
        for tweet in self.__tweets:
            vertices.append(Vertice(tweet))


if __name__ == "__main__":
    main = Main()
    main.execute()
