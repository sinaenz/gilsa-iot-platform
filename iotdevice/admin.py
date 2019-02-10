from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_verified', 'is_connected')
    list_editable = ('name',)
    list_display_links = ('id',)