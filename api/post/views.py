from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from core.models import Post
from .serializers import PostSerializer


class APIPostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    http_method_names = ['get', 'post', 'head', 'options']
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        author_id = self.request.query_params.get('author_id')
        if author_id is not None:
            queryset = queryset.filter(author=author_id)
        return queryset
