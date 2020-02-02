import json
import os
from os.path import isfile, join

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
        self.__universal_counter: int = 0

    def execute(self):
        """Execução principal da classe."""
        self.__find_real_news()
        # self.__find_fake_news()

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
        self.__execute_network(search_term,"fake_news.json")

    def __find_real_news(self):
        """Encontra real news"""
        search_term = 'Auto da compadecida lang:pt'
        self.__execute_network(search_term,"real_news.json")

    def __execute_network(self, search_term, fileName):
        """Executa a rede."""
        if not self.__check_json_file(fileName):
            print("nova consulta")
            # self.__find_tweet(search_term, fileName)
        else:
            self.__load_tweets(fileName)
        self.__get_retweets()
        self.__get_friends(self.__selected_tweet.user_id)
        self.__create_network()

    @staticmethod
    def __check_json_file(fileName):
        """Checa se o arquivo json foi criado."""
        onlyfiles = [f for f in os.listdir('./files/') if isfile(join('./files/', f))]
        # return len(os.listdir(Constants.FOLDER_PATH)) == 0
        return fileName in onlyfiles

    def __load_tweets(self, fileName):
        """Carrega a consulta dos tweets do arquivo json."""
        with open(Constants.FOLDER_PATH + fileName) as json_file:
            x = json_file.read()
            for tweet in json.loads(x)['results']:
                retweet_count: int = 0
                retweeted_status_id = None
                # print("__get_best_tweet")
                # pprint (tweet)

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
        # sys.exit(-1)

    def __find_tweet(self, search_term, fileName):
        """Encontra o tweet."""
        # tweet_result = self.__api.request('tweets/search/%s/:%s' % (Constants.PRODUCT, Constants.LABEL),
        #                                   {'query': search_term})
        self.__save_file = open(Constants.FOLDER_PATH + fileName, 'w')
        self.__save_file.write(json.dumps(tweet_result.json()))
        self.__save_file.close()
        self.__load_tweets(fileName)
        self.__get_best_tweet()

    def save(self, fileName, file):# Método para salvar arquivos
        self.__save_file = open(Constants.FOLDER_PATH + fileName, 'w')
        self.__save_file.write(file)
        self.__save_file.close()

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
        print("get retweets")
        # print(self.__selected_tweet.retweeted_status_id)
        url: str = 'https://api.twitter.com/1.1/statuses/retweeters/ids.json'
        params = {"id": str(self.__selected_tweet.retweeted_status_id), "count": "100", "stringify_ids": "true"}
        response = self.__oauth.get(url, params=params)
        self.__retweets = json.loads(response.text)["ids"]

    def __get_friends(self, user_id):
        """Busca os amigos do usuário que escreveu o tweet."""
        print("__get_friends")
        print(user_id)

        if not self.__check_json_file('friends'):
            print("nova consulta")
            url: str = 'https://api.twitter.com/1.1/friends/ids.json'
            params = {"user_id": user_id, "count": "500"}
            response = None
            while response is None or response.status_code == 429:
                response = self.__api.request('friends/ids', params=params)

            # response.
            self.__friends = json.loads(response.text)["ids"]
            friendsToSave = {"user_id": self.__friends}
            print(friendsToSave)
            self.save("friends.json", json.dumps(str(friendsToSave)))
            self.__friends = [str(item) for item in self.__friends]
            # print(self.__friends)
        else:
            print("carregar arquivo")

    def __create_network(self):
        """Cria a rede."""
        # print("__create_network")
        retweets_temp = []
        network: Network = Network(self.__selected_tweet.user_id)
        for ret in self.__retweets:
            if ret in self.__friends:
                net: Network = Network(ret)
                network.children.append(net)
            else:
                if ret not in retweets_temp:
                    retweets_temp.append(ret)
        self.__create_network_recursive(network, retweets_temp)
        print('XXX')

    def __create_network_recursive(self, network, retweets_temp):
        for chi in network.children:
            self.__get_friends(chi.id)
            for ret in self.__retweets:
                if ret in self.__friends:
                    net: Network = Network(ret)
                    chi.children.append(net)
                else:
                    if ret not in retweets_temp:
                        retweets_temp.append(ret)
            if network.children and retweets_temp and self.__universal_counter < 50:
                self.__universal_counter = self.__universal_counter + 1
                self.__create_network_recursive(chi, retweets_temp)


if __name__ == "__main__":
    main = Main()
    main.execute()
