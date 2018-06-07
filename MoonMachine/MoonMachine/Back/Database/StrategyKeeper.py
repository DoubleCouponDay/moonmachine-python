from Back.Database.Queryer import Queryer
from logging import getLogger
from Back.ModelsModule import Language, Strategy, UsersStrategy
from django.core.cache import cache

class StrategyKeeper(Queryer):
    LANGUAGE_CACHE = "language-cache"
    """description of class"""    
    def __init__(self):
        super().__init__()
        self.log = getLogger(str(self.__class__)) 
        
    def ManageLanguageCache(self):
        if cache.get(StrategyKeeper.LANGUAGE_CACHE, None) is None:
            cache.set(StrategyKeeper.LANGUAGE_CACHE, list(Language.objects.all()), 86400) #a day in seconds

    def SubmitStrategy(self, userId, inputLanguage, strategyId = int, scriptsBytes = bytes): #fixed bug where bytes was not optional
        """returns primary key of the created strategy."""
        self.log.info("Beginning to submit strategy.")
        self.ManageLanguageCache()
        cachedLanguages = cache.get(StrategyKeeper.LANGUAGE_CACHE)

        for language in cachedLanguages:
            if language.language == inputLanguage:
                matchingLanguage = language
                correctStrategy = Strategy

                if strategyId is int:
                    correctStrategy = Strategy()
                    correctStrategy.Fill(userId, matchingLanguage.id, inputBits=scriptsBytes)

                else:
                    correctStrategy = Strategy.objects.filter(user_id = userId, id = strategyId).first()            
                    correctStrategy.Fill(inputLanguageId = matchingLanguage.id, inputBits = scriptsBytes)

                return correctStrategy.id #return the owned strategies id

        return None
    
    def FetchUserStrategies(self, userId = int):
        """Returns a list, not a queryset. Can return None!"""
        self.log.info("Fetching strategies.")
        query = Strategy.objects.filter(user_id = userId).values('id', 'language', 'is_compiled', 'compilation_result') #values doesnt have filter arguments
        self.log.info("mapping user strategies.")
        queryList = list(query)
        mappedStrats = map(self.__SelectAwayRawBits, queryList)
        usableStrats = list(mappedStrats)
        self.log.info("returning user strategies.")
        return usableStrats

    def __SelectAwayRawBits(self, currentObject = Language):
        mappedObject = dict()
        mappedObject["compilation_result"] = currentObject["compilation_result"]
        mappedObject["id"] = currentObject["id"]
        mappedObject["is_compiled"] = currentObject["is_compiled"]
        mappedObject["language"] = currentObject["language"] #gets the language name by loading two foreign keys
        return mappedObject

    def FetchStrategy(self, inputUserId = int, strategyId = int):
        """can return None"""
        self.log.info("fetching strategy.")
        query = Strategy.objects.filter(user_id = inputUserId, id = strategyId) #fixed bug where query was looking for matching id in the other strategies table
        self.log.info("returning strategy.")

        if query.exists():
            return query.first()
        
        return None

    def FetchUserStrategy(self, inputUserId = int, inputStrategyId = int):
        """can return None"""
        self.log.info("fetching userstrategy.")
        query = UsersStrategy.objects.filter(user_id = inputUserId, id = inputStrategyId) #fixed bug where query was looking for matching id in the other strategies table
        self.log.info("returning userstrategy.")

        if query.exists():
            return query.first()
        
        return None
    
    def ClearCompilationResult(self, strategyId = int, userId = int):
        self.log.info("Clearing compilation result for strategy " + str(strategyId))
        query = Strategy.objects.filter(strategyId = strategyId, user_id = userId)
        self.__TestQuery(query, self.__ClearCompilationResultOnSuccess)

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