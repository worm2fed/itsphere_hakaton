from django.core.files.base import ContentFile

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import AllowAny

from apps.auth_api.models import User
from apps.auth_api.serializers import UserSerializer
from apps.auth_api.utils import jwt_response_by_user


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = ('email',)

    @list_route()
    def current(self, request):
        return Response(self.serializer_class(request.user).data)

    @detail_route(methods=['post'])
    def set_avatar(self, request, pk=None):
        file = request.FILES.get('file')
        obj = self.get_object()
        obj.avatar.save(str(file), ContentFile(file.read()))
        return Response(obj.avatar.url)


class RegisterView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = UserSerializer

    @list_route(['POST'])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(**serializer.validated_data)
            return Response(jwt_response_by_user(user))
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
