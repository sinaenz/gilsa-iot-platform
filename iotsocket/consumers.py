from channels.generic.websocket import WebsocketConsumer
from iotdevice.models import Device
from channels import exceptions

class DeviceConsumer(WebsocketConsumer):
    def connect(self):
        self.device_id = self.scope['url_route']['kwargs']['device_id']
        try:
            device = Device.objects.get(device_id=self.device_id, is_verified=True)
            device.channel_id = self.channel_name
            device.is_connected = True
            device.save()
            self.accept()
        except:
            pass

    def disconnect(self, close_code):
        device = Device.objects.get(device_id=self.device_id, is_verified=True)
        device.channel_id = None
        device.is_connected = False
        device.save()

    def receive(self, text_data):
        self.send(text_data)

    def command_message(self, event):
        # Handles the "command.message" event when it's sent to us.
        self.send(text_data=event['command'])