from rest_framework import serializers

from ...models import Device


class DeviceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('name', 'device_id')


class DeviceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('name', 'device_id')


class DeviceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('name', 'device_id')




