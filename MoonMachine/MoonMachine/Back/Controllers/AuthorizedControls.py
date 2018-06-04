from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import requires_csrf_token
from django.core.serializers.json import DjangoJSONEncoder
from django.http.request import HttpRequest
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
import json
from Back.Trading.ParallelTrader import ParallelTrader
from django.contrib.auth.decorators import login_required
from threading import Lock
from Back.Controllers.Pages import INPUT, OUTPUT

Trader = ParallelTrader()
    
@login_required
@requires_csrf_token
@require_POST
def ToggleOperations (request = HttpRequest):
    global Trader #global must be defined everywhere that Trader is used so that it is not considered a local object     
    switchState = Trader.GetToggleSwitchesState()

    if switchState == ParallelTrader.IDLE_STATE:
        Trader.Start()                

    elif switchState == ParallelTrader.RUNNING_STATE:
        Trader.Stop(request)

    return HttpResponse()

@login_required
@requires_csrf_token
@require_GET
def GetBotsStatus(request = HttpRequest):
    return JsonResponse ({OUTPUT : Trader.GetToggleSwitchesState()}, DjangoJSONEncoder, True)  

@login_required
@requires_csrf_token
@require_POST
def AuthenticateWithFile (request = HttpRequest):
    global Trader
    inputText = request.POST.get (INPUT)

    if inputText is None:
        return HttpResponseBadRequest()

    fileAsJson = json.loads (inputText)
    authErrors = Trader.Authenticate (fileAsJson)
    return JsonResponse(authErrors, DjangoJSONEncoder, True)

@login_required
@requires_csrf_token
@require_GET
def IsAuthenticated(request = HttpRequest):
    global Trader
    return JsonResponse({OUTPUT: Trader.IsSufficientlyAuthenticated()}, DjangoJSONEncoder, True)