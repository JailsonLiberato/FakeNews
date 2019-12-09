class Vertice:
    """Classe responsável pelo agrupamento de vértices."""

    def __init__(self, tweet, api):
        self.__id = tweet.author.id
        self.__value = tweet.text
        if hasattr(tweet, 'retweeted_status'):
            self.__retweets = tweet.retweeted_status
        self.__followers = api.friends_ids(tweet.author.screen_name)

    @property
    def id(self):
        return self.__id

    @property
    def value(self):
        return self.__value

    @property
    def retweets(self):
        return self.__retweets

    @property
    def followers(self):
        return self.__followers
