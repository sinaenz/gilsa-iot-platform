from rest_framework import serializers
from utils.models import Splash


class CommandSerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()
    content = serializers.CharField()


class DeviceCategorySerializer(serializers.Serializer):
    name = serializers.CharField()


class DeviceTypeSerializer(serializers.Serializer):
    name = serializers.CharField()
    icon = serializers.ImageField()
    category = DeviceCategorySerializer()


class DeviceSerializer(serializers.Serializer):
    name = serializers.CharField()
    device_id = serializers.UUIDField()
    is_connected = serializers.BooleanField()
    is_verified = serializers.BooleanField()
    device_type = DeviceTypeSerializer()


class ZoneSerializer(serializers.Serializer):
    name = serializers.CharField()
    devices = DeviceSerializer(many=True)


class HomeSerializer(serializers.Serializer):
    name = serializers.CharField()


class HomePageSerializer(serializers.Serializer):
    name = serializers.CharField()
    zones = ZoneSerializer(many=True)


class SplashResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Splash
        exclude = ('id', 'os')


class SplashRequestSerializer(serializers.Serializer):
    os = serializers.CharField()

    def create(self, validated_data):
        return {'content': SplashResponseSerializer(Splash.objects.get(os=validated_data['os'])).data}

    def to_representation(self, instance):
        return instance
