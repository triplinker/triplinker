from django.db import models
from django.core.validators import FileExtensionValidator
from .TLAccount_frequest import TLAccount


class Post(models.Model):
    """Post model which provides users the possibility of posting thoughts,
    images and etc."""
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True,
                              validators=[FileExtensionValidator(['png', 'jpg',
                                                                  'jpeg'])])
    timestamp = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(TLAccount, related_name='author', blank=True,
                               null=True, default=None,
                               on_delete=models.CASCADE)
    likes = models.ManyToManyField(TLAccount, default=None, blank=True,
                                   related_name='like_system_post')

    def __str__(self):
        return f'Author: {self.author}, content: {self.content[:20]}'

    def number_of_likes(self):
        return self.likes.all().count()

    class Meta:
        ordering = ('-timestamp',)
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'


class Comment(models.Model):
    """Model that are connected with post model because every post must have
    it's own comments"""

    user = models.ForeignKey(TLAccount, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    likes = models.ManyToManyField(TLAccount, default=None, blank=True,
                                   related_name='like_system_comment')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return ("User: {} | To post: {} |".format(self.user, self.post.author) +
                " Body: {}".format(self.body[:20]))
