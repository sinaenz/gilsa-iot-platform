from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid


class Home(models.Model):
    pass

class Zone(models.Model):
    pass

class Device(models.Model):
    name = models.CharField(_("Device Name"), max_length=50, default='Gilsa Device')
    category = models.CharField(_("Device Category"), max_length=50)
    device_id = models.UUIDField(_("Device ID"), default=uuid.uuid4, unique=True)
    channel_id = models.CharField(_("WebSocket Channel ID"), max_length=50, blank=True, null=True)
    is_connected = models.BooleanField(_("Is Connected ?"), default=False)
    is_verified = models.BooleanField(_("Is Verified ?"), default=False)

    def __str__(self):
        return self.name