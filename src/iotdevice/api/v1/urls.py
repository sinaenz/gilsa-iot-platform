from . import views


def register_urls(router):
    router.register('devices', views.DeviceViewSet)
