from django.db import models

from accounts.models.TLAccount_frequest import TLAccount


# Model for chatting one by one
class Message(models.Model):
    from_user = models.ForeignKey(TLAccount, on_delete=models.CASCADE,
                                  related_name='message_from_user')
    to_user = models.ForeignKey(TLAccount, on_delete=models.CASCADE,
                                related_name='message_to_user')
    message = models.TextField()
    users_who_read_message = models.ManyToManyField(TLAccount, blank=True,
                                                    related_name='readersOfMsg')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.email, self.to_user.email)

    class Meta:
        app_label = 'chat'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class DialogPhoto(models.Model):
    message = models.ForeignKey('Message', on_delete=models.CASCADE)
    image = models.ImageField('Picture of message',
                              upload_to='chat/pictures_of_messages',
                              null=True, blank=True)
    name_of_file = models.TextField("The name image", null=True, blank=True)

    def __str__(self):
        return 'Message: {}, image: {}'.format(self.message, self.image)

    class Meta:
        app_label = 'chat'
        verbose_name = 'DialogPhoto'
        verbose_name_plural = 'DialogPhotos'


# Models for group chatting
class GroupChat(models.Model):
    chat_name = models.CharField("The name of group chat", max_length=25)
    participants = models.ManyToManyField(TLAccount, blank=True, default=None,
                                          related_name='get_chat_partns')
    creator = models.ForeignKey(TLAccount, on_delete=models.CASCADE, null=True,
                                blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=40, blank=True)

    def __str__(self):
        prnts = self.participants.all()

        prnts_list = []
        for participant in prnts:
            prnts_list.append(participant)

        return "Chat {}, participants: {}".format(self.chat_name, prnts_list)

    def get_name(self):
        return self.chat_name

    class Meta:
        app_label = 'chat'
        verbose_name = 'GroupChat'
        verbose_name_plural = 'GroupChats'


class GroupChatMainPhoto(models.Model):
    group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE,
                                   related_name='get_main_photo_of_chat',
                                   blank=True)
    chat_image = models.ImageField('Main photo of chat',
                                   upload_to='chat/main_chat_image',
                                   null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        app_label = 'chat'
        verbose_name = 'GroupChatMainPhoto'
        verbose_name_plural = 'GroupChatMainPhotos'


class GroupChatMessage(models.Model):
    group_chat = models.ForeignKey(GroupChat, on_delete=models.CASCADE)
    relted_name_1 = 'group_chat_msges_from_user'
    msg_from_user = models.ForeignKey(TLAccount, on_delete=models.CASCADE,
                                      related_name=relted_name_1)
    message = models.TextField()

    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        frmt_string = (self.group_chat, self.msg_from_user, self.message[:20])
        return 'Chat: {0}, from user: {1}, message: {2}'.format(*frmt_string)

    class Meta:
        app_label = 'chat'
        verbose_name = 'GroupChatMessage'
        verbose_name_plural = 'GroupChatMessages'


class GroupChatMessagePhoto(models.Model):
    message = models.ForeignKey(GroupChatMessage, on_delete=models.CASCADE)
    image = models.ImageField('Picture of message',
                              upload_to='chat/pictures_of_messages',
                              null=True, blank=True)
    name_of_file = models.TextField("The name image", null=True, blank=True)

    def __str__(self):
        return 'Message: {}, image: {}'.format(self.message, self.image)

    class Meta:
        app_label = 'chat'
        verbose_name = 'GroupChatMessagePhoto'
        verbose_name_plural = 'GroupChatMessagePhotos'


# class WhoReadChatMessage:
#     user = models.ForeignKey(TLAccount, on_delete=models.CASCADE)
