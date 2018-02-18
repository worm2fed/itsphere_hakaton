from rest_framework import serializers

from apps.auth_api.models import User, Tag, Page, Category


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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class PageBaseSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    tags_info = TagSerializer(source='tags', read_only=True, many=True)

    class Meta:
        model = Page
        fields = '__all__'

    def get_author(self, obj):
        return obj.author.username


class PageListSerializer(PageBaseSerializer):
    body = serializers.SerializerMethodField()
    author_avatar = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = '__all__'

    def get_author_avatar(self, obj):
        return obj.author.avatar_url

    def get_body(self, obj):
        return obj.body[:100]


class PageSerializer(PageBaseSerializer):
    class Meta:
        model = Page
        fields = '__all__'
