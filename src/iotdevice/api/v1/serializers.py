from rest_framework import serializers

from ... import exceptions
from ...models import Device, Command, DeviceType, Home, Zone

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class DeviceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = ('name', 'device_id')


class DeviceCreateSerializer(serializers.ModelSerializer):
    device_type = serializers.CharField()

    class Meta:
        model = Device
        fields = ('name', 'device_type', 'zone', 'home', 'device_id')
        read_only_fields = ('device_id', )

    def create(self, validated_data):
        try:
            device_type = DeviceType.objects.get(code=validated_data.pop('device_type'))
            device = Device.objects.create(**validated_data)
            device.device_type = device_type
            device.save()
            return device
        except:
            raise exceptions.DeviceCreationFailed()


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
            if device.device_type.min_firmware_version > validated_data['firmware_version']:
                return {'detail': f'update firmware! minimum version is {device.device_type.min_firmware_version}',
                        'link': device.device_type.latest_firmware.url}
            return {'detail': 'no new version'}
        except:
            raise exceptions.DeviceNotFound()

    def to_representation(self, instance):
        return instance


class DeviceCommandSerializer(serializers.Serializer):
    device_id = serializers.UUIDField(required=True)
    command_code = serializers.CharField(required=True)

    def create(self, validated_data):
        try:
            # TODO: check if device is connected
            device = Device.objects.filter(is_verified=True).get(device_id=validated_data['device_id'])
            channel_id = device.channel_id
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.send)(channel_id, {
                "type": "command.message",
                "command": Command.objects.get(
                    code=validated_data['command_code'],
                    device_type=device.device_type).content,
            })
            return {'detail': 'command sent successfully'}
        except:
            raise exceptions.DeviceNotFound()

    def to_representation(self, instance):
        return instance


class HomeCreateSerializer(serializers.Serializer):
    name = serializers.CharField()
    zone_name = serializers.CharField(write_only=True)
    zone_type = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        print(validated_data)
        zone_name = validated_data.pop('zone_name')
        zone_type = validated_data.pop('zone_type')
        home = Home.objects.create(**validated_data)
        home.owner = self.context.get('user')
        home.save()
        zone = Zone.objects.create(name=zone_name, type=zone_type, home=home)
        return home


class ZoneCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zone
        fields = '__all__'

