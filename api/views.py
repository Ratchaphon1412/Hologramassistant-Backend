from django.shortcuts import render
from django.contrib.auth.models import User
# from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from rest_framework import authentication, permissions
from utils.AI.Wit import Wit
from utils.Knowledge.main import Knowlegde
from utils.TextToSpeech.textToSpeech import textTTS
import json


from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .serializers import *

from .models import Location, DHT22

# Create your views here.

knowledge = Knowlegde(settings.WEATHER_API, settings.RAPID_API,
                      settings.GOOGLE_API, settings.GOOGLE_API)
wit = Wit(settings.WIT_API)
textToSpeechURL = textTTS({
    "Authorization": settings.PLAYHT_API_AUTHORIZATION,
    "X-User-ID": 'hREn3wmcLRTEwxYWgXTMugQj0yg2',
})


class AssistantAPI(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        if request.body.decode('utf-8'):
            requestJson = json.loads(request.body.decode('utf-8'))
            intent, confidence, entities = wit.getIntent(
                requestJson.get('query'))
            return Response({'intent': intent, 'confidence': confidence, 'entities': entities})
        return Response({'intent': None, 'confidence': None, 'entities': None})

    def get(self, request, format=None):
        return Response({'status': 'failer', 'category': 'Music'})


class KnowledgeAPI(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.body.decode('utf-8'):
            requestJson = json.loads(request.body.decode('utf-8'))
            conversation = []
            conversation.append(
                {'role': 'user', 'content': requestJson.get('question')})

            conversation = knowledge.findsomething(conversation)
            text = '{0}'.format(conversation[-1]['content'].strip())
            print(conversation)
            return Response({'answer': text})

        return Response({'answer': None})


class TextToSpeech(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.body.decode('utf-8'):
            requestJson = json.loads(request.body.decode('utf-8'))
            print("test1")
            voiceURL = textToSpeechURL.changetextTV(requestJson['text'])
            print(voiceURL)
            return Response({'url': voiceURL})
        return Response({'url': None})


class WeatherAPI(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.body.decode('utf-8'):
            requestJson = json.loads(request.body.decode('utf-8'))
            text = knowledge.weather(requestJson.get('city'))

            return Response({'weather': text})


class GoogleMapAPI(APIView):
    def post(self, request):
        if request.body.decode('utf-8'):
            requestJson = json.loads(request.body.decode('utf-8'))
            text = knowledge.findRestaurantNearMe(
                requestJson.get('lat'), requestJson.get('long'))

            return Response({'restaurant': text})


class GeolocationIOT(APIView):
    def post(self, request):
        if request.body.decode('utf-8'):
            requestJson = json.loads(request.body.decode('utf-8'))
            latitude = requestJson.get('latitude')
            longitude = requestJson.get('longitude')
            print(latitude, longitude)
            # Try to retrieve an existing Location instance with the same latitude and longitude
            try:
                location = Location.objects.get(
                    latitude=latitude, longitude=longitude)
                location.latitude = latitude
                location.longitude = longitude
            except Location.DoesNotExist:
                location = Location(latitude=latitude, longitude=longitude)

        location.save()

        return Response({'success': True})

    def get(self, request):
        locations = Location.objects.all()
        # serializer = LocationSerializer(locations, many=True)
        return Response({"locations": locations})


class showGoogleMap(APIView):
    def post(self, request):
        if request.body.decode('utf-8'):
            requestJson = json.loads(request.body.decode('utf-8'))
            if requestJson.get('place'):
                place = requestJson.get('place')
                lat, long, description = knowledge.showMapGoogle(place)

                return Response({'lat': lat, 'long': long, 'description': description})
            else:
                return Response({'lat': None, 'long': None})


class DHTSensorIOT(APIView):
    def get(self, request):

        dht = DHT22.objects.get(id=1)
        text = knowledge.getDHTSensor(dht.temperature, dht.humidity)
        return Response({'ans': text})

    def post(self, request):
        if request.body.decode('utf-8'):
            requestJson = json.loads(request.body.decode('utf-8'))
            print(requestJson)

            print(DHT22.objects.all())
            try:
                dht = DHT22.objects.get(id=1)
                print(dht.temperature)
                print(dht.humidity)

                dht.temperature = requestJson.get('temp')
                dht.humidity = requestJson.get('hum')
                print(dht.temperature)
                print(dht.humidity)

            except DHT22.DoesNotExist:
                dht = DHT22(id=1, temperature=requestJson.get(
                    'temp'), humidity=requestJson.get('hum'))

            dht.save()
            return Response({'success': True})


class SecurityIOT(APIView):
    def post(self, request):
        if request.body.decode('utf-8'):
            requestJson = json.loads(request.body.decode('utf-8'))
            if requestJson['security']:
                check = requestJson['security']
                if check == 'on':
                    channel_layer = get_channel_layer()

                    async_to_sync(channel_layer.group_send)(
                        "IOT",
                        {
                            'type': 'send_data',
                            'message': True
                        }
                    )
                    return Response({'success': True})
                else:
                    channel_layer = get_channel_layer()

                    async_to_sync(channel_layer.group_send)(
                        "IOT",
                        {
                            'type': 'send_data',
                            'message': False
                        }
                    )
                    return Response({'success': True})
