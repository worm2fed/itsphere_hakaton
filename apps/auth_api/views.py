from django.core.files.base import ContentFile

from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route, detail_route
from rest_framework.permissions import AllowAny

from apps.auth_api.models import User
from apps.auth_api.serializers import UserSerializer
from apps.auth_api.utils import jwt_response_by_user
from apps.pages.sendmail import mail_registered


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_fields = 'email',

    @list_route()
    def current(self, request):
        try:
            return Response(self.serializer_class(request.user).data)
        except Exception:
            return Response(None)

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
        slz = self.serializer_class(data=request.data)

        if slz.is_valid():
            user = User.objects.create_user(**slz.validated_data)
            mail_registered(user)
            return Response(jwt_response_by_user(user))
        else:
            return Response(slz._errors, status=status.HTTP_400_BAD_REQUEST)
