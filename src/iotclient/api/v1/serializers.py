from rest_framework import serializers


class CommandSerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()
    content = serializers.CharField()


class DeviceCategorySerializer(serializers.Serializer):
    name = serializers.CharField()


class DeviceTypeSerializer(serializers.Serializer):
    name = serializers.CharField()
    icon = serializers.ImageField()


class DeviceSerializer(serializers.Serializer):
    name = serializers.CharField()
    device_id = serializers.UUIDField()
    is_connected = serializers.BooleanField()
    is_verified = serializers.BooleanField()
    device_type = DeviceTypeSerializer()
    category = DeviceCategorySerializer()


class ZoneSerializer(serializers.Serializer):
    name = serializers.CharField()
    devices = DeviceSerializer(many=True)


class HomeSerializer(serializers.Serializer):
    name = serializers.CharField()


class HomePageSerializer(serializers.Serializer):
    name = serializers.CharField()
    zones = ZoneSerializer(many=True)
