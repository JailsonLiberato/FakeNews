import json
import time
from urllib.error import HTTPError
from file_util import FileUtil
import matplotlib.pyplot as plt
import networkx as nx
from authenticator_util import AuthenticatorUtil
from constants import Constants
from network import Network
from tweet import Tweet


class Main:
    """Classe principal do programa."""

    def __init__(self):
        self.__premium_auth = AuthenticatorUtil.get_premium_authentication()
        self.__standard_auth = AuthenticatorUtil.get_standard_authentication()
        self.__tweets = []
        self.__retweets = []
        self.__friends = []
        self.__follows = []
        self.__selected_tweet: Tweet = None
        self.__universal_counter: int = 0

    def execute(self):
        """Execução principal da classe."""
        # self.__find_real_news()
        self.__find_fake_news()

    def __find_fake_news(self):
        """Encontra fake news."""
        search_term = 'coronavírus lang:pt'
        self.__execute_network(search_term, "fake_news.json")

    def __find_real_news(self):
        """Encontra real news"""
        search_term = 'Auto da compadecida lang:pt'
        self.__execute_network(search_term, "real_news.json")

    def __execute_network(self, search_term, fileName):
        """Executa a rede."""
        if not FileUtil.check_json_file(fileName):
            self.__find_tweet(search_term, fileName)
        else:
            self.__load_tweets(fileName)
        self.__get_retweets()
        self.__get_friends(self.__selected_tweet.user_id)
        self.__get_follows(self.__selected_tweet.user_id)
        self.__create_network()
        # self._draw_graph()

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
        tweet_result = self.__premium_auth.request('tweets/search/%s/:%s' % (Constants.PRODUCT, Constants.LABEL),
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
        params = {"id": str(self.__selected_tweet.retweeted_status_id), "count": "100000", "stringify_ids": "true"}
        response = self.__standard_auth.get(url, params=params)
        self.__retweets = json.loads(response.text)["ids"]

    def __get_friends(self, user_id):
        """Busca os amigos do usuário que escreveu o tweet."""
        if not FileUtil.check_json_file("friends.json"):
            self.__create_friends_file(user_id)
            self.__load_friend_file(user_id)
        elif not self.__check_friends_file(user_id):
            self.__write_friend_file(user_id)

    def __get_follows(self, user_id):
        """Busca os amigos do usuário que escreveu o tweet."""
        if not FileUtil.check_json_file("follows.json"):
            self.__create_follows_file(user_id)
            self.__load_follow_file(user_id)
        elif not self.__check_follows_file(user_id):
            self.__write_follow_file(user_id)

    def __check_friends_file(self, user_id):
        """Checar se o user_id está presente nas chaves da consulta."""
        return self.__load_friend_file(user_id)

    def __check_follows_file(self, user_id):
        return self.__load_follow_file(user_id)

    def __write_friend_file(self, user_id):
        """Escrever o friend no arquivo."""
        self.__request_friends(user_id)
        with open(Constants.FOLDER_PATH + Constants.FILE_FRIENDS, 'r') as friend_read_file:
            friends_dict = {
                user_id: self.__friends
            }
            file_txt = friend_read_file.read()
            friend_read_file.close()
            file_txt = file_txt[:-2]
            with open(Constants.FOLDER_PATH + Constants.FILE_FRIENDS, "w") as friend_write_file:
                friend_write_file.write(file_txt)
                friend_write_file.write(", ")
                friend_write_file.write("\n")
                next_data = json.dumps(friends_dict)
                next_data = next_data[1:]
                friend_write_file.write(next_data)
                friend_write_file.close()

    def __write_follow_file(self, user_id):
        self.__request_follows(user_id)
        with open(Constants.FOLDER_PATH + Constants.FILE_FOLLOWS, 'r') as follow_read_file:
            follow_dict = {
                user_id: self.__follows
            }
            file_txt = follow_read_file.read()
            follow_read_file.close()
            file_txt = file_txt[:-2]
            with open(Constants.FOLDER_PATH + Constants.FILE_FOLLOWS, "w") as follow_write_file:
                follow_write_file.write(file_txt)
                follow_write_file.write(", ")
                follow_write_file.write("\n")
                next_data = json.dumps(follow_dict)
                next_data = next_data[1:]
                follow_write_file.write(next_data)
                follow_write_file.close()

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

    def __create_follows_file(self, user_id):
        self.__request_follows(user_id)
        with open(Constants.FOLDER_PATH + Constants.FILE_FOLLOWS, 'w') as follow_file:
            follow_dict = {
                user_id: self.__follows
            }
            follow_file.write(json.dumps(follow_dict))
            follow_file.write("\n")
            follow_file.close()

    def __request_friends(self, user_id):
        try:
            params = {"user_id": user_id, "count": "100000"}
            response = self.__premium_auth.request('friends/ids', params=params)
            self.__friends = json.loads(response.text)["ids"]
        except HTTPError as e:
            if e.code == 429:
                time.sleep(5)

    def __request_follows(self, user_id):
        try:
            params = {"user_id": user_id, "count": "100000"}
            response = self.__premium_auth.request('followers/ids', params=params)
            self.__follows = json.loads(response.text)["ids"]
        except HTTPError as e:
            if e.code == 429:
                time.sleep(5)

    def __load_friend_file(self, user_id):
        """Carrega os amigos do user_id do arquivo."""
        with open(Constants.FOLDER_PATH + Constants.FILE_FRIENDS, "r") as json_file:
            x = json_file.read()
            friend_file = json.loads(x).items()
            flag: bool = False
            for key, value in friend_file:
                if str(user_id) == str(key):
                    self.__friends = value
                    flag = True
                    break
            json_file.close()
            return flag

    def __load_follow_file(self, user_id):
        with open(Constants.FOLDER_PATH + Constants.FILE_FOLLOWS, "r") as json_file:
            x = json_file.read()
            follow_file = json.loads(x).items()
            flag: bool = False
            for key, value in follow_file:
                if str(user_id) == str(key):
                    self.__follows = value
                    flag = True
                    break
            json_file.close()
            return flag

    def __create_network(self):
        """Cria a rede."""
        network: Network = Network(self.__selected_tweet.user_id)
        for ret in self.__retweets:
            print(int(ret))
            print(int(ret) in self.__friends)
            print(int(ret) in self.__follows)
            if int(ret) in self.__friends or int(ret) in self.__follows:
                network_friend: Network = Network(str(ret))
                network.children.append(network_friend)
        self.__create_network_recursive(network)

    def __create_network_recursive(self, network):
        for chi in network.children:
            self.__get_friends(chi.id)
            self.__get_follows(chi.id)
            for ret in self.__retweets:
                if ret in self.__friends:
                    net: Network = Network(ret)
                    chi.children.append(net)
            if chi.children and self.__universal_counter < 50:
                self.__universal_counter = self.__universal_counter + 1
                self.__create_network_recursive(chi)

    def _draw_graph(self):
        G = nx.Graph()
        with open(Constants.FOLDER_PATH + Constants.FILE_FRIENDS, "r") as json_file:
            x = json_file.read()  # Ler o arquivo com as listas de amigos
            self.__friend_file = json.loads(
                x).items()  # obtém os itens presentes no arquivo como uma lista de (key, value)

            # key     #value
        for user_id, friends in self.__friend_file:  # friends representa a lista de amigos de user_id,
            user_id = int(user_id)
            for friend in friends:  # percorre a lista de amigos e adiciona arestas que ligam cada amigo presente na lista ao user_id
                G.add_edge(user_id, friend)
        # nx.draw(G,with_labels=True) caso que gerar o grafo com o id que identifica cada vértice
        nx.draw(G)
        plt.savefig("tweets_Network.png")  # salva o grafo em uma imagem
        plt.show()


if __name__ == "__main__":
    main = Main()
    main.execute()
