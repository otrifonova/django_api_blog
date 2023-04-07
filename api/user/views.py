from rest_framework.viewsets import ModelViewSet
from django.db.models import Count, F

from core.models import User
from .serializers import UserSerializer


class APIUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    http_method_names = ['get', 'head', 'options']
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        sorting = self.request.query_params.get('sorting')
        if sorting == 'post_amount_desc':
            queryset = queryset.annotate(post_amount=Count("posts")).order_by(F('post_amount').desc())
        elif sorting == 'post_amount_asc':
            queryset = queryset.annotate(post_amount=Count("posts")).order_by(F('post_amount').asc())
        return queryset
