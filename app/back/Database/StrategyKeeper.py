from back.Database.Queryer import Queryer
from logging import getLogger
from back.models import language, strategy, usersstrategy
from django.core.cache import cache

class StrategyKeeper(Queryer):
    LANGUAGE_CACHE = "language-cache"
    """description of class"""    
    def __init__(self):
        super().__init__()
        self.log = getLogger(str(self.__class__)) 
        
    def ManageLanguageCache(self):
        if cache.get(StrategyKeeper.LANGUAGE_CACHE, None) is None:
            cache.set(StrategyKeeper.LANGUAGE_CACHE, list(language.objects.all()), 86400) #a day in seconds
            

    def SubmitStrategy(self, userId, inputLanguage, strategyId = int, scriptsBytes = bytes): #fixed bug where bytes was not optional
        """returns primary key of the created strategy."""
        self.log.info("Beginning to submit strategy.")
        self.ManageLanguageCache()
        cachedLanguages = cache.get(StrategyKeeper.LANGUAGE_CACHE)

        for language in cachedLanguages:
            if language.language == inputLanguage:
                matchingLanguage = language
                correctStrategy = strategy

                if strategyId is int:
                    correctStrategy = strategy()
                    correctStrategy.Fill(userId, matchingLanguage.id, inputBits=scriptsBytes)

                else:
                    correctStrategy = strategy.objects.filter(user_id = userId, id = strategyId).first()            
                    correctStrategy.Fill(inputLanguageId = matchingLanguage.id, inputBits = scriptsBytes)

                return correctStrategy.id #return the owned strategies id

        return None
    
    def GetSubscribedStrategies(self, userId = int):
        """Returns a list, not a queryset. Can return None!"""
        self.log.info("Fetching user strategies.")
        query = userstrategy.objects.filter(user_id = userId).values('id', 'strategy_id') #values doesnt have filter arguments
        queryList = list(query)
        self.log.info("returning user strategies.")
        return queryList

    def FetchCreatedStrategies(self, userId = int):
        self.log.info("Fetching created strategies.")
        query = strategy.objects.filter(user_id = userId).values('id', 'language__language', 'is_compiled', 'compilation_result') #values doesnt have filter arguments
        self.log.info("mapping created strategies.")
        queryList = list(query)
        queryList = list(map(self.__MapCreatedStrategies, queryList))
        self.log.info("returning created strategies.")
        return queryList

    def __MapCreatedStrategies(self, currentObject = strategy):
        output = dict()
        output['compilation_result'] = currentObject['compilation_result'] #alphabetical order
        output['id'] = currentObject['id']        
        output['is_compiled'] = currentObject['is_compiled']        
        output['language'] = currentObject['language__language'] #the order of properties placed matters because im cutting corners in javascript with the spread operator!
        return output

    def FetchStrategy(self, inputUserId = int, strategyId = int):
        """can return None"""
        self.log.info("fetching strategy.")
        query = strategy.objects.filter(user_id = inputUserId, id = strategyId) #fixed bug where query was looking for matching id in the other strategies table
         #it does have objects
        

        if query.exists():
            self.log.info("returning strategy.")
            return query.first()
        
        self.log.info("returning none.")
        return None

    def FetchUserStrategy(self, inputUserId = int, inputStrategyId = int):
        """can return None"""
        self.log.info("fetching userstrategy.")
        query = usersstrategy.objects.filter(user_id = inputUserId, id = inputStrategyId) #fixed bug where query was looking for matching id in the other strategies table
         #it does have objects
        self.log.info("returning userstrategy.")

        if query.exists():
            return query.first()
        
        return None
    
    def ClearCompilationResult(self, strategyId = int, userId = int):
        self.log.info("Clearing compilation result for strategy " + str(strategyId))
        query = strategy.objects.filter(strategyId = strategyId, user_id = userId)
        self._TestQuery(query, self.__ClearCompilationResultOnSuccess)

    def __ClearCompilationResultOnSuccess(self, query):
        query.compilation_result = ''
        self.log.info("compilation result cleared.")
        query.save()

    def IsSupportedScriptType(self, fileType = str):
        self.ManageLanguageCache()
        languages = cache.get(StrategyKeeper.LANGUAGE_CACHE)

        if len(languages) > 0:
            return True
        
        return False

    def GetSupportedLanguages(self):
        """returns queryset unconsumed."""
        self.ManageLanguageCache()
        return cache.get(StrategyKeeper.LANGUAGE_CACHE)