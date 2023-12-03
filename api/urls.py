from django.urls import path, include
from .views import *

urlpatterns = [
    path('ai/', AssistantAPI.as_view()),
    path('knowledge/', KnowledgeAPI.as_view()),
    path('texttospeech/', TextToSpeech.as_view()),
    path('weather/', WeatherAPI.as_view()),
    path('restaurant/', GoogleMapAPI.as_view()),
    path('place/',showGoogleMap.as_view()),
    path('dhtIOT/',DHTSensorIOT.as_view()),
    path('securityIOT/',SecurityIOT.as_view()),
]
