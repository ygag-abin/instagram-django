from django.urls import path

from .views import PostListView, PostDetailView, PostCreateView, \
    PostEditView, PostDeleteView, LikePostView, AddCommentView

urlpatterns = [
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/new/', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/edit/', PostEditView.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(),
         name='post_delete'),
    path('like-post/<int:pk>/', LikePostView.as_view(), name='like_post'),
    path('add_comment/<int:post_id>/', AddCommentView.as_view(),
         name='add_comment'),
    path("post-list/", PostListView.as_view(), name="post-list")

]
