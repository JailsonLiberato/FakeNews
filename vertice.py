class Vertice:
    """Classe responsável pelo agrupamento de vértices."""

    def __init__(self, tweet):
        self.__id = tweet.author.id
        self.__value = tweet.text
        self.__screen_name = tweet.author.screen_name
        self.__vertices = []

    @property
    def id(self):
        return self.__id

    @property
    def value(self):
        return self.__value

    @property
    def screen_name(self):
        return self.__screen_name

    @property
    def followers(self):
        return self.__followers

    @property
    def vertices(self):
        return self.__vertices

    def __repr__(self):
        return self.screen_name
