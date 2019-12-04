import matplotlib.pyplot as plt
import networkx as nx


class GraphUtil:

    def generate_grafo(self):
        G = nx.petersen_graph()
        plt.subplot(121)
        nx.draw(G, with_labels=True, font_weight='bold')
        plt.subplot(122)
        nx.draw_shell(G, nlist=[range(5, 10), range(5)], with_labels=True, font_weight='bold')
        plt.show()


g = GraphUtil()
g.generate_grafo()
