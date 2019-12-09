import matplotlib.pyplot as plt
import networkx as nx


class GraphUtil:
    """Classe utilitária da montagem de grafo."""

    @staticmethod
    def generate_grafo(vertice, graph):
        """Gerador de grafos"""
        graph = GraphUtil.add_vertice(graph, vertice)
        return graph
        # graph.add_edge('Jejé', 'Juju', weight=0.2)

    @staticmethod
    def plot_graph(graph):
        """Plotar gráfico."""
        nx.draw(graph, node_color='#A0CBE2',
                width=2, with_labels=True, font_weight='bold')
        plt.show()

    @staticmethod
    def contains_vertice(graph, vertice):
        """Verifica se contém vértice."""
        return graph.has_node(vertice)

    @staticmethod
    def add_vertice(graph, vertice):
        """Adiciona um novo vértice."""
        if not graph:
            graph = nx.Graph()
        if not GraphUtil.contains_vertice(graph, vertice):
            graph.add_node(vertice)
        return graph


if __name__ == "__main__":
    graph_util = GraphUtil()
    graph_util.generate_grafo()
