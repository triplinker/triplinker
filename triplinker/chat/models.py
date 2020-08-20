from django.db import models

from accounts.models.TLAccount_frequest import TLAccount


class Message(models.Model):
    from_user = models.ForeignKey(TLAccount, on_delete=models.CASCADE,
                                  related_name='message_from_user')
    to_user = models.ForeignKey(TLAccount, on_delete=models.CASCADE,
                                related_name='message_to_user')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "From {}, to {}".format(self.from_user.email, self.to_user.email)

    class Meta:
        app_label = 'chat'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
