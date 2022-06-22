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
		

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', default='123e4567-f89b-19d3-a656-426614174000')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=255, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def user_comment_post(sender, instance, *args, **kwargs):
        comment = instance
        post = comment.post
        text_preview = comment.body[:90]
        sender = comment.user
        notify = Notification(post=post, sender=sender, user=post.user, text_preview=text_preview ,notification_type=2)
        notify.save()
        
    def user_del_comment_post(sender, instance, *args, **kwargs):
        like = instance
        post = like.post
        sender = like.user
        
        notify = Notification.objects.filter(post=post, sender=sender, notification_type=2)
        notify.delete()
        
        post_save.connect(Comment.user_comment_post, sender=Comment)
        post_delete.connect(Comment.user_del_comment_post, sender=Comment)
    

#Comment
post_save.connect(Comment.user_comment_post, sender=Comment)
post_delete.connect(Comment.user_del_comment_post, sender=Comment)    


#NOTIFICATION

class Notification(models.Model):
	NOTIFICATION_TYPES = ((1,'Like'),(2,'Comment'), (3,'Follow'))

	post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="noti_post", blank=True, null=True)
	sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_from_user")
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="noti_to_user")
	notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
	text_preview = models.CharField(max_length=90, blank=True)
	date = models.DateTimeField(auto_now_add=True)
	is_seen = models.BooleanField(default=False)	