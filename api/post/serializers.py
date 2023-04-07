from rest_framework import serializers
from core.models import Post


class PostSerializer(serializers.ModelSerializer):
    author_id = serializers.ReadOnlyField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'author_id', 'pub_date']
