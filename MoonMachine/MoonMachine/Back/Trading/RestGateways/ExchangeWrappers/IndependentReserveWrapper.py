from Back.Trading.RestGateways.ExchangeWrappers.IExchangeWrapper import IExchangeWrapper
from Back.ModelsModule import LabeledBar, Transaction, Order, LabeledBarSeries
from ccxt.independentreserve import independentreserve
from overrides import overrides
import json
from datetime import datetime
from logging import getLogger, Logger
from decimal import Decimal
from Back.SelectionOptions.MarketAction import MarketAction
from functools import reduce

class IndependentReserveWrapper(IExchangeWrapper):
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
        self.__base = independentreserve()
        self.__base.load_markets()
        deets = self.__base.describe()
        self.__name = deets['name'].lower()
        self.__rateLimit = deets['rateLimit'] / 1000
        self.__profitPercentage = Decimal('0.02')


    @overrides
    def Name(self):
        return self.__name

    @overrides
    def AttemptAuthentication (self, authDetails = dict):
        try:            
            self.__base.apiKey = authDetails[self.Name()]['apiKey']
            self.__base.secret = authDetails[self.Name()]['secret']

        except Exception as e:
            error = 'wrong format in auth file for exchange: ' + self.Name() + ". " + str(e)
            self._log.error(error)
            return error

        try:
            self.__base.fetch_balance()
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
            IndependentReserveWrapper.SPECULATED_SECURITY  : secondarySecurity,
            IndependentReserveWrapper.HOARDED_SECURITY : primarySecurity,
            IndependentReserveWrapper.ORDER_TYPE : 'LimitOffer',
            IndependentReserveWraper.PRICE : receiveAmount,
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
                IndependentReserveWrapper.SPECULATED_SECURITY  : speculatedSecurity,
                IndependentReserveWrapper.HOARDED_SECURITY : hoardedSecurity,
                IndependentReserveWrapper.PAGE_INDEX : str(pageIndex),
                IndependentReserveWrapper.PAGE_SIZE : str(pageSize)
            })
            sleep(self.ExchangesRateLimit())
            mapOutputAsList = list(map(self._MapJsonToOrder, response[IndependentReserveWrapper.DATA], managersName))
            combinedData += mapOutputAsList
            self._log.info('appended the page for a running total of ' + str(len(combinedData)))

            if pageIndex < response[IndependentReserveWrapper.TOTAL_PAGES]:
                pageIndex += 1

            else:
                return combinedData

    @overrides
    def CancelOrder(self, order = Order, userId = int, previousTransaction = Transaction):
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
                IndependentReserveWrapper.SPECULATED_SECURITY  : secondarySecurity,
                IndependentReserveWrapper.HOARDED_SECURITY : primarySecurity,
                IndependentReserveWrapper.PAGE_INDEX : str(pageIndex),
                IndependentReserveWrapper.PAGE_SIZE : str(pageSize)   
            })
            sleep(self.ExchangesRateLimit())

            #combined all partial transactions into one transaction
            for model in filledOrdersResponse[IndependentReserveWrapper.DATA]:
                if model[IndependentReserveWrapper.ORDER_GUID] == order.GetCloudOrderId():
                    combinedData.append(model)

            self._log.info('appended the page for a running total of ' + str(len(combinedData)))

            if pageIndex < filledOrdersResponse[IndependentReserveWrapper.TOTAL_PAGES]:
                pageIndex += 1

            elif len(combinedData) > 0:
                transactionInitializer = Transaction()
                transactionInitializer.Fill(inputUserId=userId,
                                            inputCloudId=order.GetCloudOrderId(),
                                            inputManagersPairSmbolStr=order.GetManagersPair(),
                                            stateMarketAction=order.GetOrderState(),
                                            inputPrimarySecurityStr=order.GetPrimarySecurity(),
                                            inputSecondarySecurityStr=order.GetSecondarySecurity(),
                                            inputTransactionTime=order.GetTimeOf(),
                                            inputlastTransaction=previousTransaction)
                finishedTransaction = reduce(self._ReduceToTransaction, combinedData, transactionInitializer)
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

        if jsonObject[IndependentReserveWrapper.ORDER_TYPE] is 'LimitOffer':
            marketAction = MarketAction.BUY
            currentReceivedAmount = jsonObject[IndependentReserveWrapper.VALUE]
            currentGivenAmount = jsonObject[IndependentReserveWrapper.VOLUME]

        else:
            marketAction = MarketAction.SELL
            currentReceivedAmount = jsonObject[IndependentReserveWrapper.VOLUME]
            currentGivenAmount = jsonObject[IndependentReserveWrapper.VALUE]

        return Order(jsonObject[IndependentReserveWrapper.ORDER_GUID], #fixed bug where order guid's label is pascal case
                     managersName,                     
                     jsonObject[IndependentReserveWrapper.HOARDED_SECURITY],
                     jsonObject[IndependentReserveWrapper.SPECULATED_SECURITY],
                     marketAction,
                     currentReceivedAmount,
                     currentGivenAmount,
                     jsonObject['CreatedTimestampUtc'])

    @overrides
    def _ReduceToTransaction(self, wipTransaction = Transaction, jsonOrder = dict):
        """requires all values common between jsonOrders to be prefilled."""
        currentReceivedAmount = None
        currentGivenAmount = None

        if wipTransaction.market_action is MarketAction.BUY:
            currentReceivedAmount += jsonOrder[IndependentReserveWrapper.VOLUME]
            currentGivenAmount += jsonOrder[IndependentReserveWrapper.VALUE]

        elif wipTransaction.market_action is MarketAction.SELL:
            currentReceivedAmount += jsonOrder[IndependentReserveWrapper.VALUE]
            currentGivenAmount += jsonOrder[IndependentReserveWrapper.VOLUME]

        wipTransaction.received_amount += currentReceivedAmount
        wipTransaction.given_amount += currentGivenAmount

        return wipTransaction
