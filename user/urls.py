from django.urls import path
from .views import view_profile, edit_profile, create_profile, logout_view\
    , login_view

urlpatterns = [

    path('profile/<int:pk>/', view_profile, name='view_profile'),
    path('profile/edit/<int:pk>/', edit_profile, name='edit_profile'),
    path('profile/create/', create_profile, name='create_profile'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

]