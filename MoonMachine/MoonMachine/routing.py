from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from Back.Controllers.Consumers.CompilationConsumer import CompilationConsumer
from urls import CONTAINS_ADMIN, PORTFOLIO, REGEX_EXACT_CAP
from django.conf.urls import url

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