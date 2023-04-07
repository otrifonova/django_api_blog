from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from djoser.views import UserViewSet

urlpatterns = [
    path('', UserViewSet.as_view({'post': 'create'}), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
