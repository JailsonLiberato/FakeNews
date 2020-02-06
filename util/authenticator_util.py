from TwitterAPI import TwitterAPI
from requests_oauthlib import OAuth1Session
from util.constants import Constants


class AuthenticatorUtil:
    """Classe utilitária para obter as autenticações com o Twitter."""

    @staticmethod
    def get_standard_authentication():
        """Realiza a autenticação básica, onde será responsável pelas consultas de retweets, friends, followers"""
        return OAuth1Session(Constants.CONSUMER_KEY,
                             client_secret=Constants.CONSUMER_SECRET,
                             resource_owner_key=Constants.ACCESS_TOKEN,
                             resource_owner_secret=Constants.ACCESS_TOKEN_SECRET)

    @staticmethod
    def get_premium_authentication():
        """Realiza a autenticação premium, que será utilizada apenas para consulta inicial do Twitter."""
        return TwitterAPI(Constants.CONSUMER_KEY, Constants.CONSUMER_SECRET,
                          Constants.ACCESS_TOKEN, Constants.ACCESS_TOKEN_SECRET)
