from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import APIUserViewSet

router = DefaultRouter()
router.register('user', APIUserViewSet)

urlpatterns = [path('', include(router.urls))]
