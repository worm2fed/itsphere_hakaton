from rest_framework import serializers
from drf_extra_fields.geo_fields import PointField

from apps.pages.models import Page, Image, MasterTag, Comment, Tag
from apps.auth_api.serializers import ShortUserSerializer


class ImageSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        exclude = 'file',

    def get_name(self, obj):
        return obj.file.name.split('/')[-1]

    def get_url(self, obj):
        return obj.file.url


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class MasterTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterTag
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class PageBaseSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    tags_info = TagSerializer(source='tags', read_only=True, many=True)
    uploaded_images = ImageSerializer(many=True, read_only=True)
    # comments = CommentSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()


    class Meta:
        model = Page
        fields = '__all__'

    def get_comments(self, obj):
        return []

    def get_author(self, obj):
        return obj.author.username


class PageListSerializer(PageBaseSerializer):
    body = serializers.SerializerMethodField()
    voters = ShortUserSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = '__all__'

    def get_body(self, obj):
        return obj.body[:100]


class PageSerializer(PageBaseSerializer):
    class Meta:
        model = Page
        fields = '__all__'
