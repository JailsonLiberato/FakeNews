import json
import time
from urllib.error import HTTPError

from entity.tweet import Tweet
from util.authenticator_util import AuthenticatorUtil
from util.constants import Constants
from util.file_util import FileUtil


class TwitterService:
    """Serviço do Twitter."""

    def __init__(self):
        self.__filename = ''
        self.__search_term = ''
        self.__tweets = []
        self.__friends = []
        self.__standard_auth = AuthenticatorUtil.get_standard_authentication()
        self.__premium_auth = AuthenticatorUtil.get_premium_authentication()

    def search_tweet(self, search_term, filename):
        self.__search_term = search_term
        self.__filename = filename
        if not FileUtil.check_json_file(self.__filename):
            self.__request_tweet()
        self.__load_tweets(self.__filename)
        return self.__get_best_tweet()

    def __request_tweet(self):
        """Encontra o tweet."""
        tweet_result = self.__premium_auth.request('tweets/search/%s/:%s' % (Constants.PRODUCT, Constants.LABEL),
                                                   {'query': self.__search_term})
        search_file = open(Constants.FOLDER_PATH + self.__filename, Constants.ARQUIVO_ESCRITA_ZERADA)
        search_file.write(json.dumps(tweet_result.json()))
        search_file.close()

    def __load_tweets(self, file_name):
        """Carrega a consulta dos tweets do arquivo json."""
        with open(Constants.FOLDER_PATH + file_name) as json_file:
            tweet_file = json_file.read()
            for tweet in json.loads(tweet_file)['results']:
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

    def __get_best_tweet(self):
        """Selecionar o tweet com mais retweet | seguidores."""
        selected_tweet: Tweet = None
        for tweet in self.__tweets:
            if selected_tweet is None:
                selected_tweet = tweet
            elif selected_tweet is not None and selected_tweet.retweet_count < tweet.retweet_count \
                    and selected_tweet.followers_count < \
                    tweet.followers_count:
                selected_tweet = tweet
                return selected_tweet

    def __get_retweets(self, selected_tweet):
        """Recupera os retweets."""
        url: str = 'https://api.twitter.com/1.1/statuses/retweeters/ids.json'
        params = {"id": str(selected_tweet.retweeted_status_id), "count": "100000", "stringify_ids": "true"}
        response = self.__standard_auth.get(url, params=params)
        return json.loads(response.text)["ids"]

    def get_features(self, selected_tweet, filename):
        """Busca os amigos do usuário que escreveu o tweet."""
        if not FileUtil.check_json_file(filename):
            self.__create_file(selected_tweet, filename)
            return self.__load_file(selected_tweet.user_id, filename)
        elif not self.__load_file(selected_tweet.user_id, filename) is None and filename is not Constants.FILE_RETWEETS:
            self.__write_file(selected_tweet.user_id, filename)

    def __create_file(self, selected_tweet, filename):
        """Cria um arquivo com a lista."""
        values = self.__request_values(selected_tweet, filename)
        with open(Constants.FOLDER_PATH + filename, Constants.ARQUIVO_ESCRITA_ZERADA) as write_file:
            values_dict = {
                selected_tweet.user_id: values
            }
            write_file.write(json.dumps(values_dict))
            write_file.write("\n")
            write_file.close()

    def __write_file(self, user_id, filename):
        """Escrever o friend/follow no arquivo."""
        values = self.__request_values(user_id, filename)
        with open(Constants.FOLDER_PATH + filename, Constants.ARQUIVO_APENAS_LEITURA) as read_file:
            dict_values = {
                user_id: values
            }
            file_txt = read_file.read()
            read_file.close()
            file_txt = file_txt[:-2]
            with open(Constants.FOLDER_PATH + filename, Constants.ARQUIVO_ESCRITA_ZERADA) as write_file:
                write_file.write(file_txt)
                write_file.write(", ")
                write_file.write("\n")
                next_data = json.dumps(dict_values)
                next_data = next_data[1:]
                write_file.write(next_data)
                write_file.close()

    def __request_values(self, selected_tweet, filename):
        if filename is not Constants.FILE_RETWEETS:
            request_type = Constants.REQUEST_TYPE_FOLLOWERS if filename == Constants.FILE_FOLLOWERS \
                else Constants.REQUEST_TYPE_FRIENDS
            try:
                params = {"user_id": selected_tweet.user_id, "count": "100000"}
                response = self.__premium_auth.request(request_type, params=params)
                return json.loads(response.text)["ids"]
            except HTTPError as e:
                if e.code == 429:
                    time.sleep(5)
        else:
            self.__get_retweets(selected_tweet)

    @staticmethod
    def __load_file(user_id, filename):
        """Carrega os amigos do user_id do arquivo."""
        with open(Constants.FOLDER_PATH + filename, Constants.ARQUIVO_APENAS_LEITURA) as json_file:
            text_file = json_file.read()
            file_values = json.loads(text_file).items()
            for key, value in file_values:
                if str(user_id) == str(key):
                    json_file.close()
                    return value
            return None
