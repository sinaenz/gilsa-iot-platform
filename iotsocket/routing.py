from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/connect/(?P<device_id>[^/]+)/$', consumers.DeviceConsumer),
]