from django.urls import path

from .views import APIFollowViewSet

urlpatterns = [
    path('follow/<int:user_id>/', APIFollowViewSet.as_view({'post': 'follow'})),
    path('unfollow/<int:user_id>/', APIFollowViewSet.as_view({'post': 'unfollow'})),
]
