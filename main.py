import tweepy
from password_constants import PasswordConstants


class Main:

    @staticmethod
    def execute():
        auth = tweepy.OAuthHandler(PasswordConstants.CONSUMER_API_KEYS_KEY,
                                   PasswordConstants.CONSUMER_API_KEYS_SECRET_KEY)
        auth.set_access_token(PasswordConstants.ACCESS_TOKEN, PasswordConstants.ACCESS_TOKEN_SECRET)

        api = tweepy.API(auth)
        search_words = "Bolsonaro"
        date_since = "2018-01-01"
        date_until = "2018-11-31"
        tweets = tweepy.Cursor(api.search, q=search_words, lang="pt", since=date_since).items(100)
        for tweet in tweets:
            print("-------------0-------------------\n")
            print(f"{tweet.user.name}:{tweet.text}")
            print("\n")
            print("-------------0-------------------\n")
            print("RETWEET\n")
            if hasattr(tweet, 'retweeted_status'):
                print("-------------1-------------\n")
                print(tweet.retweeted_status.user.name)
                print("-------------1-------------\n")
            else:
                print("---------2------------------\n")
                print("NO NO")
                print("---------2------------------\n")
            print("\n###################################\n")



main = Main()
main.execute()
