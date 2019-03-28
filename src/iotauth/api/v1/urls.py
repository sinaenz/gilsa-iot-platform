from . import views


def register_url(router):
    router.register('users', views.UsersViewSet)
