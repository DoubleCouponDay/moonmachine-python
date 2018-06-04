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
                    correctStrategy.Fill(inputLanguageId = languageId, inputBits = scriptsBytes)

                consumerStrategy = UsersStrategy()
                consumerStrategy.Fill(correctStrategy.id, userId)
                return correctStrategy.id

        return None
    
    def FetchUserStrategies(self, userId = int):
        """Returns UserStrategies. Can return None!"""
        self.log.info("Fetching strategies.")
        query = UsersStrategy.objects.filter(user_id = userId).values('id', 'strategy__language__language', 'strategy__is_compiled', 'strategy__compilation_result') #values doesnt have filter arguments
        return self._TestQuery(query, self.__FetchStrategiesOnSuccess)

    def __FetchStrategiesOnSuccess(self, query):
        self.log.info("returning strategies.")
        return query

    def FetchStrategy(self, inputUserId = int, inputStrategyId = int):
        """can return None"""
        self.log.info("fetching strategy.")
        query = Strategy.objects.filter(user_id = inputUserId, id = inputStrategyId) #fixed bug where query was looking for matching id in the other strategies table
        self.log.info("returning strategy.")

        if query.exists():
            return query.first()
        
        return None

    def FetchUserStrategy(self, inputUserId =int, inputStrategyId = int):
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