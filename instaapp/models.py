from django.db import models
from django.contrib.auth.models import User 
from cloudinary.models import CloudinaryField
from django.urls import reverse
import uuid
from django.utils.text import slugify
from django.db.models.signals import post_save, post_delete


class Profile(models.Model):
    username = models.OneToOneField(User, related_name = 'user_name', on_delete=models.SET_NULL, null=True)
    profile_photo =CloudinaryField('image')
    bio = models.TextField(max_length=500, default='bio', blank=True)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)
    created = models.DateField(auto_now_add=True)
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
            Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
       instance.profile.save()
       
       post_save.connect(create_user_profile, sender=User)
       post_save.connect(save_user_profile, sender=User)
    
def __str__(self):
    return self.user.username
    
    
    
#POSTS & TAG
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class PostFileContent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='content_owner')
    file = models.FileField(upload_to=user_directory_path)  
        
class Post(models.Model):
    image = CloudinaryField('image')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    caption = models.TextField(max_length=1500, verbose_name='Caption')
    posted = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    
    def get_absolute_url(self):
        return reverse('postdetails', args=[str(self.id)])
    
    def __str__(self):
        return str(self.id)
    
    
def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Tag(models.Model):
	title = models.CharField(max_length=100, verbose_name='Tag')
	slug = models.SlugField(null=False, unique=True)

	class Meta:
		verbose_name='Tag'
		verbose_name_plural = 'Tags'

	def get_absolute_url(self):
		return reverse('tags', args=[self.slug])
		
	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
		return super().save(*args, **kwargs)
		

    