import json
import os

from TwitterAPI import TwitterAPI

from constants import Constants
from tweet import Tweet


class Main:
    """Classe principal do programa."""

    def __init__(self):
        self.__api = self.__get_authentication()
        self.__save_file = None
        self.__tweets = []
        self.__selected_tweet: Tweet = None

    def execute(self):
        """Execução principal da classe."""
        # self.__find_fake_news()
        self.__find_real_news()

    def __get_authentication(self):
        """Realiza a autenticação do Twitter."""
        return TwitterAPI(Constants.CONSUMER_KEY, Constants.CONSUMER_SECRET,
                          Constants.ACCESS_TOKEN, Constants.ACCESS_TOKEN_SECRET)

    def __find_fake_news(self):
        """Encontra fake news."""
        search_term = 'Haddad kit gay, lang:pt'
        self.__execute_network(search_term)

    def __find_real_news(self):
        """Encontra real news"""
        search_term = 'Auto da compadecida, lang:pt'
        self.__execute_network(search_term)

    def __execute_network(self, search_term):
        """Executa a rede."""
        if self.__check_json_file():
            self.__find_tweet(search_term)
        else:
            self.__load_tweets()
        self.__get_retweets()
        self.__get_friends()
        self.__create_network()

    def __check_json_file(self):
        """Checa se o arquivo json foi criado."""
        return len(os.listdir(Constants.FOLDER_PATH)) == 0

    def __load_tweets(self):
        """Carrega a consulta dos tweets do arquivo json."""
        with open(Constants.FOLDER_PATH + Constants.FILE_NAME) as json_file:
            x = json_file.read()
            for tweet in json.loads(x)['results']:
                retweet_count: int = 0
                if 'retweeted_status' in tweet:
                    retweet_count: int = tweet['retweeted_status']['retweet_count']
                followers_count: int = tweet['user']['followers_count']
                friends_count: int = tweet['user']['friends_count']
                tweet_id = tweet['id']
                user_id = tweet['user']['id']
                tweet_text = tweet['text']
                t: Tweet = Tweet(tweet_id, user_id, tweet_text, followers_count, friends_count, retweet_count)
                self.__tweets.append(t)
        self.__get_best_tweet()

    def __find_tweet(self, search_term):
        """Encontra o tweet."""
        tweet_result = self.__api.request('tweets/search/%s/:%s' % (Constants.PRODUCT, Constants.LABEL),
                                          {'query': search_term})
        self.__save_file = open(Constants.FOLDER_PATH + Constants.FILE_NAME, 'w')
        self.__save_file.write(json.dumps(tweet_result.json()))
        self.__save_file.close()
        self.__load_tweets()
        self.__get_best_tweet()

    def __get_best_tweet(self):
        """Selecionar o tweet com mais seguidores."""
        tweet_selected: Tweet = self.__tweets[0]
        for tweet in self.__tweets:
            if tweet_selected.retweet_count < tweet.retweet_count and tweet_selected.followers_count < \
                    tweet.followers_count:
                tweet_selected = tweet
        self.__selected_tweet = tweet_selected

    def __get_retweets(self):
        """Recupera os retweets."""
        pass

    def __get_friends(self):
        """Busca os amigos do usuário que escreveu o tweet."""
        pass

    def __create_network(self):
        """Cria a rede."""
        pass


if __name__ == "__main__":
    main = Main()
    main.execute()
