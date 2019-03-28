from django.apps import AppConfig


class IotauthConfig(AppConfig):
    name = 'iotauth'

    def ready(self):
        from . import signals

