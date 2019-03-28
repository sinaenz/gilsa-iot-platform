from rest_framework import exceptions
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from iotauth import permissions
from . import serializers
from ...models import Device


class DeviceListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Device.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return serializers.DeviceCreateSerializer
        else:
            return serializers.DeviceDetailSerializer

    @action(detail=True, methods=['get'])
    def verify(self, request, device_id):
        try:
            device = Device.objects.get(device_id=device_id)
            device.is_verified = True
            device.save()
            return Response({'detail': 'دستگاه با موفقیت تایید شد'}, status=200)
        except:
            raise exceptions.NotFound('دستگاهی با شناسه وارد شده یافت نشد')
