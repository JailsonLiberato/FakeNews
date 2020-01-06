class Network:
    """Entidade de Rede para geração do grafo."""

    def __init__(self, id):
        self.__id = id
        self.__children = []

    @property
    def id(self):
        return self.__id

    @property
    def children(self):
        return self.__children
