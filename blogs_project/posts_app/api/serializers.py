from rest_framework import serializers
from posts_app.models import Post

# Post serializer


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'text')
