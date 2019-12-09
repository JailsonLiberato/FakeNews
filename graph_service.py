from graph_util import GraphUtil


class GraphService:
    """Classe de serviço de grafos."""

    def __init__(self):
        self.__graph = []

    def execute(self, vertices):
        for vertice in vertices:
            self.__graph = GraphUtil.generate_grafo(vertice, self.__graph)
        GraphUtil.plot_graph(self.__graph)
