import uuid

from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from iotauth.models import User


# ===========================================================================
# =============================== Home Model ================================
# ===========================================================================
class Home(models.Model):
    name = models.CharField(_("Home Name"), max_length=50, default='No Name Home')
    owner = models.ForeignKey(User, related_name='owned_homes', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# ===========================================================================
# =============================== Zone Model ================================
# ===========================================================================
class Zone(models.Model):
    name = models.CharField(_("Zone Name"), max_length=50, default='No Name Zone')
    # home
    home = models.ForeignKey(Home, related_name='zones', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


# ===========================================================================
# =========================== Device Type Model =============================
# ===========================================================================
class DeviceType(models.Model):
    name = models.CharField(_("Device Type Name"), max_length=50, default='Gilsa Device')
    code = models.CharField(_("Device Type Code"), max_length=50, blank=True, unique=True)
    # device type icon
    icon = models.ImageField(_("Icon"), upload_to='DeviceTypeIcons/%Y/%m/%d', default='DeviceTypeIcons/icon.png')
    # firmware
    latest_firmware = models.FileField(_("Firmware"), upload_to='FW/%Y/%m/%d', default='FW/icon.png')
    min_firmware_version = models.CharField(_("Device Type Minimum Firmware Version"), max_length=50, default='1.0.0')

    def image_tag(self):
        img = '/media/DeviceTypeIcons/icon.png'
        if hasattr(self, 'icon'):
            try:
                img = self.icon.url
            except:
                pass
        return mark_safe('<img src="{}" style="width: 50px; height:50px; border-radius:25px;"/>'.format(img))

    def __str__(self):
        return self.name


# ===========================================================================
# ============================== Device Model ===============================
# ===========================================================================
class DeviceCategory(models.Model):
    name = models.CharField(_("Device Category Name"), max_length=50, default='Gilsa Device')

    def __str__(self):
        return self.name


# ===========================================================================
# ============================== Device Model ===============================
# ===========================================================================
class Device(models.Model):
    name = models.CharField(_("Device Name"), max_length=50, default='Gilsa Device')
    device_id = models.UUIDField(_("Device ID"), default=uuid.uuid4, unique=True)
    channel_id = models.CharField(_("WebSocket Channel ID"), max_length=50, blank=True, null=True)
    is_connected = models.BooleanField(_("Is Connected ?"), default=False)
    is_verified = models.BooleanField(_("Is Verified ?"), default=False)
    # device type
    device_type = models.ForeignKey(DeviceType, related_name='devices', null=True, on_delete=models.PROTECT)
    # category
    category = models.ForeignKey(DeviceCategory, related_name='devices', null=True, on_delete=models.PROTECT)
    # zone
    zone = models.ForeignKey(Zone, related_name='devices', blank=True, null=True, on_delete=models.SET_NULL)
    # home
    home = models.ForeignKey(Home, related_name='devices', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


# ===========================================================================
# ============================= Command Model ===============================
# ===========================================================================
class Command(models.Model):
    name = models.CharField(_("Command Name"), max_length=50, default='Gilsa Device')
    code = models.CharField(_("Command Code"), max_length=50, blank=True, unique=True)
    content = models.CharField(_("Command Content"), max_length=500, blank=True, null=True)
    # device Type
    device_type = models.ForeignKey(DeviceType, related_name='commands', null=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.name
