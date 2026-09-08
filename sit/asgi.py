import os

import django
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter

from chat.middleware import JWTAuthMiddleware
import chat.routing


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sit.settings")

django.setup()


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),

        "websocket": JWTAuthMiddleware(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        ),
    }
)