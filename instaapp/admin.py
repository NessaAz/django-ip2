import profile
from django.contrib import admin
from .models import *


admin.site.register(Stream)
admin.site.register(Likes)
admin.site.register(Follow)
admin.site.register(Notification)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(Post)
# admin.site.register(PostFileContent)
admin.site.register(Profile)
