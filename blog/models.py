from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_content = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        return self.post_content[:50]

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.post_id})


class Type(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.type_name


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    comment_content = models.TextField()
    comment_date = models.DateTimeField(default=timezone.now)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    class Meta:
        ordering = ['-comment_date']

    def __str__(self):
        return self.comment_content[:50]


class PostTag(models.Model):
    type_id = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='post_tags')
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_tags')

    class Meta:
        unique_together = ('type_id', 'post_id')

    def __str__(self):
        return f"{self.post_id.post_id} -> {self.type_id.type_name}"
