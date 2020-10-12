# Django modules.
from django.contrib import admin

# !Triplinker modules:

# Current app modules.
from .models import Post, Comment, Notification

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Notification)
