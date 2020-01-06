class Tweet:
    """Entidade Tweet."""

    def __init__(self, id, user_id ,username, text, followers_count, friends_count):
        self.__id = id
        self.__user_id = user_id
        self.__username = username
        self.__text = text
        self.__followers_count = followers_count
        self.__friends_count = friends_count

    @property
    def followers_count(self):
        return self.__followers_count

    @property
    def username(self):
        return self.__username

    @property
    def id(self):
        return self.__id

    @property
    def user_id(self):
        return self.__user_id

    @property
    def text(self):
        return self.__text

    @property
    def friends_count(self):
        return self.__friends_count
