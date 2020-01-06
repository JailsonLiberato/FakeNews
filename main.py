import json
import os
import tkinter.filedialog

from twarc import Twarc
from tweepy import API
from tweepy import OAuthHandler
from tweepy import Stream

from network import Network
from network_service import NetworkService
from password_constants import PasswordConstants
from slistener import SListener
from tweet import Tweet


class Main:
    """Classe principal do desenvolvimento."""

    def __init__(self):
        self.__auth = OAuthHandler(
            PasswordConstants.CONSUMER_KEY, PasswordConstants.CONSUMER_SECRET)
        self.__auth.set_access_token(
            PasswordConstants.ACCESS_TOKEN, PasswordConstants.ACCESS_TOKEN_SECRET)
        self.__api = API(self.__auth)
        self.__tweets = []
        self.__selected_tweet = None
        self.__users_retweets = []
        self.__friends = []
        self.__followers = []
        self.__twarc = Twarc(consumer_key=PasswordConstants.CONSUMER_KEY,
                             consumer_secret=PasswordConstants.CONSUMER_SECRET,
                             access_token=PasswordConstants.ACCESS_TOKEN,
                             access_token_secret=PasswordConstants.ACCESS_TOKEN_SECRET)
        self.__network_service = NetworkService()
        self.__network = None

    def execute(self):
        """Método de execução da classe."""
        self.__generate_tweets_json()

    """" self.__open_json()
     self.__build_tweet_list()
     self.__choose_main_tweet()
     self.__get_retweets_by_id()
     self.__get_friends_by_id()
     self.__get_followers_by_id()
     self.__create_network()
     self.__network_service.generate_network(self.__network)
     self.__network_service.plot_network()"""

    def __create_network(self, temp_network=[], flag=False):
        """Criando a rede."""
        if not temp_network and not flag:
            self.__network = Network(self.__selected_tweet.user_id)
            for user in self.__users_retweets:
                network = Network(user)
                if user in self.__get_followers_by_id:
                    self.__network.children.append(network)
                else:
                    temp_network.append(network)
        else:
            while not temp_network:
                list_temp = []
                for net in self.__network.children:
                    if net in temp_network:
                        self.__network.children.append(net)
                        list_temp.append(net)
                temp_network.remove(list_temp)

                self.__create_network(temp_network=temp_network, flag=True)

    def __get_retweets_by_id(self):
        """Retorna uma lista de usuários que retuitaram a mensagem escolhida."""
        users_retweets = []
        for tweet in self.__twarc.retweets(self.__selected_tweet.id):
            users_retweets.append(tweet['user']['id_str'])
        self.__users_retweets = users_retweets

    def __get_friends_by_id(self):
        """Retorna a lista de friends do usuário do tweet principal."""
        users = []
        for user in self.__twarc.friend_ids(user=self.__selected_tweet.user_id):
            users.append(user)
        self.__friends = users

    def __get_followers_by_id(self):
        """Retorna a lista de followers do usuário do tweet principal."""
        users = []
        for user in self.__twarc.follower_ids(user=self.__selected_tweet.user_id):
            users.append(user)
        self.__followers = users

    def __build_tweet_list(self):
        """Constrói a lista de tweets."""
        tweets = []
        for tw in self.__tweets:
            tweets.append(
                Tweet(tw['id'], tw['user']['id'], tw['user']['screen_name'], tw['text'], tw['user']['followers_count'],
                      tw['user']['friends_count']))
        self.__tweets = tweets

    def __choose_main_tweet(self):
        """Escolhe o tweet com mais followers."""
        tweet = self.__tweets[0]
        for tw in self.__tweets:
            if tweet.followers_count < tw.followers_count:
                tweet = tw
        self.__selected_tweet = tweet

    def __check_is_retweet(self, tweettext):
        if tweettext.startswith("rt @") == True:
            print('This tweet is a retweet')
        else:
            print('This tweet is not retweet')

    def __open_json(self):
        """Abre o arquivo JSON e extrai os tweets."""
        filename_path = tkinter.filedialog.askopenfilename(
            initialdir=os.getcwd(), title="Select json file...",
            filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        with open(filename_path) as json_file:
            data = json.load(json_file)
            self.__tweets = list(data['tweets'].values())

    def __generate_tweets_json(self):
        """Gerador de tweets de json."""
        keywords_to_track = ['#python']
        listen = SListener(self.__api)
        stream = Stream(self.__auth, listen)
        stream.filter(track=keywords_to_track)


if __name__ == "__main__":
    main = Main()
    main.execute()
