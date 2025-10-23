import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "panel.settings")

# جلوگیری از خطای مسیر در runserver
try:
    from task.routing import websocket_urlpatterns
except Exception as e:
    print(f"⚠️ Failed to import websocket routes: {e}")
    websocket_urlpatterns = []

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
