import tweepy


class SListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.__save_file = open('file.json', 'w')
        self.__save_file.write('{"tweets": \n{')
        self.__n = 0

    def on_data(self, tweet):
        tw_string = '"tweet' + str(self.__n) + '"' + ':'
        self.__save_file.write(tw_string)
        self.__save_file.write(str(tweet))
        self.__n += 1
        if self.__n < 3:
            self.__save_file.write(', ')
            return True
        else:
            self.__save_file.write('}\n}')
            self.__save_file.close()
            return False
