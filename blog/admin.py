from django.contrib import admin
from blog.models import Post, Comment, Type, PostTag


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Type)
admin.site.register(PostTag)
