from back.RestGateways.iexchangewrapper import IExchangeWrapper
from back.models import transaction, Order
from ccxt.independentreserve import independentreserve
from overrides import overrides
import json
from datetime import datetime
from logging import getLogger, Logger
from decimal import Decimal
from back.SelectionOptions.marketaction import marketaction
from functools import reduce
from time import sleep

class exchangewrapper(IExchangeWrapper):
    """description of class"""
    SPECULATED_SECURITY = 'primaryCurrencyCode' #fixed bug where labels are lowercase
    HOARDED_SECURITY = 'secondaryCurrencyCode'
    VALUE = 'Value'
    VOLUME = 'Volume'
    PAGE_INDEX = 'pageIndex'
    PAGE_SIZE = 'pageSize'
    TOTAL_PAGES = 'TotalPages'
    DATA = 'Data'
    PRICE = 'price'
    ORDER_TYPE = 'orderType'
    ORDER_GUID = 'OrderGuid'

    def __init__(self):
        super().__init__()

        self.__apiKey = str()
        self.__apiSecret = str()
        # self.__base = independentreserve()
        # self.__base.load_markets()
        # deets = self.__base.describe()
        # self.__name = deets['name'].lower()
        # self.__rateLimit = deets['rateLimit'] / 1000
        self.__profitPercentage = Decimal('0.02')


    @overrides
    def Name(self):
        # return self.__name
        return ""

    @overrides
    def AttemptAuthentication (self, authDetails = dict):
        try:            
            # self.__base.apiKey = authDetails[self.Name()]['apiKey']
            # self.__base.secret = authDetails[self.Name()]['secret']
            pass

        except Exception as e:
            error = 'wrong format in auth file for exchange: ' + self.Name() + ". " + str(e)
            self._log.error(error)
            return error

        try:
            # self.__base.fetch_balance()
            pass
            return ''

        except Exception as e:
            error = 'authentication failed using given apiKey and secret for exchange: ' + self.Name() + ". " + str(e)
            self._log.error(error)
            return error

    @overrides
    def GetMarketUpdate(self, lastKnownBar = None, labels = list, pairsSymbol = str):
        """Returns a LabeledBar of todays market summary."""
        
        #response = requests.get (requestLocator)
        #jsonResult = response.json()
        #dateBarCreated = jsonResult['CreatedTimestampUtc']
        #DayHighestPrice = jsonResult['DayHighestPrice']
        #DayLowestPrice = jsonResult['DayLowestPrice']
        #DayVolumeXbt = jsonResult['DayVolumeXbt']
        #LastPrice = jsonResult['LastPrice']

        #dateBarCreated = datetime.utcfromtimestamp(dateBarCreated)

        #rawSummary = BasicBar(dateBarCreated,
        #                        lastKnownBar.getClose(),
        #                        DayHighestPrice,
        #                        DayLowestPrice,
        #                        LastPrice,
        #                        DayVolumeXbt,
        #                        LastPrice,
        #                        0,
        #                        None)

        #labeledSeries = LabeledBarSeries([labeledSummary], labels)
        #return labeledSeries

    @overrides
    def Buy(self, pairsSymbol = str, giveAmount = Decimal, receiveAmount = Decimal):
        return Order()

    @overrides
    def Sell(self, primarySecurity = str, secondarySecurity = str, giveAmount = Decimal, receiveAmount = Decimal):
        response = self._BubbleWrapRequest(self.__base.privatePostPlaceLimitOrder, {
            exchangewrapper.SPECULATED_SECURITY  : secondarySecurity,
            exchangewrapper.HOARDED_SECURITY : primarySecurity,
            exchangewrapper.ORDER_TYPE : 'LimitOffer',
            exchangewrapper.PRICE : receiveAmount,
            'volume': giveAmount,
        })
        sleep(self.ExchangesRateLimit())

    @overrides
    def ExchangesFeePercentage(self):
        self._log.info("returning a profit percentage of " + str(self.__profitPercentage))
        return self.__profitPercentage

    @overrides
    def GetOpenOrders(self, speculatedSecurity = str, hoardedSecurity = str, managersName = str):
        pageIndex = 1
        pageSize = 50
        combinedData = []

        while True:
            self._log.info('Fetching another page of open orders..')
            response = self._BubbleWrapRequest(self.__base.privatePostGetOpenOrders, {
                exchangewrapper.SPECULATED_SECURITY  : speculatedSecurity,
                exchangewrapper.HOARDED_SECURITY : hoardedSecurity,
                exchangewrapper.PAGE_INDEX : str(pageIndex),
                exchangewrapper.PAGE_SIZE : str(pageSize)
            })
            sleep(self.ExchangesRateLimit())
            mapOutputAsList = list(map(self._MapJsonToOrder, response[exchangewrapper.DATA], managersName))
            combinedData += mapOutputAsList
            self._log.info('appended the page for a running total of ' + str(len(combinedData)))

            if pageIndex < response[exchangewrapper.TOTAL_PAGES]:
                pageIndex += 1

            else:
                return combinedData

    @overrides
    def CancelOrder(self, order = Order, userId = int, previousTransaction = transaction):
        """Can return None!"""
        cancelsResponse = self._BubbleWrapRequest(self.__base.cancel_order, order.GetCloudOrderId())
        sleep(self.ExchangesRateLimit())
        pageIndex = 1
        pageSize = 50
        combinedData = []

        #paginate through filled orders
        while True:
            self._log.info('Fetching another page of partially filled transactions...')
            filledOrdersResponse = self._BubbleWrapRequest(self.__base.privatePostGetClosedFilledOrders, {
                exchangewrapper.SPECULATED_SECURITY  : order.GetSecondarySecurity(),
                exchangewrapper.HOARDED_SECURITY : order.GetPrimarySecurity(),
                exchangewrapper.PAGE_INDEX : str(pageIndex),
                exchangewrapper.PAGE_SIZE : str(pageSize)   
            })
            sleep(self.ExchangesRateLimit())

            #combined all partial transactions into one transaction
            for model in filledOrdersResponse[exchangewrapper.DATA]:
                if model[exchangewrapper.ORDER_GUID] == order.GetCloudOrderId():
                    combinedData.append(model)

            self._log.info('appended the page for a running total of ' + str(len(combinedData)))

            if pageIndex < filledOrdersResponse[exchangewrapper.TOTAL_PAGES]:
                pageIndex += 1

            elif len(combinedData) > 0:
                transactioninitializer = transaction()
                transactioninitializer.Fill(inputUserId=userId,
                                            inputCloudId=order.GetCloudOrderId(),
                                            inputManagersPairSymbolStr=order.GetManagersPair(),
                                            stateMarketAction=order.GetOrderState(),
                                            inputPrimarySecurityStr=order.GetPrimarySecurity(),
                                            inputSecondarySecurityStr=order.GetSecondarySecurity(),
                                            inputTransactionTime=order.GetTimeOf(),
                                            inputLastTransaction=previousTransaction)
                finishedTransaction = reduce(self._ReduceToTransaction, combinedData, transactioninitializer)
                finishedTransaction.save()
                return finishedTransaction

            else:
                return None

    @overrides
    def ExchangesRateLimit(self):
        return self.__rateLimit

    @overrides
    def _MapJsonToOrder(self, jsonObject = dict, managersName = str):
        marketAction = None
        currentReceivedAmount = None
        currentGivenAmount = None

        if jsonObject[exchangewrapper.ORDER_TYPE] is 'LimitOffer':
            marketAction = marketaction.BUY
            currentReceivedAmount = jsonObject[exchangewrapper.VALUE]
            currentGivenAmount = jsonObject[exchangewrapper.VOLUME]

        else:
            marketAction = marketaction.SELL
            currentReceivedAmount = jsonObject[exchangewrapper.VOLUME]
            currentGivenAmount = jsonObject[exchangewrapper.VALUE]

        return Order(jsonObject[exchangewrapper.ORDER_GUID], #fixed bug where order guid's label is pascal case
                     managersName,                     
                     jsonObject[exchangewrapper.HOARDED_SECURITY],
                     jsonObject[exchangewrapper.SPECULATED_SECURITY],
                     marketAction,
                     currentReceivedAmount,
                     currentGivenAmount,
                     jsonObject['CreatedTimestampUtc'])

    @overrides
    def _ReduceToTransaction(self, wipTransaction = transaction, jsonOrder = dict):
        """requires all values common between jsonOrders to be prefilled."""
        currentReceivedAmount = None
        currentGivenAmount = None

        if wipTransaction.market_action is marketaction.BUY:
            currentReceivedAmount += jsonOrder[exchangewrapper.VOLUME]
            currentGivenAmount += jsonOrder[exchangewrapper.VALUE]

        elif wipTransaction.market_action is marketaction.SELL:
            currentReceivedAmount += jsonOrder[exchangewrapper.VALUE]
            currentGivenAmount += jsonOrder[exchangewrapper.VOLUME]

        wipTransaction.received_amount += currentReceivedAmount
        wipTransaction.given_amount += currentGivenAmount

        return wipTransaction
