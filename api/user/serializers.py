from rest_framework import serializers
from core.models import User, Follow


class UserSerializer(serializers.ModelSerializer):
    number_of_posts = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'number_of_posts']
