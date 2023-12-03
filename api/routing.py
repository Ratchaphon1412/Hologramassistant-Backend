from django.urls import  path
from .consumers import SecurityConsumer

ws_urlpatterns = [
    path('ws/security/', SecurityConsumer.as_asgi()),
]