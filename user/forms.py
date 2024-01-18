from django import forms
from .models import Profile

from django.contrib.auth.forms import UserCreationForm


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_pic']


# class SignUpForm(UserCreationForm):
#     class Meta:
#         model = Profile
#         fields = ['name', 'password1', 'password2']
