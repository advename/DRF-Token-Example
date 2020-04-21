from rest_framework import generics

from posts_app.models import Post  # import Post Model
from posts_app.api.serializers import PostSerializer  # import Post Serializer
from django.utils.decorators import method_decorator
# Retrieve all or create new Post


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# Retrieve or delete single Post
class PostDetail(generics.RetrieveDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
