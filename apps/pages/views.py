from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view, list_route, detail_route

from apps.pages.models import Page, MasterTag, Comment, Image, Tag
from apps.common.utils import (
        make_tree_by_root_nodes,
        _CustomPageViewSetPagination,
        MultiSerializerViewSetMixin,
        save_image
)

from apps.pages.serializers import (
    PageSerializer,
    PageListSerializer,
    ImageSerializer,
    MasterTagSerializer,
    CommentSerializer,
    TagSerializer
)


class PageViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    lookup_field = 'permlink'
    queryset = Page.objects.all()
    filter_fields = 'author__username',
    pagination_class = _CustomPageViewSetPagination
    serializer_class = PageSerializer
    serializer_action_classes = {
        'list': PageListSerializer
    }

    def get_queryset(self):
        return self.queryset.prefetch_related('voters', 'tags') \
            .order_by('-updated_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class MasterTagViewSet(viewsets.ModelViewSet):
    queryset = MasterTag.objects.all()
    serializer_class = MasterTagSerializer

    @list_route(methods=['GET'])
    def tree(self, request):
        # TODO тут нужно кешировать
        tree = make_tree_by_root_nodes(self.queryset, ['id', 'name'])

        return Response(tree)

    @detail_route(methods=['GET'])
    def ancestors(self, request, pk=None):
        obj = self.get_object()

        return Response(obj.get_ancestors().values_list('id', flat=True))


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_fields = 'page',



@api_view(['POST'])
def post_image(request):
    """
    Compress and save image
    """
    if request.method == 'POST':
        file = request.FILES['file']
        image = save_image(file, 'post_images/')

        return Response(ImageSerializer(image).data)

    return HttpResponse('err')
