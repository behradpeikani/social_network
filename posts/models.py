from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid

# Create your models here.

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.username, filename)

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(upload_to=user_directory_path)
    post_caption = models.TextField(null=True, blank=True, verbose_name='caption')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
    
    def get_absolute_url(self):
        return reverse('posts:post_detail', kwargs={'post_id': str(self.id)})
 
    def __str__(self):
        return f'{self.user}-{self.post_caption[:15]}'

    def likes_count(self):
        return self.plike.count()

    def user_likes(self, user):
        likes = user.ulike.all()
        qs = likes.filter(post=self)
        if qs.exists():
            return True
        return False


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply = models.ForeignKey('self', on_delete= models.CASCADE, null=True, blank=True, related_name='reply_comment')
    is_reply = models.BooleanField(default=False)
    content = models.TextField(max_length=500)
    published = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return f'{self.user}-{self.content[:15]}'

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='plike')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ulike')

    def __str__(self):
        return f'{self.user} liked {self.post}'