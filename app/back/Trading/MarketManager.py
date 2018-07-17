from back.Database.RecordKeeper import RecordKeeper
from back.RestGateways.iexchangewrapper import IExchangeWrapper
from back.models import Order
from back.Trading.ExecutiveAnalyzer import ExecutiveAnalyzer
from back.SelectionOptions.marketaction import marketaction

import logging
from decimal import Decimal
from django.http.request import HttpRequest

class MarketManager(object):
    """description of class"""
    def __init__(self, speculatedSecurity = str, hoardedSecurity = str, exchangeInstance = IExchangeWrapper): #fixed bug where params were in the wrong order
        self.__log = logging.getLogger(str(self.__class__))
        self.__primarySecurity = speculatedSecurity #placed here since it controls which item to buy / sell. makes exchangewrapper a little more universal
        self.__secondarySecurity = hoardedSecurity
        self.__exchange = exchangeInstance
        self.__recordKeeper = RecordKeeper()
        self.__executiveAnalyzer = ExecutiveAnalyzer()
        self.__isAuthenticated = False   
        pairsSymbol = str.capitalize(hoardedSecurity + "/" + speculatedSecurity)
        self.__managerName = exchangeInstance.Name() + " " + pairsSymbol

        #volatile injections
        self.__multiThreadedRequest = None

        self.__log.info('marketManager created.')

    def SetRequestObject(self, injectedObject = HttpRequest):
        """You are unable to set this to none."""
        if injectedObject is not None:
            self.__multiThreadedRequest = injectedObject

    def GetManagerName(self):
        return self.__managerName

    def Work(self):
        if self.__isAuthenticated:
            pass

    def AttemptAuthentication(self, serviceCredentials = dict):
        authErrors = self.__exchange.AttemptAuthentication(serviceCredentials)
        authErrors = authErrors + self.__recordKeeper.Authenticate(serviceCredentials)

        if authErrors == "":
            self.__isAuthenticated = True

        else:
            self.__isAuthenticated = False

        return authErrors 

    def IsAuthenticated(self):
        return self.__isAuthenticated

    def Dispose(self):
        if self.__isAuthenticated:
            if self.__multiThreadedRequest is not None:
                self.__log.info("Beginning disposal of the " + self.GetManagerName() + " market.")
                cloudOpenOrders = self.__exchange.GetOpenOrders(self.__primarySecurity, self.__secondarySecurity, self.GetManagerName())

                #close open orders
                for order in cloudOpenOrders:                
                    if order.GetOrderState() == marketaction.BUY:
                        self.__log.info("Cancelling open buy order.")
                        lastTransaction = RecordKeeper().GetLastTransaction(self.__multiThreadedRequest.user, self.GetManagerName())
                        possibleCompletion = self.__exchange.CancelOrder(order, self.__multiThreadedRequest.user.id, lastTransaction)                         

            else:
                errorMessage = 'volatile multithreaded request object was not injected before dispose was called.'
                self.__log.error(errorMessage)
                raise Exception(errorMessage)

        else:
            self.__log.info("Market manager was not authenticated. Did not dispose.")

        self.__multiThreadedRequest = None
