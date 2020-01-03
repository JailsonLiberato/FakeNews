from tweepy import API
from tweepy import OAuthHandler
from tweepy import Stream
from slistener import SListener
from password_constants import PasswordConstants
import tkinter.filedialog
import json
import os


class Main:
    """Classe principal do desenvolvimento."""

    def __init__(self):
        self.__auth = OAuthHandler(
            PasswordConstants.CONSUMER_KEY, PasswordConstants.CONSUMER_SECRET)
        self.__auth.set_access_token(
            PasswordConstants.ACCESS_TOKEN, PasswordConstants.ACCESS_TOKEN_SECRET)
        self.__api = API(self.__auth)
        self.__tweets = []

    def execute(self):
        """Método de execução da classe."""
        #self.__generate_json()
        self.__open_json()

    def __open_json(self):
        """Abre o arquivo JSON e extrai os tweets."""
        filename_path = tkinter.filedialog.askopenfilename(
            initialdir=os.getcwd(), title="Select json file...",
            filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        with open(filename_path) as json_file:
            data = json.load(json_file)
            self.__tweets = data['tweets'].items()

    def __generate_tweets_json(self):
        """Gerador de tweets de json."""
        keywords_to_track = ['#python']
        listen = SListener(self.__api)
        stream = Stream(self.__auth, listen)
        stream.filter(track=keywords_to_track)


if __name__ == "__main__":
    main = Main()
    main.execute()
