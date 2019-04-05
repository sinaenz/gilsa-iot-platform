from . import views


def register_urls(router):
    router.register('users', views.UsersViewSet)
