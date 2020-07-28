from django.db import models
from django.core.validators import FileExtensionValidator
from accounts.models import TLAccount


class Post(models.Model):
	content = models.TextField()
	image = models.ImageField(upload_to='posts/', blank=True,null=True,
								validators=[
									FileExtensionValidator(
										['png','jpg','jpeg']
										)
									])
	timestamp = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(TLAccount, related_name='author', 
								on_delete = models.CASCADE)
	likes = models.ManyToManyField(TLAccount, default=None, blank=True, 
									related_name='likes')

	def __str__(self):
		return f'Author: {self.author.email}, content: {self.content[:20]}'

	def number_of_likes(self):
		return self.likes.all().count()

	
	class Meta:
		ordering = ('-timestamp',)
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'


class Comment(models.Model):
	user = models.ForeignKey(TLAccount, on_delete = models.CASCADE)
	post = models.ForeignKey(Post, on_delete = models.CASCADE)
	body = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True)


	class Meta:
		verbose_name = 'Comment'
		verbose_name_plural = 'Comments'

	def __str__(self):
		return ("User: {} | To post: {} |".format(self.user, self.post.author) +
				" Body: {}".format(self.body[:20]))


class Like(models.Model):
	user = models.ForeignKey(TLAccount, on_delete = models.CASCADE)
	post = models.ForeignKey(Post, default=None, null=True, blank=True,
							on_delete = models.CASCADE)
	comment = models.ForeignKey(Comment, default=None, null=True, blank=True,
								on_delete = models.CASCADE)
	post_liked = models.BooleanField(default=False)
	comment_liked = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True)


	class Meta:
		verbose_name = 'Like'
		verbose_name_plural = 'Likes'


	def __str__(self):
		if self.post_liked:
			return f"{self.user.email} likes post of {self.post.author}"
		elif self.comment_liked:
			return f"{self.user.email} likes comment of {self.comment.user}"
		else:
			return f"ERROR! There is no boolean value for like!"
