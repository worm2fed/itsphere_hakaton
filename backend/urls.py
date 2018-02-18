import django
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from backend.views import IndexView
from rest_framework_jwt.views import obtain_jwt_token
from apps.auth_api import views

router = DefaultRouter()
# router.register('posts', views.PostViewSet)
router.register('pages', views.PageViewSet)
router.register('users', views.UserViewSet)
router.register('tags', views.TagViewSet)
router.register('category', views.CategoryViewSet)

urlpatterns = []

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))

    urlpatterns.append(
        url(r'^media/(?P<path>.*)$', django.views.static.serve, {
            'document_root': settings.MEDIA_ROOT})
    )


urlpatterns += [
    url(r'^admin/', admin.site.urls),
    url(r'^api-auth/', obtain_jwt_token),
    url(r'^sign-up/', views.RegisterView.as_view()),
    url(r'^api/', include(router.urls)),

    # Vue on frontend
    url(r'^', IndexView.as_view()),
]
