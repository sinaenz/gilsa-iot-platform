from . import views


def register_urls(router):
    router.register('devices', views.DeviceViewSet, 'DeviceViewSet')
    router.register('homes', views.HomeViewSet, 'HomeViewSet')
    router.register('zones', views.ZoneViewSet, 'ZoneViewSet')
