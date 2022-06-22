from django.db import models
from django.contrib.auth.models import User 
from cloudinary.models import CloudinaryField



class Profile(models.Model):
    username = models.OneToOneField(User, related_name = 'user_name', on_delete=models.SET_NULL, null=True)
    profile_photo =CloudinaryField('image')
    bio = models.TextField(max_length=500, default='bio', blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
