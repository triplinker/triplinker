import datetime
from django.utils import timezone
from django.db import models
from django.core.validators import FileExtensionValidator

from accounts.models.TLAccount_frequest import TLAccount
from trip_places.models import Place


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
    place = models.ForeignKey(Place, related_name='posts_of_place', null=True,
                              blank=True, on_delete=models.CASCADE)
    likes = models.ManyToManyField(TLAccount, default=None, blank=True,
                                   related_name='like_system_post')

    is_place = models.BooleanField(default=False)
    notification_post = models.BooleanField(default=False)

    def __str__(self):
        return f'Author: {self.author}, content: {self.content[:20]}'

    def number_of_likes(self):
        return self.likes.all().count()

    def was_published_recently(self):
        return self.timestamp >= timezone.now() - datetime.timedelta(minutes=59)

    class Meta:
        ordering = ('-timestamp',)
        app_label = 'feed'
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
        app_label = 'feed'
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return ("User: {} | To post: {} |".format(self.user, self.post.author) +
                " Body: {}".format(self.body[:20]))


class Notification(models.Model):

    post = models.ForeignKey(Post, related_name="notifications",
                             on_delete=models.CASCADE)
    users = models.ManyToManyField(TLAccount, related_name="notifications")
    text = models.CharField("Notification text", max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_seen = models.ManyToManyField(TLAccount, blank=True,
                                     related_name='seen_notifications')

    def __str__(self):
        return f"Post {self.post}"

    class Meta:
        ordering = ('-timestamp',)
        app_label = 'feed'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
