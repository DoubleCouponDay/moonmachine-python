"""
Definition of urls for project.
"""

from django.conf.urls import url

from django.contrib.auth.decorators import login_required
from django.conf.urls import include
from django.contrib.auth import views
from django.contrib import admin
from django.views.generic import TemplateView
admin.autodiscover()
from settings import STATIC_URL
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from Back.Controllers.Pages import AuthorizedControls, Index, Portfolio
from Back.Controllers.AuthorizedControls import AuthenticateWithFile, GetBotsStatus, ToggleOperations, IsAuthenticated
from Back.Controllers.Portfolio import GetMyStrategiesInfo, GetSupportedLanguages, GetValidationRules, CreateStrategy, PutStrategy

AUTHORIZED_CONTROLS = 'authorizedcontrols/'
PORTFOLIO = 'portfolio/'
CONTAINS_ADMIN = 'admin/'
REGEX_EXACT_START = r'^(?i)'
REGEX_EXACT_CAP = '$'

urlpatterns = [
    #PAGES    
    #===============================
    url(r'^$',
        Index),

    staticfiles_urlpatterns(),

    url(REGEX_EXACT_START + CONTAINS_ADMIN + AUTHORIZED_CONTROLS + REGEX_EXACT_CAP, 
        AuthorizedControls),

    url(REGEX_EXACT_START + CONTAINS_ADMIN, admin.site.urls,
        name = 'admin'),

    url(REGEX_EXACT_START + CONTAINS_ADMIN + PORTFOLIO + REGEX_EXACT_CAP,
        Portfolio),

    #HOOKS
    #===============================
    #omitting the appended $ means it will match on a string which contains, not equals, the expression   

    #authorized controls
    url(REGEX_EXACT_START + CONTAINS_ADMIN + AUTHORIZED_CONTROLS + 'toggleoperations' + REGEX_EXACT_CAP, 
        ToggleOperations),

    url(REGEX_EXACT_START + CONTAINS_ADMIN + AUTHORIZED_CONTROLS + 'getbotsstatus' + REGEX_EXACT_CAP,
        GetBotsStatus),

    url(REGEX_EXACT_START + CONTAINS_ADMIN + AUTHORIZED_CONTROLS + 'authenticatewithfile' + REGEX_EXACT_CAP,
        AuthenticateWithFile),

    url(REGEX_EXACT_START + CONTAINS_ADMIN + AUTHORIZED_CONTROLS + 'IsAuthenticated' + REGEX_EXACT_CAP,
        IsAuthenticated),

    #portfolio
    url(REGEX_EXACT_START + CONTAINS_ADMIN + PORTFOLIO + 'getsupportedlanguages' + REGEX_EXACT_CAP, 
        GetSupportedLanguages),

    url(REGEX_EXACT_START + CONTAINS_ADMIN + PORTFOLIO + 'getmystrategiesinfo' + REGEX_EXACT_CAP, 
        GetMyStrategiesInfo),

    url(REGEX_EXACT_START + CONTAINS_ADMIN + PORTFOLIO + 'getvalidationrules' + REGEX_EXACT_CAP, 
        GetValidationRules),

    url(REGEX_EXACT_START + CONTAINS_ADMIN + PORTFOLIO + 'createstrategy' + REGEX_EXACT_CAP, 
        CreateStrategy),

    url(REGEX_EXACT_START + CONTAINS_ADMIN + PORTFOLIO + 'putstrategy' + REGEX_EXACT_CAP, 
        PutStrategy)

]
