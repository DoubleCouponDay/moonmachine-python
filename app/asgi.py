import sys
import os
from django.core.management import execute_from_command_line
from logging import getLogger



logger = getLogger("asgi")
logger.info("using asgi")

BASE_DIR = os.path.abspath(os.path.split(__file__)[0])
sys.path.insert(0, os.path.join(BASE_DIR, 'MoonMachine'))
sys.path.insert(0, BASE_DIR) #fixed bug where wsgi boot didnt have path configured correctly

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
execute_from_command_line([os.path.join(BASE_DIR, "manage.py"), "check"])

from javascriptjob import javascriptjob #this needs to be after the settings module.
javascriptjob() #this must happen before collectstatic!

execute_from_command_line([os.path.join(BASE_DIR, "manage.py"), "makemigrations"])
execute_from_command_line([os.path.join(BASE_DIR, "manage.py"), "migrate", "--no-input"])

execute_from_command_line([os.path.join(BASE_DIR, "manage.py"), "collectstatic", "--no-input"])

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from back.Controllers.Consumers.CompilationConsumer import CompilationConsumer
from urls import CONTAINS_ADMIN, PORTFOLIO, REGEX_EXACT_CAP
from django.conf.urls import url
from settings import DEBUG

WEB_SOCKET = 'ws/'

websocket_urlpatterns = [
    url(CONTAINS_ADMIN + PORTFOLIO + WEB_SOCKET + 'compilation' + REGEX_EXACT_CAP,
        CompilationConsumer)
]

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        ),
    )
})

if DEBUG == False:
    logger.info("touching nginx startup file.")
    abstouchpath = os.path.abspath("tmp/app-initialized/requiredfile.txt")
    os.system(abstouchpath)