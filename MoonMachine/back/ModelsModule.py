from django.db import models
from back.Database.Queryer import Queryer
from django.contrib.auth.models import User
from django.conf import settings
from django.http.request import HttpRequest

from back.SelectionOptions.ModelLimits import *
from back.SelectionOptions.MarketAction import MarketAction

from datetime import datetime
from decimal import Decimal
import csv
from io import StringIO
from logging import Logger, getLogger

from collections.abc import MutableSequence
from overrides import overrides

################################################
##DATABASE TABLES
class transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, db_column = 'user_id', db_index = False)
    cloud_transaction = models.CharField(max_length = FAIR_STRING_SIZE)

    managers_pair_symbol = models.CharField(max_length = FAIR_STRING_SIZE)
    market_action = models.CharField(max_length=MARKET_ACTION_ENUM_LENGTH)

    primary_security = models.CharField(max_length=MARKET_ACTION_ENUM_LENGTH)
    secondary_security = models.CharField(max_length=MARKET_ACTION_ENUM_LENGTH)
    received_amount = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=SUPER_MAX_DIGITS)
    given_amount = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=SUPER_MAX_DIGITS)
    date = models.DateField()    

    current_exposure = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=SUPER_MAX_DIGITS)

    def Fill(self, inputUserId, inputCloudId, inputManagersPairSymbolStr, stateMarketAction, inputPrimarySecurityStr, inputSecondarySecurityStr, inputTransactionTime, inputlastTransaction, inputReceivedAmount = Decimal, inputGivenAmount = Decimal,  **kwargs): #fixed bug where could not import transaction. just leave it blank ffs
        """all arguments are optional. will save the object"""
        log = getLogger(str(self.__class__)) # temporary variable since I have no idea what will happen if you store a property on a database record
        log.info('filling transaction object...')

        user_id = inputUserId
        
        cloud_transaction = inputCloudId

        if inputLastTransaction is not type:
            current_exposure = self.__CalculateCurrentExposure(inputLastTransaction.current_exposure)

        else:
            current_exposure = self.__CalculateCurrentExposure(Decimal())

        if inputManagersPairSymbolStr is not type:
            managers_pair_symbol = inputManagersPairSymbolStr

        if stateMarketAction == MarketAction.HOLD:
            log.error("A transaction cannot have the state: " + MarketAction.HOLD)
            raise Exception()

        market_action = stateMarketAction

        primary_security = inputPrimarySecurityStr

        secondary_security = inputSecondarySecurityStr

        if inputReceivedAmount is not Decimal:
            received_amount = inputReceivedAmount

        if inputReceivedAmount is not Decimal:
            given_amount = inputGivenAmount

        self.date = inputTransactionTime

        self.save()
        log.info('Transaction ' + str(self.date) + ' filled')

    def __CalculateCurrentExposure(self, previousExposure = Decimal):
        if possiblePrevious.marketAction == MarketAction.BUY:
                currentExposure -= previousExposure

        elif transaction.marketAction == MarketAction.SELL:
            currentExposure += previousExposure

class marketinfo(models.Model):
    market_pair = models.CharField(max_length = FAIR_STRING_SIZE)
    #current_ticker_open = models.DecimalField(max)
    #current_ticker_close = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=AVERAGE_DECIMAL_PLACES)
    #current_ticker_high = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=AVERAGE_DECIMAL_PLACES)
    #current_ticker_close = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=AVERAGE_DECIMAL_PLACES)
    #current_ticker_volume = 
    miscellaneous = models.CharField(max_length = SERIALIZED_DATA_LIMIT)

    def Fill(self, inputMarketPair = str, **kwargs):
        """will save the object"""
        log = getLogger(str(self.__class__))
        log.info('filling market info object...')

        if inputMarketPair is not str:
            self.market_pair = inputMarketPair

        if kwargs is not None: #kwargs default state
            with StringIO() as fileLikeObj:
                log.info('serializing ' + str(len(kwargs)) + ' key word arguments to csv.')
                serialiser = csv.writer(fileLikeObj, delimiter='#')
                keyWordItems = kwargs.items()

                for key, value in keyWordItems:
                    serialiser.writerow([key, value])
                
                writersValues = fileLikeObj.getvalue()
                valuesLength = len(writersValues)
                finalLength = valuesLength + 1
                stringsToJoin = [] * finalLength

                if self.miscellaneous is not None:
                    stringsToJoin[0] = self.miscellaneous

                for index in range(valuesLength): #range starts from 0 and ends one before the stop argument
                    correctedIndex = index + 1 if index != valuesLength - 1 else index
                    stringsToJoin[correctedIndex] = writersValues[index] # im building self.misc this way because this string has the potential to greatly impact performance.

                self.miscellaneous = str().join(stringsToJoin)

        else:
            self.miscellaneous = str()
                
        self.save()
        log.info('filled the market info object.')

class strategy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, db_column = 'user_id', db_index = False)
    language = models.ForeignKey("language", on_delete = models.CASCADE, db_column = 'language_id', db_index = False)

    bits = models.BinaryField()
    is_compiled = models.BooleanField(default = False)
    compilation_result = models.CharField(max_length = SERIALIZED_DATA_LIMIT)

    name = models.CharField(max_length = FAIR_STRING_SIZE)
    description = models.CharField(max_length = DESCRIPTION)    

    def Fill(self, userId = int, inputLanguageId = int, inputBits = bytes, inputCompilationStatus = bool, inputCompilationResult = str, inputName = str, inputDescription = str):
        """will save the object. bytes optional"""
        log = getLogger(str(self.__class__))
        log.info('filling strategy record...')

        #foreign keys
        if userId is not int:
            self.user_id = userId

        if inputLanguageId is not int:
            self.language_id = inputLanguageId

        if inputBits is not bytes:
            self.bits = inputBits

        else:
            self.bits = bytes()

        if inputCompilationResult is not str:
            self.compilation_result = inputCompilationResult

        else:
            self.compilation_result = ""

        if inputCompilationStatus is not bool:
            self.is_compiled = inputCompilationStatus

        else:
            self.is_compiled = False
        


        if inputName is not str:
            self.name = inputName

        else:
            self.name = ""

        if inputDescription is not str:
            self.description = inputDescription

        else:
            self.description = ""

        self.save()
        log.info('filled the strategy record.')

class language(models.Model):
    language = models.CharField(max_length = AVERAGE_DECIMAL_PLACES)

class usersstrategy(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, db_column = 'user_id', db_index = False)
    strategy = models.ForeignKey("strategy", on_delete = models.CASCADE, db_column = 'strategy_id', db_index = False)

    def Fill(self, strategyId, userId): #all foreign keys are required
        self.strategy_id = strategyId
        self.user_id = userId

        self.save()


##################################################
##SERVER MODELS
class Order(object):    
    """orders must have enough information to convert to a transaction."""
    def __init__(self, cloudOrderIdInt = int, managersPairSymbolStr = str, primarySecurityStr = str, secondarySecurityStr = str, stateMarketAction = MarketAction, inputReceivedAmount = Decimal, inputGivenAmountDec = Decimal, inputOrderTimeDatetime = datetime, **kwargs):
        if state == MarketAction.HOLD:
            getLogger().error("An order cannot have the state: " + str(MarketAction.HOLD))
            raise Exception()

        self.__cloudOrderId = cloudOrderId
        self.__pairsSymbol = managersPairSymbol
        self.__primary = primarySecurity
        self.__secondary = secondarySecurity
        self.__orderState = state
        self.__receivedAmount = receivedAmount
        self.__GivenAmount = givenAmount
        self.__orderTime = orderTime

        if self.__miscellaneous is not None:
            self.__miscellaneous = {}

        if kwargs is not None:
            self.__miscellaneous.update(kwargs)

    def GetCloudOrderId(self):
        return self.__cloudOrderId

    def GetManagersPair(self):
        return self.__pairsSymbol

    def GetPrimarySecurity(self):
        return self.__primary

    def GetSecondarySecurity(self):
        return self.__secondary

    def GetOrderState(self):
        return self.__orderState

    def GetReceivedAmount(self):
        return self.__receivedAmount

    def GetGivenAmount(self):
        return self.__GivenAmount

    def GetTimeOf(self):
        return self.__orderTime

    def GetMiscellaneousProperties(self):
        return self.__miscellaneous

class LabeledBar(object):
    def __init__(self, bar, labels = list):   
        self.Labels = labels  
        self.Bar = bar

class DatedLabel(object):
    """Date will be rounded down to the nearest hour."""
    def __init__(self, date = datetime, label = str):
        self.Date = date
        self.Label = str

class LabeledBarSeries(MutableSequence):
    def __init__(self, listOfNormalBars = list, listOfDatedLabels = list):
        """creates a series of LabeledBars by tagging bars with their closest labels. datetimes are automatically rounded down to the nearest day."""
        super().__init__()
        self.UnderlyingBars = BarDataSeries()
        self.__combined = list()
        self.__log = Logger(str(self.__class__))
        self.__log.info("constructing.")

        for currentBar in listOfNormalBars:
            self.UnderlyingBars.append(currentBar)
            labeledBarWip = LabeledBar(currentBar, [])
            barsDate = labeledBarWip.Bar.getDateTime()

            for datedLabel in listOfDatedLabels:
                #datetimes are immutable
                datedLabel.Date = datetime.replace(datedLabel.Date, hour = 0, minute = 0, second = 0, microsecond = 0) #im using a class method version in order to get at design time intellisense of a boxed datetime

                if datedLabel.Date <= barsDate: #assuming bar dates are ordered                    
                    self.__removePreviousOccurrencesOfLabel(datedLabel.Label) 
                    labeledBarWip.Labels.append(datedLabel.Label)

            self.__combined.append(labeledBarWip)         
            
        self.__log.info(str(self.__class__) + "constructed. ")

    def __removePreviousOccurrencesOfLabel(self, label = str):
        counter = 0

        for removalBar in self.__combined:
            for comparisonLabel in reverse(removalBar.Labels): #removing in reverse order ensures that the working index does not change
                if comparisonLabel == label:
                    counter += 1
                    removalBar.Labels.remove(comparisonLabel)

        self.__log.info("Duplicate labels of title '" + label + "' removed: " + str(counter))

    @overrides
    def append(self, value = LabeledBar):
        self.__combined.append(value)

    @overrides
    def clear(self):
        self.__combined.clear()

    @overrides
    def count(self, value):
        self.__log.error("count override not supported")
        raise NotImplementedError()

    @overrides
    def extend(self, values = list):
        self.__combined.extend(list)

    @overrides
    def index(self, value, start = 0, stop = None):
        return self.__combined.index(value, start, stop)

    @overrides
    def insert(self, index, value):
        self.__combined.insert(index, value)

    @overrides
    def pop(self, index):
        return self.__combined.pop(index)

    @overrides
    def remove(self, value):
        self.__combined.remove(value)

    @overrides
    def reverse(self):
        self.__combined.reverse()

    @overrides
    def __delitem__(self, index):
        self._combined.remove(index)

    @overrides 
    def __setitem__(self, index, value):
        self.__combined[index] = value

    def __len__(self):
        return len(self.__combined)

    def __getitem__(self, index):
        return self.__combined[index]

