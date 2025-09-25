from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse



class Post(models.Model):
    post_content = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    username = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.post_content[:5]

    # ...existing code...

# Modelo Type
class Type(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50)

# Modelo PostTag
class PostTag(models.Model):
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('type_id', 'post_id')


class Comment(models.Model):
    comment_content = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)


    # ...existing code...
