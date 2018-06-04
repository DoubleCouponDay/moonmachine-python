from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.views.decorators.csrf import requires_csrf_token
from django.core.serializers.json import DjangoJSONEncoder
from Back.Controllers.Pages import INPUT, OUTPUT
from Back.Database.StrategyKeeper import StrategyKeeper
from Back.ModelsModule import Language
from Back.SelectionOptions.ScriptLimits import *
from django.core.cache import cache

@login_required
@requires_csrf_token
@require_GET    
def GetSupportedLanguages(request = HttpRequest):
    languages = list(StrategyKeeper().GetSupportedLanguages())
    mappedLanguages = list(map(__SelectLanguageStrings, languages))
    return JsonResponse ({OUTPUT : mappedLanguages}, DjangoJSONEncoder, True) 

def __SelectLanguageStrings(currentObject = Language):
    return currentObject.language
    
@login_required
@requires_csrf_token
@require_GET   
def GetMyStrategiesInfo(request = HttpRequest):
    strategies = StrategyKeeper().FetchUserStrategies(request.user.id)

    if strategies is None:
        return JsonResponse ({OUTPUT : []}, DjangoJSONEncoder, True) 

    else:
        mappedStrategies = list(map(__SelectAwayRawBits, list(strategies)))
        return JsonResponse ({OUTPUT : mappedStrategies }, DjangoJSONEncoder, True) 

def __SelectAwayRawBits(currentObject = Language):
    mappedObject = dict()
    mappedObject["compilation_result"] = currentObject["strategy__compilation_result"]
    mappedObject["id"] = currentObject["id"]
    mappedObject["is_compiled"] = currentObject["strategy__is_compiled"]
    mappedObject["language"] = currentObject["strategy__language__language"] #gets the language name by loading two foreign keys
    return mappedObject

@login_required
@requires_csrf_token
@require_GET   
def GetValidationRules(request = HttpRequest):
    return JsonResponse ({OUTPUT : {"FILE_SIZE": FILE_SIZE_BYTES}}, DjangoJSONEncoder, True) 

@login_required
@requires_csrf_token
@require_POST
def CreateStrategy(request = HttpRequest):
    possibleError = __BaseChecksForInserts(request)

    if possibleError is not None:
        return possibleError

    strategyId = StrategyKeeper().SubmitStrategy(request.user.id, request.POST.get("language"))

    if strategyId is None:
        return HttpResponseBadRequest("strategy language '" + str(inputLanguage) + "' is not supported.")

    cache.set(request.user.id, strategyId)   #saved for a few seconds. refer to settings.CACHES for the default timeout
    return HttpResponse()

@login_required
@requires_csrf_token
@require_POST
def PutStrategy(request = HttpRequest):
    possibleError = __BaseChecksForInserts(request)

    if possibleError is not None:
        return possibleError
    
    strategyId = request.POST.get("id")
    if strategyId is "0" or strategyId is "":
        return HttpResponseBadRequest("Strategy with that id could not be found.")    

    strategyKeeper = StrategyKeeper()
    usersStrategy = strategyKeeper.FetchUserStrategy(request.user.id, strategyId) # fixed bug where changes to strategykeeper made matching by id impossible

    if usersStrategy is None:
        return HttpResponseBadRequest("You do not own this strategy or strategy could not be found.")

    cache.set(request.user.id, usersStrategy.strategy.id)
    return HttpResponse()

def __BaseChecksForInserts(request):
    if cache.get(request.user.id) is not None:
        return HttpResponseBadRequest("Please wait a few seconds before trying again.")

    if StrategyKeeper().IsSupportedScriptType(request.POST.get("Language")) is False:
        return HttpResponseBadRequest("script files extension is not supported.")