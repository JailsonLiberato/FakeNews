import matplotlib.pyplot as plt
import networkx as nx

from entity.network import Network
from service.twitter_service import TwitterService
from util.constants import Constants


class NetworkService:

    def __init__(self):
        self.__friends = []
        self.__followers = []
        self.__twitter_service = TwitterService()
        self.__retweets = []

    def create_network(self, selected_tweet, retweets, friends, followers):
        """Cria a rede."""
        network: Network = Network(selected_tweet.user_id)
        self.__retweets = retweets
        for ret in retweets:
            if int(ret) in friends or int(ret) in followers:
                network_friend: Network = Network(str(ret))
                network.children.append(network_friend)
        network = self.__create_network_recursive(network)
        self.__draw_graph(network)

    def __create_network_recursive(self, network):
        for chi in network.children:
            self.__friends = self.__twitter_service.get_features_by_user_id(chi.id, Constants.FILE_FRIENDS)
            self.__followers = self.__twitter_service.get_features_by_user_id(chi.id, Constants.FILE_FOLLOWERS)
            for ret in self.__retweets:
                if int(ret) in self.__friends:
                    net: Network = Network(ret)
                    chi.children.append(net)
                    self.__retweets.remove(ret)
            if chi.children:
                self.__create_network_recursive(chi)
        return network

    def __edges_recursive(self, id, graph, network):
        for chi in network.children:
            graph.add_edge(id, chi.id)
            if chi.children:
                self.__edges_recursive(chi.id, graph, chi)
        return graph

    def __draw_graph(self, network):
        graph = nx.Graph()
        self.__edges_recursive(network.id, graph, network)
        nx.draw(graph)
        plt.savefig("results/tweets_Network.png")
        plt.show()
