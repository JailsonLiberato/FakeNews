from service.network_service import NetworkService
from service.twitter_service import TwitterService
from util.constants import Constants


class Main:
    """Classe principal do programa."""

    def __init__(self):
        self.__twitter_service: TwitterService = TwitterService()
        self.__network_service: NetworkService = NetworkService()

    def execute(self):
        """Execução principal da classe."""
        selected_tweet = self.__twitter_service.search_tweet(Constants.SEARCH_TERM_FAKE,
                                                             Constants.FILE_FAKE_NAME)
        retweets = self.__twitter_service.get_features(selected_tweet, Constants.FILE_RETWEETS)
        friends = self.__twitter_service.get_features(selected_tweet, Constants.FILE_FRIENDS)
        followers = self.__twitter_service.get_features(selected_tweet, Constants.FILE_FOLLOWERS)
        self.__network_service.create_network(selected_tweet, retweets, friends, followers)


if __name__ == "__main__":
    main = Main()
    main.execute()
