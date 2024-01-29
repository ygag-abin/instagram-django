from rest_framework.generics import get_object_or_404, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from post.models import Post
from .serializers import PostSerializer


class PostListView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
