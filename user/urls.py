from django.urls import path
from .views import CreateProfileView, ViewProfileView, EditProfileView, \
    RegisterUserView, AllUsersView, FollowProfileView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

urlpatterns = [

    path('profile/<int:pk>/', ViewProfileView.as_view(), name='view_profile'),
    path('profile/edit/<int:pk>/', EditProfileView.as_view(),
         name='edit_profile'),
    path('profile/create/', CreateProfileView.as_view(),
         name='create_profile'),
    path('login/', LoginView.as_view(template_name='user/login.html',
                                     next_page=reverse_lazy('post-list')),
         name='login'),

    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('all_users/', AllUsersView.as_view(), name='all_users'),
    path('follow_profile/<int:pk>/', FollowProfileView.as_view(),
         name='follow_profile'),

]
