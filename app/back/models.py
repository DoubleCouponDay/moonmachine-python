from django.db import models
from back.Database.Queryer import Queryer
from django.contrib.auth.models import User
from django.conf import settings
from django.http.request import HttpRequest
from back.SelectionOptions.ModelLimits import *
from back.SelectionOptions.marketaction import marketaction
from datetime import datetime
from decimal import Decimal
import csv
from io import StringIO
from logging import Logger, getLogger
from collections.abc import MutableSequence
from overrides import overrides
from phonenumber_field.modelfields import PhoneNumberField


################################################
##DATABASE TABLES
class transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, db_column = 'user_id', db_index = False)
    cloud_transaction_id = models.CharField(max_length = FAIR_STRING_SIZE)

    managers_pair_symbol = models.CharField(max_length = FAIR_STRING_SIZE)
    market_action = models.CharField(max_length=MARKET_ACTION_ENUM_LENGTH)

    primary_security = models.CharField(max_length=MARKET_ACTION_ENUM_LENGTH)
    secondary_security = models.CharField(max_length=MARKET_ACTION_ENUM_LENGTH)
    received_amount = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=SUPER_MAX_DIGITS, default=Decimal())
    given_amount = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=SUPER_MAX_DIGITS, default=Decimal())
    date = models.DateField()    

    current_exposure = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=SUPER_MAX_DIGITS)

    def Fill(self, inputUserId, inputCloudId, inputManagersPairSymbolStr, stateMarketAction, inputPrimarySecurityStr, inputSecondarySecurityStr, inputTransactionTime, inputLastTransaction, inputReceivedAmount = Decimal, inputGivenAmount = Decimal,  **kwargs): #fixed bug where could not import transaction. just leave it blank ffs
        """inputreceivedamount and inputgivenamount are optional. will save the object"""
        log = getLogger(str(self.__class__)) # temporary variable since I have no idea what will happen if you store a property on a database record
        log.info('filling transaction object...')

        self.user_id = inputUserId
        
        self.cloud_transaction_id = inputCloudId

        if inputLastTransaction is not type:
            self.current_exposure = self.__CalculateCurrentExposure(inputLastTransaction)

        else:
            self.current_exposure = self.__CalculateCurrentExposure(None)

        if inputManagersPairSymbolStr is not type:
            self.managers_pair_symbol = inputManagersPairSymbolStr

        if stateMarketAction == marketaction.HOLD:
            log.error("A transaction cannot have the state: " + marketaction.HOLD)
            raise Exception()

        self.market_action = stateMarketAction

        self.primary_security = inputPrimarySecurityStr

        self.secondary_security = inputSecondarySecurityStr

        if inputReceivedAmount is not type:
            self.received_amount = inputReceivedAmount

        if inputReceivedAmount is not type:
            self.given_amount = inputGivenAmount

        self.date = inputTransactionTime

        self.save()
        log.info('Transaction ' + str(self.date) + ' filled')

    def __CalculateCurrentExposure(self, previoustransaction): #cant reference an input class
        if previoustransaction is not None:
            if previoustransaction.market_action == marketaction.BUY:
                    self.current_exposure -= previoustransaction.current_exposure

            elif previoustransaction.market_action == marketaction.SELL:
                self.current_exposure += previoustransaction.current_exposure

class marketinfo(models.Model):
    market_pair = models.CharField(max_length = FAIR_STRING_SIZE)
    open = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=SUPER_MAX_DIGITS, default=Decimal())
    close = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=SUPER_MAX_DIGITS, default=Decimal())
    high = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=SUPER_MAX_DIGITS, default=Decimal())
    low = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=SUPER_MAX_DIGITS, default=Decimal())
    volume = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=SUPER_MAX_DIGITS, default=Decimal())
    miscellaneous = models.CharField(max_length = SERIALIZED_DATA_LIMIT)

    def Fill(self, inputMarketPair = str, inputopen = Decimal, inputclose = Decimal, inputhigh = Decimal, inputlow = Decimal, inputvolume = Decimal, **kwargs):
        """will save the object"""
        log = getLogger(str(self.__class__))
        log.info('filling market info object...')

        if inputMarketPair is not type:
            self.market_pair = inputMarketPair

        if open is not type:
            self.open = inputopen

        if inputclose is not type:
            self.close = inputclose

        if inputhigh is not type:
            self.high = inputhigh

        if inputlow is not type:
            self.low = inputlow

        if inputvolume is not type:
            self.volume = inputvolume

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

    class Meta:
        abstract = True


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

###############################################
#miscellaneous tables
class availablemarket(models.Model):
    exchangename = models.CharField(max_length = FAIR_STRING_SIZE)
    marketcode = models.CharField(max_length = FAIR_STRING_SIZE)
    hoursavailable = models.BooleanField(default = False)
    daysavailable = models.BooleanField(default = False)
    monthsavailable = models.BooleanField(default = False)
    minimumprice = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=SUPER_MAX_DIGITS, default=Decimal())
    minimumvolume = models.DecimalField(decimal_places=ETHEREUM_DECIMALS, max_digits=SUPER_MAX_DIGITS, default=Decimal())

class servicelog(models.Model):
    logsdatetime = models.DateTimeField()
    logslevel = models.CharField(max_length = FAIR_STRING_SIZE)
    message = models.CharField(max_length = FAIR_STRING_SIZE)

class regionalfarmer(models.Model):
    hook = models.CharField(max_length = SERIALIZED_DATA_LIMIT)
    key = models.CharField(max_length = SERIALIZED_DATA_LIMIT)

class extendeduser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phonenumber = PhoneNumberField()


##################################################
##SERVER ONLY MODELS
class Order(object):    
    """orders must have enough information to convert to a transaction."""
    def __init__(self, cloudOrderIdInt = int, managersPairSymbolStr = str, primarySecurityStr = str, secondarySecurityStr = str, stateMarketAction = marketaction, inputReceivedAmount = Decimal, inputGivenAmountDec = Decimal, inputOrderTimeDatetime = datetime, **kwargs):
        if stateMarketAction == marketaction.HOLD:
            getLogger().error("An order cannot have the state: " + str(marketaction.HOLD))
            raise Exception()

        self.__cloudOrderId = cloudOrderIdInt
        self.__pairsSymbol = managersPairSymbolStr
        self.__primary = primarySecurityStr
        self.__secondary = secondarySecurityStr
        self.__orderState = stateMarketAction
        self.__receivedAmount = inputReceivedAmount
        self.__GivenAmount = inputGivenAmountDec
        self.__orderTime = inputOrderTimeDatetime
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


#################################################
#EXCHANGE SPECIFIC TABLES

class independent_reserve_marketinfo(marketinfo):
    pass      