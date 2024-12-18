from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter


router      = DefaultRouter()
urlpatterns = []


# configuration for API endpoint or resource
from apps.api.resources.users import UserViewSet
router.register('users', UserViewSet, basename='user')


# configuration for Blog endpoint or resource
from apps.blog.resources.preferences import PreferenceViewSet
from apps.blog.resources.posts import PostViewset

router.register('preferences', PreferenceViewSet, basename='preference')
router.register('posts', PostViewset, basename='post')
    

urlpatterns += router.urls