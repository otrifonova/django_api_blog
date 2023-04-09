from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import APIUserViewSet, APIFollowViewSet

router = DefaultRouter()
router.register('user', APIUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/<int:user_id>/follow/', APIFollowViewSet.as_view({'put': 'follow'})),
    path('user/<int:user_id>/unfollow/', APIFollowViewSet.as_view({'put': 'unfollow'})),
]
