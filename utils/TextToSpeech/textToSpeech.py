# from playsound import playsound
import requests
import asyncio
import json
# import os
import time

from pyht import Client
from pyht.client import TTSOptions
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class textTTS:
    def __init__(self, playhtHeader):
        self.playhtHeader = playhtHeader

    def changetextTV(self, text):
        # url = "https://voicerss-text-to-speech.p.rapidapi.com/"

        # querystring = {"key": "4ce978988ca4480e99d37e13a6f4abf8"}

        # payload = {
        #     "src": text,
        #     "hl": "th-th",
        #     "r": "0",
        #     "c": "mp3",
        #     "f": "8khz_8bit_mono"
        # }

        # headers = {
        #     "content-type": "application/x-www-form-urlencoded",
        #     "X-RapidAPI-Key": "091aed48d7mshac28a14304d11cap1182e7jsn2d5daa5546cc",
        #     "X-RapidAPI-Host": "voicerss-text-to-speech.p.rapidapi.com"
        # }

        # response = requests.post(
        #     url, data=payload, headers=headers, params=querystring)

        # print(response.content)

        # filename = f'{datetime.now().strftime("%Y%m%d%H%M%S")}.mp3'

        # with open(f'media/temp/' + filename, 'wb+') as f:
        #     # f.write(response.content)
        #     for chunk in response.iter_content(chunk_size=1024):
        #         f.write(chunk)

        # return settings.BACKEND_URL + '/media/temp/' + filename

        endpoint = "https://api.play.ht/api/v1/"
        print(self.playhtHeader['Authorization'])
        print(self.playhtHeader['X-User-ID'])
        headers = {

            "AUTHORIZATION": self.playhtHeader['Authorization'],
            'X-USER-ID': self.playhtHeader['X-User-ID'],

        }
        payloads = {
            "voice": 'th-TH-NiwatNeural',
            "content": [text],
            "title": 'test'
        }
        response = requests.post(
            endpoint+'convert', headers=headers, json=payloads)
        time.sleep(8)
        # await asyncio.sleep(10)
        print(response.text)

        dic_response = json.loads(response.text)
        print(dic_response)
        # print(dic_response['status'])
        if (dic_response['status'] == 'CREATED'):
            responseVoice = requests.get(
                endpoint + 'articleStatus?transcriptionId=' + dic_response['transcriptionId'], headers=headers)
            print(dic_response['transcriptionId'])
            print(responseVoice.text)
            dic_responseVoice = json.loads(responseVoice.text)
            print(dic_responseVoice)
            # print(dic_responseVoice['audioUrl'])
            if (dic_responseVoice.get('audioUrl') != None):
                return dic_responseVoice['audioUrl']
            else:
                return None
        # client = Client(
        #     user_id="vD41VMMqWoUWDrFViMdT6C7ecwe2",
        #     api_key="3923110b70874785bfc512add693bc82",
        # )
        # options = TTSOptions(
        #     voice="s3://voice-cloning-zero-shot/d9ff78ba-d016-47f6-b0ef-dd630f59414e/female-cs/manifest.json")
        # filename = datetime.now().strftime("%Y%m%d%H%M%S") + ".mp3"
        # filepath = f"media/temp/{filename}"
        # with open(filepath, "wb") as f:
        #     for chunk in client.tts(text, options):
        #         f.write(chunk)
        # return filepath
            

        return None

    # async def main(self, text):

    #     # return await asyncio.gather(self.findingData(), self.changetextTV(text))
    #     return await asyncio.run(self.changetextTV(text))

    # def nofeature(self):
    #     return playsound('./Sound/nofeature.mp3')

    # def dontunderstand(self):
    #     return playsound('./Sound/don\'tunderstand.mp3')

    # async def findingData(self):
    #     return playsound('./Sound/finddata.mp3')

    # def problemPlayht(self):
    #     return playsound('./Sound/problem.mp3')
