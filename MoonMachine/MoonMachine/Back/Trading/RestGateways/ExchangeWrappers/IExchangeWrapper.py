from abc import ABC, abstractmethod, abstractproperty
from Back.ModelsModule import Order, Transaction
from decimal import Decimal
from functools import partial
from time import sleep
from logging import getLogger
from Back.Trading.RestGateways.BubbleWrapRequester import BubbleWrapRequester

class IExchangeWrapper(ABC, BubbleWrapRequester):
    """description of class"""
    def __init__(self):
        self._log = getLogger(str(self.__class__))
        ABC.__init__(self)    
        BubbleWrapRequester.__init__(self)    

    @abstractmethod
    def Name(self):
        raise NotImplementedError()

    @abstractmethod
    def AttemptAuthentication(self, authDetails = dict):
        raise NotImplementedError()

    @abstractmethod
    def GetMarketUpdate(self, lastKnownBar = None, labels = list, pairsSymbol = str):
        raise NotImplementedError()

    @abstractmethod
    def Buy(self, pairsSymbol = str, giveAmount = Decimal, receiveAmount = Decimal):
        raise NotImplementedError()

    @abstractmethod
    def Sell(self, pairsSymbol = str, giveAmount = Decimal, receiveAmount = Decimal):
        raise NotImplementedError()

    @abstractmethod
    def ExchangesFeePercentage(self):
        raise NotImplementedError()

    @abstractmethod
    def GetOpenOrders(self, primarySecurity = str, secondarySecuity = str, managersName = str):        
        raise NotImplementedError()

    @abstractmethod
    def CancelOrder(self, order = Order, userId = int):
        raise NotImplementedError() 

    @abstractmethod
    def ExchangesRateLimit(self):
        raise NotImplementedError()

    @abstractmethod
    def _MapJsonToOrder(self, jsonObject = dict):
        raise NotImplementedError()
    
    @abstractmethod
    def _ReduceToTransaction(self, wipTransaction = Transaction, jsonObject = dict):
        raise NotImplementedError()