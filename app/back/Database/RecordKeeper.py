from back.ModelsModule import Order, transaction, marketinfo
from back.Database.Queryer import Queryer

from logging import getLogger
from decimal import Decimal

from django.contrib.auth.models import User
from django.http.request import HttpRequest


class RecordKeeper(Queryer):
    """description of class"""
    def __init__(self): #fixed bug where the naming convention for constructor was missing an underscore on each side
        super().__init__()

    def Authenticate(self, authCredentials = list):
        return ""

    def GetTransactions(self):
        raise NotImplementedError()

    def GetLastTransaction(self, userId = int, managersName = str):
        """Can return None!"""
        query = transaction.objects.filter(user_id = userId, managers_pair_symbol = managersName) .order_by('date') #it does have objects
        return self._TestQuery(query, self.__GetLastTransactionOnSuccess)        

    def __GetLastTransactionOnSuccess(self, query):
        return query.last()

    def GetMarketSummaries(self):
        raise NotImplementedError()

    def GetOneMarketSummary(self):
        raise NotImplementedError()

    def GetMarketInfo(self, marketName = str, currentUserId = int):
        """Can return None!"""

        possibleMatch = marketinfo.objects.filter(market_pair = marketName, user_id = currentUserId)  #it does have objects
        return self._TestQuery(possibleMatch, self.__GetMarketInfoOnSuccess)

    def __GetMarketInfoOnSuccess(self, query):
        return query.first()