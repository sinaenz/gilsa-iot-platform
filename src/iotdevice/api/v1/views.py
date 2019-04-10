from rest_framework import exceptions
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from iotauth import permissions
from . import serializers
from ...models import Device


class DeviceViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    lookup_field = 'device_id'
    queryset = Device.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.DeviceCreateSerializer
        if self.action == 'retrieve':
            return serializers.DeviceRetrieveSerializer
        return serializers.DeviceListSerializer

    # TODO: fix it!
    def get_permissions(self):
        self.permission_classes = []
        if self.action in ['me', 'logout']:
            self.permission_classes = [permissions.IsAuthenticated]
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    @action(detail=False, methods=['post'], name='verify device')
    def verify(self, request):
        """ device verification """
        serializer = serializers.DeviceVerificationSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    @action(detail=False, methods=['post'], name='update firmware')
    def firmware(self, request):
        """ request for firmware update """
        serializer = serializers.DeviceFirmwareSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    @action(detail=False, methods=['post'], name='command device')
    def command(self, request):
        """ command a device """
        serializer = serializers.DeviceCommandSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)