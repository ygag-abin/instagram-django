from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images')
    caption = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
