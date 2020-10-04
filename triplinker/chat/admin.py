from django.contrib import admin
from .models import (Message, DialogPhoto, GroupChat, GroupChatMainPhoto,
                     GroupChatMessage, GroupChatMessagePhoto)

admin.site.register(Message)
admin.site.register(DialogPhoto)
admin.site.register(GroupChat)
admin.site.register(GroupChatMainPhoto)
admin.site.register(GroupChatMessage)
admin.site.register(GroupChatMessagePhoto)
