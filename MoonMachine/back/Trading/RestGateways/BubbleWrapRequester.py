from logging import getLogger

class BubbleWrapRequester(object):
    """description of class"""
    def __init__(self):
        self.__log = getLogger(str(self.__class__))

    def _BubbleWrapRequest(self, requestFunc, *args): #one dash to allow access to derived classes
        """can return None!"""
        self.__log.info("bubble wrapping request.")
        try:
            if len(args) > 0:
                return requestFunc(*args)

            else:
                return requestFunc()
            
        except Exception as e:
            self.__log.error(str(e))
            return None


