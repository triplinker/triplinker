from django.contrib import admin
from .models import (Message, DialogPhoto, GroupChat, GroupChatMessage,
                     MessagePhoto)

admin.site.register(Message)
admin.site.register(DialogPhoto)
admin.site.register(GroupChat)
admin.site.register(GroupChatMessage)
admin.site.register(MessagePhoto)
