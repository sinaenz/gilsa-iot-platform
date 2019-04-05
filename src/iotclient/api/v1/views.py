from rest_framework import exceptions
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from django.core import serializers

from iotauth import permissions
from . import serializers


class MobileViewSet(viewsets.ViewSet):
    # TODO: fix it!
    def get_permissions(self):
        self.permission_classes = []
        return super().get_permissions()

    def list(self, request):
        """ client home page """
        resp = {}
        # homes
        # TODO: also should list homes in which user is admin!
        homes = request.user.owned_homes.all()
        return Response(serializers.HomePageSerializer(homes, many=True).data)

