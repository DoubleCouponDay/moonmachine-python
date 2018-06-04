from Back.ModelsModule import Order
import logging
from decimal import Decimal

class ExecutiveAnalyzer(object):
    """description of class"""
    def __init__(self):
        self.__log = logging.getLogger(str(self.__class__))

    def ForumlateDecision(self):
        pass

    def GetMinimumProfitPrice(self, purchasePrice = Decimal, exchangeFeePercentage = Decimal): 
        self.__log.info("Calculating the minimum profit price of sale...")
        self.__log.info("purchasePrice: " + str(purchasePrice))                      
        self.__log.info("exchangeFeePercentage: " + str(exchangeFeePercentage))
        calculatedPrice = purchasePrice + (purchasePrice * exchangeFeePercentage)
        self.__log.info("calculated to " + str(calculatedPrice))
        return calculatedPrice
        