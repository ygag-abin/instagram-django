from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    name = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True,
                                    null=True)


class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='follower',
                                 on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following',
                                  on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
