import django
from django.conf import settings
from django.contrib import admin
from django.conf.urls import url, include

from rest_framework.routers import DefaultRouter

from backend.views import IndexView
from rest_framework_jwt.views import obtain_jwt_token
from apps.pages import views as page_views
from apps.auth_api import views as auth_views

router = DefaultRouter()
router.register('pages', page_views.PageViewSet)
router.register('users', auth_views.UserViewSet)
router.register('tags', page_views.TagViewSet)
router.register('images', page_views.ImageViewSet)
router.register('master-tags', page_views.MasterTagViewSet)
router.register('comments', page_views.CommentViewSet)


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
    url(r'^post_image/', page_views.post_image),
    url(r'^sign-up/', auth_views.RegisterView.as_view()),
    url(r'^api/', include(router.urls)),

    # Vue on frontend
    url(r'^', IndexView.as_view()),
]
