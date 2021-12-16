from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True, upload_to='', default='/user.png')
    followers = models.ManyToManyField(User, blank=True, related_name='followers')
    created = models.DateTimeField(auto_now_add=True)
 
    def __str__(self):
        return self.user.username

    @property
    def get_number_of_posts(self):
        return self.user.posts.all().count()
