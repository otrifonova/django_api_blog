from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from django.db.models import Count, F

from core.models import User, Follow
from .serializers import UserSerializer


class APIUserViewSet(ModelViewSet):
    queryset = User.objects.all().annotate(number_of_posts=Count("posts"))
    http_method_names = ['get', 'head', 'options']
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = self.queryset
        sorting = self.request.query_params.get('sorting')
        if sorting == 'posts_desc':
            queryset = queryset.order_by(F('number_of_posts').desc())
        elif sorting == 'posts_asc':
            queryset = queryset.order_by(F('number_of_posts').asc())
        return queryset


class APIFollowViewSet(ViewSet):
    http_method_names = ['put']
    permission_classes = (IsAuthenticated,)

    def follow(self, request, user_id):
        if user_id == self.request.user.id:
            return Response({'message': 'Cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        current_user = User.objects.get(id=self.request.user.id)
        user_to_follow = get_object_or_404(User, id=user_id)

        if user_to_follow in current_user.following.all():
            return Response(data={'message': f'User with id {user_to_follow.id} is already followed.'})

        return Response(data={'message': f'User with id {user_to_follow.id} was successfully followed.'})

    def unfollow(self, request, user_id):
        if user_id == self.request.user.id:
            return Response({'message': 'Cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        current_user = User.objects.get(id=self.request.user.id)
        user_to_unfollow = get_object_or_404(User, id=user_id)

        if user_to_unfollow not in current_user.following.all():
            return Response(data={'message': f'User with id {user_to_unfollow.id} is already not followed.'})

        current_user.following.remove(user_to_unfollow)

        return Response(data={'message': f'User with id {user_to_unfollow.id} was successfully unfollowed.'})
