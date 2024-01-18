from django.urls import path

from .views import post_list, post_detail, post_create, post_edit, \
    post_delete, like_post, add_comment

urlpatterns = [
    path('posts/', post_list, name='post-list'),
    path('posts/<int:pk>/', post_detail, name='post_detail'),
    path('posts/new/', post_create, name='post_create'),
    path('posts/<int:pk>/edit/', post_edit, name='post_edit'),
    path('posts/<int:pk>/delete/', post_delete, name='post_delete'),
    path('like-post/<int:pk>/', like_post, name='like_post'),
    # path('posts/comment/<int:post_id>/', add_comment, name='add_comment'),
    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),

]
