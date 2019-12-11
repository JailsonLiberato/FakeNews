import tweepy
from password_constants import PasswordConstants
from vertice import Vertice
from graph_service import GraphService


class Main:
    """Classe principal do sistema."""

    def __init__(self):
        self.__api = self.__authenticator()
        self.__tweets = []
        self.__vertices = []
        self.__graph_service = GraphService()

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
        quantity_results = 5
        language = 'pt'
        self.__tweets = tweepy.Cursor(self.__api.search, q=search_words, lang=language, since=date_since)\
            .items(quantity_results)

    def __get_tweet_by_max_retweet(self):
        """Retorna o twitter com maior número de retweets."""
        tweet_temp = None
        for tweet in self.__tweets:
            if tweet_temp is None:
                tweet_temp = tweet
            elif tweet.retweet_count > tweet_temp.retweet_count:
                tweet_temp = tweet
        return tweet_temp

    def execute(self):
        """Método principal de execução."""
        self.__query_tweets()
        tweet_selected = self.__get_tweet_by_max_retweet()
        self.__graph_service.execute(self.__vertices)


if __name__ == "__main__":
    main = Main()
    main.execute()
