from channels.generic.websocket import WebsocketConsumer
from iotdevice.models import Device
import json


Handlers = {
    'KeyModule': 'key_module',
}


class DeviceConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.device = None

    def connect(self):
        device_id = self.scope['url_route']['kwargs']['device_id']
        try:
            self.device = Device.objects.get(device_id=device_id, is_verified=True)
            self.device.channel_id = self.channel_name
            self.device.is_connected = True
            self.device.save()
            self.accept()
        except:
            pass

    def disconnect(self, close_code):
        try:
            self.device.channel_id = None
            self.device.is_connected = False
            self.device.save()
        except:
            pass

    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        # call corresponding method
        try:
            getattr(self, Handlers[text_data['handler']])(text_data)
            self.send(json.dumps({'status': 'ok', 'detail': 'received'}))
        except:
            print(text_data)

    def key_module(self, *args):
        self.device.status = json.dumps(args[0]['content'])
        self.device.save()

    def command_message(self, event):
        # Handles the "command.message" event when it's sent to us.
        self.send(text_data=event['command'])
