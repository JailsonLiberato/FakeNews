import json
import os
import tkinter.filedialog

from requests_oauthlib import OAuth1Session
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
        self.__session = OAuth1Session(PasswordConstants.CONSUMER_KEY, PasswordConstants.CONSUMER_SECRET,
                                       PasswordConstants.ACCESS_TOKEN,
                                       PasswordConstants.ACCESS_TOKEN_SECRET)
        self.__network_service = NetworkService()
        self.__network = None

    def execute(self):  # self.__generate_tweets_json()
        self.__open_json()
        self.__build_tweet_list()
        self.__choose_main_tweet()
        self.__get_retweets_by_id()
        self.__get_friends_by_id()
        self.__get_followers_by_id()
        """self.__create_network()
        self.__network_service.generate_network(self.__network)
        self.__network_service.plot_network()"""

    def __get_trend_topics(self):
        session = OAuth1Session(PasswordConstants.CONSUMER_KEY, PasswordConstants.CONSUMER_SECRET,
                                PasswordConstants.ACCESS_TOKEN,
                                PasswordConstants.ACCESS_TOKEN_SECRET)
        response = session.get("https://api.twitter.com/1.1/trends/place.json?id=23424768")
        brazils = json.loads(response.content)[0]["trends"]
        for trend in brazils:
            print(trend["name"])

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
        response = self.__session.get(
            "https://api.twitter.com/1.1/statuses/retweeters/ids.json?id=" + str(self.__selected_tweet.id)
            + "&stringify_ids=true")
        self.__users_retweets = json.loads(response.content)['ids']

    def __get_friends_by_id(self):
        """Retorna a lista de friends do usuário do tweet principal."""
        response = self.__session.get(
            "https://api.twitter.com/1.1/friends/list.json?user_id=" + str(
                self.__selected_tweet.user_id))
        self.__friends = json.loads(response.content)['users']

    def __get_followers_by_id(self):
        """Retorna a lista de followers do usuário do tweet principal."""
        response = self.__session.get(
            "https://api.twitter.com/1.1/followers/ids.json?user_id=" + str(
                self.__selected_tweet.user_id))
        self.__followers = json.loads(response.content)['ids']

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
