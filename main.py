from tweepy import API
from tweepy import OAuthHandler
from tweepy import Stream
from slistener import SListener
from password_constants import PasswordConstants
import tkinter.filedialog
import json
import os


class Main:

    def __init__(self):
        self.__auth = OAuthHandler(
            PasswordConstants.CONSUMER_KEY, PasswordConstants.CONSUMER_SECRET)
        self.__auth.set_access_token(
            PasswordConstants.ACCESS_TOKEN, PasswordConstants.ACCESS_TOKEN_SECRET)
        self.__api = API(self.__auth)

    def execute(self):
        #self.__generate()
        self.__open_json()

    def __open_json(self):
        filename_path = tkinter.filedialog.askopenfilename(
            initialdir=os.getcwd(), title="Select json file...",
            filetypes=(("JSON files", "*.json"), ("all files", "*.*")))
        with open(filename_path) as json_file:
            data = json.load(json_file)
            print(data['tweets']['tweet1']['text'])

    def __generate(self):
        keywords_to_track = ['#rstats', '#python']
        listen = SListener(self.__api)
        stream = Stream(self.__auth, listen)
        stream.filter(track=keywords_to_track)


if __name__ == "__main__":
    main = Main()
    main.execute()
