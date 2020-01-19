class Tweet:
    """Entidade Tweet."""

    def __init__(self, tweet_id, user_id, tweet_text, followers_count, friends_count, retweet_count: int = 0):
        self.__tweet_id = tweet_id
        self.__user_id = user_id
        self.__tweet_text = tweet_text
        self.__followers_count = followers_count
        self.__friends_count = friends_count
        self.__retweet_count = retweet_count

    @property
    def followers_count(self):
        return self.__followers_count

    @property
    def friends_count(self):
        return self.__friends_count

    @property
    def retweet_count(self):
        return self.__retweet_count
