from logging import getLogger

class Queryer(object):
    SUCCEEDED = True
    FAILED = None

    """description of class"""
    def __init__(self):
        self.__log = getLogger(str(self.__class__))

    def _TestQuery (self, query, onSuccess, *args):
        """can return none!"""
        self.__log.info("testing query.")

        if query.exists():
            self.__log.info('query found a match.')

            if len(args) > 0:                
                return onSuccess(query, *args)

            else:
                return onSuccess(query)
            
        else:
            self.__log.warning('query did not work!')
            return Queryer.FAILED



