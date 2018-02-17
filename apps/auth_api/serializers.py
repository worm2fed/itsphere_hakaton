from rest_framework import serializers

from apps.auth_api.models import User
from apps.auth_api.utils import check_steam_key


class UserSerializer(serializers.ModelSerializer):

    # TODO валидировать юзера на патчинг самого себя
    has_posting_key = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'avatar', 'fio', 'is_staff')

        extra_kwargs = {
            'posting_key': {'write_only': True, 'required': False},
            'password': {'write_only': True, 'required': False},
        }

    def get_has_posting_key(self, obj):
        return bool(obj.posting_key)

    def validate_posting_key(self, data):
        if not data:
            return data

        if not check_steam_key(data):
            raise serializers.ValidationError('Неверный формат постинг ключа')

        return data


class ShortUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')
