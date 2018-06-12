from logging import getLogger
from overrides import overrides
from django.http.request import HttpRequest
from back.Database.StrategyKeeper import StrategyKeeper
from HiddenSettings import HiddenSettings
import requests
from back.Trading.RestGateways.BubbleWrapRequester import BubbleWrapRequester
from back.Controllers.Pages import OUTPUT
from django.core.cache import cache
import json

class ServerlessContext:
    """description of class"""
    def __init__(self):
        super().__init__()
        self.__log = getLogger(str(self.__class__))
        self.__strategyKeeper = StrategyKeeper()
        self.__log.info('created serverless context.')

    def SubmitScriptForCompilation(self, compressedScript, consumerInstance):
        self.__log.info('started the compilation procedure.')
        self.__userId = consumerInstance.scope['user'].id
        self.__currentStrategyId = cache.get(consumerInstance.scope['user'].id)
        strategy = self.__strategyKeeper.FetchStrategy(self.__userId, self.__currentStrategyId)

        if strategy is None:
            message = "You do not own this strategy or strategy could not be found."
            self.__log.error(message)

            consumerInstance.send(text_data = json.dumps({
                'user error: ': message
            }))
            return

        strategy.bits = compressedScript
        strategy.save()
        result = self.__Compile(consumerInstance)

        if result.reason == 'Internal Server Error':
            self.__log.error(result.text)

            consumerInstance.send(text_data = json.dumps({
                'internal error: ': result.text
            }))
            return
        self.__CompileOnSuccess(consumerInstance)
        
    def __Compile(self, consumerInstance):
        settings = HiddenSettings()

        inputHeaders = {
            'content-type': 'application/json'
        }

        hostkey = settings.GetFunctionHostKey()

        if hostkey != "":
            inputHeaders["x-functions-key"] = hostkey
        
        return requests.get(settings.GetFunctionHook() + "compile?userid=" + str(self.__userId) + "&strategyid=" + str(self.__currentStrategyId), headers = inputHeaders)

    def __CompileOnSuccess(self, consumerInstance):
        self.__log.info("compilation request succeeded. returning verdict.")
        consumerInstance.send(text_data = json.dumps({}))
        return
