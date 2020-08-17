from django.db import models

from accounts.models.TLAccount_frequest import TLAccount

class Message(models.Model):
	from_user = models.ForeignKey(TLAccount, on_delete=models.CASCADE,
		                          related_name='message_from_user')
	to_user = models.ForeignKey(TLAccount, on_delete=models.CASCADE,
		                        related_name='message_to_user')
	message = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)

	def get_author(self):
		return self.from_user

