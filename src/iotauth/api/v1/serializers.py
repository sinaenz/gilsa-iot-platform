from rest_framework import serializers
from rest_framework.response import Response
from django.test import Client
from oauth2_provider.models import Application, AccessToken, RefreshToken
from ... import exceptions
from ...models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'full_name')


class UserCreateSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)
    full_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_phone(self, value):
        if User.objects.filter(phone=value, is_verified=False).exists():
            raise exceptions.VerificationIsRequired()
        if User.objects.filter(phone=value, is_verified=True).exists():
            raise exceptions.UserAlreadyExist()
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = User.objects.create(**validated_data)
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
    password = serializers.CharField(required=False)

    def create(self, validated_data):
        phone = validated_data['phone']
        code = validated_data['code']
        try:
            user = User.objects.filter(is_verified=False).get(phone=phone, verification_code=code)
            # login user automatically
            user.is_verified = True
            user.save()
            if user.has_usable_password():
                user.set_password(validated_data['password'])
                user.save()
                serializer = UserLoginSerializer(data=validated_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return {'access_token': serializer.data['access_token'],
                        'refresh_token': serializer.data['refresh_token'],
                        'phone': user.phone,
                        'full_name': user.full_name,
                        }
            # if user was requested to change password
            return {'detail': 'تایید با موفقیت انجام شد'}
        except Exception as error:
            print(error)
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
        user = User.objects.filter(is_verified=True).get(phone=validated_data['phone'])
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
        return {'access_token': response.json()['access_token'],
                'refresh_token': response.json()['refresh_token'],
                'phone': user.phone,
                'full_name': user.full_name,
                }

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


class UserForgotPasswordSerializer(serializers.Serializer):
    phone = serializers.CharField(required=True)

    def create(self, validated_data):
        try:
            user = User.objects.get(phone=validated_data['phone'])
            AccessToken.objects.filter(user__phone=validated_data['phone']).delete()
            RefreshToken.objects.filter(user__phone=validated_data['phone']).delete()
            # set password unusable
            user.set_unusable_password()
            # send verification code
            user.send_verification_sms()
            return {'detail': 'کد تایید برای شما ارسال شد'}
        except:
            raise exceptions.UserNotFound()

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
