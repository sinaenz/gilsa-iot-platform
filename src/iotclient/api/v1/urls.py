from . import views


def register_urls(router):
    router.register('mobile', views.MobileViewSet, 'MobileViewSet')
