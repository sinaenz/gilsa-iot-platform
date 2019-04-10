from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import mixins
from ...models import User
from ... import permissions
from . import serializers


class UsersViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    lookup_field = 'uuid'
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return serializers.UserCreateSerializer
        if self.action == 'retrieve':
            return serializers.UserRetrieveSerializer
        return serializers.UserListSerializer

    def get_permissions(self):
        self.permission_classes = []
        if self.action in ['me', 'logout', 'change_password']:
            self.permission_classes = [permissions.IsAuthenticated]
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    @action(detail=False, methods=['get'], name='user info')
    def me(self, request, pk=None):
        """ current user info """
        serializer = serializers.UserRetrieveSerializer(instance=self.request.user)
        return Response(serializer.data, status=200)

    @action(detail=False, methods=['post'], name='user sms verification')
    def verify(self, request, pk=None):
        """ user sms verification """
        serializer = serializers.UserVerificationSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    @action(detail=False, methods=['post'], name='user resend sms verification')
    def resend(self, request, pk=None):
        """ user sms verification """
        serializer = serializers.UserResendSmsSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    @action(detail=False, methods=['post'], name='user login')
    def login(self, request, pk=None):
        """ user login """
        serializer = serializers.UserLoginSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    @action(detail=False, methods=['post'], name='user logout')
    def logout(self, request, pk=None):
        """ user logout """
        serializer = serializers.UserLogoutSerializer(data=self.request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    @action(detail=False, methods=['post', 'put'], name='user reset pass')
    def reset_password(self, request, pk=None):
        """ reset and recreate password """
        # reset password
        if request.method == 'POST':
            serializer = serializers.UserResetPasswordSerializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=200)
        # recreate password
        if request.method == 'PUT':
            serializer = serializers.UserRecreatePasswordSerializer(data=self.request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=200)

    @action(detail=False, methods=['post'], name='user change pass')
    def change_password(self, request, pk=None):
        """ user change pass while is logged in """
        serializer = serializers.UserChangePassSerializer(data=self.request.data, context={'user': request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)


