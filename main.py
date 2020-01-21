import json
import os

from TwitterAPI import TwitterAPI
from requests_oauthlib import OAuth1Session

from constants import Constants
from network import Network
from tweet import Tweet


class Main:
    """Classe principal do programa."""

    def __init__(self):
        self.__api = self.__get_authentication()
        self.__oauth = self.__get_other_authentication()
        self.__save_file = None
        self.__tweets = []
        self.__retweets = []
        self.__friends = []
        self.__follows = []
        self.__selected_tweet: Tweet = None

    def execute(self):
        """Execução principal da classe."""
        # self.__find_fake_news()
        self.__find_real_news()

    @staticmethod
    def __get_other_authentication():
        return OAuth1Session(Constants.CONSUMER_KEY,
                             client_secret=Constants.CONSUMER_SECRET,
                             resource_owner_key=Constants.ACCESS_TOKEN,
                             resource_owner_secret=Constants.ACCESS_TOKEN_SECRET)

    @staticmethod
    def __get_authentication():
        """Realiza a autenticação do Twitter."""
        return TwitterAPI(Constants.CONSUMER_KEY, Constants.CONSUMER_SECRET,
                          Constants.ACCESS_TOKEN, Constants.ACCESS_TOKEN_SECRET)

    def __find_fake_news(self):
        """Encontra fake news."""
        search_term = 'Haddad kit gay -is:retweet -is:reply  lang:pt'
        self.__execute_network(search_term)

    def __find_real_news(self):
        """Encontra real news"""
        search_term = 'Auto da compadecida lang:pt'
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

    @staticmethod
    def __check_json_file():
        """Checa se o arquivo json foi criado."""
        return len(os.listdir(Constants.FOLDER_PATH)) == 0

    def __load_tweets(self):
        """Carrega a consulta dos tweets do arquivo json."""
        with open(Constants.FOLDER_PATH + Constants.FILE_NAME) as json_file:
            x = json_file.read()
            for tweet in json.loads(x)['results']:
                retweet_count: int = 0
                retweeted_status_id = None
                if 'retweeted_status' in tweet:
                    retweet_count: int = tweet['retweeted_status']['retweet_count']
                    retweeted_status_id = tweet['retweeted_status']['id']
                followers_count: int = tweet['user']['followers_count']
                friends_count: int = tweet['user']['friends_count']
                tweet_id = tweet['id']
                user_id = tweet['user']['id']
                tweet_text = tweet['text']

                t: Tweet = Tweet(tweet_id, user_id, tweet_text, followers_count, friends_count, retweeted_status_id,
                                 retweet_count)
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
        tweet_selected: Tweet = None
        for tweet in self.__tweets:
            if tweet_selected is None:  # RT' not in tweet.tweet_text and
                tweet_selected = tweet
            elif tweet_selected is not None and tweet_selected.retweet_count < tweet.retweet_count \
                    and tweet_selected.followers_count < \
                    tweet.followers_count:  # and 'RT' not in tweet.tweet_text:
                tweet_selected = tweet
        self.__selected_tweet = tweet_selected

    def __get_retweets(self):
        """Recupera os retweets."""
        url: str = 'https://api.twitter.com/1.1/statuses/retweeters/ids.json'
        params = {"id": str(self.__selected_tweet.retweeted_status_id), "count": "100", "stringify_ids": "true"}
        response = self.__oauth.get(url, params=params)
        self.__retweets = json.loads(response.text)["ids"]

    def __get_friends(self):
        """Busca os amigos do usuário que escreveu o tweet."""
        url: str = 'https://api.twitter.com/1.1/friends/ids.json'
        params = {"user_id": self.__selected_tweet.user_id}
        response = self.__oauth.get(url, params=params)
        self.__friends = json.loads(response.text)["ids"]
        self.__friends = [str(item) for item in self.__friends]

    def __create_network(self):
        """Cria a rede."""
        network: Network = Network(self.__selected_tweet.user_id)
        for ret in self.__retweets:
            if ret in self.__friends:
                print("Amigo")
            else:
                print("Não amigo")


if __name__ == "__main__":
    main = Main()
    main.execute()
