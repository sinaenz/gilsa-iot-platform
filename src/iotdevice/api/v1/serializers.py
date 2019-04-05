from rest_framework import serializers

from ... import exceptions
from ...models import Device


class DeviceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('name', 'device_id')


class DeviceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('name', 'device_id')


class DeviceRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class DeviceVerificationSerializer(serializers.Serializer):
    device_id = serializers.UUIDField(required=True)

    def create(self, validated_data):
        try:
            device = Device.objects.filter(is_verified=False).get(device_id=validated_data['device_id'])
            device.is_verified = True
            device.save()
            return {'detail': 'verified'}
        except:
            raise exceptions.DeviceVerificationFailed()

    def to_representation(self, instance):
        return instance


class DeviceFirmwareSerializer(serializers.Serializer):
    firmware_version = serializers.CharField(required=True)
    device_id = serializers.UUIDField(required=True)

    def create(self, validated_data):
        try:
            device = Device.objects.filter(is_verified=True).get(device_id=validated_data['device_id'])
            # if firmware needs upgrade
            print(device.device_type.latest_firmware.url)
            if device.device_type.min_firmware_version > validated_data['firmware_version']:
                return {'detail': f'update firmware! minimum version is {device.device_type.min_firmware_version}',
                        'link': device.device_type.latest_firmware.url}
            return {'detail': 'no new version'}
        except:
            raise exceptions.DeviceNotFound()

    def to_representation(self, instance):
        return instance
