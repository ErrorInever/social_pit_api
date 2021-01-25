import debug_toolbar
from django.urls import path, include
from django.conf.urls import url
from django.contrib import admin
from rest_framework.routers import SimpleRouter
from user.views import CustomUserViewSet, auth, index, PostViewSet, UserPostRelationView



router = SimpleRouter()
router.register(r'api/users', CustomUserViewSet, basename='users')
router.register(r'api/post', PostViewSet, basename='post')
router.register(r'api/post_relation', UserPostRelationView, basename='post_relation')

urlpatterns = [
    path('admin/', admin.site.urls),
    url('', include('social_django.urls', namespace='social')),
    path('__debug__/', include(debug_toolbar.urls)),
    path('auth/', auth),
    #path('', index)
]

urlpatterns += router.urls