from rest_framework import exceptions
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from django.core import serializers

from iotauth import permissions
from . import serializers
from iotdevice.models import DeviceType


class MobileViewSet(viewsets.ViewSet):
    # TODO: fix it!
    def get_permissions(self):
        self.permission_classes = [permissions.IsAuthenticated, ]
        if self.action == 'splash':
            self.permission_classes = []
        return super().get_permissions()

    def list(self, request):
        """ client home page """
        resp = {}
        # homes
        # TODO: also should list homes in which user is admin!
        homes = request.user.owned_homes.all()
        return Response(serializers.HomePageSerializer(homes, many=True).data)

    @action(detail=False, methods=['post'], name='client os splash data')
    def splash(self, request):
        """ user splash """
        serializer = serializers.SplashRequestSerializer(data=self.request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        if request.user.is_authenticated:
            return Response(serializer.data['content'], status=200)
        return Response(serializer.data['content'], status=403)

    @action(detail=False, methods=['get'], name='device types data')
    def device_types(self, request):
        """ get all device types """
        serializer = serializers.DeviceTypeSerializer(DeviceType.objects.all(), many=True)
        return Response(serializer.data, status=200)
