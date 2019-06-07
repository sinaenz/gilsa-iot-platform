from django.contrib import admin
from .models import Home, Zone, DeviceType, Device, Command, DeviceCategory


admin.site.register(DeviceCategory)


class DeviceInline(admin.TabularInline):
    model = Device
    extra = 1


class ZoneInline(admin.TabularInline):
    model = Zone
    extra = 1


@admin.register(Home)
class HomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')
    inlines = (ZoneInline, DeviceInline,)


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ('name', 'home', 'type')
    inlines = (DeviceInline,)


@admin.register(DeviceType)
class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'name', 'code')


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'device_type', 'is_verified', 'is_connected')


@admin.register(Command)
class CommandAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'device_type')

