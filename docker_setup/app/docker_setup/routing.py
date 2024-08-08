import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

from django.core.asgi import get_asgi_application
from django.urls import re_path

from sockets.consumers import EchoConsumer
from sockets.token_middleware import TokenAuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docker_setup.settings')
django_asgi_app = get_asgi_application()


application = ProtocolTypeRouter(
    {
        # "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(
                TokenAuthMiddlewareStack(
                    URLRouter([
                        re_path(r'^socket/(?P<room_id>[\w.-]+)/$',EchoConsumer.as_asgi()),
                        ])
                    )

                )
            ),
    }
)

#if there is some error moove AuthMiddlewareStack inside TokenAuthMiddlewareStack