from rest_framework import serializers
from utils.models import Splash
import json


class CommandSerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.CharField()
    content = serializers.CharField()


class DeviceCategorySerializer(serializers.Serializer):
    name = serializers.CharField()
    code = serializers.IntegerField()
    icon = serializers.ImageField()


class DeviceTypeSerializer(serializers.Serializer):
    name = serializers.CharField()
    icon = serializers.ImageField()
    code = serializers.CharField()
    category = DeviceCategorySerializer()


class DeviceSerializer(serializers.Serializer):
    name = serializers.CharField()
    device_id = serializers.UUIDField()
    is_connected = serializers.BooleanField()
    is_verified = serializers.BooleanField()
    device_type = DeviceTypeSerializer()
    status = serializers.CharField()

    def to_representation(self, instance):
        instance = super().to_representation(instance)
        # TODO: Should be fixed!
        try:
            instance['status'] = json.loads(instance['status'])
        except:
            pass
        return instance


class ZoneSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    type = serializers.IntegerField()
    devices = DeviceSerializer(many=True)


class HomeSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()


class HomePageSerializer(serializers.Serializer):
    id = serializers.CharField()
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
