from rest_framework import serializers
from django.test import Client
from oauth2_provider.models import Application, AccessToken, RefreshToken
from ... import exceptions
from ...models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'full_name')


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('phone', 'password', 'full_name')

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = super().create(validated_data)
        instance.set_password(password)
        instance.save()
        return instance


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserVerificationSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    def create(self, validated_data):
        phone = validated_data['phone']
        code = validated_data['code']
        try:
            user = User.objects.filter(is_verified=False).get(phone=phone, verification_code=code)
            user.is_verified = True
            user.save()
            return {'detail': 'تایید با موفقیت انجام شد'}
        except:
            raise exceptions.UserVerificationFailed()

    def to_representation(self, instance):
        return instance


class UserResendSmsSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)

    def create(self, validated_data):
        phone = validated_data['phone']
        try:
            user = User.objects.filter(is_verified=False).get(phone=phone)
            user.send_verification_sms()
            return {'detail': 'کد تایید مجدد برای شما ارسال شد'}
        except:
            raise exceptions.UserSendSmsFailed()

    def to_representation(self, instance):
        return instance


class UserLoginSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate_phone(self, value):
        """ check if user with given phone exists """
        try:
            user = User.objects.filter(is_verified=True).get(phone=value)
            return value
        except:
            raise exceptions.UserLoginFailed()

    def create(self, validated_data):
        app = Application.objects.last()
        # TODO: Clear old tokens
        c = Client(SERVER_NAME='localhost:8000')
        response = c.post('http://127.0.0.1:8000/o/token/', data={
            'grant_type': 'password',
            'username': validated_data['phone'],
            'password': validated_data['password'],
            'client_id': app.client_id,
            'client_secret': app.client_secret
        })
        if response.status_code == 400:
            raise exceptions.UserLoginFailed()
        return response.json()

    def to_representation(self, instance: dict):
        return instance


class UserLogoutSerializer(serializers.Serializer):

    def create(self, validated_data):
        user = self.context['user']
        AccessToken.objects.filter(user=user).delete()
        RefreshToken.objects.filter(user=user).delete()
        return {'detail': 'خروج از حساب کاربری'}

    def to_representation(self, instance: dict):
        return instance


class UserResetPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User.objects.filter(is_verified=True).get(phone=validated_data['phone'])
        AccessToken.objects.filter(user__phone=validated_data['phone']).delete()
        RefreshToken.objects.filter(user__phone=validated_data['phone']).delete()
        # set password unusable
        user.set_unusable_password()
        # send verification code
        user.send_verification_sms()
        return {'detail': 'کد تایید برای شما ارسال شد'}

    def to_representation(self, instance: dict):
        return instance


class UserRecreatePasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    new_pass = serializers.CharField(required=True)

    def create(self, validated_data):
        user = User.objects.filter(is_verified=True).get(phone=validated_data['phone'])
        AccessToken.objects.filter(user__phone=validated_data['phone']).delete()
        RefreshToken.objects.filter(user__phone=validated_data['phone']).delete()
        # check if password is unusable
        if not user.has_usable_password():
            user.set_password(validated_data['new_pass'])
            user.save()
            return {'detail': 'رمز عبور با موفقیت تغییر یافت'}
        raise exceptions.UserChangePasswordFailed()

    def to_representation(self, instance: dict):
        return instance


class UserChangePassSerializer(serializers.Serializer):
    new_pass = serializers.CharField(required=True)

    def create(self, validated_data):
        user = self.context['user']
        # check if password is usable
        if user.has_usable_password():
            user.set_password(validated_data['new_pass'])
            user.save()
            return {'detail': 'رمز عبور با موفقیت تغییر یافت'}
        raise exceptions.UserChangePasswordFailed()

    def to_representation(self, instance: dict):
        return instance
