from django.http.request import HttpRequest
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.views.decorators.csrf import requires_csrf_token
from django.core.serializers.json import DjangoJSONEncoder
from back.Controllers.Pages import INPUT, OUTPUT
from back.Database.StrategyKeeper import StrategyKeeper
from back.ModelsModule import language
from back.SelectionOptions.ScriptLimits import *
from django.core.cache import cache

UPLOAD_TIMER = "uploadtimer"

@login_required
@requires_csrf_token
@require_GET    
def GetSupportedLanguages(request = HttpRequest):
    languages = list(StrategyKeeper().GetSupportedLanguages())
    mappedLanguages = list(map(__SelectLanguageStrings, languages))
    return JsonResponse ({OUTPUT : mappedLanguages}, DjangoJSONEncoder, True) 

def __SelectLanguageStrings(currentObject = language):
    return currentObject.language
    
@login_required
@requires_csrf_token
@require_GET   
def GetSubscribedStrategies(request = HttpRequest):
    strategies = StrategyKeeper().GetSubscribedStrategies(request.user.id)

    if strategies is None:
        return JsonResponse ({OUTPUT : []}, DjangoJSONEncoder, True) 

    else:
        return JsonResponse ({OUTPUT : strategies }, DjangoJSONEncoder, True) 

@login_required
@requires_csrf_token
@require_GET   
def GetCreatedStrategies(request = HttpRequest):
    strategies = StrategyKeeper().FetchCreatedStrategies(request.user.id)

    if strategies is None:
        return JsonResponse ({OUTPUT : []}, DjangoJSONEncoder, True) 

    else:
        return JsonResponse ({OUTPUT : strategies }, DjangoJSONEncoder, True) 

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
    cache.set(UPLOAD_TIMER, 0, 5)

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
    cache.set(UPLOAD_TIMER, 0, 5)

    if possibleError is not None:
        return possibleError
    
    strategyId = request.POST.get("id")

    if strategyId is "0" or strategyId is "":
        return HttpResponseBadRequest("Strategy with that id could not be found.")    

    strategyKeeper = StrategyKeeper()
    usersStrategy = strategyKeeper.FetchStrategy(request.user.id, strategyId) # fixed bug where changes to strategykeeper made matching by id impossible

    if usersStrategy is None:
        return HttpResponseBadRequest("You do not own this strategy or strategy could not be found.")

    strategyKeeper.SubmitStrategy(request.user.id, request.POST.get("language"), strategyId)
    cache.set(request.user.id, usersStrategy.id)
    return HttpResponse()

def __BaseChecksForInserts(request):
    if cache.get(UPLOAD_TIMER) is not None:
        return HttpResponseBadRequest("Please wait a few seconds before trying again.")

    if StrategyKeeper().IsSupportedScriptType(request.POST.get("language")) is False:
        return HttpResponseBadRequest("script files extension is not supported.")