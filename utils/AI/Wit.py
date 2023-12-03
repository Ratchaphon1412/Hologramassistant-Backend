from textwrap import indent
import requests
import json


class Wit:
    def __init__(self, witAPI):
        self.witapiKey = witAPI
        self.endpointMessage = "https://api.wit.ai/message?v=20231202&q="

    def getIntent(self, text):

        headers = {
            'Authorization': 'Bearer ' + self.witapiKey
        }
        try:
            response = requests.get(self.endpointMessage+text, headers=headers)
            dicresponse = json.loads(response.text)

            intent = None
            confidence = None
            entities = None
            if (dicresponse["intents"] != list()):
                intent = dicresponse["intents"][0]["name"]
                confidence = dicresponse["intents"][0]["confidence"]
            if (dicresponse["entities"] != dict()):
                entities = dicresponse["entities"]
            return intent, confidence, entities
        except Exception as e:
            intent = None
            confidence = None
            entities = None

        return intent, confidence, entities
