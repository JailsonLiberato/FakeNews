import json

from tweet import Tweet
from util.authenticator_util import AuthenticatorUtil
from util.constants import Constants
from util.file_util import FileUtil


class TwitterService:
    """Serviço do Twitter."""

    def __init__(self):
        self.__filename = ''
        self.__search_term = ''
        self.__tweets = []
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
        tweet_selected: Tweet = None
        for tweet in self.__tweets:
            if tweet_selected is None:
                tweet_selected = tweet
            elif tweet_selected is not None and tweet_selected.retweet_count < tweet.retweet_count \
                    and tweet_selected.followers_count < \
                    tweet.followers_count:
                tweet_selected = tweet
                return tweet_selected

    def get_retweets(self):
        pass

    def get_friends(self):
        pass

    def get_followers(self):
        pass
