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
        self.__create_network_recursive(network)

    def __create_network_recursive(self, network):
        for chi in network.children:
            self.__friends = self.__twitter_service.get_features(chi.id, Constants.FILE_FRIENDS)
            self.__followers = self.__twitter_service.get_features(chi.id, Constants.FILE_FOLLOWERS)
            for ret in self.__retweets:
                if ret in self.__friends:
                    net: Network = Network(ret)
                    chi.children.append(net)
            if chi.children:
                self.__create_network_recursive(chi)

    def __draw_graph(self):
        G = nx.Graph()
        with open(Constants.FOLDER_PATH + Constants.FILE_FRIENDS, "r") as json_file:
            x = json_file.read()  # Ler o arquivo com as listas de amigos
            self.__friend_file = json.loads(
                x).items()  # obtém os itens presentes no arquivo como uma lista de (key, value)

            # key     #value
        for user_id, friends in self.__friend_file:  # friends representa a lista de amigos de user_id,
            user_id = int(user_id)
            for friend in friends:  # percorre a lista de amigos e adiciona arestas que ligam cada amigo presente na lista ao user_id
                G.add_edge(user_id, friend)
        # nx.draw(G,with_labels=True) caso que gerar o grafo com o id que identifica cada vértice
        nx.draw(G)
        plt.savefig("tweets_Network.png")  # salva o grafo em uma imagem
        plt.show()
