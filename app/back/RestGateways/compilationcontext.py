from logging import getLogger
from overrides import overrides
from django.http.request import HttpRequest
from back.Database.StrategyKeeper import StrategyKeeper
from HiddenSettings import HiddenSettings
import requests
from back.Controllers.Pages import OUTPUT
from django.core.cache import cache
import json
from back.models import strategy

class compilationcontext:
    """description of class"""
    def __init__(self):        
        self.__log = getLogger(str(self.__class__))
        self.__strategyKeeper = StrategyKeeper()
        self.__log.info('created serverless context.')

    def SubmitScriptForCompilation(self, compressedScript, consumerInstance):
        self.__log.info('started the compilation procedure.')
        self.__userId = consumerInstance.scope['user'].id
        self.__currentStrategyId = cache.get(consumerInstance.scope['user'].id)
        possibleStrategy = self.__strategyKeeper.FetchStrategy(self.__userId, self.__currentStrategyId)

        if possibleStrategy is None:
            message = "You do not own this strategy or strategy could not be found."
            self.__log.error(message)

            consumerInstance.send(text_data = json.dumps({
                'user error: ': message
            }))
            return

        possibleStrategy.bits = compressedScript
        possibleStrategy.save()
        result = None

        try:
            result = self.__Compile(consumerInstance)

        except Exception as e:     
            message = "compilation request crashed. "
            self.__log.exception(message)

            consumerInstance.send(text_data = json.dumps({
                'internal error: ': message + str(e)
            }))
            return

        if result.status_code != 200: #result.status_code is not a string
            message = result.reason if result.text == "" else result.text 

            self.__log.info("result.reason: " + result.reason)
            self.__log.info("result.text: " + result.text)
            self.__log.exception("internal error: " + message)

            consumerInstance.send(text_data = json.dumps({
                'internal error: ': message
            }))
            return

        self.__log.info("compilation request succeeded: response = " + str(result.text))
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
        consumerInstance.send(text_data = json.dumps({}))
        return
