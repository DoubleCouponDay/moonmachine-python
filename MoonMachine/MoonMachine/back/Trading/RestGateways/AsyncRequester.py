from back.Trading.RestGateways.BubbleWrapRequester import BubbleWrapRequester
from threading import Thread
from functools import partial, partialmethod
from overrides import overrides

class AsyncRequester(Thread, BubbleWrapRequester):
    """run Request() instead of start()"""
    def __init__(self):        
        Thread.__init__(self)
        BubbleWrapRequester.__init__(self)
        self.__log = getLogger(str(self.__class__))
        self.__requestInvoked = False
        self.__log.info('initialized.')

    @overrides
    def run(self):
        if self.__requestInvoked:
            self.__log.info('started the async request')

            if len(self.__requestArgs) > 0:
                self.Response = self._BubbleWrapRequest(self.__request, *self.__requestArgs) #requestargs is a list

            else:
                self.Response = self._BubbleWrapRequest(self.__request)

            if len(self.__onSuccessArgs) > 0:
                self.__onSuccess(self.Response, *self.__onSuccessArgs) #successArgs is a list

            else:
                self.__onSuccess(self.Response)
            self.__log.info('completed the async request')

        else:
            err = 'Do not run start(). run StartRequest() instead.'
            self.__log.error(err)
            raise NotImplementedError(err)

        self.__requestInvoked = False
        
    def StartRequest(self, requestFunc, onSuccessFunc, requestArgs = list, onSuccessArgs = list):
        """supply the arguments for "requestFunc" and "onSuccessFunc" as two kwargs arrays with previously mentioned keys."""
        self.__request = requestFunc
        self.__onSuccess = onSuccessFunc

        if requestArgs is not list:
            self.__requestArgs = requestArgs

        else:
            self.__requestArgs = []

        if onSuccessArgs is not list:
            self.__onSuccessArgs = onSuccessArgs

        else:
            self.__onSuccessArgs = []

        self.__requestInvoked = True
        self.start()
