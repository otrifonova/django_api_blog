from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated

from core.models import Follow, User
from .serializers import FollowSerializer


class APIFollowViewSet(ViewSet):
    http_method_names = ['post']
    permission_classes = (IsAuthenticated,)

    def follow(self, request, user_id):
        if user_id == self.request.user.id:
            return Response({'message': 'Cannot follow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        current_user = User.objects.get(id=self.request.user.id)
        user_to_follow = get_object_or_404(User, id=user_id)

        if user_to_follow in current_user.following.all():
            return Response(data={'message': f'User with id {user_to_follow.id} is already followed.'})

        current_user.following.add(user_to_follow)
        query = Follow.objects\
            .filter(from_user_id=current_user.id)\
            .filter(to_user_id=user_to_follow.id)\
            .first()
        serializer = FollowSerializer(query)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def unfollow(self, request, user_id):
        if user_id == self.request.user.id:
            return Response({'message': 'Cannot unfollow yourself.'}, status=status.HTTP_400_BAD_REQUEST)

        current_user = User.objects.get(id=self.request.user.id)
        user_to_unfollow = get_object_or_404(User, id=user_id)

        if user_to_unfollow not in current_user.following.all():
            return Response(data={'message': f'User with id {user_to_unfollow.id} is already not followed.'})

        current_user.following.remove(user_to_unfollow)

        return Response(status=status.HTTP_204_NO_CONTENT)
