from rest_framework import serializers

from apps.auth_api.models import User, Tag, Post
from apps.auth_api.utils import check_steam_key


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }


class ShortUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PostBaseSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    tags_info = TagSerializer(source='tags', read_only=True, many=True)

    class Meta:
        model = Post
        fields = '__all__'

    def get_author(self, obj):
        return obj.author.name


class PostListSerializer(PostBaseSerializer):
    body = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_body(self, obj):
        return obj.body[:100]


class PostSerializer(PostBaseSerializer):
    class Meta:
        model = Post
        fields = '__all__'
