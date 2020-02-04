import json
import os
import time
from os.path import isfile, join
from urllib.error import HTTPError

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
        self.__execute_network(search_term, "fake_news.json")

    def __find_real_news(self):
        """Encontra real news"""
        search_term = 'Auto da compadecida lang:pt'
        self.__execute_network(search_term, "real_news.json")

    def __execute_network(self, search_term, fileName):
        """Executa a rede."""
        if not self.__check_json_file(fileName):
            self.__find_tweet(search_term, fileName)
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

    def __load_tweets(self, file_name):
        """Carrega a consulta dos tweets do arquivo json."""
        with open(Constants.FOLDER_PATH + file_name) as json_file:
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

    def __find_tweet(self, search_term, fileName):
        """Encontra o tweet."""
        tweet_result = self.__api.request('tweets/search/%s/:%s' % (Constants.PRODUCT, Constants.LABEL),
                                          {'query': search_term})
        search_file = open(Constants.FOLDER_PATH + fileName, 'w')
        search_file.write(json.dumps(tweet_result.json()))
        search_file.close()
        self.__load_tweets(fileName)
        self.__get_best_tweet()

    def __get_best_tweet(self):
        """Selecionar o tweet com mais seguidores."""
        tweet_selected: Tweet = None
        for tweet in self.__tweets:
            if tweet_selected is None:  # RT' not in tweet.tweet_text and
                tweet_selected = tweet
            elif tweet_selected is not None and tweet_selected.retweet_count < tweet.retweet_count \
                    and tweet_selected.followers_count < \
                    tweet.followers_count:
                tweet_selected = tweet
        self.__selected_tweet = tweet_selected

    def __get_retweets(self):
        """Recupera os retweets."""
        print("get retweets")
        url: str = 'https://api.twitter.com/1.1/statuses/retweeters/ids.json'
        params = {"id": str(self.__selected_tweet.retweeted_status_id), "count": "100", "stringify_ids": "true"}
        response = self.__oauth.get(url, params=params)
        self.__retweets = json.loads(response.text)["ids"]

    def __get_friends(self, user_id):
        """Busca os amigos do usuário que escreveu o tweet."""
        if not self.__check_json_file("friends.json"):
            self.__create_friends_file(user_id)
            self.__load_friend_file(user_id)
        elif not self.__check_friends_file(user_id):
            self.__write_friend_file(user_id)

    def __check_friends_file(self, user_id):
        """Checar se o user_id está presente nas chaves da consulta."""
        return self.__load_friend_file(user_id)

    def __write_friend_file(self, user_id):
        """Escrever o friend no arquivo."""
        self.__request_friends(user_id)
        with open(Constants.FOLDER_PATH + Constants.FILE_FRIENDS, 'a') as friend_file:
            friends_dict = {
                user_id: self.__friends
            }
            friend_file.seek(-1, os.SEEK_END)
            friend_file.truncate()
            friend_file.write(",")
            friend_file.write(json.dumps(friends_dict))
            friend_file.write("\n")
            friend_file.close()

    def __create_friends_file(self, user_id):
        """Cria um arquivo com a lista de amigos."""
        self.__request_friends(user_id)
        with open(Constants.FOLDER_PATH + Constants.FILE_FRIENDS, 'w') as friend_file:
            friends_dict = {
                user_id: self.__friends
            }
            friend_file.write(json.dumps(friends_dict))
            friend_file.write("\n")
            friend_file.close()

    def __request_friends(self, user_id):
        try:
            params = {"user_id": user_id, "count": "500"}
            response = self.__api.request('friends/ids', params=params)
            self.__friends = json.loads(response.text)["ids"]
        except HTTPError as e:
            if e.code == 429:
                time.sleep(5)

    def __load_friend_file(self, user_id):
        """Carrega os amigos do user_id do arquivo."""
        with open("files/" + Constants.FILE_FRIENDS, "r") as json_file:
            x = json_file.read()
            friend_file = json.loads(x).items()
            flag: bool = False
            for key, value in friend_file:
                if user_id == int(key):
                    self.__friends = value
                    flag = True
                    break
            json_file.close()
            return flag

    def __create_network(self):
        """Cria a rede."""
        network: Network = Network(self.__selected_tweet.user_id)
        for ret in self.__retweets:
            if int(ret) in self.__friends:
                network_friend: Network = Network(str(ret))
                network.children.append(network_friend)
        self.__create_network_recursive(network)

    def __create_network_recursive(self, network):
        for chi in network.children:
            self.__get_friends(chi.id)
            for ret in self.__retweets:
                if ret in self.__friends:
                    net: Network = Network(ret)
                    chi.children.append(net)
            if network.children and self.__universal_counter < 50:
                self.__universal_counter = self.__universal_counter + 1
                self.__create_network_recursive(chi)


if __name__ == "__main__":
    main = Main()
    main.execute()
