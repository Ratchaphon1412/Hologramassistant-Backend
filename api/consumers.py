from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync

class SecurityConsumer(WebsocketConsumer):
    def connect(self):
        self.security_name ='IOT'
        async_to_sync(self.channel_layer.group_add)(
            self.security_name,
            self.channel_name
        )
        
        self.accept()
    
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print(message)
        async_to_sync(self.channel_layer.group_send)(
            self.security_name,
            {
                'type':'send_data',
                'message':message
            })
        

    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.security_name,
            self.channel_name
        )
        
    def send_data(self,event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type':'send_data',
            'message':message
        }
        ))
        
        