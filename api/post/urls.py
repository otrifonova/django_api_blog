from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import APIPostViewSet

router = DefaultRouter()
router.register('post', APIPostViewSet)

urlpatterns = [path('', include(router.urls))]
