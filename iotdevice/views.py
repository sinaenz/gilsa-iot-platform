from django.shortcuts import render
from .models import Device
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


def command(request, device_id):
    if request.method == 'POST':
        channel_id = Device.objects.get(device_id=device_id).channel_id
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(channel_id, {
            "type": "command.message",
            "command": request.POST['command'],
        })
    return render(request, 'command.html')
