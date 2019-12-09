import matplotlib.pyplot as plt
import networkx as nx


class GraphUtil:

    def generate_grafo(self, vertice):
        g = nx.Graph()
        g.add_nodes_from(['Jajá', 'Jejé', 'Juju'])
        g.add_edge('Jajá', 'Jejé', weight=0.4)
        g.add_edge('Jajá', 'Juju', weight=0.6)
        g.add_edge('Jejé', 'Juju', weight=0.2)
        nx.draw(g, node_color='#A0CBE2',
                width=2, with_labels=True, font_weight='bold')
        plt.show()


if __name__ == "__main__":
    g = GraphUtil()
    g.generate_grafo()
