from django.urls import path
from .views import post_list, post_detail

urlpatterns = [
    path('api/posts/', post_list, name='post-list'),
    path('api/posts/<int:pk>/', post_detail, name='post-detail'),
]
