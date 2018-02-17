from rest_framework import serializers

from apps.auth_api.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'avatar', 'fio', 'is_staff')
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'avatar': {'read_only': True},
        }


class ShortUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')
