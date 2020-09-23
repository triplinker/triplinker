from django.contrib import admin
from .models import Message, GroupChat, GroupChatMessage

admin.site.register(Message)
admin.site.register(GroupChat)
admin.site.register(GroupChatMessage)
