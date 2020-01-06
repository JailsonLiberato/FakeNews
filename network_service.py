import networkx as nx
import matplotlib.pyplot as plt


class NetworkService:
    """Serviço de redes."""

    def __init__(self):
        self.__network = nx.Graph()

    def generate_network(self, network):
        """Gerando a rede."""
        self.__network.add_node(network.id)
        if network.children:
            for net in network.children:
                self.__network.add_node(net.id)
                self.__network.add_edge(network.id, net.id)
                self.generate_network(net)
                return

    def plot_network(self):
        """Plota a rede."""
        plt.subplot(121)
        nx.draw(self.__network, node_color='#A0CBE2',
                width=2, with_labels=True, font_weight='bold')
        plt.show()
