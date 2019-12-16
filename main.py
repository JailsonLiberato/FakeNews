import tweepy
from password_constants import PasswordConstants
from query_constants import QueryConstants
from vertice import Vertice
from graph_service import GraphService
from twarc import Twarc


class Main:
    """Classe principal de execução da aplicação."""

    def __init__(self):
        self.__api = self.__authenticator()
        self.__retweets = []
        self.__main_vertice = None
        self.__graph_service = GraphService()

    def execute(self):
        """Método principal de execução."""
        self.__query_tweets()
        selected_tweet = self.__get_tweet_by_max_retweet()
        self.__main_vertice = Vertice(selected_tweet)
        selected_tweet_ids = self.__api.friends_ids(selected_tweet.author.screen_name)
        retweets = self.__query_retweets_by_id(selected_tweet)
        for ret in retweets:
            if ret.user.id in selected_tweet_ids:
                self.__main_vertice.vertices.append(Vertice(ret))
            else:
                self.__retweets.append(ret)
        self.__graph_service.execute(self.__main_vertice)

    @staticmethod
    def __authenticator():
        """"Autentica as informações com o Twitter Dev."""
        auth = tweepy.OAuthHandler(PasswordConstants.CONSUMER_API_KEYS_KEY,
                                   PasswordConstants.CONSUMER_API_KEYS_SECRET_KEY)
        auth.set_access_token(PasswordConstants.ACCESS_TOKEN, PasswordConstants.ACCESS_TOKEN_SECRET)
        return tweepy.API(auth)

    def __query_tweets(self):
        """Parâmetros de pesquisa no Twitter."""
        search_words = QueryConstants.SEARCH_WORLD
        date_since = QueryConstants.DATE_SINCE
        quantity_results = QueryConstants.QUANTITY_RESULTS
        language = QueryConstants.QUERY_LANGUAGE
        self.__tweets = tweepy.Cursor(self.__api.search, q=search_words, lang=language, since=date_since, ) \
            .items(quantity_results)

    def __query_retweets_by_id(self, selected_twitter):
        return self.__api.retweets(selected_twitter.retweeted_status.id, 500)

    def __get_tweet_by_max_retweet(self):
        """Retorna o twitter com maior número de retweets."""
        tweet_temp = None
        for tweet in self.__tweets:
            if tweet_temp is None:
                tweet_temp = tweet
            elif tweet.retweet_count > tweet_temp.retweet_count:
                tweet_temp = tweet
        return tweet_temp

    def __is_retweet_follow(self, author, retweeter):
        """Checa se quem retweetou também"""
        status = self.__api.show_friendship(author, retweeter)
        return status[0].following == False and status[1].following == True


if __name__ == "__main__":
    main = Main()
    main.execute()
